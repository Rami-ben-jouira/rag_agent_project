# 🗄️ Neo4j AuraDB Setup Guide

## Step-by-Step Instructions to Create Your Own Neo4j Database

### Step 1: Create Neo4j AuraDB Account

1. **Go to Neo4j AuraDB**: https://neo4j.com/cloud/aura/
2. **Click "Try Free"** or "Sign Up"
3. **Create Account**:
   - Use email or Google/GitHub account
   - Verify your email if required

### Step 2: Create a New Database Instance

1. **Login** to Neo4j AuraDB Console: https://console.neo4j.io/
2. **Click "New Instance"** or "Create Database"
3. **Choose Plan**:
   - Select **"Free"** tier (200K nodes, 400K relationships)
   - Perfect for development and testing

4. **Configure Database**:
   - **Name**: Choose a name (e.g., "medical-rag-db")
   - **Region**: Select closest region
   - **Version**: Use latest stable version

5. **Set Password**:
   - Create a **strong password** (save it securely!)
   - You'll need this for connection

### Step 3: Get Your Connection Details

After database creation (takes 1-2 minutes):

1. **Click on your database instance**
2. **Find "Connection Details"** section
3. **Copy these values**:

```
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password_here
```

**Important Notes:**
- URI format: `neo4j+s://` (the `+s` means secure/encrypted)
- Username is always `neo4j` for AuraDB
- Password is the one you set during creation

### Step 4: Update Your .env File

1. **Open `.env` file** in your project
2. **Replace with your new credentials**:

```env
NEO4J_URI=neo4j+s://your-instance-id.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_new_password
```

### Step 5: Test Connection

Run this Python command to test:

```python
from src.graph import get_graph_db
graph = get_graph_db()
result = graph.query("RETURN 1 as test")
print("✅ Connected successfully!" if result else "❌ Connection failed")
```

Or use the Neo4j Browser:
1. Click **"Open"** button in AuraDB console
2. Login with your credentials
3. Run: `MATCH (n) RETURN count(n)`

### Step 6: Access Neo4j Browser (Optional)

1. In AuraDB console, click **"Open"** button
2. Enter your password
3. You'll see the Neo4j Browser interface
4. Run Cypher queries directly

### Troubleshooting

**❌ "Connection timeout"**
- Check your internet connection
- Verify URI format: `neo4j+s://` (not `neo4j://`)
- Ensure database is running (check AuraDB console)

**❌ "Authentication failed"**
- Double-check username (should be `neo4j`)
- Verify password (copy-paste to avoid typos)
- Try resetting password in AuraDB console

**❌ "Database not found"**
- Ensure database status is "Running" in console
- Check URI matches exactly from console
- Wait a few minutes if database was just created

### Free Tier Limits

- **200,000 nodes** maximum
- **400,000 relationships** maximum
- **1 database** instance
- **Auto-pauses** after 3 days of inactivity
- **Resumes** automatically when accessed

### Security Best Practices

1. ✅ **Never commit `.env` to git** (already in `.gitignore`)
2. ✅ **Use strong passwords** (12+ characters, mixed case, numbers, symbols)
3. ✅ **Rotate passwords** periodically
4. ✅ **Don't share credentials** publicly
5. ✅ **Use environment variables** in production

### Next Steps

After setting up Neo4j:
1. ✅ Update `.env` with your credentials
2. ✅ Run `python src/rag_etl.py` to populate database
3. ✅ Verify data: `MATCH (n) RETURN count(n)`
4. ✅ Start using the application!

---

**Need Help?**
- Neo4j Documentation: https://neo4j.com/docs/
- AuraDB Support: https://neo4j.com/cloud/aura/support/

