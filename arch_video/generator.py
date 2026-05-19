"""Image generation for title cards and content images."""

import os
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import textwrap


def generate_title_card(
    title: str,
    resolution: Tuple[int, int] = (1920, 1080),
    bg_color: Tuple[int, int, int] = (30, 30, 30),
    text_color: Tuple[int, int, int] = (255, 255, 255),
) -> Image.Image:
    """
    Generate a title card image with centered text.

    Args:
        title: The title text to display
        resolution: Image resolution (width, height)
        bg_color: Background color RGB tuple
        text_color: Text color RGB tuple

    Returns:
        PIL Image object
    """
    img = Image.new('RGB', resolution, bg_color)
    draw = ImageDraw.Draw(img)

    # Try to load a nice font, fall back to default
    try:
        # Try common Windows fonts
        font_size = resolution[1] // 15
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("Arial.ttf", font_size)
        except OSError:
            try:
                # Linux fallback
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except OSError:
                # Use default font
                font = ImageFont.load_default()

    # Wrap text if too long
    max_chars_per_line = 30
    wrapped_title = textwrap.fill(title, width=max_chars_per_line)

    # Get text bounding box
    bbox = draw.textbbox((0, 0), wrapped_title, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center the text
    x = (resolution[0] - text_width) // 2
    y = (resolution[1] - text_height) // 2

    draw.text((x, y), wrapped_title, fill=text_color, font=font)

    return img


def generate_content_image_placeholder(
    section_title: str,
    content: str,
    resolution: Tuple[int, int] = (1920, 1080),
    color_index: int = 0,
) -> Image.Image:
    """
    Generate a placeholder content image with section text.

    Args:
        section_title: Title of the section
        content: Content text to display
        resolution: Image resolution (width, height)
        color_index: Index for color variation

    Returns:
        PIL Image object
    """
    # Color palette for variety
    colors = [
        (60, 80, 100),   # Blue-grey
        (80, 60, 90),    # Purple-grey
        (70, 90, 80),    # Green-grey
        (100, 70, 60),   # Brown-grey
        (90, 80, 70),    # Tan
    ]

    bg_color = colors[color_index % len(colors)]
    img = Image.new('RGB', resolution, bg_color)
    draw = ImageDraw.Draw(img)

    # Try to load font
    try:
        title_font_size = resolution[1] // 20
        content_font_size = resolution[1] // 35
        title_font = ImageFont.truetype("arial.ttf", title_font_size)
        content_font = ImageFont.truetype("arial.ttf", content_font_size)
    except OSError:
        try:
            title_font = ImageFont.truetype("Arial.ttf", title_font_size)
            content_font = ImageFont.truetype("Arial.ttf", content_font_size)
        except OSError:
            title_font = ImageFont.load_default()
            content_font = ImageFont.load_default()

    # Draw title at top
    title_y = resolution[1] // 8
    title_bbox = draw.textbbox((0, 0), section_title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (resolution[0] - title_width) // 2
    draw.text((title_x, title_y), section_title, fill=(255, 255, 255), font=title_font)

    # Draw content text (wrapped)
    max_chars_per_line = 60
    wrapped_content = textwrap.fill(content[:500], width=max_chars_per_line)  # Limit content length

    content_y = resolution[1] // 3
    content_x = resolution[0] // 10

    draw.text((content_x, content_y), wrapped_content, fill=(220, 220, 220), font=content_font)

    return img


def generate_image_dalle(
    prompt: str,
    resolution: Tuple[int, int] = (1920, 1080),
    api_key: Optional[str] = None,
) -> Optional[Image.Image]:
    """
    Generate an image using DALL-E API.

    Args:
        prompt: The image generation prompt
        resolution: Desired image resolution (will be converted to DALL-E size)
        api_key: OpenAI API key (uses OPENAI_API_KEY env var if not provided)

    Returns:
        PIL Image object or None if generation fails
    """
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        return None

    try:
        from openai import OpenAI
        import requests
        from io import BytesIO

        client = OpenAI(api_key=api_key)

        # DALL-E 3 supports 1024x1024, 1024x1792, or 1792x1024
        # Choose closest aspect ratio
        aspect = resolution[0] / resolution[1]
        if aspect > 1.5:
            size = "1792x1024"
        elif aspect < 0.7:
            size = "1024x1792"
        else:
            size = "1024x1024"

        print(f"  Generating image with DALL-E (size: {size})...")

        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Architectural visualization: {prompt}. Modern, professional, clean design.",
            size=size,
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url

        # Download the image
        img_response = requests.get(image_url, timeout=30)
        img_response.raise_for_status()
        img = Image.open(BytesIO(img_response.content))

        # Resize to target resolution
        img = img.resize(resolution, Image.Resampling.LANCZOS)

        return img

    except Exception as e:
        print(f"  Warning: DALL-E generation failed: {e}")
        return None


def add_text_overlay(
    img: Image.Image,
    text: str,
    position: str = "bottom",
    bg_opacity: int = 180,
) -> Image.Image:
    """
    Add a semi-transparent text overlay to an image.

    Args:
        img: The base image
        text: Text to overlay
        position: Position of overlay ("top" or "bottom")
        bg_opacity: Opacity of background (0-255)

    Returns:
        Modified PIL Image object
    """
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Try to load font
    try:
        font_size = img.size[1] // 30
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("Arial.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()

    # Wrap text
    max_chars_per_line = 80
    wrapped_text = textwrap.fill(text[:300], width=max_chars_per_line)

    # Get text size
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_height = bbox[3] - bbox[1]

    # Draw semi-transparent background
    margin = 40
    if position == "bottom":
        rect_y = img.size[1] - text_height - margin * 2
    else:
        rect_y = 0

    draw.rectangle(
        [(0, rect_y), (img.size[0], rect_y + text_height + margin * 2)],
        fill=(0, 0, 0, bg_opacity)
    )

    # Draw text
    text_y = rect_y + margin
    draw.text((margin, text_y), wrapped_text, fill=(255, 255, 255, 255), font=font)

    # Composite overlay onto original image
    img_rgba = img.convert('RGBA')
    result = Image.alpha_composite(img_rgba, overlay)

    return result.convert('RGB')
