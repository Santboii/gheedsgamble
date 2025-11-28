-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  image TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create runs table
CREATE TABLE IF NOT EXISTS runs (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  timestamp BIGINT NOT NULL,
  class_name TEXT NOT NULL,
  build TEXT NOT NULL,
  challenges JSONB DEFAULT '[]'::jsonb,
  status TEXT NOT NULL CHECK (status IN ('active', 'completed', 'failed')),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_runs_user_id ON runs(user_id);

-- Create index on timestamp for sorting
CREATE INDEX IF NOT EXISTS idx_runs_timestamp ON runs(timestamp DESC);
