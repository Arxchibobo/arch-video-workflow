"""Markdown script parser for extracting sections."""

import re
from typing import List, Dict


class Section:
    """Represents a section in the architectural presentation."""

    def __init__(self, title: str, content: str, image_prompt: str = None):
        self.title = title
        self.content = content
        self.image_prompt = image_prompt or f"Modern architectural design: {title}"

    def __repr__(self):
        return f"Section(title='{self.title}', content_length={len(self.content)})"


def parse_markdown_script(markdown_text: str) -> List[Section]:
    """
    Parse markdown text into sections.

    Sections are defined by ## headings. Each section can optionally have
    an image prompt specified with [image: prompt text].

    Args:
        markdown_text: The markdown script content

    Returns:
        List of Section objects
    """
    sections = []

    # Split by ## headings (but not # or ###)
    parts = re.split(r'^## (.+)$', markdown_text, flags=re.MULTILINE)

    # First part before any heading (skip if exists)
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            title = parts[i].strip()
            content = parts[i + 1].strip() if i + 1 < len(parts) else ""

            # Check for custom image prompt
            image_prompt = None
            image_match = re.search(r'\[image:\s*([^\]]+)\]', content, re.IGNORECASE)
            if image_match:
                image_prompt = image_match.group(1).strip()
                # Remove the image directive from content
                content = re.sub(r'\[image:\s*[^\]]+\]\s*', '', content, flags=re.IGNORECASE)

            sections.append(Section(title, content.strip(), image_prompt))

    return sections


def parse_script_file(filepath: str) -> List[Section]:
    """
    Parse a markdown file into sections.

    Args:
        filepath: Path to the markdown file

    Returns:
        List of Section objects
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return parse_markdown_script(content)
