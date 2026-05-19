"""Video assembly using moviepy."""

import os
from typing import List, Tuple, Optional
from moviepy import ImageClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
from moviepy.video.fx import FadeIn, FadeOut
from PIL import Image

from .parser import Section
from .generator import (
    generate_title_card,
    generate_content_image_placeholder,
    generate_image_dalle,
    add_text_overlay,
)


def create_section_clip(
    section: Section,
    section_index: int,
    resolution: Tuple[int, int],
    duration_per_section: float = 5.0,
    use_dalle: bool = False,
    api_key: Optional[str] = None,
) -> List:
    """
    Create video clips for a single section.

    Args:
        section: Section object
        section_index: Index of the section (for color variation)
        resolution: Video resolution (width, height)
        duration_per_section: Duration in seconds for each clip
        use_dalle: Whether to use DALL-E for image generation
        api_key: OpenAI API key for DALL-E

    Returns:
        List of video clips
    """
    clips = []

    print(f"Processing section {section_index + 1}: {section.title}")

    # Generate title card
    print("  Generating title card...")
    title_img = generate_title_card(section.title, resolution)
    title_img.save(f"temp_title_{section_index}.png")
    title_clip = ImageClip(f"temp_title_{section_index}.png", duration=duration_per_section)
    title_clip = title_clip.with_effects([FadeIn(0.5), FadeOut(0.5)])
    clips.append(title_clip)

    # Generate content image
    print("  Generating content image...")
    if use_dalle and api_key:
        content_img = generate_image_dalle(section.image_prompt, resolution, api_key)
        if content_img is None:
            print("  Falling back to placeholder...")
            content_img = generate_content_image_placeholder(
                section.title, section.content, resolution, section_index
            )
    else:
        content_img = generate_content_image_placeholder(
            section.title, section.content, resolution, section_index
        )

    # Add text overlay if content is not empty
    if section.content:
        content_img = add_text_overlay(content_img, section.content[:200])

    content_img.save(f"temp_content_{section_index}.png")
    content_clip = ImageClip(f"temp_content_{section_index}.png", duration=duration_per_section)
    content_clip = content_clip.with_effects([FadeIn(0.5), FadeOut(0.5)])
    clips.append(content_clip)

    return clips


def assemble_video(
    sections: List[Section],
    output_path: str,
    resolution: Tuple[int, int] = (1920, 1080),
    duration_per_section: float = 5.0,
    music_path: Optional[str] = None,
    use_dalle: bool = False,
    api_key: Optional[str] = None,
):
    """
    Assemble the final video from sections.

    Args:
        sections: List of Section objects
        output_path: Path to output video file
        resolution: Video resolution (width, height)
        duration_per_section: Duration in seconds for each clip
        music_path: Optional path to background music file
        use_dalle: Whether to use DALL-E for image generation
        api_key: OpenAI API key for DALL-E
    """
    print(f"\nAssembling video with {len(sections)} sections...")
    print(f"Resolution: {resolution[0]}x{resolution[1]}")
    print(f"Duration per clip: {duration_per_section}s")
    print(f"DALL-E: {'Enabled' if use_dalle else 'Disabled (placeholder mode)'}")
    print()

    all_clips = []

    # Process each section
    for i, section in enumerate(sections):
        section_clips = create_section_clip(
            section, i, resolution, duration_per_section, use_dalle, api_key
        )
        all_clips.extend(section_clips)

    # Concatenate all clips
    print("\nConcatenating clips...")
    final_clip = concatenate_videoclips(all_clips, method="compose")

    # Add background music if provided
    if music_path and os.path.exists(music_path):
        print(f"Adding background music: {music_path}")
        audio = AudioFileClip(music_path)

        # Loop audio if shorter than video
        if audio.duration < final_clip.duration:
            n_loops = int(final_clip.duration / audio.duration) + 1
            audio = audio.loop(n=n_loops)

        # Trim audio to video length
        audio = audio.with_subclip(0, final_clip.duration)

        # Mix with existing audio or set as audio
        final_clip = final_clip.with_audio(audio)

    # Write output video
    print(f"\nWriting output video: {output_path}")
    final_clip.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
    )

    # Cleanup temporary files
    print("\nCleaning up temporary files...")
    for i in range(len(sections)):
        for prefix in ['temp_title_', 'temp_content_']:
            temp_file = f"{prefix}{i}.png"
            if os.path.exists(temp_file):
                os.remove(temp_file)

    print(f"\n✓ Video created successfully: {output_path}")
    print(f"  Total duration: {final_clip.duration:.1f}s")
