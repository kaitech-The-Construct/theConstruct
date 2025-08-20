"""
Performance and load testing for The Construct application layer.
"""

import pytest
import asyncio
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi.testclient import TestClient
from httpx import AsyncClient
import json


class TestAPIPerformance:
    """Performance tests for API endpoints."""

    def test_robots_endpoint_response_time(self, client: TestClient):
        """Test robots endpoint response time under normal load."""
        response_times = []
        
        for _ in range(50):  # 50 requests
            start_time = time.time()
            response = client.get("/api/v1/robots")
            end_time = time.time()
            
            response_times.append(end_time - start_time)
            assert response.status_code == 200
        
        # Performance assertions
        avg_response_time = statistics.mean(response_times)
        p95_response_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
        
        assert avg_response_time < 0.5  # Average response time should be under 500ms
        assert p95_response_time < 1.0   # 95th percentile should be under 1 second
        assert max(response_times) < 2.0  # No request should take more than 2 seconds

    def test_search_endpoint_performance(self, client: TestClient):
        """Test search endpoint performance with various queries."""
        search_queries = [
            {"type": "robot"},
            {"minPrice": 10000, "maxPrice": 50000},
            {"category": "industrial"},
            {"name": "robot"},
            {"type": "robot", "minPrice": 20000}
        ]
        
        response_times = []
        
        for query in search_queries:
            for _ in range(10):  # 10 requests per query
                start_time = time.time()
                response = client.get("/api/v1/robots/search", params=query)
                end_time = time.time()
                
                response_times.append(end_time - start_time)
                assert response.status_code == 200
        
        avg_response_time = statistics.mean(response_times)
        assert avg_response_time < 0.8  # Search should be fast

    @pytest.mark.asyncio
    async def test_concurrent_requests_performance(self, async_client: AsyncClient):
        """Test performance under concurrent load."""
        concurrent_requests = 20
        
        async def make_request():
            start_time = time.time()
            response = await async_client.get("/api/v1/robots")
            end_time = time.time()
            return end_time - start_time, response.status_code
        
        # Create concurrent tasks
        tasks = [make_request() for _ in range(concurrent_requests)]
        results = await asyncio.gather(*tasks)
        
        response_times = [result[0] for result in results]
        status_codes = [result[1] for result in results]
        
        # All requests should succeed
        assert all(code == 200 for code in status_codes)
        
        # Performance under concurrent load
        avg_response_time = statistics.mean(response_times)
        assert avg_response_time < 1.0  # Should handle concurrent requests well

    def test_database_query_performance(self, client: TestClient):
        """Test database query performance."""
        # Test various endpoints that hit the database
        endpoints = [
            "/api/v1/robots",
            "/api/v1/robots/search?type=robot",
            "/api/v1/robots/categories"
        ]
        
        for endpoint in endpoints:
            response_times = []
            
            for _ in range(20):
                start_time = time.time()
                response = client.get(endpoint)
                end_time = time.time()
                
                response_times.append(end_time - start_time)
                assert response.status_code == 200
            
            avg_time = statistics.mean(response_times)
            # Database queries should be optimized
            assert avg_time < 0.3, f"Endpoint {endpoint} too slow: {avg_time}s"


class TestLoadTesting:
    """Load testing scenarios."""

    def test_sustained_load(self, client: TestClient):
        """Test sustained load over time."""
        duration = 30  # 30 seconds
        start_time = time.time()
        request_count = 0
        errors = 0
        response_times = []
        
        while time.time() - start_time < duration:
            request_start = time.time()
            try:
                response = client.get("/api/v1/robots")
                request_end = time.time()
                
                response_times.append(request_end - request_start)
                request_count += 1
                
                if response.status_code != 200:
                    errors += 1
                    
            except Exception:
                errors += 1
            
            time.sleep(0.1)  # Small delay between requests
        
        # Calculate metrics
        total_time = time.time() - start_time
        requests_per_second = request_count / total_time
        error_rate = errors / request_count if request_count > 0 else 1
        avg_response_time = statistics.mean(response_times) if response_times else 0
        
        # Assertions
        assert requests_per_second > 5  # Should handle at least 5 RPS
        assert error_rate < 0.05  # Error rate should be less than 5%
        assert avg_response_time < 1.0  # Average response time under 1 second

    def test_spike_load(self, client: TestClient):
        """Test handling of sudden load spikes."""
        # Normal load phase
        for _ in range(10):
            response = client.get("/api/v1/robots")
            assert response.status_code == 200
            time.sleep(0.1)
        
        # Spike phase - sudden increase in requests
        spike_responses = []
        spike_start = time.time()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(client.get, "/api/v1/robots") for _ in range(50)]
            
            for future in as_completed(futures):
                try:
                    response = future.result(timeout=5)
                    spike_responses.append(response.status_code)
                except Exception:
                    spike_responses.append(500)  # Treat exceptions as server errors
        
        spike_duration = time.time() - spike_start
        
        # Most requests should succeed even during spike
        success_rate = sum(1 for code in spike_responses if code == 200) / len(spike_responses)
        assert success_rate > 0.8  # At least 80% success rate during spike
        assert spike_duration < 10  # Spike should be handled within 10 seconds

    @pytest.mark.asyncio
    async def test_memory_usage_under_load(self, async_client: AsyncClient):
        """Test memory usage doesn't grow excessively under load."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Generate load
        tasks = []
        for _ in range(100):
            task = async_client.get("/api/v1/robots")
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable
        assert memory_increase < 100  # Less than 100MB increase


class TestStressTesting:
    """Stress testing to find breaking points."""

    def test_maximum_concurrent_users(self, client: TestClient):
        """Test maximum number of concurrent users the system can handle."""
        max_workers = 50  # Start with 50 concurrent users
        success_count = 0
        error_count = 0
        
        def make_request():
            try:
                response = client.get("/api/v1/robots", timeout=10)
                return response.status_code == 200
            except Exception:
                return False
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(make_request) for _ in range(max_workers * 2)]
            
            for future in as_completed(futures):
                if future.result():
                    success_count += 1
                else:
                    error_count += 1
        
        total_requests = success_count + error_count
        success_rate = success_count / total_requests
        
        # Should handle reasonable concurrent load
        assert success_rate > 0.7  # At least 70% success rate under stress

    def test_large_payload_handling(self, client: TestClient, auth_headers):
        """Test handling of large payloads."""
        # Create a large robot specification
        large_specifications = {
            "technical": {f"spec_{i}": f"value_{i}" for i in range(1000)},
            "compatibility": [f"protocol_{i}" for i in range(100)],
            "dimensions": {f"dimension_{i}": f"{i}mm" for i in range(100)}
        }
        
        robot_data = {
            "name": "Large Payload Robot",
            "description": "Robot with large specifications for testing",
            "type": "robot",
            "specifications": large_specifications,
            "pricing": {"basePrice": 50000, "currency": "USD"}
        }
        
        start_time = time.time()
        response = client.post("/api/v1/robots", json=robot_data, headers=auth_headers)
        end_time = time.time()
        
        # Should handle large payloads
        assert response.status_code in [201, 400, 413]  # Created, Bad Request, or Payload Too Large
        assert end_time - start_time < 5.0  # Should process within 5 seconds

    def test_rapid_sequential_requests(self, client: TestClient):
        """Test rapid sequential requests from single client."""
        response_times = []
        error_count = 0
        
        for i in range(100):
            start_time = time.time()
            try:
                response = client.get("/api/v1/robots")
                end_time = time.time()
                
                response_times.append(end_time - start_time)
                
                if response.status_code != 200:
                    error_count += 1
                    
            except Exception:
                error_count += 1
                response_times.append(5.0)  # Assume 5s for failed requests
        
        # Performance should remain consistent
        avg_response_time = statistics.mean(response_times)
        error_rate = error_count / 100
        
        assert avg_response_time < 1.0  # Average should stay reasonable
        assert error_rate < 0.1  # Less than 10% error rate


class TestScalabilityTesting:
    """Tests for system scalability."""

    def test_database_connection_pooling(self, client: TestClient):
        """Test database connection pooling under load."""
        # Simulate multiple concurrent database operations
        def database_intensive_request():
            try:
                # Make requests that require database access
                response = client.get("/api/v1/robots/search?type=robot")
                return response.status_code == 200
            except Exception:
                return False
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(database_intensive_request) for _ in range(100)]
            results = [future.result() for future in as_completed(futures)]
        
        success_rate = sum(results) / len(results)
        assert success_rate > 0.9  # Should handle database connections well

    def test_cache_performance(self, client: TestClient):
        """Test caching performance."""
        # First request (cache miss)
        start_time = time.time()
        response1 = client.get("/api/v1/robots/test-robot-id")
        first_request_time = time.time() - start_time
        
        # Second request (should be cached)
        start_time = time.time()
        response2 = client.get("/api/v1/robots/test-robot-id")
        second_request_time = time.time() - start_time
        
        # Cache should improve performance
        if response1.status_code == 200 and response2.status_code == 200:
            # Second request should be faster (cached)
            assert second_request_time <= first_request_time * 1.5  # Allow some variance

    @pytest.mark.asyncio
    async def test_websocket_performance(self, async_client: AsyncClient):
        """Test WebSocket performance if implemented."""
        # This would test WebSocket connections for real-time features
        # Implementation depends on WebSocket endpoints being available
        pass


class TestResourceUtilization:
    """Tests for resource utilization monitoring."""

    def test_cpu_usage_under_load(self, client: TestClient):
        """Monitor CPU usage under load."""
        import psutil
        
        # Baseline CPU usage
        cpu_before = psutil.cpu_percent(interval=1)
        
        # Generate load
        for _ in range(50):
            client.get("/api/v1/robots")
        
        # CPU usage after load
        cpu_after = psutil.cpu_percent(interval=1)
        
        # CPU usage should be reasonable
        cpu_increase = cpu_after - cpu_before
        assert cpu_increase < 80  # Should not max out CPU

    def test_response_size_optimization(self, client: TestClient):
        """Test response size optimization."""
        response = client.get("/api/v1/robots")
        
        if response.status_code == 200:
            content_length = len(response.content)
            
            # Response should be reasonably sized
            assert content_length < 1024 * 1024  # Less than 1MB
            
            # Check if compression is working
            if 'content-encoding' in response.headers:
                assert response.headers['content-encoding'] in ['gzip', 'deflate']


class TestPerformanceRegression:
    """Performance regression tests."""

    def test_baseline_performance_metrics(self, client: TestClient, performance_test_config):
        """Establish baseline performance metrics."""
        endpoints = performance_test_config["endpoints"]
        baseline_metrics = {}
        
        for endpoint in endpoints:
            response_times = []
            
            for _ in range(20):
                start_time = time.time()
                response = client.get(endpoint)
                end_time = time.time()
                
                if response.status_code == 200:
                    response_times.append(end_time - start_time)
            
            if response_times:
                baseline_metrics[endpoint] = {
                    "avg_response_time": statistics.mean(response_times),
                    "p95_response_time": statistics.quantiles(response_times, n=20)[18] if len(response_times) >= 20 else max(response_times),
                    "max_response_time": max(response_times)
                }
        
        # Store or compare with previous baselines
        # In a real scenario, you'd store these metrics and compare with previous runs
        for endpoint, metrics in baseline_metrics.items():
            assert metrics["avg_response_time"] < 1.0  # Baseline expectation
            assert metrics["p95_response_time"] < 2.0   # Baseline expectation


# Utility functions for performance testing
def measure_response_time(func, *args, **kwargs):
    """Utility function to measure response time."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time


def generate_load(client: TestClient, endpoint: str, duration: int, rps: int):
    """Generate load for a specific endpoint."""
    start_time = time.time()
    request_count = 0
    errors = 0
    response_times = []
    
    while time.time() - start_time < duration:
        request_start = time.time()
        try:
            response = client.get(endpoint)
            request_end = time.time()
            
            response_times.append(request_end - request_start)
            request_count += 1
            
            if response.status_code != 200:
                errors += 1
                
        except Exception:
            errors += 1
        
        # Control request rate
        time.sleep(1.0 / rps)
    
    return {
        "request_count": request_count,
        "errors": errors,
        "response_times": response_times,
        "duration": time.time() - start_time
    }
