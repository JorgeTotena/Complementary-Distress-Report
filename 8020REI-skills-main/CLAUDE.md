# 8020REI Skills Repository

> This is the central repository of operational skill packages for 8020REI. Each top-level folder is a self-contained skill package for a specific department or function.

## How This Repo Works

Each skill package contains everything needed to operate in a role: business context, communication standards, templates, brand assets, and client work. Packages are designed to be loaded into AI tools (Claude Projects) or read by team members during onboarding.

## Available Skill Packages

| Folder | Department | Status |
|--------|-----------|--------|
| `customer_success/` | Customer Success | Active |

## Routing

When a user asks for help, determine which department the task belongs to and load the corresponding skill package. Each package has its own `CLAUDE.md` with specific instructions.

- **Client reports, engagement calls, health scores, churn, onboarding, BuyBox audits** → `customer_success/`

## Rules

1. **Read the skill package's `CLAUDE.md` first.** It contains role-specific instructions that override general behavior.
2. **Read `context/` files before answering domain questions.** Never invent facts about the company, products, or clients.
3. **Follow the standards in `standards/`.** Every skill package defines how communication and output should look.
4. **Use templates from `templates/` as starting points.** Don't create reports from scratch when a template exists.
5. **Save client work to `clients/`.** Each client gets a subfolder. Read the client's `context.md` before generating any output for them.

## Company Context

8020REI is a premium B2B SaaS platform providing exclusive, predictive real estate data to professional investors. ~140 active clients, 1,200+ protected counties, ~$350K MRR. The company runs on EOS (Entrepreneurial Operating System). For full business context, see `customer_success/context/01-company-and-product.md`.
