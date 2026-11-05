# FDE Bootcamp Starter Kit

Pre-work for the **Forward Deployed Engineering Bootcamp** (Traversaal.ai). This repo is your tutor: open it in Claude Code and type `/start`.

The learning path, reading, demos and unlock checks live on the pre-work site. This repo holds the labs and the scripts that prove they work.

## Get started

1. On GitHub, click **Use this template → Create a new repository** to get your own copy.
2. Clone *your* copy and open it:
   ```bash
   git clone https://github.com/<your-handle>/fde-starter-kit.git
   cd fde-starter-kit
   code .
   ```
3. Copy `.env.example` to `.env` and add your OpenRouter key.
4. Open Claude Code (VS Code panel, or `claude` in the terminal) and type:
   ```
   /start
   ```

## Commands

| Command | What it does |
|---|---|
| `/start` | Sets your GitHub handle, shows your progress, tells you what's next |
| `/preflight` | L01: checks your machine is ready, prints the L01 code |
| `/check l02` (`l03`, `l04`) | Checks a lab and prints its unlock code |
| `/explain <term>` | Explains a concept with book references |

## What's inside

```
CLAUDE.md               the tutor's instructions
.claude/skills/         /start, /preflight, /check, /explain
labs/                   one folder per level
checks/                 the scripts that verify each lab (standard-library Python)
glossary.md             every term on the path, with level and book section
ME.md                   your intro: your first commit
```

## Honor system

Unlock codes are generated from your GitHub handle by the check scripts. They're friction, not security, and nobody grades them. The goal is that you walk into Session 1 with a working setup and the foundations in your hands.

## Learn more

- Book: *Claude Code: A Practitioner's Approach*, free online at traversaal.ai/academy
- Free course: *Claude Code in Practice*, traversaal.ai/academy
- Skills and sub-agents to borrow: [hamzafarooq/claude-code-starter](https://github.com/hamzafarooq/claude-code-starter)
