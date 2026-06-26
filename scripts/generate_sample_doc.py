#!/usr/bin/env python3
"""
Generate a sample Word document for DITA conversion testing.
Creates a realistic multi-topic document with various element types.
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

def add_heading_with_style(doc, text, level):
    """Add heading with proper style."""
    return doc.add_heading(text, level=level)

def add_code_block(doc, code_text, language=""):
    """Add a code block (monospace paragraph)."""
    p = doc.add_paragraph()
    p.style = 'Normal'
    run = p.add_run(code_text)
    run.font.name = 'Courier New'
    run.font.size = Pt(10)
    # Add background color for code blocks
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), 'F0F0F0')
    p._element.get_or_add_pPr().append(shading_elm)
    return p

def add_table(doc, rows, cols, data):
    """Add a table to document."""
    table = doc.add_table(rows=rows, cols=cols)
    table.style = 'Light Grid Accent 1'

    # Fill data
    for i, row_data in enumerate(data):
        for j, cell_data in enumerate(row_data):
            table.rows[i].cells[j].text = str(cell_data)

    return table

def create_sample_document(output_path):
    """Create sample Word document for DITA conversion."""
    doc = Document()

    # Document Title
    title = doc.add_heading('Getting Started with DITA Documentation', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph(
        'A comprehensive guide covering DITA concepts, implementation tasks, '
        'and reference documentation.',
        style='Normal'
    )

    # ========== SECTION 1: CONCEPT TOPIC ==========
    doc.add_heading('Understanding DITA', 1)

    doc.add_heading('What is DITA?', 2)
    doc.add_paragraph(
        'DITA (Darwin Information Typing Architecture) is an XML-based standard for '
        'creating, managing, and publishing structured technical documentation. It is '
        'designed to enable single-sourcing and content reuse across multiple outputs '
        'and formats.'
    )

    doc.add_heading('Core Principles', 2)
    doc.add_paragraph(
        'DITA is built on three fundamental principles:', style='Normal'
    )

    # Bulleted list
    doc.add_paragraph('Topic-based authoring: Content organized into modular, reusable topics',
                      style='List Bullet')
    doc.add_paragraph('Typed content: Different topic types (concept, task, reference) serve specific purposes',
                      style='List Bullet')
    doc.add_paragraph('Separation of content and presentation: XML markup defines structure, not formatting',
                      style='List Bullet')

    doc.add_heading('Topic Types', 2)
    doc.add_paragraph(
        'DITA defines three primary topic types:', style='Normal'
    )

    # Add table
    table_data = [
        ['Topic Type', 'Purpose', 'Example'],
        ['Concept', 'Explains what something is', 'Overview of DITA architecture'],
        ['Task', 'Provides step-by-step instructions', 'How to create a DITA topic'],
        ['Reference', 'Documents specifications and facts', 'DITA element reference guide']
    ]
    add_table(doc, len(table_data), 3, table_data)

    # ========== SECTION 2: TASK TOPIC ==========
    doc.add_heading('Creating Your First DITA Topic', 1)

    doc.add_heading('Prerequisites', 2)
    doc.add_paragraph('Before you begin, ensure you have:', style='Normal')
    doc.add_paragraph('An XML editor (e.g., Oxygen XML Editor, VS Code with XML extensions)',
                      style='List Bullet')
    doc.add_paragraph('DITA 1.3 or later schema files', style='List Bullet')
    doc.add_paragraph('A text editor or IDE for XML authoring', style='List Bullet')

    doc.add_heading('Step-by-Step Instructions', 2)

    doc.add_paragraph('Step 1: Set Up Your Project', style='Heading 3')
    doc.add_paragraph(
        'Create a project directory with the following structure:'
    )
    add_code_block(doc, '''project-root/
├── topics/
│   ├── concept-*.dita
│   ├── task-*.dita
│   └── reference-*.dita
├── images/
│   └── [all image files]
└── project.ditamap''')

    doc.add_paragraph('Step 2: Create a New Concept Topic', style='Heading 3')
    doc.add_paragraph(
        'Open your XML editor and create a new file with the following structure:'
    )
    add_code_block(doc, '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE concept PUBLIC "-//OASIS//DTD DITA Concept//EN" "concept.dtd">
<concept id="my_concept">
  <title>My Concept Title</title>
  <conbody>
    <p>Concept content goes here.</p>
  </conbody>
</concept>''')

    doc.add_paragraph('Step 3: Add Metadata', style='Heading 3')
    doc.add_paragraph('Include a prolog section for metadata:')
    add_code_block(doc, '''<prolog>
  <author>Your Name</author>
  <created date="2026-06-26"/>
  <revised modified="2026-06-26"/>
  <metadata>
    <keywords>
      <keyword>DITA</keyword>
      <keyword>documentation</keyword>
    </keywords>
  </metadata>
</prolog>''')

    doc.add_paragraph('Step 4: Validate and Save', style='Heading 3')
    doc.add_paragraph(
        'Save the file with a .dita extension. Use your XML editor\'s validation '
        'feature to ensure the file is well-formed and conforms to the DITA schema.'
    )

    # ========== SECTION 3: REFERENCE TOPIC ==========
    doc.add_heading('DITA Elements Reference', 1)

    doc.add_heading('Common Elements', 2)
    doc.add_paragraph('This section documents frequently used DITA elements:')

    # Reference table
    ref_data = [
        ['Element', 'Description', 'Parent Elements'],
        ['<concept>', 'Root element for concept topics', 'N/A (root)'],
        ['<title>', 'Topic or section title', 'concept, section, xref'],
        ['<conbody>', 'Container for concept content', 'concept'],
        ['<p>', 'Paragraph element', 'conbody, taskbody, refbody'],
        ['<image>', 'Image reference element', 'fig, p'],
        ['<xref>', 'Cross-reference to another topic', 'p, li'],
        ['<table>', 'Table element', 'conbody, taskbody, refbody']
    ]
    add_table(doc, len(ref_data), 3, ref_data)

    doc.add_heading('Best Practices', 2)
    doc.add_paragraph('Follow these best practices when authoring DITA:')
    doc.add_paragraph('Use semantic elements: Choose elements based on meaning, not appearance',
                      style='List Number')
    doc.add_paragraph('Keep topics modular: One idea per topic, make topics reusable',
                      style='List Number')
    doc.add_paragraph('Use consistent terminology: Maintain a glossary for key terms',
                      style='List Number')
    doc.add_paragraph('Include metadata: Always add prolog information for tracking',
                      style='List Number')
    doc.add_paragraph('Validate regularly: Ensure XML is well-formed throughout authoring',
                      style='List Number')

    # ========== ADDITIONAL CONTENT ==========
    doc.add_page_break()
    doc.add_heading('Converting Existing Documentation', 1)
    doc.add_paragraph(
        'Converting existing documentation from formats like Word or plain text to DITA '
        'requires a systematic approach. The conversion process involves:'
    )
    doc.add_paragraph('Analyzing source content structure', style='List Bullet')
    doc.add_paragraph('Classifying content into DITA topic types', style='List Bullet')
    doc.add_paragraph('Creating appropriate XML markup', style='List Bullet')
    doc.add_paragraph('Organizing topics in a ditamap', style='List Bullet')
    doc.add_paragraph('Managing images and external resources', style='List Bullet')

    doc.add_heading('Quality Assurance', 1)
    doc.add_paragraph(
        'Ensure your DITA deliverables meet quality standards:'
    )

    qa_data = [
        ['Check', 'Description', 'Tool/Method'],
        ['XML Validation', 'Verify well-formed XML against DITA DTD', 'XML Editor validation'],
        ['Link Verification', 'Confirm all xref and image hrefs are valid', 'Link checker tool'],
        ['Terminology Consistency', 'Check for consistent term usage', 'Manual review'],
        ['Metadata Completeness', 'Ensure prolog information is complete', 'Schema validation']
    ]
    add_table(doc, len(qa_data), 3, qa_data)

    # Save document
    doc.save(output_path)
    print(f"Sample document created: {output_path}")
    return output_path

if __name__ == '__main__':
    # Create samples directory if it doesn't exist
    samples_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'samples'
    )
    os.makedirs(samples_dir, exist_ok=True)

    # Generate sample document
    output_file = os.path.join(samples_dir, 'sample-dita-guide.docx')
    create_sample_document(output_file)
