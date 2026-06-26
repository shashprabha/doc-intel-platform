# DITA Converter Skill - User Guide

## Overview

The **DITA Converter Skill** automatically transforms Word documents and other structured content into production-ready DITA XML documentation sets. This guide helps you use the skill effectively to migrate your documentation to DITA format.

## Quick Start

### 1. Prepare Your Source Document

Before conversion, organize your Word document with clear structure:

- **Use H1 headings** to define major topics (each becomes a DITA topic)
- **Use H2 headings** for subsections within topics
- **Add title and metadata** (author, dates) if available
- **Structure content** logically with paragraphs, lists, tables, and code blocks

**Example structure:**
```
# Getting Started with DITA          (→ becomes a topic)
## What is DITA?                     (→ becomes a section)
## Key Principles                    (→ becomes a section)

# Creating Your First Topic          (→ becomes another topic)
## Prerequisites
## Step-by-Step Instructions
```

### 2. Invoke the Skill

Tell Claude to convert your document:

> "Convert my Word document (product-guide.docx) to DITA XML. Create proper concept, task, and reference topics, organize them in a ditamap, and provide a conversion report."

Or for specific guidance:

> "I have a technical documentation Word document about API setup. Convert it to DITA, classifying sections as concept or task topics as appropriate."

### 3. Review the Output

The skill generates:
- **DITA Topic Files** (`concept-*.dita`, `task-*.dita`, `reference-*.dita`)
- **Navigation Map** (`project.ditamap`)
- **Conversion Report** (`conversion-report.md`)
- **Output Directory** with organized `/topics` and `/images` folders

## Understanding DITA Topic Types

The converter automatically classifies your content into three DITA topic types:

### Concept Topics (`concept-*.dita`)
**When to use**: Explains *what* something is, *why* it exists, or *how* it works

**Characteristics**:
- Introductory, background, or overview information
- Explanations of principles, architecture, or concepts
- Does NOT contain step-by-step procedures
- Contains paragraphs, lists, images, but not numbered instructions

**Examples**:
- "Understanding DITA Architecture"
- "Why Use Structured Authoring"
- "Overview of Documentation Standards"

### Task Topics (`task-*.dita`)
**When to use**: Provides step-by-step instructions to *do* something

**Characteristics**:
- Prerequisites section listing required setup
- Numbered steps with clear commands/actions
- Expected results after each step
- Post-requisite information (what comes next)
- Goal-oriented and procedural

**Examples**:
- "Installing the Software"
- "Creating Your First DITA Topic"
- "Configuring User Permissions"

### Reference Topics (`reference-*.dita`)
**When to use**: Documents specifications, facts, and *lookup* information

**Characteristics**:
- API documentation and parameter specifications
- Element or property reference guides
- Lookup tables and data specifications
- Configuration options and settings
- Facts that don't involve procedures

**Examples**:
- "DITA Elements Reference"
- "API Endpoint Specifications"
- "Database Schema Reference"

## Classification Guide

The converter uses **intelligent analysis** to classify topics:

| Content Contains | Likely Type | Confidence |
|---|---|---|
| "Step 1", "Step 2", numbered instructions | Task | High |
| "Prerequisites", "How to", "Setup", "Install" | Task | High |
| "Reference", "Specification", "API", "Element" | Reference | High |
| Bulleted explanations, overview paragraphs | Concept | Medium |
| Numbered lists without prerequisite context | Task/Reference | Medium |
| Generic content | Concept | Low (default) |

**Pro Tip**: If classification seems wrong, mention it to Claude:
> "The 'API Specification' section should be a reference topic, not a concept. Please reclassify."

## Output Structure

The converter creates this directory structure:

```
project-output/
├── topics/
│   ├── concept-understanding-dita.dita
│   ├── task-creating-first-topic.dita
│   ├── reference-api-spec.dita
│   └── ... (more .dita files)
├── images/
│   ├── diagram-1.png
│   ├── screenshot-2.jpg
│   └── ... (images from source document)
├── project.ditamap
└── conversion-report.md
```

### Files Explained

- **`topics/*.dita`**: Individual DITA XML topic files
  - Named by type and subject: `[type]-[subject].dita`
  - Each contains valid DITA 1.3 XML
  - Include metadata (author, creation date, keywords)

- **`project.ditamap`**: Navigation map linking all topics
  - Hierarchical structure mirrors source document
  - References all topics with relative paths
  - Can be opened in DITA editors for publishing

- **`images/`**: Folder containing all images from source
  - Maintains original filenames or auto-numbered
  - Referenced by topics using relative paths

- **`conversion-report.md`**: Detailed conversion summary
  - Lists all topics created and their types
  - Conversion decisions and assumptions
  - Conversion log with timestamps
  - Useful for verification and documentation

## Post-Conversion Workflow

### 1. Review the Conversion Report

Open `conversion-report.md` to see:
- Total topics created and breakdown by type
- List of all generated files
- Any issues or decisions made during conversion

### 2. Validate XML Structure

All generated DITA files are valid XML. To verify:

**Using online validator**: Copy a `.dita` file content and validate at:
- https://www.liquid-technologies.com/online-xml-validator

**Using command line** (if you have xmllint):
```bash
xmllint --dtdvalid concept.dtd topic.dita
```

### 3. Check Content Accuracy

- Read each generated topic for semantic correctness
- Verify tables preserved data accurately
- Confirm code blocks are properly formatted
- Review alt-text for images

### 4. Verify Cross-References

- Check that all `<xref>` links reference existing files
- Confirm all image paths point to files in `/images` folder
- Validate ditamap topic references

### 5. Publish or Further Customize

Use the generated DITA files with:
- **DITA-OT** (DITA Open Toolkit) for PDF, HTML, ePub
- **Oxygen XML Editor** for advanced editing and publishing
- **Other DITA-compliant tools** for your platform

## Common Tasks & Solutions

### Q: How do I fix topic classification?

**A:** If a topic was classified incorrectly, ask Claude to reclassify:

> "The 'API Reference' section is classified as a concept but should be a reference topic. Please regenerate it with the correct topic type."

### Q: Can I convert Markdown instead of Word?

**A:** Yes! The skill also accepts Markdown files:

> "Convert my README.md file to DITA topics, treating each H1 section as a separate topic."

### Q: How do I handle images in the conversion?

**A:** Images are automatically organized into the `/images` folder. They're referenced correctly in the DITA files. If images don't appear in the conversion, provide them separately:

> "Convert this Word document (with-images.docx) to DITA. If images aren't embedded, I'll provide them separately."

### Q: Can I customize the output structure?

**A:** Yes! Specify preferences during conversion:

> "Convert to DITA with these preferences: use 'docs/' instead of 'topics/' folder, name the ditamap 'documentation.ditamap', include a table of contents topic."

### Q: How do I handle complex tables?

**A:** Complex tables are converted to DITA table elements with proper structure. For very complex tables, you might need manual refinement after conversion:

> "After conversion, I need to manually format the complex table in reference-specifications.dita to use DITA's advanced table features."

## Advanced Usage

### Batch Conversion

Convert multiple documents into one project:

> "I have 3 Word documents: overview.docx, user-guide.docx, and reference.docx. Convert all three to DITA topics and link them in a single ditamap, organized by document."

### Custom Metadata

Add specific metadata during conversion:

> "Convert product-guide.docx to DITA, adding these keywords to all topics: 'product-xyz', 'v2.0', 'enterprise'."

### Topic Reordering

Adjust the ditamap hierarchy after conversion:

> "After generating DITA topics, reorganize the ditamap so that task topics come before reference topics, with prerequisites-related tasks first."

## Best Practices for Quality DITA

### Before Conversion
✓ **Use consistent heading styles** (H1, H2, H3 only)  
✓ **Add clear section boundaries** with headings  
✓ **Include metadata** (author, dates) in document  
✓ **Use meaningful formatting** (lists, tables, code blocks)  
✗ Don't use visual formatting alone (spacing, colors for meaning)  

### After Conversion
✓ **Review the conversion report** for decisions made  
✓ **Validate XML** structure of generated files  
✓ **Test publishing** with your DITA publishing tool  
✓ **Check cross-references** for accuracy  
✓ **Verify keyword completeness** in metadata  

### Content Guidelines
✓ **One idea per topic** — keep topics modular  
✓ **Use semantic markup** — choose elements by meaning  
✓ **Maintain terminology consistency** — use glossary  
✓ **Add descriptive keywords** — enable better searchability  
✓ **Write for reuse** — topics should work independently  

## Troubleshooting

| Issue | Cause | Solution |
|---|---|---|
| Topics have empty content | Source headings had no text below them | Add content under H1/H2 headings in source |
| Incorrect topic classification | Poor keyword matching | Reclassify with Claude: "Section X should be a reference topic" |
| Missing images | Embedded images not detected | Provide images separately; reference by name |
| Large file size | DITA XML is verbose | Expected; size reduces when compressed |
| Validation errors | DTD not found during validation | Ensure DITA DTD files are in your schema path |

## File Formats Supported

| Format | Support | Notes |
|---|---|---|
| Word (.docx) | ✓ Full | Recommended; all formatting detected |
| Markdown (.md) | ✓ Full | Structure via headings; limited styling |
| Plain Text | ✓ Limited | Requires explicit heading structure |
| PDF | ✗ Not supported | Convert to Word first |
| Google Docs | ✗ Not supported | Export to Word, then convert |

## Getting Help

- **For DITA questions**: Ask Claude about DITA concepts, best practices, or standards
- **For conversion issues**: Provide the source document and describe the issue
- **For publishing questions**: Specify your target format (PDF, HTML, etc.) and tool

## Next Steps

1. **Prepare your source document** with clear H1 headings
2. **Ask the DITA Converter skill** to convert your document
3. **Review the conversion report** and generated files
4. **Validate XML** and content accuracy
5. **Publish** using DITA-OT, Oxygen, or your preferred tool
6. **Iterate** — refine topics and regenerate as needed

## Resources

- **DITA Standard**: https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=dita
- **DITA Specification**: https://docs.oasis-open.org/dita/dita/v1.3/
- **DITA-OT (Publishing)**: https://www.dita-ot.org/
- **Oxygen XML Editor**: https://www.oxygenxml.com/

---

**Version**: 1.0  
**Last Updated**: 2026-06-26  
**For Issues or Feedback**: Contact the DITA Converter skill maintainer
