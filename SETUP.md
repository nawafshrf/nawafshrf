# SmartTools AI - Setup Guide

## Quick Start

### 1. Set Up Supabase (Free)
1. Go to [supabase.com](https://supabase.com) and create a free project
2. Go to **SQL Editor** and run the contents of `supabase-schema.sql`
3. Go to **Settings > API** and copy your:
   - Project URL → `NEXT_PUBLIC_SUPABASE_URL`
   - Anon key → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - Service role key → `SUPABASE_SERVICE_ROLE_KEY`

### 2. Set Up OpenAI API
1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new API key → `OPENAI_API_KEY`
3. Add credits ($5-10 is enough to start)

### 3. Set Up Stripe
1. Go to [dashboard.stripe.com](https://dashboard.stripe.com)
2. Create an account (use test mode first)
3. Copy your API keys:
   - Secret key → `STRIPE_SECRET_KEY`
   - Publishable key → `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
4. Create a Product:
   - Name: "SmartTools Pro"
   - Price: $9.99/month recurring
   - Copy the Price ID → `STRIPE_PRICE_ID`
5. Set up Webhook:
   - Endpoint URL: `https://your-domain.com/api/stripe/webhook`
   - Events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`
   - Copy Webhook signing secret → `STRIPE_WEBHOOK_SECRET`

### 4. Set Up Google OAuth (Optional)
1. Go to [console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)
2. Create OAuth 2.0 credentials
3. Set redirect URI: `https://your-domain.com/api/auth/callback/google`
4. Copy Client ID → `GOOGLE_CLIENT_ID`
5. Copy Client Secret → `GOOGLE_CLIENT_SECRET`

### 5. Create `.env.local`
```bash
cp .env.example .env.local
# Fill in all the values from steps above
```

### 6. Run Locally
```bash
npm install
npm run dev
# Open http://localhost:3000
```

### 7. Deploy to Vercel
1. Push to GitHub
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import your repository
4. Add all environment variables from `.env.local`
5. Set `NEXTAUTH_URL` to your Vercel domain
6. Deploy!

## Monthly Costs
- **Vercel**: Free (hobby tier)
- **Supabase**: Free (500MB database)
- **OpenAI**: ~$15-30/month at 1,000 daily users
- **Stripe**: 2.9% + $0.30 per transaction

## Revenue Model
- Free: 5 uses/day (drives SEO traffic)
- Pro: $9.99/month unlimited
- Target: 2-5% conversion rate from free to paid
