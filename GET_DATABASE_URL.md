# Get Your Database Connection URL

## Option 1: Via Render Dashboard (Easiest)

1. **Go to your database dashboard**:
   https://dashboard.render.com/d/dpg-d65le1cr85hc73e7b0jg-a

2. **Scroll down to "Connections" section**

3. **Copy the "Internal Database URL"**
   - It will look like: `postgresql://username:password@hostname/database`
   - This is the complete connection string with password included

4. **Add it to your web service**:
   - Go to: https://dashboard.render.com/web/srv-d65m9gnpm1nc73ecaglg
   - Click "Environment" tab
   - Add new environment variable:
     - Key: `DATABASE_URL`
     - Value: [paste the Internal Database URL]
   - Click "Save Changes"

## Option 2: Let me add it programmatically

If you provide me with the Internal Database URL (from step 3 above), I can add it for you using the Render MCP.

---

## Why This is Needed

Your Django app needs the `DATABASE_URL` to connect to PostgreSQL. Without it:
- ❌ Build will succeed but app will crash
- ❌ Database migrations won't run
- ❌ App won't start properly

## Current Deployment Status

- Service URL: https://codeventure-ez4m.onrender.com
- Status: Building (will fail without DATABASE_URL)
- Region: Singapore
- Database: codeventure-db (available)
