---
name: dita-converter
description: Convert Word documents and unstructured content into production-ready DITA XML with semantic markup, ditamaps, and organized media assets. Use this whenever the user wants to migrate documentation to DITA format, create reusable topic-based content, structure technical documentation into concept/task/reference topics, convert existing Word/Markdown files to DITA XML, or modernize documentation with structured authoring practices.
compatibility:
  tools:
    - file reading/writing
    - XML generation
    - document parsing
  languages: Python, XML
---

# DITA Converter Skill

Convert Word documents (.docx), Markdown, or other structured content into fully compliant DITA XML documentation sets. This skill automates the entire conversion pipeline: analyzing source structure, classifying content into appropriate topic types (concept/task/reference), generating semantic XML markup, creating navigation maps, and organizing media assets.

## When to Use This Skill

Invoke the DITA converter when you need to:
- **Migrate existing documentation** to DITA from Word, Markdown, or proprietary formats
- **Structure technical content** using DITA's topic-based authoring model
- **Enable content reuse** by modularizing documentation into typed topics
- **Prepare for multi-channel publishing** (HTML, PDF, mobile, etc.)
- **Implement structured authoring** practices with semantic XML markup
- **Create or update ditamaps** for topic organization and navigation

The skill handles the technical complexity of XML generation, element classification, metadata insertion, and project structure setup.

## Input Requirements

### Source Document
Provide a Word document (.docx), Markdown file (.md), or other structured document containing:
- **Hierarchical structure**: Headings (H1, H2, H3) that define topic boundaries and sections
- **Typed content**: Paragraphs, lists, tables, code blocks, links, and images
- **Metadata hints**: Document title, author information, revision notes (if available)

### Optional Information
- **Topic classification guidance**: Which sections should become concept, task, or reference topics
- **Image files**: Any images to be included (will be organized into `/images` folder)
- **Glossary or terminology list**: For consistent terminology in metadata
- **Style/branding guidelines**: Corporate standards for output structure

### Example Input
```
# Getting Started with DITA Documentation
## Understanding DITA (concept topic)
## Creating Your First Topic (task topic)
## DITA Elements Reference (reference topic)
```

## Conversion Process

### Phase 1: Source Analysis
1. Parse document structure and identify hierarchical levels
2. Detect content patterns: lists, tables, code blocks, images
3. Extract metadata: title, author, creation/revision dates
4. Identify section boundaries for topic creation

### Phase 2: Topic Classification
Classify each major section (H1/H2) into one of three DITA topic types:

- **Concept**: Explains *what* something is or *why* it exists
  - Use for: Overview, architecture, principles, background information
  - Contains: Paragraphs, lists, images, but NOT step-by-step procedures

- **Task**: Provides step-by-step instructions to accomplish something
  - Use for: Procedures, how-to guides, setup instructions
  - Contains: Prerequisites, numbered steps, expected results

- **Reference**: Documents specifications, facts, and data
  - Use for: API docs, element references, lookup tables, configuration options
  - Contains: Definitions, tables, code samples, specification details

### Phase 3: Semantic XML Generation
Generate DITA XML with proper structure and semantic elements:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE concept PUBLIC "-//OASIS//DTD DITA Concept//EN" "concept.dtd">
<concept id="unique-topic-id">
  <title>Topic Title</title>
  <prolog>
    <author>Author Name</author>
    <created date="YYYY-MM-DD"/>
    <revised modified="YYYY-MM-DD"/>
    <metadata>
      <keywords>
        <keyword>keyword1</keyword>
        <keyword>keyword2</keyword>
      </keywords>
    </metadata>
  </prolog>
  <conbody>
    <!-- Content goes here -->
  </conbody>
</concept>
```

**Element Mapping:**
- Headings H1 → Topic titles
- Headings H2/H3 → Section titles (`<section>`)
- Paragraphs → `<p>` elements
- Bullet lists → `<ul><li>` elements
- Numbered lists → `<ol><li>` elements
- Tables → `<table>` elements with proper DITA structure
- Code blocks → `<codeblock>` elements with language attribute
- Images → `<fig><image>` elements with alt text
- Links/references → `<xref>` cross-references

### Phase 4: DITAMAP Creation
Create a hierarchical navigation map that links all topics:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "map.dtd">
<map id="project-map">
  <title>Project Documentation</title>
  <topicref href="topics/concept-getting-started.dita">
    <topicref href="topics/task-first-steps.dita"/>
    <topicref href="topics/reference-api.dita"/>
  </topicref>
</map>
```

### Phase 5: Asset Organization
Organize project structure:
```
output/
├── topics/
│   ├── concept-*.dita
│   ├── task-*.dita
│   └── reference-*.dita
├── images/
│   └── [all image files]
├── project.ditamap
└── conversion-report.md
```

## Quality Standards

### XML Compliance
✓ Well-formed XML that validates against DITA 1.3 DTD
✓ All required elements properly nested and closed
✓ Valid DOCTYPE declarations for each topic type
✓ Proper character encoding (UTF-8)

### Semantic Accuracy
✓ Elements chosen based on *meaning*, not appearance
✓ Topic types match content purpose (concept/task/reference)
✓ Paragraph-level markup uses semantic elements (`<p>`, `<dl>`, not `<div>`)
✓ Lists properly typed (`<ul>` vs `<ol>`)

### Content Integrity
✓ No information loss during conversion
✓ Original meaning and technical accuracy preserved
✓ Formatting translated appropriately (bold → emphasis, etc.)
✓ All images, tables, and code samples included

### Metadata Completeness
✓ All topics have `<prolog>` with creation/revision dates
✓ Keywords populated for searchability
✓ Topic IDs unique and human-readable
✓ Ditamap structure reflects source document hierarchy

### Reusability
✓ Topics are modular and self-contained
✓ Cross-references (`<xref>`) used appropriately
✓ No topic depends on file-order for meaning
✓ Topics can be reused across multiple ditamaps

## Output Specification

### DITA Topic Files
- **File naming**: `[type]-[descriptive-name].dita`
  - Example: `concept-overview.dita`, `task-setup.dita`, `reference-api.dita`
- **File encoding**: UTF-8 without BOM
- **ID attributes**: Each topic has unique, lowercase, hyphenated id
  - Example: `<concept id="getting-started">`

### DITAMAP
- **File name**: `project.ditamap` (or source-document-name.ditamap)
- **Root element**: `<map>`
- **Organization**: Hierarchical `<topicref>` structure mirroring source document

### Images Folder
- **Location**: `images/` subdirectory
- **File naming**: Preserve original names or auto-name as `img-1.png`, `img-2.jpg`, etc.
- **Image elements**: `<fig><image href="images/filename.ext" alt="descriptive alt text"/></fig>`

### Conversion Report
- **File name**: `conversion-report.md`
- **Contents**:
  - Source document analysis
  - Topic classification breakdown
  - Conversion decisions and assumptions
  - Any warnings or manual review items
  - Statistics: total topics, topic type counts, image count

## Post-Conversion Validation

After generation, verify:

1. **XML Validation**
   ```bash
   xmllint --dtdvalid concept.dtd topic.dita
   ```

2. **Link Verification**
   - All `<xref>` hrefs point to existing .dita files
   - All `<image>` hrefs point to files in `/images` folder
   - Ditamap references exist

3. **Content Review**
   - Read each topic for semantic correctness
   - Verify table structure and data integrity
   - Check code blocks for proper syntax highlighting
   - Review alt-text for images

4. **Terminology Consistency**
   - Search for synonyms and standardize language
   - Verify product names and version numbers
   - Check capitalization and terminology

## Common Conversion Patterns

### Converting Task-Heavy Content
Source: Numbered lists with explanations
→ DITA: `<task>` with `<steps>`, `<stepresult>`, `<postreq>`

### Converting Reference Tables
Source: Word tables with specifications
→ DITA: Semantic `<table>` with `<thead>`, `<tbody>`, `<tgroup>`

### Converting Code Examples
Source: Formatted code blocks with syntax highlighting
→ DITA: `<codeblock>` with `outputclass="language-python"` (or relevant language)

### Converting Embedded Images
Source: Images in document body
→ DITA: `<fig><image>` with alt text; image file moved to `/images/`

### Converting Hyperlinks
Source: Blue underlined text linking to external/internal references
→ DITA: `<xref>` for internal links, `<external-link>` for external URLs

## Example Conversion

**Source (Word):**
```
# Setting Up Your Environment
Before you begin, you'll need...

## Installation Steps
1. Download the installer
2. Run the setup wizard
3. Verify installation
```

**Output (DITA - task-*.dita):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE task PUBLIC "-//OASIS//DTD DITA Task//EN" "task.dtd">
<task id="setup-environment">
  <title>Setting Up Your Environment</title>
  <prolog>
    <created date="2026-06-26"/>
  </prolog>
  <taskbody>
    <prereq>
      <p>You will need the following before beginning...</p>
    </prereq>
    <steps>
      <step>
        <cmd>Download the installer</cmd>
      </step>
      <step>
        <cmd>Run the setup wizard</cmd>
      </step>
      <step>
        <cmd>Verify installation</cmd>
      </step>
    </steps>
  </taskbody>
</task>
```

## Tips for Best Results

1. **Before conversion**: Organize source document with clear H1 headings for topics
2. **Use consistent formatting**: Don't rely on visual formatting; use Word styles
3. **Add metadata hints**: Include author name and revision dates in source
4. **Review classification**: If topics are misclassified, provide guidance
5. **Test output**: Validate generated XML and test publishing to your target format
6. **Iterate**: If first pass needs refinement, provide feedback and re-run

## Technical Details

### Dependencies
- Python 3.8+
- python-docx (for Word parsing)
- lxml (for XML generation)
- DITA DTD files (1.3 or later)

### Supported Input Formats
- Word (.docx) — primary
- Markdown (.md) — supported
- Plain text with structure hints — supported

### Generated Formats
- DITA XML (.dita) — DITA 1.3
- DITA Map (.ditamap)
- Markdown conversion report

### Performance
- Typical document (20-50 pages): < 10 seconds
- Large document (100+ pages): < 30 seconds
- Output size: ~3-5x source size (due to XML verbosity)
