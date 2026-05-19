"""Command-line interface for arch-video workflow."""

import argparse
import os
import sys
from typing import Tuple

from .parser import parse_script_file
from .assembler import assemble_video


def parse_resolution(resolution_str: str) -> Tuple[int, int]:
    """Parse resolution string like '1920x1080' into tuple."""
    try:
        width, height = resolution_str.lower().split('x')
        return (int(width), int(height))
    except (ValueError, AttributeError):
        raise argparse.ArgumentTypeError(
            f"Invalid resolution format: {resolution_str}. Expected format: WIDTHxHEIGHT (e.g., 1920x1080)"
        )


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog='arch-video',
        description='Automated architectural presentation video workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate video with placeholder images
  python -m arch_video --script project.md --output final.mp4

  # Generate video with custom resolution
  python -m arch_video --script project.md --output final.mp4 --resolution 1280x720

  # Generate video with DALL-E images (requires OPENAI_API_KEY)
  export OPENAI_API_KEY=your_key_here
  python -m arch_video --script project.md --output final.mp4 --dalle

  # Generate video with background music
  python -m arch_video --script project.md --output final.mp4 --music background.mp3

  # All options combined
  python -m arch_video --script project.md --output final.mp4 \\
      --resolution 1920x1080 --music bg.mp3 --dalle --duration 6
        """
    )

    parser.add_argument(
        '--script',
        required=True,
        help='Path to markdown script file describing the architectural project'
    )

    parser.add_argument(
        '--output',
        required=True,
        help='Path to output video file (e.g., final.mp4)'
    )

    parser.add_argument(
        '--resolution',
        type=parse_resolution,
        default='1920x1080',
        help='Video resolution in WIDTHxHEIGHT format (default: 1920x1080)'
    )

    parser.add_argument(
        '--music',
        help='Path to background music file (optional)'
    )

    parser.add_argument(
        '--dalle',
        action='store_true',
        help='Use DALL-E to generate images (requires OPENAI_API_KEY environment variable)'
    )

    parser.add_argument(
        '--duration',
        type=float,
        default=5.0,
        help='Duration in seconds for each clip (default: 5.0)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.script):
        print(f"Error: Script file not found: {args.script}", file=sys.stderr)
        sys.exit(1)

    # Validate music file if provided
    if args.music and not os.path.exists(args.music):
        print(f"Error: Music file not found: {args.music}", file=sys.stderr)
        sys.exit(1)

    # Check for DALL-E API key if requested
    api_key = os.getenv('OPENAI_API_KEY')
    if args.dalle and not api_key:
        print("Warning: --dalle flag set but OPENAI_API_KEY not found in environment.", file=sys.stderr)
        print("Falling back to placeholder mode.", file=sys.stderr)
        args.dalle = False

    # Parse the script
    print(f"Parsing script: {args.script}")
    try:
        sections = parse_script_file(args.script)
    except Exception as e:
        print(f"Error parsing script: {e}", file=sys.stderr)
        sys.exit(1)

    if not sections:
        print("Error: No sections found in script. Make sure to use '## Section Title' format.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(sections)} sections")

    # Assemble the video
    try:
        assemble_video(
            sections=sections,
            output_path=args.output,
            resolution=args.resolution,
            duration_per_section=args.duration,
            music_path=args.music,
            use_dalle=args.dalle,
            api_key=api_key,
        )
    except Exception as e:
        print(f"\nError assembling video: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
