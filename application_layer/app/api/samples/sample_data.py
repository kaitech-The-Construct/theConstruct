"""Sample data to simulate robot catalog"""
robot_catalog = [
    {
        "id": 1,
        "manufacturer": "Turbotics Inc.",
        "manufacturer_id": "12345",
        "model": "R1000",
        "price": {
            "model": "R1000",
            "subscription_price": 16.00,
            "listing_price": 300.00,
        },
        "description": "High-performance mechanic robot.",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/mechanic.png",
    },
    {
        "id": 2,
        "manufacturer": "TechBot Corp.",
        "manufacturer_id": "23456",
        "model": "TB200",
        "price": {
            "model": "TB200",
            "subscription_price": 83.00,
            "listing_price": 1500.00,
        },
        "description": "Versatile educational robot.",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/playmate.png",
    },
    {
        "id": 3,
        "manufacturer": "RoboTech Systems",
        "manufacturer_id": "34567",
        "model": "RT3000",
        "price": {
            "model": "RT3000",
            "subscription_price": 25.00,
            "listing_price": 450.00,
        },
        "description": "Advanced robotic system for meal prepping and dinner dates.",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/cook.png",
    },
    {
        "id": 4,
        "manufacturer": "InnoBotics",
        "manufacturer_id": "45678",
        "model": "AI9000",
        "price": {
            "model": "AI9000",
            "subscription_price": 40.00,
            "listing_price": 750.00,
        },
        "description": "AI-powered autonomous robot for all your gardening needs.",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/gardener.png",
    },
    {
        "id": 5,
        "manufacturer": "InnoBotics",
        "manufacturer_id": "45678",
        "model": "INNO-X5",
        "price": {
            "model": "INNO-X5",
            "subscription_price": 20.00,
            "listing_price": 380.00,
        },
        "description": "Innovative personal assistant robot with cutting-edge features.",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/assistant.png",
    },
    # Add more robot listings as needed
]

"""Sample data to simulate software listings"""

software_repository = [
    {
        "name": "RobotControlApp",
        "version": "1.0.0",
        "author": "Robotics Inc.",
        "description": "Control application for robotic arms.",
        "compatibility": ["R1000", "TB200"],
        "license": "MIT License",
        "documentation_url": "https://example.com/robotcontrolapp-docs",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/software.png",
    },
    {
        "name": "VisionProcessing",
        "version": "2.1.0",
        "author": "VisionTech Corp.",
        "description": "Computer vision processing software for robots.",
        "compatibility": ["RT3000"],
        "license": "Apache License 2.0",
        "documentation_url": "https://example.com/visionprocessing-docs",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/software.png",
    },
    {
        "name": "RobotSimulator",
        "version": "3.5.2",
        "author": "SimuRobotics LLC",
        "description": "Simulation software for testing robot behaviors.",
        "compatibility": ["R1000", "TB200", "RT3000"],
        "license": "GNU GPL v3",
        "documentation_url": "https://example.com/robotsimulator-docs",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/software.png",
    },
    {
        "name": "MotionControlApp",
        "version": "2.0.1",
        "author": "Robotics Inc.",
        "description": "Advanced motion control software for robotic systems.",
        "compatibility": ["R1000", "TB200", "AI9000"],
        "license": "Apache License 2.0",
        "documentation_url": "https://example.com/motioncontrolapp-docs",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/software.png",
    },
    {
        "name": "RobotVisionAI",
        "version": "1.5.0",
        "author": "AI VisionTech",
        "description": "Artificial intelligence-based vision processing software for robots.",
        "compatibility": ["RT3000", "INNO-X5"],
        "license": "MIT License",
        "documentation_url": "https://example.com/robotvisionai-docs",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/software.png",
    },
    {
        "name": "RoboticsSimSuite",
        "version": "4.0.3",
        "author": "SimuRobotics LLC",
        "description": "Comprehensive simulation suite for robot testing and development.",
        "compatibility": ["R1000", "AI9000", "INNO-X5"],
        "license": "GNU GPL v3",
        "documentation_url": "https://example.com/roboticssimsuite-docs",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/software.png",
    },
    {
        "name": "RobotControlPro",
        "version": "3.2.1",
        "author": "RoboTech Systems",
        "description": "Professional robot control software for industrial applications.",
        "compatibility": ["AI9000", "INNO-X5"],
        "license": "Proprietary",
        "documentation_url": "https://example.com/robotcontrolpro-docs",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/software.png",
    },
    {
        "name": "InnoBoticsAI",
        "version": "2.1.2",
        "author": "InnoBotics",
        "description": "AI-driven software for Inno-X5 robot optimization.",
        "compatibility": ["R1000"],
        "license": "MIT License",
        "documentation_url": "https://example.com/innoboticsai-docs",
        "image_url": "https://storage.googleapis.com/app-images-the-construct-401518/software.png",
    },
]
