# Deployment Guide - Finance Data Processing API

## 🚀 Best FREE Deployment Options

### Option 1: Render.com (RECOMMENDED ⭐)
**Best for:** FastAPI projects, Easy setup, Free tier
**URL:** https://render.com

#### Pros:
- ✅ Free tier with no credit card required
- ✅ Automatic deployments from GitHub
- ✅ Great for FastAPI/Python
- ✅ Built-in database persistence
- ✅ Free SSL certificate

#### Deployment Steps:

1. **Push your code to GitHub** (see GITHUB_UPLOAD.md)

2. **Sign up on Render**: https://render.com

3. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repo

4. **Configure Settings**:
   ```
   Name: finance-api (or any name)
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Environment Variables** (Optional):
   ```
   DATABASE_URL=sqlite:///./finance_db.sqlite
   DEBUG=False
   ```

6. **Click "Create Web Service"**

7. **Wait 2-3 minutes** for deployment

8. **Your API will be live at**: `https://your-app-name.onrender.com`

9. **Access API docs**: `https://your-app-name.onrender.com/docs`

---

### Option 2: Railway.app
**Best for:** Quick deployments, Modern platform
**URL:** https://railway.app

#### Deployment Steps:

1. Sign up at https://railway.app
2. Click "New Project"
3. Choose "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python and deploys
6. Get your live URL

---

### Option 3: PythonAnywhere
**Best for:** Traditional Python hosting
**URL:** https://www.pythonanywhere.com

#### Steps:
1. Sign up for free account
2. Upload code or clone from GitHub
3. Configure WSGI
4. Your API will be at: `username.pythonanywhere.com`

---

### Option 4: Fly.io
**Best for:** Docker deployments, Global edge network
**URL:** https://fly.io

Requires Docker setup but very powerful.

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [ ] Code is pushed to GitHub
- [ ] `.env` file is NOT in GitHub (already in .gitignore)
- [ ] `requirements.txt` is updated
- [ ] SQLite database file is excluded (.gitignore)
- [ ] All sensitive data removed from code

---

## 🔧 Files to Add for Deployment

### Create `Procfile` (for some platforms):
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Create `runtime.txt` (specify Python version):
```
python-3.11.0
```

---

## 🌐 After Deployment

Once deployed, you'll get a URL like:
- `https://your-app.onrender.com`
- `https://your-app.up.railway.app`
- `username.pythonanywhere.com`

Access your API:
- Main API: `https://your-app.onrender.com/api`
- Docs: `https://your-app.onrender.com/docs`
- Health: `https://your-app.onrender.com/health`

---

## 🔐 Important Notes

1. **Database**: SQLite file will reset on Render's free tier after inactivity
   - Consider upgrading to PostgreSQL for production
   - Or use Render's persistent disk (paid)

2. **Sleep Mode**: Free tier apps sleep after 15 min of inactivity
   - First request after sleep takes ~30 seconds

3. **Limitations**: Free tier has limited resources
   - Good for testing/portfolio
   - Upgrade for production use

---

## 🎯 Recommended: Deploy to Render

**Why Render?**
- Easiest setup
- Best free tier
- Great for FastAPI
- Automatic HTTPS
- No credit card needed

---

## 📊 Comparison Table

| Platform | Free Tier | Ease | Best For |
|----------|-----------|------|----------|
| **Render** | ✅ Yes | ⭐⭐⭐⭐⭐ | FastAPI/Python |
| **Railway** | ✅ Trial | ⭐⭐⭐⭐ | Quick deploys |
| **PythonAnywhere** | ✅ Yes | ⭐⭐⭐ | Python apps |
| **Fly.io** | ✅ Yes | ⭐⭐⭐ | Docker apps |
| **Vercel** | ✅ Yes | ⭐⭐ | Serverless |

---

## 🆘 Need Help?

If you get stuck:
1. Check deployment logs
2. Verify environment variables
3. Ensure all dependencies in requirements.txt
4. Check Python version compatibility

**Ready to deploy? Start with Render!** 🚀
