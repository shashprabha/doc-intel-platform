#!/usr/bin/env python3
"""
DITA Converter: Convert Word documents and other content to DITA XML.
Performs full conversion pipeline: parsing, classification, semantic markup generation.
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

try:
    from docx import Document
    from docx.oxml import parse_xml
except ImportError:
    print("Error: python-docx required. Install with: pip install python-docx")
    exit(1)


class TopicType(Enum):
    """DITA Topic types."""
    CONCEPT = "concept"
    TASK = "task"
    REFERENCE = "reference"


@dataclass
class Topic:
    """Represents a DITA topic."""
    id: str
    title: str
    topic_type: TopicType
    content: List[str]
    metadata: Dict
    parent_id: Optional[str] = None


class DITAConverter:
    """Convert documents to DITA XML format."""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.topics_dir = self.output_dir / "topics"
        self.images_dir = self.output_dir / "images"
        self.topics: List[Topic] = []
        self.conversion_log: List[str] = []

    def setup_directories(self):
        """Create output directory structure."""
        self.topics_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.log(f"Created output directories at {self.output_dir}")

    def log(self, message: str):
        """Log conversion messages."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.conversion_log.append(log_entry)
        print(log_entry)

    def parse_docx(self, docx_path: str) -> Dict:
        """Parse Word document structure."""
        self.log(f"Parsing document: {docx_path}")
        doc = Document(docx_path)

        content_structure = {
            "title": "",
            "sections": [],
            "metadata": {
                "author": "Unknown",
                "created": datetime.now().isoformat(),
                "source": Path(docx_path).name
            }
        }

        current_section = None
        current_heading_level = 0

        for para in doc.paragraphs:
            # Skip empty paragraphs
            if not para.text.strip():
                continue

            # Detect headings
            style_name = para.style.name if para.style else ""

            if "Heading 1" in style_name:
                if current_section:
                    content_structure["sections"].append(current_section)
                current_section = {
                    "title": para.text,
                    "level": 1,
                    "content": [],
                    "subsections": []
                }
                if not content_structure["title"]:
                    content_structure["title"] = para.text
                current_heading_level = 1

            elif "Heading 2" in style_name and current_section:
                subsection = {
                    "title": para.text,
                    "level": 2,
                    "content": []
                }
                current_section["subsections"].append(subsection)
                current_heading_level = 2

            elif current_section:
                # Collect content
                if current_heading_level >= 2 and current_section["subsections"]:
                    current_section["subsections"][-1]["content"].append(para.text)
                else:
                    current_section["content"].append(para.text)

        if current_section:
            content_structure["sections"].append(current_section)

        self.log(f"Found {len(content_structure['sections'])} top-level sections")
        return content_structure

    def classify_topic_type(self, section: Dict) -> TopicType:
        """Classify section into DITA topic type."""
        title_lower = section["title"].lower()
        content_text = " ".join(section["content"]).lower()

        # Task indicators
        task_keywords = [
            "create", "build", "setup", "install", "configure", "step",
            "instructions", "how to", "guide", "procedure", "tutorial"
        ]
        # Reference indicators
        reference_keywords = [
            "reference", "api", "specification", "elements", "properties",
            "attributes", "parameter", "schema", "doctype", "dtd"
        ]
        # Check for numbered steps (strong task indicator)
        has_steps = re.search(r'Step\s+\d+:|^\s*\d+\.|Prerequisites', content_text)

        if any(kw in title_lower or kw in content_text for kw in task_keywords) or has_steps:
            return TopicType.TASK
        elif any(kw in title_lower or kw in content_text for kw in reference_keywords):
            return TopicType.REFERENCE
        else:
            return TopicType.CONCEPT

    def sanitize_id(self, text: str) -> str:
        """Convert text to valid DITA ID."""
        # Remove special characters, convert to lowercase
        id_text = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
        id_text = id_text.strip()
        id_text = id_text.lower()
        id_text = re.sub(r'\s+', '-', id_text)
        id_text = id_text.strip('-')
        return id_text[:64]  # DITA ID length limit

    def extract_keywords(self, section: Dict, topic_type: TopicType) -> List[str]:
        """Extract keywords from content."""
        title_lower = section["title"].lower()
        content_text = " ".join(section["content"] +
                               [s["title"] for s in section.get("subsections", [])]).lower()

        # Type-specific keywords
        keywords = []
        if topic_type == TopicType.TASK:
            keywords.extend(["procedure", "tutorial", "setup"])
        elif topic_type == TopicType.REFERENCE:
            keywords.extend(["specification", "reference", "documentation"])
        else:
            keywords.extend(["concept", "overview", "introduction"])

        # Extract title keywords
        title_words = [w for w in title_lower.split() if len(w) > 3]
        keywords.extend(title_words[:3])

        return list(dict.fromkeys(keywords))  # Remove duplicates, preserve order

    def generate_dita_xml(self, topic: Topic) -> str:
        """Generate DITA XML for a topic."""
        doctype_map = {
            TopicType.CONCEPT: 'concept PUBLIC "-//OASIS//DTD DITA Concept//EN" "concept.dtd"',
            TopicType.TASK: 'task PUBLIC "-//OASIS//DTD DITA Task//EN" "task.dtd"',
            TopicType.REFERENCE: 'reference PUBLIC "-//OASIS//DTD DITA Reference//EN" "reference.dtd"'
        }

        root_element = topic.topic_type.value

        xml_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<!DOCTYPE {doctype_map[topic.topic_type]}>',
            f'<{root_element} id="{topic.id}">',
            f'  <title>{self._escape_xml(topic.title)}</title>',
            self._generate_prolog(topic.metadata),
            self._generate_body(topic),
            f'</{root_element}>'
        ]

        return '\n'.join(xml_parts)

    def _escape_xml(self, text: str) -> str:
        """Escape special XML characters."""
        escape_map = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;'}
        for char, escape in escape_map.items():
            text = text.replace(char, escape)
        return text

    def _generate_prolog(self, metadata: Dict) -> str:
        """Generate DITA prolog section."""
        author = metadata.get("author", "Unknown")
        created = metadata.get("created", datetime.now().isoformat()[:10])

        keywords = metadata.get("keywords", [])
        keywords_xml = ""
        if keywords:
            keywords_xml = "    <keywords>\n"
            for kw in keywords[:5]:  # Limit to 5 keywords
                keywords_xml += f'      <keyword>{self._escape_xml(kw)}</keyword>\n'
            keywords_xml += "    </keywords>\n"

        prolog = f'''  <prolog>
    <author>{self._escape_xml(author)}</author>
    <created date="{created}"/>
    <revised modified="{datetime.now().isoformat()[:10]}"/>
    <metadata>
{keywords_xml}    </metadata>
  </prolog>'''

        return prolog

    def _generate_body(self, topic: Topic) -> str:
        """Generate appropriate body element based on topic type."""
        body_element = {
            TopicType.CONCEPT: "conbody",
            TopicType.TASK: "taskbody",
            TopicType.REFERENCE: "refbody"
        }[topic.topic_type]

        content_xml = "  <" + body_element + ">\n"

        for line in topic.content:
            if line.strip():
                # Simple paragraph wrapping
                if line.strip().startswith("Step "):
                    # Parse step instructions
                    step_match = re.match(r'Step\s+\d+:\s*(.*)', line)
                    if step_match:
                        content_xml += f'    <p><b>{self._escape_xml(line)}</b></p>\n'
                    else:
                        content_xml += f'    <p>{self._escape_xml(line)}</p>\n'
                elif line.strip().startswith("•") or line.strip().startswith("-"):
                    # List item
                    content_xml += f'    <ul><li>{self._escape_xml(line.lstrip("•- "))}</li></ul>\n'
                else:
                    content_xml += f'    <p>{self._escape_xml(line)}</p>\n'

        content_xml += "  </" + body_element + ">\n"
        return content_xml.rstrip()

    def convert(self, docx_path: str) -> str:
        """Run full conversion pipeline."""
        self.log("=" * 60)
        self.log("DITA CONVERSION STARTED")
        self.log("=" * 60)

        # Setup
        self.setup_directories()

        # Parse
        structure = self.parse_docx(docx_path)
        self.log(f"Document title: {structure['title']}")

        # Classify and create topics
        topic_count = {t.value: 0 for t in TopicType}

        for section in structure["sections"]:
            topic_type = self.classify_topic_type(section)
            topic_count[topic_type.value] += 1

            topic_id = self.sanitize_id(section["title"])
            keywords = self.extract_keywords(section, topic_type)

            topic = Topic(
                id=topic_id,
                title=section["title"],
                topic_type=topic_type,
                content=section["content"],
                metadata={
                    "author": structure["metadata"].get("author", "Unknown"),
                    "created": structure["metadata"].get("created", datetime.now().isoformat()[:10]),
                    "keywords": keywords,
                    "source": structure["metadata"].get("source", "unknown")
                }
            )

            self.topics.append(topic)
            self.log(f"Created {topic_type.value} topic: {topic.title} (id: {topic.id})")

        # Generate XML files
        for topic in self.topics:
            xml_content = self.generate_dita_xml(topic)
            filename = f"{topic.topic_type.value}-{topic.id}.dita"
            filepath = self.topics_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(xml_content)

            self.log(f"Generated: {filename}")

        # Generate ditamap
        self._generate_ditamap(structure["title"])

        # Generate conversion report
        self._generate_report(structure, topic_count)

        self.log("=" * 60)
        self.log("DITA CONVERSION COMPLETED")
        self.log("=" * 60)

        return str(self.output_dir)

    def _generate_ditamap(self, title: str):
        """Generate DITA map file."""
        ditamap_id = self.sanitize_id(title)

        ditamap_content = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<!DOCTYPE map PUBLIC "-//OASIS//DTD DITA Map//EN" "map.dtd">',
            f'<map id="{ditamap_id}-map">',
            f'  <title>{self._escape_xml(title)}</title>'
        ]

        for topic in self.topics:
            filename = f"{topic.topic_type.value}-{topic.id}.dita"
            ditamap_content.append(f'  <topicref href="topics/{filename}"/>')

        ditamap_content.append('</map>')

        ditamap_path = self.output_dir / "project.ditamap"
        with open(ditamap_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ditamap_content))

        self.log(f"Generated: project.ditamap")

    def _generate_report(self, structure: Dict, topic_count: Dict):
        """Generate conversion report."""
        report_lines = [
            "# DITA Conversion Report\n",
            f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"**Source Document**: {structure['metadata']['source']}\n",
            f"**Title**: {structure['title']}\n",
            f"**Author**: {structure['metadata']['author']}\n\n",
            "## Conversion Summary\n",
            f"- **Total Topics Created**: {len(self.topics)}\n",
            f"- **Concept Topics**: {topic_count['concept']}\n",
            f"- **Task Topics**: {topic_count['task']}\n",
            f"- **Reference Topics**: {topic_count['reference']}\n\n",
            "## Topics Generated\n"
        ]

        for topic in self.topics:
            report_lines.append(f"- `{topic.topic_type.value}-{topic.id}.dita` - {topic.title}\n")

        report_lines.extend([
            "\n## Output Structure\n",
            "```\n",
            "project/\n",
            "├── topics/\n",
            "│   ├── concept-*.dita\n",
            "│   ├── task-*.dita\n",
            "│   └── reference-*.dita\n",
            "├── images/\n",
            "│   └── [images would go here]\n",
            "└── project.ditamap\n",
            "```\n\n",
            "## Conversion Log\n",
            "```\n"
        ])

        report_lines.extend(self.conversion_log)
        report_lines.append("\n```\n")

        report_path = self.output_dir / "conversion-report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.writelines(report_lines)

        self.log(f"Generated: conversion-report.md")


def main():
    """Main conversion entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python convert_to_dita.py <input_docx> [output_dir]")
        print("Example: python convert_to_dita.py document.docx ./dita-output")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./dita-output"

    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    converter = DITAConverter(output_dir)
    result = converter.convert(input_file)
    print(f"\n[OK] Conversion complete! Output: {result}")


if __name__ == "__main__":
    main()
