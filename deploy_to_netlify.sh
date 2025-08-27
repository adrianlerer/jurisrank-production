#!/bin/bash

# JurisRank API - Netlify Deployment Script
# ==========================================
# Automated deployment script for production-ready serverless API

set -e  # Exit on any error

echo "🚀 JurisRank API - Netlify Deployment Script"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [[ ! -f "netlify.toml" ]]; then
    echo -e "${RED}❌ Error: netlify.toml not found. Please run from project root.${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Pre-deployment checklist:${NC}"

# Check for required files
echo -n "   ✓ Checking netlify.toml... "
if [[ -f "netlify.toml" ]]; then
    echo -e "${GREEN}Found${NC}"
else
    echo -e "${RED}Missing${NC}"
    exit 1
fi

echo -n "   ✓ Checking requirements.txt... "
if [[ -f "requirements.txt" ]]; then
    echo -e "${GREEN}Found${NC}"
else
    echo -e "${RED}Missing${NC}"
    exit 1
fi

echo -n "   ✓ Checking API functions directory... "
if [[ -d "api" ]] && [[ $(ls api/*.py 2>/dev/null | wc -l) -ge 8 ]]; then
    echo -e "${GREEN}Found ($(ls api/*.py | wc -l) functions)${NC}"
else
    echo -e "${RED}Missing or incomplete${NC}"
    exit 1
fi

# Test functions locally
echo -e "\n${BLUE}🧪 Running local function tests...${NC}"
if python3 test_netlify_functions.py; then
    echo -e "${GREEN}✅ All local tests passed${NC}"
else
    echo -e "${RED}❌ Local tests failed. Please fix issues before deployment.${NC}"
    exit 1
fi

# Check git status
echo -e "\n${BLUE}📦 Checking git repository...${NC}"
if git status --porcelain | grep -q .; then
    echo -e "${YELLOW}⚠️  Uncommitted changes detected:${NC}"
    git status --short
    
    read -p "Do you want to commit these changes? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}📝 Committing changes...${NC}"
        git add .
        git commit -m "deploy: prepare for Netlify production deployment

- All serverless functions tested and verified
- Configuration optimized for production
- Ready for maintenance-free operation"
    else
        echo -e "${YELLOW}⚠️  Proceeding with uncommitted changes${NC}"
    fi
fi

# Check if Netlify CLI is available
echo -e "\n${BLUE}🔧 Checking deployment method...${NC}"
if command -v netlify >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Netlify CLI found${NC}"
    
    # Check if logged in
    if netlify status >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Netlify CLI authenticated${NC}"
        
        read -p "Deploy to Netlify now? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "\n${BLUE}🚀 Deploying to Netlify...${NC}"
            
            # Deploy to Netlify
            netlify deploy --build --prod
            
            if [[ $? -eq 0 ]]; then
                echo -e "\n${GREEN}🎉 Deployment successful!${NC}"
                
                # Get site URL
                SITE_URL=$(netlify status --json | grep -o '"url":"[^"]*"' | sed 's/"url":"//' | sed 's/"//')
                
                echo -e "\n${GREEN}📍 Your JurisRank API is now live at:${NC}"
                echo -e "   ${BLUE}$SITE_URL${NC}"
                echo -e "\n${GREEN}📚 Test your deployment:${NC}"
                echo -e "   Health: ${BLUE}$SITE_URL/health${NC}"
                echo -e "   Status: ${BLUE}$SITE_URL/api/v1/status${NC}"
                echo -e "   Docs:   ${BLUE}$SITE_URL/docs${NC}"
                
            else
                echo -e "\n${RED}❌ Deployment failed. Check logs above.${NC}"
                exit 1
            fi
        fi
    else
        echo -e "${YELLOW}⚠️  Not logged into Netlify CLI${NC}"
        echo -e "   Run: ${BLUE}netlify login${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Netlify CLI not found${NC}"
    echo -e "\n${BLUE}📋 Manual deployment options:${NC}"
    echo -e "   1. Install Netlify CLI: ${BLUE}npm install -g netlify-cli${NC}"
    echo -e "   2. Or deploy via GitHub: https://app.netlify.com/start"
    echo -e "   3. Or manual upload: Drag project folder to Netlify dashboard"
fi

echo -e "\n${GREEN}✅ Pre-deployment checks complete${NC}"
echo -e "\n${BLUE}📖 For detailed instructions, see:${NC} NETLIFY_DEPLOYMENT_INSTRUCTIONS.md"
echo -e "\n${YELLOW}🏛️  JurisRank API - Ready for production deployment${NC}"
echo -e "   Patent P7 methodology • Maintenance-free • Globally distributed"