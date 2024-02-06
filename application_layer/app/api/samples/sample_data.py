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
design_catalog = [
  {
    "design_id": "RD003",
    "designer": "Robotics Inc.",
    "robot_model": "Model B",
    "specifications": {
      "dimensions": { "height": 1.5, "width": 1.0, "depth": 0.8 },
      "weight": 200,
      "materials": ["Steel", "Plastic"],
      "mobility": ["Wheels", "Tracks"],
      "power": "Fuel",
      "operationalTime": "10 hours"
    },
    "category": "Military",
    "date_created": "2023-03-01T12:00:00Z",
    "url_to_images": [
      "https://storage.googleapis.com/app-images-the-construct-401518/design_001.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_002.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_003.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_004.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_005.png"
    ],
    "current_status": "Prototype",
    "tags": ["Combat", "Surveillance"],
    "additional_info": { "note": "This is a military robot design." }
  },
  {
    "design_id": "RD004",
    "designer": "RoboTech Ltd.",
    "robot_model": "Rover 3000",
    "specifications": {
      "dimensions": { "height": 1.1, "width": 1.4, "depth": 0.9 },
      "weight": 220,
      "materials": ["Titanium", "Plastic"],
      "mobility": ["Wheels", "Legs", "Wings"],
      "power": "Nuclear",
      "operationalTime": "24 hours"
    },
    "category": "Transportation",
    "date_created": "2023-03-15T16:30:00Z",
    "url_to_images": [
      "https://storage.googleapis.com/app-images-the-construct-401518/design_001.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_002.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_003.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_004.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_005.png"
    ],
    "current_status": "Production",
    "tags": ["Cargo", "Passenger"],
    "additional_info": { "note": "Built for long-distance transportation." }
  },

  {
    "design_id": "RD005",
    "designer": "Robotics Inc.",
    "robot_model": "Model C",
    "specifications": {
      "dimensions": { "height": 1.8, "width": 1.2, "depth": 1.0 },
      "weight": 250,
      "materials": ["Ceramic", "Plastic"],
      "mobility": ["Wheels", "Tracks", "Propellers"],
      "power": "Fusion",
      "operationalTime": "Unlimited"
    },
    "category": "Research",
    "date_created": "2023-04-01T10:00:00Z",
    "url_to_images": [
      "https://storage.googleapis.com/app-images-the-construct-401518/design_001.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_002.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_003.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_004.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_005.png"
    ],
    "current_status": "Prototype",
    "tags": ["Exploration", "Robotics"],
    "additional_info": { "note": "This is a research robot design." }
  },

  {
    "design_id": "RD006",
    "designer": "RoboTech Ltd.",
    "robot_model": "Rover 4000",
    "specifications": {
      "dimensions": { "height": 1.3, "width": 1.6, "depth": 1.1 },
      "weight": 280,
      "materials": ["Diamond", "Plastic"],
      "mobility": ["Wheels", "Legs", "Wings", "Propellers"],
      "power": "Infinite",
      "operationalTime": "Infinite"
    },
    "category": "Entertainment",
    "date_created": "2023-04-15T14:15:00Z",
    "url_to_images": [
      "https://storage.googleapis.com/app-images-the-construct-401518/design_001.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_002.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_003.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_004.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_005.png"
    ],
    "current_status": "Production",
    "tags": ["Amusement", "Entertainment"],
    "additional_info": {
      "note": "Built for amusement parks and entertainment venues."
    }
  },

  {
    "design_id": "RD007",
    "designer": "Robotics Inc.",
    "robot_model": "Model D",
    "specifications": {
      "dimensions": { "height": 2.0, "width": 1.4, "depth": 1.2 },
      "weight": 300,
      "materials": ["Carbon fiber", "Plastic"],
      "mobility": ["Wheels", "Tracks", "Propellers", "Wings"],
      "power": "Unlimited",
      "operationalTime": "Infinite"
    },
    "category": "Medical",
    "date_created": "2023-05-01T12:00:00Z",
    "url_to_images": [
      "https://storage.googleapis.com/app-images-the-construct-401518/design_001.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_002.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_003.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_004.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_005.png"
    ],
    "current_status": "Prototype",
    "tags": ["Surgery", "Diagnostics"],
    "additional_info": { "note": "This is a medical robot design." }
  },
  {
    "design_id": "RD008",
    "designer": "RoboTech Ltd.",
    "robot_model": "Rover 5000",
    "specifications": {
      "dimensions": { "height": 1.5, "width": 1.8, "depth": 1.3 },
      "weight": 320,
      "materials": ["Graphene", "Plastic"],
      "mobility": ["Wheels", "Legs", "Wings", "Propellers"],
      "power": "Unlimited",
      "operationalTime": "Infinite"
    },
    "category": "Manufacturing",
    "date_created": "2023-05-15T16:30:00Z",
    "url_to_images": [
      "https://storage.googleapis.com/app-images-the-construct-401518/design_001.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_002.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_003.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_004.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_005.png"
    ],
    "current_status": "Production",
    "tags": ["Assembly", "Welding"],
    "additional_info": { "note": "Built for manufacturing and assembly tasks." }
  },
  {
    "design_id": "RD009",
    "designer": "Robotics Inc.",
    "robot_model": "Model E",
    "specifications": {
      "dimensions": { "height": 1.7, "width": 1.6, "depth": 1.4 },
      "weight": 350,
      "materials": ["Titanium", "Plastic"],
      "mobility": ["Wheels", "Tracks", "Propellers", "Wings"],
      "power": "Unlimited",
      "operationalTime": "Infinite"
    },
    "category": "Construction",
    "date_created": "2023-06-01T10:00:00Z",
    "url_to_images": [
      "https://storage.googleapis.com/app-images-the-construct-401518/design_001.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_002.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_003.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_004.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_005.png"
    ],
    "current_status": "Prototype",
    "tags": ["Excavation", "Demolition"],
    "additional_info": { "note": "This is a construction robot design." }
  },

  {
    "design_id": "RD010",
    "designer": "RoboTech Ltd.",
    "robot_model": "Rover 6000",
    "specifications": {
      "dimensions": { "height": 1.9, "width": 1.8, "depth": 1.5 },
      "weight": 380,
      "materials": ["Carbon fiber", "Plastic"],
      "mobility": ["Wheels", "Tracks", "Propellers", "Wings"],
      "power": "Unlimited",
      "operationalTime": "Infinite"
    },
    "category": "Agriculture",
    "date_created": "2023-06-15T14:15:00Z",
    "url_to_images": [
      "https://storage.googleapis.com/app-images-the-construct-401518/design_001.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_002.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_003.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_004.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_005.png"
    ],
    "current_status": "Production",
    "tags": ["Farming", "Harvesting"],
    "additional_info": { "note": "Built for agricultural tasks." }
  },
  {
    "design_id": "RD011",
    "designer": "Robotics Inc.",
    "robot_model": "Model F",
    "specifications": {
      "dimensions": { "height": 2.1, "width": 2.0, "depth": 1.6 },
      "weight": 400,
      "materials": ["Ceramic", "Plastic"],
      "mobility": ["Wheels", "Tracks", "Propellers", "Wings"],
      "power": "Unlimited",
      "operationalTime": "Infinite"
    },
    "category": "Transportation",
    "date_created": "2023-07-01T12:00:00Z",
    "url_to_images": [
      "https://storage.googleapis.com/app-images-the-construct-401518/design_001.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_002.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_003.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_004.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_005.png"
    ],
    "current_status": "Prototype",
    "tags": ["Cargo", "Passenger"],
    "additional_info": { "note": "This is a transportation robot design." }
  },

  {
    "design_id": "RD012",
    "designer": "RoboTech Ltd.",
    "robot_model": "Rover 7000",
    "specifications": {
      "dimensions": { "height": 2.3, "width": 2.2, "depth": 1.7 },
      "weight": 420,
      "materials": ["Diamond", "Plastic"],
      "mobility": ["Wheels", "Tracks", "Propellers", "Wings"],
      "power": "Unlimited",
      "operationalTime": "Infinite"
    },
    "category": "Exploration",
    "date_created": "2023-07-15T16:30:00Z",
    "url_to_images": [
      "https://storage.googleapis.com/app-images-the-construct-401518/design_001.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_002.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_003.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_004.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_005.png"
    ],
    "current_status": "Production",
    "tags": ["Space", "Research"],
    "additional_info": { "note": "Built for space exploration and research." }
  },

  {
    "design_id": "RD013",
    "designer": "Robotics Inc.",
    "robot_model": "Model G",
    "specifications": {
      "dimensions": { "height": 2.5, "width": 2.4, "depth": 1.8 },
      "weight": 450,
      "materials": ["Carbon fiber", "Plastic"],
      "mobility": ["Wheels", "Tracks", "Propellers", "Wings"],
      "power": "Unlimited",
      "operationalTime": "Infinite"
    },
    "category": "Military",
    "date_created": "2023-08-01T10:00:00Z",
    "url_to_images": [
      "https://storage.googleapis.com/app-images-the-construct-401518/design_001.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_002.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_003.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_004.png",
      "https://storage.googleapis.com/app-images-the-construct-401518/design_005.png"
    ],
    "current_status": "Prototype",
    "tags": ["Combat", "Surveillance"],
    "additional_info": { "note": "This is a military robot design." }
  }
]
