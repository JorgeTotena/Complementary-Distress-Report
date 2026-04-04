#!/bin/bash
# 8020REI Skills — Claude Desktop Setup
# Run this script to configure Claude Desktop with the 8020REI skills MCP server.
#
# Usage:
#   chmod +x install.sh
#   ./install.sh

set -e

CONFIG_DIR="$HOME/Library/Application Support/Claude"
CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"

echo ""
echo "==================================="
echo "  8020REI Skills — Claude Setup"
echo "==================================="
echo ""

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is required but not installed."
    echo ""
    echo "Install it from: https://nodejs.org (LTS version)"
    echo "Or with Homebrew:  brew install node"
    exit 1
fi

echo "Node.js found: $(node -v)"
echo ""

# Get GitHub token
echo "You need a GitHub Personal Access Token to access the 8020REI-skills repo."
echo ""
echo "If you don't have one yet:"
echo "  1. Go to https://github.com/settings/tokens"
echo "  2. Click 'Generate new token (classic)'"
echo "  3. Name it '8020REI Skills'"
echo "  4. Select the 'repo' scope"
echo "  5. Click 'Generate token' and copy it"
echo ""
read -p "Paste your GitHub token here: " GITHUB_TOKEN

if [ -z "$GITHUB_TOKEN" ]; then
    echo "ERROR: No token provided. Exiting."
    exit 1
fi

# Verify token works
echo ""
echo "Verifying token..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/repos/ignacioaraya1995/8020REI-skills")

if [ "$HTTP_STATUS" != "200" ]; then
    echo "ERROR: Token could not access the 8020REI-skills repo (HTTP $HTTP_STATUS)."
    echo "Make sure the token has 'repo' scope and you have access to the repository."
    exit 1
fi

echo "Token verified — repo access confirmed."
echo ""

# Create config directory if needed
mkdir -p "$CONFIG_DIR"

# Build the MCP config
# If config already exists, merge; otherwise create new
if [ -f "$CONFIG_FILE" ]; then
    echo "Existing Claude config found. Adding MCP server..."

    # Use node to merge JSON safely
    node -e "
const fs = require('fs');
const config = JSON.parse(fs.readFileSync('$CONFIG_FILE', 'utf8'));
if (!config.mcpServers) config.mcpServers = {};
config.mcpServers['8020rei-skills'] = {
    command: 'npx',
    args: ['-y', '@modelcontextprotocol/server-github'],
    env: {
        GITHUB_PERSONAL_ACCESS_TOKEN: '$GITHUB_TOKEN'
    }
};
fs.writeFileSync('$CONFIG_FILE', JSON.stringify(config, null, 2));
"
else
    echo "Creating new Claude config..."

    cat > "$CONFIG_FILE" << CONFIGEOF
{
  "mcpServers": {
    "8020rei-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN"
      }
    }
  }
}
CONFIGEOF
fi

echo ""
echo "==================================="
echo "  Setup complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "  1. Quit Claude Desktop completely (Cmd+Q)"
echo "  2. Reopen Claude Desktop"
echo "  3. Start a new conversation and try:"
echo ""
echo '     "Read the file customer_success/CLAUDE.md from the'
echo '      repo ignacioaraya1995/8020REI-skills and follow'
echo '      those instructions as my CSM assistant."'
echo ""
echo "Claude now has access to all 8020REI skill packages"
echo "directly from GitHub — always up to date."
echo ""
