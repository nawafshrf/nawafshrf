-- NotionBoost Database Schema
-- Run this SQL in your Supabase dashboard SQL editor

-- Users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  image TEXT,
  stripe_customer_id TEXT,
  subscription_status TEXT DEFAULT 'free',
  subscription_id TEXT,
  gumroad_access_token TEXT,
  gumroad_user_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Usage tracking table
CREATE TABLE IF NOT EXISTS usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  session_id TEXT,
  tool_slug TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Template purchases table
CREATE TABLE IF NOT EXISTS template_purchases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  template_slug TEXT NOT NULL,
  stripe_payment_id TEXT,
  amount INTEGER NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Gumroad published templates
CREATE TABLE IF NOT EXISTS gumroad_listings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) NOT NULL,
  template_name TEXT NOT NULL,
  gumroad_product_id TEXT,
  gumroad_url TEXT,
  notion_template_url TEXT,
  price INTEGER NOT NULL,
  status TEXT DEFAULT 'draft',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for fast lookups
CREATE INDEX IF NOT EXISTS idx_usage_session ON usage(session_id, created_at);
CREATE INDEX IF NOT EXISTS idx_usage_user ON usage(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_stripe ON users(stripe_customer_id);
CREATE INDEX IF NOT EXISTS idx_purchases_user ON template_purchases(user_id);
CREATE INDEX IF NOT EXISTS idx_purchases_template ON template_purchases(template_slug);
CREATE INDEX IF NOT EXISTS idx_gumroad_user ON gumroad_listings(user_id);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE template_purchases ENABLE ROW LEVEL SECURITY;
ALTER TABLE gumroad_listings ENABLE ROW LEVEL SECURITY;

-- Policies (service role bypasses RLS)
CREATE POLICY "Service role can manage users" ON users
  FOR ALL USING (true);

CREATE POLICY "Service role can manage usage" ON usage
  FOR ALL USING (true);

CREATE POLICY "Service role can manage purchases" ON template_purchases
  FOR ALL USING (true);

CREATE POLICY "Service role can manage gumroad" ON gumroad_listings
  FOR ALL USING (true);
