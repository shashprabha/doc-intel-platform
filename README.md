# Document Intelligence Platform PoC

A practical proof of concept for converting Word documents to DITA-XML, applying brand terminology updates, and validating the output—all through a single Claude Code command.

---

## New: DITA Converter Skill

The **DITA Converter Skill** provides an intelligent, automated solution for converting Word documents and structured content into production-ready DITA XML documentation sets.

### Quick Start

Tell Claude to convert your document:

```
Convert my Word document (sample.docx) to DITA XML with proper concept, task, and reference topics.
```

### What You Get

- **DITA XML Files** — Automatically classified into concept, task, and reference topics
- **Navigation Map** — Hierarchical ditamap linking all topics
- **Organized Output** — Topics in `/topics`, images in `/images`
- **Conversion Report** — Detailed summary of conversion decisions and statistics

### Key Features

✓ **Intelligent Classification** — Analyzes content to classify topics as concept/task/reference  
✓ **Semantic Markup** — Generates proper DITA elements (`<p>`, `<ul>`, `<codeblock>`, `<table>`, etc.)  
✓ **Metadata Generation** — Adds author, creation date, and keywords to topics  
✓ **Cross-Reference Support** — Creates xref links between related topics  
✓ **Image Organization** — Automatically manages images in `/images` folder  
✓ **Multi-Format Support** — Converts Word, Markdown, and plain text  

### Example Conversion

**Input:** Word document with sections like "Getting Started", "Step-by-Step Guide", "API Reference"

**Output:**
```
dita-output/
├── topics/
│   ├── concept-getting-started.dita
│   ├── task-step-by-step-guide.dita
│   └── reference-api.dita
├── images/
│   └── [images from document]
├── project.ditamap
└── conversion-report.md
```

### For More Details

- **User Guide:** See [`skills/dita-converter/USER_GUIDE.md`](skills/dita-converter/USER_GUIDE.md)
- **Skill Definition:** See [`skills/dita-converter/SKILL.md`](skills/dita-converter/SKILL.md)

---

## Original Pipeline (PoC)

The original proof of concept platform demonstrates:

```
Word Document → Conversion → Rebranding → Validation → DITA-XML Output
```

1. **Converter:** Reads Word `.docx` files and writes DITA-XML
2. **Rebranding Engine:** Applies brand terminology rules from JSON
3. **Validator:** Checks XML structure, content, and quality

## Quick Start: 2 Ways to Run

### Way 1: Claude Code Plugin (Recommended)

```text
/pipeline sample-data/input/Gmail_Installation_Guide.docx
```

Outputs:
- `Gmail_Installation_Guide-output.dita` (converted)
- `Gmail_Installation_Guide-rebranded.dita` (with branding)

### Way 2: Manual Commands

```bash
python prototype/converter.py --input sample-data/input/Gmail_Installation_Guide.docx --output sample-data/output/Gmail_Installation_Guide-output.dita

python prototype/rebranding-engine.py --input sample-data/output/Gmail_Installation_Guide-output.dita --rules prototype/rebranding-rules.json --output sample-data/output/Gmail_Installation_Guide-rebranded.dita

bash prototype/validation-script.sh sample-data/output/Gmail_Installation_Guide-rebranded.dita
```

---

## Folders and Files

| Path | Purpose |
|------|---------|
| `skills/dita-converter/` | **NEW:** DITA Converter Skill — Converts documents to DITA XML |
| `skills/dita-converter/SKILL.md` | Skill definition, trigger phrases, and detailed conversion workflow |
| `skills/dita-converter/USER_GUIDE.md` | User guide with best practices and troubleshooting |
| `skills/dita-converter/scripts/` | Python implementation for DITA conversion |
| `skills/dita-converter/evals/` | Test cases and evaluation prompts |
| `.claude/` | Claude Code plugin (command name: `/pipeline`) |
| `prototype/` | Python converter, rebranding engine, and validation script |
| `sample-data/input/` | Example Word documents for testing |
| `sample-data/output/` | Generated DITA-XML files (created at runtime) |
| `sample-data/expected_output/` | Reference expected DITA outputs for comparison |
| `docs/` | Quality criteria, workflow, assumptions, and sample metadata |
| `results/` | Demo guides and validation summaries |
| `validation/` | Formal test results and evidence |
| `samples/` | Sample documents for testing (e.g., `sample-dita-guide.docx`) |

---

## Key Files

| File | Purpose |
|------|---------|
| `.claude/plugin.json` | Plugin manifest (name, version, author) |
| `.claude/commands/pipeline.md` | Slash command prompt orchestrating all three steps |
| `prototype/converter.py` | Converts Word to DITA-XML |
| `prototype/rebranding-engine.py` | Applies terminology rules to DITA |
| `prototype/rebranding-rules.json` | Brand terminology mappings |
| `prototype/validation-script.sh` | Validates DITA output |
| `docs/quality-criteria.md` | What PASS, WARN, FAIL mean |
| `DEPLOYMENT-GUIDE.md` | Setup and testing instructions |
| `LEADER-DEMO-GUIDE.md` | Demo script for stakeholders |
| `results/demo_guide.md` | Quick demo guide for the build team |

---

## Prerequisites

- **Python 3.10 or 3.11** (required)
- **Git with Git Bash** (Windows)
- **Claude Code** (for `/pipeline` command)

---

## Setup (5 minutes)

### Step 1: Create Python Environment

```bash
python -m venv .venv
```

### Step 2: Activate

```bash
# Windows
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r prototype/requirements.txt
```

---

## Test It

### Using Claude Code

1. Open the repo in Claude Code
2. Run: `/pipeline sample-data/input/Gmail_Installation_Guide.docx`
3. Check outputs in `sample-data/output/`

### Using Terminal

See **Way 2** under [Quick Start](#quick-start-2-ways-to-run) above.

---

## How It Works

### The Pipeline Command

The `.claude/commands/pipeline.md` file:
- Takes a Word document path as input (`$ARGUMENTS`)
- Preserves the filename in outputs for traceability
- Runs conversion, rebranding, and validation in order
- Reports PASS, WARN, or FAIL status

### What Happens at Each Step

**Step 1: Conversion**
- Reads Word document structure
- Writes valid DITA-XML with topics, sections, paragraphs, tables

**Step 2: Rebranding**
- Reads JSON rules (e.g., "Gmail" → "NewGmail")
- Applies terminology updates to the DITA output
- No code changes needed; edit rules.json directly

**Step 3: Validation**
- Checks XML well-formedness
- Verifies DITA structure (root topic, body, sections)
- Counts content (paragraphs, tables, sections)
- Returns PASS, WARN, or FAIL

---

## Scope

### In Scope ✓

- Word → DITA conversion for standard structure
- JSON-based terminology rebranding
- Repeatable quality validation
- Claude Code plugin delivery

### Out of Scope ✗

- Formatting preservation (fonts, colors, spacing)
- Complex DITA specialization
- Batch UI or production integrations
- Multi-language support

---

## Expected Output

Successfully converting the Gmail guide produces:

```
Gmail_Installation_Guide-output.dita     (17 KB)  - Converted DITA
Gmail_Installation_Guide-rebranded.dita  (17 KB)  - With brand terms updated
```

Both files are valid DITA-XML, ready for manual review or downstream workflows.

---

## Documentation

- **`DEPLOYMENT-GUIDE.md`** — Setup and testing steps
- **`LEADER-DEMO-GUIDE.md`** — Executive demo script
- **`results/demo_guide.md`** — Quick demo for the build team
- **`docs/quality-criteria.md`** — PASS/WARN/FAIL definitions
- **`docs/assumptions.md`** — Known limits and conversion rules
- **`SKILLS-MARKETPLACE-GUIDE.md`** — Publishing to a skills marketplace

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError: docx` | Run `pip install -r prototype/requirements.txt` |
| `bash: command not found` (Windows) | Use Git Bash, not PowerShell |
| `lxml build fails` | Use Python 3.10 or 3.11 (not 3.14) |
| No output files | Check `sample-data/output/` exists; converter creates it |

For more, see [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md#troubleshooting).

---

## Demo

To see a demo:

1. Read `LEADER-DEMO-GUIDE.md` for the full script (15 min)
2. Or read `results/demo_guide.md` for a quick version (10 min)

Both include setup, talking points, and what to do if something breaks.

---

## Next Steps

1. **Run the PoC:** Follow [DEPLOYMENT-GUIDE.md](DEPLOYMENT-GUIDE.md)
2. **Review outputs:** Check against `docs/quality-criteria.md`
3. **Demo to stakeholders:** Use [LEADER-DEMO-GUIDE.md](LEADER-DEMO-GUIDE.md)
4. **Publish as skill:** Follow [SKILLS-MARKETPLACE-GUIDE.md](SKILLS-MARKETPLACE-GUIDE.md)

---

## Project Info

- **Timeline:** 22 June – 5 July 2026
- **Owner:** Samyak Mukherjee
- **Team:** 7 people (see `roster.md`)
- **Status:** PoC complete and tested

For more on project scope and success criteria, see [CHARTER.md](CHARTER.md).

---

## License

See LICENSE file.
