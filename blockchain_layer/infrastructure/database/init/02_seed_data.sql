-- Seed data for The Construct blockchain layer development

-- Insert test users
INSERT INTO blockchain.users (wallet_address, wallet_type, public_key, reputation_score, metadata) VALUES
('rTestManufacturer1234567890ABCDEF', 'xrpl', 'ED01234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF', 85, '{"company": "RoboTech Industries", "location": "San Francisco, CA", "specialties": ["servo_motors", "sensors"]}'),
('rTestCustomer1234567890FEDCBA', 'xrpl', 'ED0FEDCBA9876543210FEDCBA9876543210FEDCBA9876543210FEDCBA9876543210', 92, '{"company": "AutoBot Corp", "location": "Austin, TX", "projects": ["industrial_automation", "warehouse_robotics"]}'),
('rTestSupplier1234567890ABCDEF', 'xrpl', 'ED0ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890', 78, '{"company": "Component Supply Co", "location": "Seattle, WA", "inventory": ["electronic_components", "mechanical_parts"]}'),
('rTestInspector1234567890FEDCBA', 'xrpl', 'ED0FEDCBA0987654321FEDCBA0987654321FEDCBA0987654321FEDCBA0987654321', 95, '{"company": "Quality Assurance LLC", "location": "Denver, CO", "certifications": ["ISO9001", "IPC-A-610"]}}'),
('rTestTrader1234567890ABCDEF12', 'xrpl', 'ED012345ABCDEF67890123456789ABCDEF0123456789ABCDEF0123456789ABCDEF', 67, '{"trading_focus": "robotics_components", "risk_tolerance": "medium", "location": "New York, NY"}}')
ON CONFLICT (wallet_address) DO NOTHING;

-- Insert test assets (tokenized components)
INSERT INTO blockchain.assets (asset_id, asset_name, asset_description, asset_type, token_count, issuer_address, transaction_hash, metadata, specifications, manufacturer_info, status) VALUES
('SERVO_MOTOR_001', 'High-Precision Servo Motor', 'Industrial-grade servo motor with encoder feedback', 'component', 100, 'rTestManufacturer1234567890ABCDEF', 'mock_tx_servo_motor_001', 
 '{"category": "actuators", "weight": "2.5kg", "warranty": "2_years"}',
 '{"torque": "10Nm", "speed": "3000rpm", "voltage": "24V", "encoder_resolution": "4096ppr"}',
 '{"manufacturer": "RoboTech Industries", "model": "RT-SM-001", "batch": "2024-001"}', 'active'),

('TEMP_SENSOR_002', 'Temperature Sensor Module', 'High-accuracy temperature sensor with digital output', 'component', 250, 'rTestSupplier1234567890ABCDEF', 'mock_tx_temp_sensor_002',
 '{"category": "sensors", "weight": "0.1kg", "warranty": "1_year"}',
 '{"range": "-40C to 125C", "accuracy": "±0.5C", "interface": "I2C", "resolution": "0.1C"}',
 '{"manufacturer": "Component Supply Co", "model": "CS-TS-002", "batch": "2024-002"}', 'active'),

('GRIPPER_ARM_003', 'Robotic Gripper Assembly', 'Pneumatic gripper with force feedback', 'component', 50, 'rTestManufacturer1234567890ABCDEF', 'mock_tx_gripper_003',
 '{"category": "end_effectors", "weight": "1.8kg", "warranty": "18_months"}',
 '{"grip_force": "500N", "opening": "150mm", "pressure": "6bar", "feedback": "force_sensor"}',
 '{"manufacturer": "RoboTech Industries", "model": "RT-GA-003", "batch": "2024-003"}', 'active'),

('CONTROLLER_004', 'Motion Controller Board', 'Multi-axis motion controller with Ethernet interface', 'component', 75, 'rTestSupplier1234567890ABCDEF', 'mock_tx_controller_004',
 '{"category": "controllers", "weight": "0.5kg", "warranty": "3_years"}',
 '{"axes": "8", "interface": "Ethernet", "power": "24V", "io_points": "32"}',
 '{"manufacturer": "Component Supply Co", "model": "CS-MC-004", "batch": "2024-004"}', 'active'),

('VISION_CAM_005', 'Industrial Vision Camera', 'High-resolution camera for machine vision applications', 'component', 30, 'rTestManufacturer1234567890ABCDEF', 'mock_tx_vision_005',
 '{"category": "vision", "weight": "0.8kg", "warranty": "2_years"}',
 '{"resolution": "5MP", "fps": "60", "interface": "GigE", "lens_mount": "C-mount"}',
 '{"manufacturer": "RoboTech Industries", "model": "RT-VC-005", "batch": "2024-005"}', 'active')
ON CONFLICT (asset_id) DO NOTHING;

-- Insert test trading orders
INSERT INTO trading.orders (order_id, user_id, asset_id, order_type, amount, price, filled_amount, status, transaction_hash, expiration) VALUES
('ORDER_BUY_20250101120000', 
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestCustomer1234567890FEDCBA'),
 (SELECT id FROM blockchain.assets WHERE asset_id = 'SERVO_MOTOR_001'),
 'buy', 10.0, 25.50, 0, 'active', 'mock_order_tx_buy_001', NOW() + INTERVAL '7 days'),

('ORDER_SELL_20250101130000',
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestSupplier1234567890ABCDEF'),
 (SELECT id FROM blockchain.assets WHERE asset_id = 'TEMP_SENSOR_002'),
 'sell', 50.0, 15.75, 25.0, 'partially_filled', 'mock_order_tx_sell_002', NOW() + INTERVAL '5 days'),

('ORDER_BUY_20250101140000',
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestTrader1234567890ABCDEF12'),
 (SELECT id FROM blockchain.assets WHERE asset_id = 'GRIPPER_ARM_003'),
 'buy', 5.0, 120.00, 5.0, 'filled', 'mock_order_tx_buy_003', NOW() + INTERVAL '3 days'),

('ORDER_SELL_20250101150000',
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestManufacturer1234567890ABCDEF'),
 (SELECT id FROM blockchain.assets WHERE asset_id = 'CONTROLLER_004'),
 'sell', 20.0, 85.25, 0, 'active', 'mock_order_tx_sell_004', NOW() + INTERVAL '10 days')
ON CONFLICT (order_id) DO NOTHING;

-- Insert test escrows
INSERT INTO trading.escrows (escrow_id, creator_id, destination_address, amount, condition_hash, finish_after, status, transaction_hash) VALUES
('ESCROW_20250101160000',
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestCustomer1234567890FEDCBA'),
 'rTestManufacturer1234567890ABCDEF', 1275.0, 'mock_condition_hash_001', NOW() + INTERVAL '30 days', 'active', 'mock_escrow_tx_001'),

('ESCROW_20250101170000',
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestTrader1234567890ABCDEF12'),
 'rTestSupplier1234567890ABCDEF', 600.0, 'mock_condition_hash_002', NOW() + INTERVAL '14 days', 'active', 'mock_escrow_tx_002')
ON CONFLICT (escrow_id) DO NOTHING;

-- Insert test manufacturing orders
INSERT INTO manufacturing.orders (order_id, customer_id, manufacturer_id, component_id, quantity, specifications, delivery_address, max_price, deadline, status) VALUES
('MFG_ORDER_20250101180000',
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestCustomer1234567890FEDCBA'),
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestManufacturer1234567890ABCDEF'),
 (SELECT id FROM blockchain.assets WHERE asset_id = 'SERVO_MOTOR_001'),
 25, '{"custom_torque": "12Nm", "custom_voltage": "48V", "special_coating": "corrosion_resistant"}',
 '123 Industrial Blvd, Austin, TX 78701', 750.00, NOW() + INTERVAL '45 days', 'in_progress'),

('MFG_ORDER_20250101190000',
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestTrader1234567890ABCDEF12'),
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestManufacturer1234567890ABCDEF'),
 (SELECT id FROM blockchain.assets WHERE asset_id = 'VISION_CAM_005'),
 10, '{"custom_resolution": "8MP", "special_lens": "wide_angle", "housing": "IP67"}',
 '456 Tech Park Dr, New York, NY 10001', 1200.00, NOW() + INTERVAL '60 days', 'pending')
ON CONFLICT (order_id) DO NOTHING;

-- Insert test manufacturing milestones
INSERT INTO manufacturing.milestones (order_id, milestone_number, description, payment_percentage, status, completed_at, payment_released, transaction_hash) VALUES
((SELECT id FROM manufacturing.orders WHERE order_id = 'MFG_ORDER_20250101180000'), 1, 'Design approval and material procurement', 25.00, 'completed', NOW() - INTERVAL '10 days', true, 'mock_milestone_tx_001'),
((SELECT id FROM manufacturing.orders WHERE order_id = 'MFG_ORDER_20250101180000'), 2, 'Manufacturing and initial testing', 50.00, 'in_progress', NULL, false, NULL),
((SELECT id FROM manufacturing.orders WHERE order_id = 'MFG_ORDER_20250101180000'), 3, 'Quality assurance and final testing', 20.00, 'pending', NULL, false, NULL),
((SELECT id FROM manufacturing.orders WHERE order_id = 'MFG_ORDER_20250101180000'), 4, 'Packaging and shipping', 5.00, 'pending', NULL, false, NULL),

((SELECT id FROM manufacturing.orders WHERE order_id = 'MFG_ORDER_20250101190000'), 1, 'Requirements analysis and design', 30.00, 'pending', NULL, false, NULL),
((SELECT id FROM manufacturing.orders WHERE order_id = 'MFG_ORDER_20250101190000'), 2, 'Prototype development', 40.00, 'pending', NULL, false, NULL),
((SELECT id FROM manufacturing.orders WHERE order_id = 'MFG_ORDER_20250101190000'), 3, 'Production and testing', 25.00, 'pending', NULL, false, NULL),
((SELECT id FROM manufacturing.orders WHERE order_id = 'MFG_ORDER_20250101190000'), 4, 'Delivery and installation support', 5.00, 'pending', NULL, false, NULL);

-- Insert test quality assurance records
INSERT INTO manufacturing.quality_assurance (order_id, inspector_id, quality_metrics, passed, notes) VALUES
((SELECT id FROM manufacturing.orders WHERE order_id = 'MFG_ORDER_20250101180000'),
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestInspector1234567890FEDCBA'),
 '{"dimensional_accuracy": 0.98, "surface_finish": "excellent", "electrical_tests": "passed", "performance_tests": "passed"}',
 true, 'All milestone 1 deliverables meet specifications. Approved for next phase.');

-- Insert test governance proposals
INSERT INTO governance.proposals (proposal_id, proposer_id, title, description, proposal_type, voting_start, voting_end, status, votes_for, votes_against, total_votes) VALUES
('PROP_20250101200000',
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestManufacturer1234567890ABCDEF'),
 'Implement Quality Certification Program',
 'Proposal to establish a blockchain-based quality certification program for all manufactured components, including mandatory third-party inspections and digital certificates.',
 'platform_improvement', NOW() - INTERVAL '2 days', NOW() + INTERVAL '5 days', 'active', 3, 1, 4),

('PROP_20250101210000',
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestCustomer1234567890FEDCBA'),
 'Reduce Trading Fees for High-Volume Users',
 'Proposal to implement a tiered fee structure that reduces trading fees for users who complete more than 100 transactions per month.',
 'fee_adjustment', NOW() - INTERVAL '1 day', NOW() + INTERVAL '6 days', 'active', 2, 0, 2)
ON CONFLICT (proposal_id) DO NOTHING;

-- Insert test governance votes
INSERT INTO governance.votes (proposal_id, voter_id, vote_type, voting_power, transaction_hash) VALUES
((SELECT id FROM governance.proposals WHERE proposal_id = 'PROP_20250101200000'),
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestCustomer1234567890FEDCBA'),
 'for', 1, 'mock_vote_tx_001'),
((SELECT id FROM governance.proposals WHERE proposal_id = 'PROP_20250101200000'),
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestSupplier1234567890ABCDEF'),
 'for', 1, 'mock_vote_tx_002'),
((SELECT id FROM governance.proposals WHERE proposal_id = 'PROP_20250101200000'),
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestInspector1234567890FEDCBA'),
 'for', 1, 'mock_vote_tx_003'),
((SELECT id FROM governance.proposals WHERE proposal_id = 'PROP_20250101200000'),
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestTrader1234567890ABCDEF12'),
 'against', 1, 'mock_vote_tx_004'),

((SELECT id FROM governance.proposals WHERE proposal_id = 'PROP_20250101210000'),
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestTrader1234567890ABCDEF12'),
 'for', 1, 'mock_vote_tx_005'),
((SELECT id FROM governance.proposals WHERE proposal_id = 'PROP_20250101210000'),
 (SELECT id FROM blockchain.users WHERE wallet_address = 'rTestManufacturer1234567890ABCDEF'),
 'for', 1, 'mock_vote_tx_006')
ON CONFLICT (proposal_id, voter_id) DO NOTHING;

-- Insert test transactions
INSERT INTO blockchain.transactions (transaction_hash, transaction_type, from_address, to_address, amount, fee, status, block_number, block_hash, gas_used, metadata, confirmed_at) VALUES
('mock_tx_servo_motor_001', 'TokenCreate', 'rTestManufacturer1234567890ABCDEF', NULL, 0, 0.00001, 'confirmed', 1234567, 'mock_block_hash_001', 21000, '{"asset_id": "SERVO_MOTOR_001", "token_count": 100}', NOW() - INTERVAL '5 days'),
('mock_tx_temp_sensor_002', 'TokenCreate', 'rTestSupplier1234567890ABCDEF', NULL, 0, 0.00001, 'confirmed', 1234568, 'mock_block_hash_002', 21000, '{"asset_id": "TEMP_SENSOR_002", "token_count": 250}', NOW() - INTERVAL '4 days'),
('mock_order_tx_buy_001', 'OfferCreate', 'rTestCustomer1234567890FEDCBA', NULL, 255.0, 0.00001, 'confirmed', 1234569, 'mock_block_hash_003', 21000, '{"order_id": "ORDER_BUY_20250101120000", "order_type": "buy"}', NOW() - INTERVAL '3 days'),
('mock_escrow_tx_001', 'EscrowCreate', 'rTestCustomer1234567890FEDCBA', 'rTestManufacturer1234567890ABCDEF', 1275.0, 0.00001, 'confirmed', 1234570, 'mock_block_hash_004', 21000, '{"escrow_id": "ESCROW_20250101160000"}', NOW() - INTERVAL '2 days'),
('mock_milestone_tx_001', 'Payment', 'rTestCustomer1234567890FEDCBA', 'rTestManufacturer1234567890ABCDEF', 187.5, 0.00001, 'confirmed', 1234571, 'mock_block_hash_005', 21000, '{"milestone": 1, "order_id": "MFG_ORDER_20250101180000"}', NOW() - INTERVAL '1 day')
ON CONFLICT (transaction_hash) DO NOTHING;

-- Insert test price feeds
INSERT INTO blockchain.price_feeds (asset_symbol, price, source, timestamp, metadata) VALUES
('XRP', 0.52, 'coingecko', NOW() - INTERVAL '5 minutes', '{"volume_24h": 1234567890, "market_cap": 29876543210}'),
('XRP', 0.521, 'coinmarketcap', NOW() - INTERVAL '3 minutes', '{"volume_24h": 1245678901, "market_cap": 29987654321}'),
('SOL', 98.45, 'coingecko', NOW() - INTERVAL '4 minutes', '{"volume_24h": 987654321, "market_cap": 43210987654}'),
('SOL', 98.52, 'coinmarketcap', NOW() - INTERVAL '2 minutes', '{"volume_24h": 998765432, "market_cap": 43321098765}'),
('BTC', 43250.75, 'coingecko', NOW() - INTERVAL '6 minutes', '{"volume_24h": 12345678901, "market_cap": 847392847392}'),
('ETH', 2650.25, 'coinmarketcap', NOW() - INTERVAL '1 minute', '{"volume_24h": 8765432109, "market_cap": 318472847392}');

-- Update sequences to avoid conflicts with inserted data
SELECT setval('blockchain.users_id_seq', (SELECT MAX(id) FROM blockchain.users), true);
SELECT setval('blockchain.assets_id_seq', (SELECT MAX(id) FROM blockchain.assets), true);
SELECT setval('trading.orders_id_seq', (SELECT MAX(id) FROM trading.orders), true);
SELECT setval('trading.escrows_id_seq', (SELECT MAX(id) FROM trading.escrows), true);
SELECT setval('manufacturing.orders_id_seq', (SELECT MAX(id) FROM manufacturing.orders), true);
SELECT setval('manufacturing.milestones_id_seq', (SELECT MAX(id) FROM manufacturing.milestones), true);
SELECT setval('manufacturing.quality_assurance_id_seq', (SELECT MAX(id) FROM manufacturing.quality_assurance), true);
SELECT setval('governance.proposals_id_seq', (SELECT MAX(id) FROM governance.proposals), true);
SELECT setval('governance.votes_id_seq', (SELECT MAX(id) FROM governance.votes), true);
SELECT setval('blockchain.transactions_id_seq', (SELECT MAX(id) FROM blockchain.transactions), true);
SELECT setval('blockchain.price_feeds_id_seq', (SELECT MAX(id) FROM blockchain.price_feeds), true);
