# Upload to GitHub - Step by Step Guide

## Step 1: Create a New Repository on GitHub

1. Go to https://github.com
2. Click the **"+"** button (top right) → **"New repository"**
3. Enter a repository name (e.g., `finance-backend`)
4. Choose **Public** or **Private**
5. **DO NOT** check "Initialize with README" (we already have files)
6. Click **"Create repository"**
7. **Copy the repository URL** (e.g., `https://github.com/yourusername/finance-backend.git`)

## Step 2: Initialize Git and Push (Run these commands)

```bash
# Navigate to your project folder (if not already there)
cd "D:\resume\Offcampus\Zorvyn bakend developer"

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: Finance Data Processing Backend API"

# Add your GitHub repository as remote (replace with YOUR repository URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Important Notes

- Replace `YOUR_USERNAME` with your GitHub username
- Replace `YOUR_REPO_NAME` with your repository name
- The `.gitignore` file is already configured to exclude:
  - `venv/` (virtual environment)
  - `__pycache__/` (Python cache)
  - `.env` (secrets)
  - `finance_db.sqlite` (database file)

## If You Get Authentication Error

You may need to use a **Personal Access Token** instead of password:

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` permissions
3. Use this token as password when git asks

## Alternative: Using GitHub Desktop

If you prefer a GUI:
1. Download GitHub Desktop
2. File → Add Local Repository
3. Select your project folder
4. Publish to GitHub
