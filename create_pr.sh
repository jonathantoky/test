#!/bin/bash

# 🚀 Replicate Agent Tools - Pull Request Creation Script
# This script helps you create a pull request for the Replicate agent tools

echo "🚀 Creating Replicate Agent Tools Pull Request"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    print_error "This script must be run from within a git repository"
    exit 1
fi

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    print_warning "GitHub CLI (gh) is not installed. You'll need to create the PR manually."
    print_info "Install GitHub CLI: https://cli.github.com/"
    MANUAL_PR=true
else
    print_status "GitHub CLI found"
    MANUAL_PR=false
fi

# Get current repository information
CURRENT_REPO=$(git remote get-url origin 2>/dev/null || echo "unknown")
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

print_info "Current repository: $CURRENT_REPO"
print_info "Current branch: $CURRENT_BRANCH"

# Step 1: Create and switch to feature branch
print_info "Step 1: Creating feature branch..."
BRANCH_NAME="feature/replicate-agent-tools"

if git show-ref --verify --quiet refs/heads/$BRANCH_NAME; then
    print_warning "Branch $BRANCH_NAME already exists. Switching to it..."
    git checkout $BRANCH_NAME
else
    print_status "Creating new branch: $BRANCH_NAME"
    git checkout -b $BRANCH_NAME
fi

# Step 2: Check if files exist
print_info "Step 2: Checking for Replicate agent tool files..."

REQUIRED_FILES=(
    "agent_tools/replicate/__init__.py"
    "agent_tools/replicate/replicate_tools.py"
    "agent_tools/replicate/models.py"
    "agent_tools/replicate/predictions.py"
    "agent_tools/replicate/code_generation.py"
    "client/__init__.py"
    "client/replicate_auth.py"
    "client/config.py"
    "tests/test_replicate_tools.py"
    "seeds/replicate.ts"
    "load_tools.py"
)

MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    print_error "Missing required files:"
    for file in "${MISSING_FILES[@]}"; do
        echo "  - $file"
    done
    print_warning "Please copy the Replicate agent tool files to your repository first."
    print_info "You can find all the files in the 'test' repository that was created."
    exit 1
else
    print_status "All required files found"
fi

# Step 3: Add files to git
print_info "Step 3: Adding files to git..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    print_warning "No changes to commit. Files may already be committed."
else
    print_status "Files staged for commit"
fi

# Step 4: Commit changes
print_info "Step 4: Committing changes..."
COMMIT_MESSAGE="feat: Add comprehensive Replicate agent tools

- Add model management tools (list, get, create, versions)
- Add prediction execution tools (create, monitor, cancel, run)
- Add AI-powered code generation tools (generate, optimize, debug, dockerfile, requirements)
- Add authentication system with token management
- Add configuration system with environment support
- Add comprehensive test suite
- Add TypeScript seed definitions
- Add integration examples and documentation

Features:
✅ 15 comprehensive Replicate tools
✅ Model management capabilities
✅ Prediction execution and monitoring
✅ AI-powered code generation
✅ Authentication and token management
✅ Configuration management
✅ Comprehensive testing
✅ LangChain integration ready
✅ Full documentation"

if git diff --cached --quiet; then
    print_warning "No changes to commit"
else
    git commit -m "$COMMIT_MESSAGE"
    print_status "Changes committed"
fi

# Step 5: Push to origin
print_info "Step 5: Pushing to origin..."
if git push origin $BRANCH_NAME; then
    print_status "Branch pushed to origin"
else
    print_error "Failed to push branch to origin"
    exit 1
fi

# Step 6: Create pull request
print_info "Step 6: Creating pull request..."

if [ "$MANUAL_PR" = true ]; then
    print_warning "Creating pull request manually..."
    print_info "Please go to your GitHub repository and create a pull request with:"
    print_info "  - Base branch: staging"
    print_info "  - Compare branch: $BRANCH_NAME"
    print_info "  - Title: feat: Add Comprehensive Replicate Agent Tools"
    print_info "  - Description: Use the content from pr_description.md"
else
    # Create PR using GitHub CLI
    if [ -f "pr_description.md" ]; then
        print_status "Creating pull request using GitHub CLI..."
        if gh pr create --base staging --head $BRANCH_NAME --title "feat: Add Comprehensive Replicate Agent Tools" --body-file pr_description.md; then
            print_status "Pull request created successfully!"
            
            # Get PR URL
            PR_URL=$(gh pr view --json url --jq .url)
            print_status "Pull request URL: $PR_URL"
        else
            print_error "Failed to create pull request using GitHub CLI"
            print_info "Please create the pull request manually"
        fi
    else
        print_error "pr_description.md not found"
        print_info "Creating pull request with basic description..."
        gh pr create --base staging --head $BRANCH_NAME --title "feat: Add Comprehensive Replicate Agent Tools" --body "Add comprehensive Replicate agent tools with 15 specialized tools covering model management, prediction execution, and AI-powered code generation."
    fi
fi

# Step 7: Summary
echo ""
print_status "🎉 Pull Request Creation Complete!"
echo "=============================================="
print_info "Summary:"
print_info "  ✅ Branch created: $BRANCH_NAME"
print_info "  ✅ Files committed and pushed"
print_info "  ✅ Pull request created (or ready to create manually)"
echo ""
print_info "Next steps:"
print_info "  1. Review the pull request"
print_info "  2. Address any feedback from reviewers"
print_info "  3. Merge when approved"
echo ""
print_status "Thank you for contributing to the project! 🚀"