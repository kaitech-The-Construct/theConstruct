# core/middleware.py

import time
from typing import Dict
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import asyncio


class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, list] = {}
        self.max_requests = 100  # requests per minute
        self.window_size = 60  # seconds

    def is_allowed(self, client_ip: str) -> bool:
        current_time = time.time()
        
        # Clean old requests
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if current_time - req_time < self.window_size
            ]
        else:
            self.requests[client_ip] = []
        
        # Check if limit exceeded
        if len(self.requests[client_ip]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[client_ip].append(current_time)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware"""
    client_ip = request.client.host
    
    if not rate_limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded. Please try again later."}
        )
    
    response = await call_next(request)
    return response


async def security_headers_middleware(request: Request, call_next):
    """Security headers middleware"""
    response = await call_next(request)
    
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    return response


async def error_handling_middleware(request: Request, call_next):
    """Global error handling middleware"""
    try:
        response = await call_next(request)
        return response
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as exc:
        # Log the error (in production, use proper logging)
        print(f"Unhandled error: {exc}")
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )


async def request_logging_middleware(request: Request, call_next):
    """Request logging middleware"""
    start_time = time.time()
    
    # Log request
    print(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log response time
    process_time = time.time() - start_time
    print(f"Response time: {process_time:.4f}s")
    
    return response
