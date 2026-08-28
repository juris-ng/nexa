-- NEXA Database Schema
-- Migration: 001_initial_schema
-- Description: Core tables for world state

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Cities
CREATE TABLE cities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Districts
CREATE TABLE districts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    city_id UUID REFERENCES cities(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Locations
CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    district_id UUID REFERENCES districts(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    coordinates JSONB,
    location_type VARCHAR(50) NOT NULL,
    access_level VARCHAR(50) DEFAULT 'public',
    importance DECIMAL(5,2) DEFAULT 50.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Buildings
CREATE TABLE buildings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location_id UUID REFERENCES locations(id) ON DELETE CASCADE,
    building_type VARCHAR(50) NOT NULL,
    owner_id UUID,
    security_level DECIMAL(5,2) DEFAULT 50.00,
    importance DECIMAL(5,2) DEFAULT 50.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Businesses
CREATE TABLE businesses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    building_id UUID REFERENCES buildings(id) ON DELETE CASCADE,
    owner_id UUID,
    name VARCHAR(255) NOT NULL,
    revenue DECIMAL(15,2) DEFAULT 0.00,
    expenses DECIMAL(15,2) DEFAULT 0.00,
    reputation DECIMAL(5,2) DEFAULT 50.00,
    inventory JSONB,
    prices JSONB,
    operating_hours JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Characters
CREATE TABLE characters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    age INTEGER,
    occupation VARCHAR(255),
    location_id UUID REFERENCES locations(id),
    wealth DECIMAL(15,2) DEFAULT 0.00,
    health_state VARCHAR(50) DEFAULT 'healthy',
    personality JSONB,
    goals JSONB,
    needs JSONB,
    fears JSONB,
    beliefs JSONB,
    faction_id UUID,
    reputation DECIMAL(5,2) DEFAULT 50.00,
    memories JSONB,
    knowledge JSONB,
    secrets JSONB,
    schedule JSONB,
    current_activity VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Character Traits
CREATE TABLE character_traits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    character_id UUID REFERENCES characters(id) ON DELETE CASCADE,
    trait_type VARCHAR(100) NOT NULL,
    trait_value JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Factions
CREATE TABLE factions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    ideology VARCHAR(255),
    leaders JSONB,
    members JSONB,
    resources DECIMAL(15,2) DEFAULT 0.00,
    wealth DECIMAL(15,2) DEFAULT 0.00,
    political_power DECIMAL(5,2) DEFAULT 50.00,
    public_support DECIMAL(5,2) DEFAULT 50.00,
    relationships JSONB,
    goals JSONB,
    conflicts JSONB,
    secrets JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Organizations
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    org_type VARCHAR(50) NOT NULL,
    leaders JSONB,
    members JSONB,
    resources DECIMAL(15,2) DEFAULT 0.00,
    headquarters_id UUID REFERENCES locations(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Relationships
CREATE TABLE relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    character_a_id UUID REFERENCES characters(id) ON DELETE CASCADE,
    character_b_id UUID REFERENCES characters(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL,
    trust DECIMAL(5,2) DEFAULT 50.00,
    affection DECIMAL(5,2) DEFAULT 50.00,
    fear DECIMAL(5,2) DEFAULT 0.00,
    respect DECIMAL(5,2) DEFAULT 50.00,
    resentment DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Players
CREATE TABLE players (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    external_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Player Reputation
CREATE TABLE player_reputation (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    player_id UUID REFERENCES players(id) ON DELETE CASCADE,
    faction_id UUID REFERENCES factions(id) ON DELETE CASCADE,
    reputation_score DECIMAL(5,2) DEFAULT 50.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Events
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    cause VARCHAR(255),
    actors JSONB,
    location_id UUID REFERENCES locations(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    visibility VARCHAR(50) DEFAULT 'public',
    importance INTEGER DEFAULT 1,
    evidence JSONB,
    consequences JSONB,
    related_factions JSONB,
    related_mysteries JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Event Consequences
CREATE TABLE event_consequences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_id UUID REFERENCES events(id) ON DELETE CASCADE,
    consequence_type VARCHAR(100) NOT NULL,
    target_type VARCHAR(50) NOT NULL,
    target_id UUID NOT NULL,
    effect JSONB NOT NULL,
    delay_type VARCHAR(50) DEFAULT 'immediate',
    executed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Mysteries
CREATE TABLE mysteries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    premise TEXT NOT NULL,
    hidden_truth TEXT,
    suspects JSONB,
    evidence JSONB,
    false_leads JSONB,
    events JSONB,
    revelations JSONB,
    resolution TEXT,
    state VARCHAR(50) DEFAULT 'hidden',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Evidence
CREATE TABLE evidence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    mystery_id UUID REFERENCES mysteries(id) ON DELETE CASCADE,
    source VARCHAR(255),
    reliability DECIMAL(5,2) DEFAULT 50.00,
    location_id UUID REFERENCES locations(id),
    visibility VARCHAR(50) DEFAULT 'hidden',
    linked_character_id UUID REFERENCES characters(id),
    linked_event_id UUID REFERENCES events(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- World State
CREATE TABLE world_state (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    simulation_day INTEGER DEFAULT 1,
    simulation_time TIME DEFAULT '00:00:00',
    mayor_approval DECIMAL(5,2) DEFAULT 50.00,
    food_prices_change DECIMAL(5,2) DEFAULT 0.00,
    unemployment_rate DECIMAL(5,2) DEFAULT 10.00,
    union_anger DECIMAL(5,2) DEFAULT 50.00,
    crime_rate DECIMAL(5,2) DEFAULT 20.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Economy
CREATE TABLE economy (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Politics
CREATE TABLE politics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- News
CREATE TABLE news (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    headline VARCHAR(500) NOT NULL,
    article TEXT,
    source_organization_id UUID REFERENCES organizations(id),
    event_id UUID REFERENCES events(id),
    visibility VARCHAR(50) DEFAULT 'public',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Memories
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    character_id UUID REFERENCES characters(id) ON DELETE CASCADE,
    memory_type VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    importance INTEGER DEFAULT 50,
    emotional_weight INTEGER DEFAULT 50,
    recency DECIMAL(5,2) DEFAULT 50.00,
    relationship_id UUID REFERENCES relationships(id),
    secrecy INTEGER DEFAULT 50,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    participant_a_id UUID REFERENCES characters(id) ON DELETE CASCADE,
    participant_b_id UUID REFERENCES characters(id) ON DELETE CASCADE,
    content JSONB NOT NULL,
    location_id UUID REFERENCES locations(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    simulation_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_characters_location ON characters(location_id);
CREATE INDEX idx_characters_faction ON characters(faction_id);
CREATE INDEX idx_events_location ON events(location_id);
CREATE INDEX idx_relationships_character_a ON relationships(character_a_id);
CREATE INDEX idx_relationships_character_b ON relationships(character_b_id);
CREATE INDEX idx_memories_character ON memories(character_id);