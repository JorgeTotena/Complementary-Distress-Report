# 8020REI Skills

A centralized repository of operational skill packages for 8020REI. Each skill package contains the complete context, standards, templates, and assets a team member — or an AI assistant — needs to perform their role effectively.

## What This Is

8020REI is a premium B2B SaaS platform providing exclusive, predictive real estate data to professional investors. This repository houses the institutional knowledge that powers each department, packaged as portable "skills" that can be:

- Connected to Claude Desktop via MCP — Claude reads the repo directly, always up to date
- Loaded into Claude Projects on the web as uploaded knowledge files
- Read by new hires during onboarding to get up to speed quickly

## Repository Structure

```
8020REI-skills/
  setup/
    install.sh                 ← Automated setup script (run this first)
  customer_success/            ← CSM skill package
    CLAUDE.md                     Instructions for AI assistants
    context/                      Business knowledge (6 files, read in order)
    standards/                    Communication & design rules
    templates/                    Report starting points
    logos/                        Brand assets (light/dark, full/icon)
    clients/                      Client work (local only, not in repo)
```

## Skill Packages

### Customer Success (`customer_success/`)

Everything a Customer Success Manager needs to serve 8020REI clients: company context, communication frameworks (Pyramid Principle, MECE), a complete design system for print-ready HTML reports, templates for every report type, and client account management structure.

---

## Team Setup Guide

### Prerequisites

Before you start, you need:

1. **Claude Pro subscription** — Get it at [claude.ai/pricing](https://claude.ai/pricing)
2. **Claude Desktop app** — Download from [claude.ai/download](https://claude.ai/download)
3. **Node.js** — Download from [nodejs.org](https://nodejs.org) (LTS version) or install with `brew install node`
4. **GitHub account** — With access to this repo (ask your manager to invite you)
5. **GitHub Personal Access Token** — You'll create this during setup

---

### Option A: Automated Setup (Recommended)

This is the fastest way. One script configures everything.

#### Step 1: Create your GitHub token

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Name it `8020REI Skills`
4. Check the **repo** scope (full control of private repositories)
5. Click **Generate token**
6. **Copy the token** — you'll need it in the next step

#### Step 2: Run the setup script

Open Terminal and run:

```bash
# Download and run the setup script
curl -sL https://raw.githubusercontent.com/ignacioaraya1995/8020REI-skills/main/setup/install.sh -o /tmp/8020rei-setup.sh
chmod +x /tmp/8020rei-setup.sh
/tmp/8020rei-setup.sh
```

The script will:
- Verify Node.js is installed
- Ask for your GitHub token and verify it works
- Configure the MCP server in Claude Desktop
- Tell you to restart Claude

#### Step 3: Restart Claude Desktop

1. **Quit** Claude Desktop completely (Cmd+Q, not just close the window)
2. **Reopen** Claude Desktop

#### Step 4: Activate your skill package

Start a new conversation in Claude Desktop and send this message:

```
Read the file customer_success/CLAUDE.md from the repo
ignacioaraya1995/8020REI-skills on GitHub, then read all files
in customer_success/context/ and customer_success/standards/.
Follow those instructions as my CSM assistant from now on.
```

Claude will load all the skills, context, and standards directly from GitHub. You're ready to work.

---

### Option B: Manual Setup

If you prefer to set it up yourself, or the script doesn't work.

#### Step 1: Create your GitHub token

Same as Option A, Step 1 above.

#### Step 2: Edit the Claude Desktop config

Open this file (create it if it doesn't exist):

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

On Mac, you can open it with:

```bash
open -a TextEdit ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Add or merge this into the file:

```json
{
  "mcpServers": {
    "8020rei-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN_HERE"
      }
    }
  }
}
```

Replace `YOUR_TOKEN_HERE` with your actual token.

**If the file already has content**, just add the `"8020rei-skills": { ... }` block inside the existing `"mcpServers"` object. If there's no `"mcpServers"` key, add it.

#### Step 3: Restart and activate

Same as Option A, Steps 3 and 4.

---

### Option C: Claude Projects (Web Only — No MCP)

If you only use claude.ai in the browser and don't want to install the desktop app.

#### Step 1: Create a Claude Project

1. Go to [claude.ai](https://claude.ai) and log in
2. Click **Projects** in the sidebar, then **Create Project**
3. Name it: `8020REI — Customer Success`

#### Step 2: Set project instructions

1. Click the **gear icon** (Project Settings)
2. Find **Custom Instructions**
3. Copy the entire contents of `customer_success/CLAUDE.md` and paste it in
4. Save

#### Step 3: Upload knowledge files

In Project Settings > **Project Knowledge**, upload these files:

| Folder | Files |
|--------|-------|
| `context/` | `01-company-and-product.md`, `02-platform.md`, `03-deal-pipeline.md`, `04-cs-operations.md`, `05-marketing-funnel.md`, `06-glossary.md` |
| `standards/` | `DESIGN_SYSTEM.md`, `report.css` |
| `templates/` | All 8 HTML files |
| `logos/` | All 4 PNG files |

#### Step 4: Start working

Open a conversation inside the project and go.

**Downside of this option:** When the repo updates, you have to re-upload changed files manually.

---

## How to Use Your Skills

Once setup is complete, Claude becomes your role-specific assistant. Here are examples for Customer Success:

| What you need | What to say |
|---------------|-------------|
| Engagement report | "Prepare an engagement report for [client]. Here's their context: [paste context.md]" |
| Call prep | "Create a call prep worksheet for my meeting with [client] tomorrow" |
| Health alert | "Draft a health alert — [client]'s health score dropped from 3.8 to 2.9" |
| BuyBox audit | "Audit the BuyBox configuration for [client]: [paste details]" |
| Email draft | "Draft a re-engagement email for [client] who hasn't responded in 3 weeks" |

### Client Context

Client data stays local — it's not in this repo. Each CSM maintains their own `clients/` folder:

```
clients/
  acme-investments/
    context.md          ← Everything about this account
    2026-03-engagement.html
  summit-property-group/
    context.md
    2026-03-fulfillment.html
```

Before generating anything for a client, paste or attach their `context.md` in the conversation. This grounds Claude in real account data instead of guessing.

---

## Updating

When the skills repo gets updated:

- **MCP users (Options A/B):** Nothing to do — Claude reads from GitHub directly, always current.
- **Projects users (Option C):** Pull the latest changes and re-upload any files that changed.

---

## Conventions

- **Skill packages are self-contained.** Each folder includes everything needed to operate in that role.
- **Context files are numbered.** `01-`, `02-`, etc. to establish reading order.
- **CLAUDE.md is the entry point.** Every skill package has one — it tells AI assistants how to use the package.
- **Reports are HTML.** All generated documents use inline CSS and produce clean PDFs via browser print.
- **Clients stay local.** The `clients/` folder is in `.gitignore` — each team member manages their own.
