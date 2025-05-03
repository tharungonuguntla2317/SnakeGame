# Deploying Snake Game to GitHub Pages

This guide will help you deploy your Snake Game to GitHub Pages for free hosting.

## Prerequisites

1. A GitHub account
2. Git installed on your computer

## Steps to Deploy

### 1. Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click on the "+" icon in the top right corner and select "New repository"
3. Name your repository (e.g., "snake-game")
4. Make it public
5. Click "Create repository"

### 2. Initialize Git in Your Project

```bash
cd /Users/gotharun/workplace/SnakeGame
git init
git add .
git commit -m "Initial commit"
```

### 3. Connect to GitHub Repository

Replace `YOUR_USERNAME` with your GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/snake-game.git
git branch -M main
git push -u origin main
```

### 4. Deploy to GitHub Pages

#### Option 1: Deploy the build directory

1. Push your build directory to GitHub:

```bash
# Copy the build files to a docs directory (GitHub Pages can serve from /docs)
mkdir -p docs
cp -r build/build/web/* docs/

# Add and commit the docs directory
git add docs
git commit -m "Add build files for GitHub Pages"
git push origin main
```

2. Go to your repository on GitHub
3. Go to Settings > Pages
4. Under "Source", select "Deploy from a branch"
5. Select "main" branch and "/docs" folder
6. Click "Save"

#### Option 2: Use GitHub Actions for automatic deployment

1. Create a GitHub Actions workflow file:

```bash
mkdir -p .github/workflows
```

2. Create a file named `.github/workflows/deploy.yml` with the following content:

```yaml
name: Build and Deploy

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pygame pygbag
          
      - name: Build with pygbag
        run: |
          python -m pygbag --build --ume_block=0 build
          
      - name: Deploy to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@v4
        with:
          folder: build/build/web
```

3. Commit and push this file:

```bash
git add .github/workflows/deploy.yml
git commit -m "Add GitHub Actions workflow for deployment"
git push origin main
```

4. Go to your repository on GitHub
5. Go to Settings > Pages
6. Under "Source", select "GitHub Actions"

### 5. Access Your Game

After deployment is complete (which may take a few minutes), your game will be available at:

```
https://YOUR_USERNAME.github.io/snake-game/
```

## Troubleshooting

- If your game doesn't load, check the browser console for errors
- Make sure all paths in your code are relative, not absolute
- Check that all required files were included in the build
