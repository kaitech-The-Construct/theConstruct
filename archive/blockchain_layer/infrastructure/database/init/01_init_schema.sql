-- Initialize The Construct blockchain layer database schema

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS blockchain;
CREATE SCHEMA IF NOT EXISTS trading;
CREATE SCHEMA IF NOT EXISTS manufacturing;
CREATE SCHEMA IF NOT EXISTS governance;

-- Set search path
SET search_path TO blockchain, trading, manufacturing, governance, public;

-- Users and accounts table
CREATE TABLE IF NOT EXISTS blockchain.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    wallet_address VARCHAR(255) UNIQUE NOT NULL,
    wallet_type VARCHAR(50) NOT NULL DEFAULT 'xrpl',
    public_key TEXT,
    reputation_score INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Assets table for tokenized components
CREATE TABLE IF NOT EXISTS blockchain.assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id VARCHAR(255) UNIQUE NOT NULL,
    asset_name VARCHAR(255) NOT NULL,
    asset_description TEXT,
    asset_type VARCHAR(50) NOT NULL,
    token_count INTEGER NOT NULL,
    issuer_address VARCHAR(255) NOT NULL,
    transaction_hash VARCHAR(255),
    metadata JSONB DEFAULT '{}'::jsonb,
    specifications JSONB DEFAULT '{}'::jsonb,
    manufacturer_info JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'pending'
);

-- Trading orders table
CREATE TABLE IF NOT EXISTS trading.orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id VARCHAR(255) UNIQUE NOT NULL,
    user_id UUID REFERENCES blockchain.users(id),
    asset_id UUID REFERENCES blockchain.assets(id),
    order_type VARCHAR(10) NOT NULL CHECK (order_type IN ('buy', 'sell')),
    amount DECIMAL(18, 8) NOT NULL,
    price DECIMAL(18, 8) NOT NULL,
    filled_amount DECIMAL(18, 8) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    transaction_hash VARCHAR(255),
    expiration TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Escrows table
CREATE TABLE IF NOT EXISTS trading.escrows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    escrow_id VARCHAR(255) UNIQUE NOT NULL,
    creator_id UUID REFERENCES blockchain.users(id),
    destination_address VARCHAR(255) NOT NULL,
    amount DECIMAL(18, 8) NOT NULL,
    condition_hash VARCHAR(255),
    finish_after TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'created',
    transaction_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Manufacturing orders table
CREATE TABLE IF NOT EXISTS manufacturing.orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id VARCHAR(255) UNIQUE NOT NULL,
    customer_id UUID REFERENCES blockchain.users(id),
    manufacturer_id UUID REFERENCES blockchain.users(id),
    component_id UUID REFERENCES blockchain.assets(id),
    quantity INTEGER NOT NULL,
    specifications JSONB NOT NULL,
    delivery_address TEXT NOT NULL,
    max_price DECIMAL(18, 8) NOT NULL,
    deadline TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Manufacturing milestones table
CREATE TABLE IF NOT EXISTS manufacturing.milestones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES manufacturing.orders(id),
    milestone_number INTEGER NOT NULL,
    description TEXT NOT NULL,
    payment_percentage DECIMAL(5, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    completed_at TIMESTAMP WITH TIME ZONE,
    payment_released BOOLEAN DEFAULT false,
    transaction_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Quality assurance table
CREATE TABLE IF NOT EXISTS manufacturing.quality_assurance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES manufacturing.orders(id),
    inspector_id UUID REFERENCES blockchain.users(id),
    quality_metrics JSONB NOT NULL,
    passed BOOLEAN NOT NULL,
    notes TEXT,
    inspection_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Governance proposals table
CREATE TABLE IF NOT EXISTS governance.proposals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    proposal_id VARCHAR(255) UNIQUE NOT NULL,
    proposer_id UUID REFERENCES blockchain.users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    proposal_type VARCHAR(50) NOT NULL,
    voting_start TIMESTAMP WITH TIME ZONE NOT NULL,
    voting_end TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    votes_for INTEGER DEFAULT 0,
    votes_against INTEGER DEFAULT 0,
    total_votes INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Governance votes table
CREATE TABLE IF NOT EXISTS governance.votes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    proposal_id UUID REFERENCES governance.proposals(id),
    voter_id UUID REFERENCES blockchain.users(id),
    vote_type VARCHAR(10) NOT NULL CHECK (vote_type IN ('for', 'against', 'abstain')),
    voting_power INTEGER NOT NULL DEFAULT 1,
    transaction_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(proposal_id, voter_id)
);

-- Transactions log table
CREATE TABLE IF NOT EXISTS blockchain.transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_hash VARCHAR(255) UNIQUE NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    from_address VARCHAR(255),
    to_address VARCHAR(255),
    amount DECIMAL(18, 8),
    fee DECIMAL(18, 8),
    status VARCHAR(20) DEFAULT 'pending',
    block_number BIGINT,
    block_hash VARCHAR(255),
    gas_used BIGINT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    confirmed_at TIMESTAMP WITH TIME ZONE
);

-- Price feeds table for oracle data
CREATE TABLE IF NOT EXISTS blockchain.price_feeds (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_symbol VARCHAR(20) NOT NULL,
    price DECIMAL(18, 8) NOT NULL,
    source VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_wallet_address ON blockchain.users(wallet_address);
CREATE INDEX IF NOT EXISTS idx_assets_asset_id ON blockchain.assets(asset_id);
CREATE INDEX IF NOT EXISTS idx_assets_issuer ON blockchain.assets(issuer_address);
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON trading.orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_asset_id ON trading.orders(asset_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON trading.orders(status);
CREATE INDEX IF NOT EXISTS idx_escrows_creator ON trading.escrows(creator_id);
CREATE INDEX IF NOT EXISTS idx_manufacturing_orders_customer ON manufacturing.orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_manufacturing_orders_manufacturer ON manufacturing.orders(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_milestones_order_id ON manufacturing.milestones(order_id);
CREATE INDEX IF NOT EXISTS idx_proposals_status ON governance.proposals(status);
CREATE INDEX IF NOT EXISTS idx_votes_proposal_id ON governance.votes(proposal_id);
CREATE INDEX IF NOT EXISTS idx_transactions_hash ON blockchain.transactions(transaction_hash);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON blockchain.transactions(transaction_type);
CREATE INDEX IF NOT EXISTS idx_price_feeds_symbol ON blockchain.price_feeds(asset_symbol);
CREATE INDEX IF NOT EXISTS idx_price_feeds_timestamp ON blockchain.price_feeds(timestamp);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at columns
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON blockchain.users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_assets_updated_at BEFORE UPDATE ON blockchain.assets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_orders_updated_at BEFORE UPDATE ON trading.orders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_escrows_updated_at BEFORE UPDATE ON trading.escrows FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_manufacturing_orders_updated_at BEFORE UPDATE ON manufacturing.orders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_milestones_updated_at BEFORE UPDATE ON manufacturing.milestones FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_proposals_updated_at BEFORE UPDATE ON governance.proposals FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
