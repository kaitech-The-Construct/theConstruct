-- The Construct Database Initialization Script
-- Creates initial tables and data for the Decentralized Robotics Exchange

-- Create database if it doesn't exist
SELECT 'CREATE DATABASE theconstruct_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'theconstruct_db');

-- Connect to the database
\c theconstruct_db;

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    wallet_address VARCHAR(255),
    reputation_score INTEGER DEFAULT 0,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Products/Components table
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    seller_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    specifications JSONB,
    images TEXT[],
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    buyer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    seller_id UUID REFERENCES users(id) ON DELETE CASCADE,
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    transaction_hash VARCHAR(255),
    escrow_address VARCHAR(255),
    shipping_address JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Manufacturing orders table
CREATE TABLE IF NOT EXISTS manufacturing_orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    manufacturer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    specifications JSONB NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    milestones JSONB,
    smart_contract_address VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Blockchain transactions table
CREATE TABLE IF NOT EXISTS blockchain_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    blockchain VARCHAR(20) NOT NULL, -- 'xrpl' or 'solana'
    transaction_hash VARCHAR(255) NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    amount DECIMAL(20, 8),
    status VARCHAR(20) DEFAULT 'pending',
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reviewer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    reviewee_id UUID REFERENCES users(id) ON DELETE CASCADE,
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Software/Programs table
CREATE TABLE IF NOT EXISTS software_programs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    developer_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    version VARCHAR(20) NOT NULL,
    compatibility JSONB, -- Compatible robot types/models
    license_type VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2),
    download_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Subscriptions table
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    software_id UUID REFERENCES software_programs(id) ON DELETE CASCADE,
    subscription_type VARCHAR(50) NOT NULL,
    start_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_date TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    payment_method VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_wallet ON users(wallet_address);
CREATE INDEX IF NOT EXISTS idx_products_seller ON products(seller_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_orders_buyer ON orders(buyer_id);
CREATE INDEX IF NOT EXISTS idx_orders_seller ON orders(seller_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_blockchain_tx_user ON blockchain_transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_blockchain_tx_hash ON blockchain_transactions(transaction_hash);

-- Insert some sample data for development
INSERT INTO users (email, username, password_hash, wallet_address, reputation_score, is_verified) VALUES
('alice@example.com', 'alice_builder', '$2b$12$KIXkWx.DoFLPlvP8KT5Ske7mGV/L5vZ.LhF9H6XHkF5dD8w9Xqv3W', 'rN7n7otQDd6FDbvzLYgMBZyEG1w8LnFz4s', 95, true),
('bob@example.com', 'bob_dev', '$2b$12$KIXkWx.DoFLPlvP8KT5Ske7mGV/L5vZ.LhF9H6XHkF5dD8w9Xqv3W', 'rLNaPoKeeBjZe2qs6x8EyLwcsYe5QU5W4X', 88, true),
('charlie@example.com', 'charlie_manufacturer', '$2b$12$KIXkWx.DoFLPlvP8KT5Ske7mGV/L5vZ.LhF9H6XHkF5dD8w9Xqv3W', 'rBKPS4oLBuEYF5NQmPvQJQJ3zwh9L9b6xL', 92, true);

INSERT INTO products (seller_id, name, description, category, price, stock_quantity, specifications) VALUES
((SELECT id FROM users WHERE username = 'alice_builder'), 
 'High-Torque Servo Motor', 
 'Industrial grade servo motor with precise control and high torque output', 
 'actuators', 
 149.99, 
 25, 
 '{"voltage": "12V", "torque": "15kg-cm", "speed": "60RPM", "weight": "120g"}'
),
((SELECT id FROM users WHERE username = 'alice_builder'), 
 'Aluminum Robot Chassis', 
 'Lightweight aluminum chassis for medium-sized robots', 
 'chassis', 
 89.99, 
 15, 
 '{"material": "6061 Aluminum", "weight": "500g", "dimensions": "30x20x10cm", "mounting_holes": 20}'
);

INSERT INTO software_programs (developer_id, name, description, version, compatibility, license_type, price) VALUES
((SELECT id FROM users WHERE username = 'bob_dev'), 
 'RoboNav Pro', 
 'Advanced navigation software with obstacle avoidance and path planning', 
 '2.1.0', 
 '{"robot_types": ["mobile", "autonomous"], "min_sensors": ["lidar", "camera"]}', 
 'subscription', 
 29.99
);

-- Create triggers to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply the trigger to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON orders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_manufacturing_orders_updated_at BEFORE UPDATE ON manufacturing_orders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_software_programs_updated_at BEFORE UPDATE ON software_programs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
