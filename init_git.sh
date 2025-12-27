#!/bin/bash
set -e

echo "Initializing Git Repository..."
git init
git checkout -b main

# Configure user if needed (you might want to remove this or prompt)
# git config user.email "you@example.com"
# git config user.name "Your Name"

echo "Creating Commit 1: Project Docs & Scripts"
git add .gitignore README.md start_dev.sh
git commit -m "Initialize project: Add documentation and startup scripts"

echo "Creating Commit 2: Shared DB & Requirements"
git add backend/shared backend/requirements.txt
git commit -m "Add shared database models and requirements"

echo "Creating Commit 3: Collector Service"
git add backend/collector
git commit -m "Implement Collector Service with Riot API integration"

echo "Creating Commit 4: Core API"
git add backend/core_api
git commit -m "Implement Core API with Score Engine and AI Analysis"

echo "Creating Commit 5: Frontend"
git add frontend
git commit -m "Implement React Frontend with Team Builder"

echo "Git initialization complete!"
echo "Now run: git remote add origin https://github.com/mackim-3768/LOL-TeamForge-AI.git"
echo "Then run: git push -u origin main"
