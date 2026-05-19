# arch-video-workflow

Automated architectural presentation video workflow: text → multi-clip → final cut

Transform markdown scripts into professional architectural presentation videos with title cards, content images, text overlays, and background music.

## Features

- 📝 **Markdown-based scripting**: Write your presentation as simple markdown sections
- 🎬 **Automated video assembly**: Generates title cards and content clips with smooth transitions
- 🎨 **Dual mode operation**:
  - **Placeholder mode**: Generates videos without API keys using styled backgrounds
  - **DALL-E mode**: Uses OpenAI's DALL-E 3 for AI-generated architectural visualizations
- 🎵 **Background music**: Optional audio track support
- ⚙️ **Customizable**: Control resolution, timing, and visual styles
- 🪟 **Windows-ready**: Fully compatible with Windows systems

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Windows Installation

```bash
# Clone the repository
git clone <repository-url>
cd arch-video-workflow

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m arch_video --help
```

### Linux/Mac Installation

```bash
# Clone the repository
git clone <repository-url>
cd arch-video-workflow

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m arch_video --help
```

## Quick Start

### 1. Create a Markdown Script

Create a markdown file with sections using `##` headings:

```markdown
# My Architectural Project

## Introduction

This is the introduction section with project overview.

## Design Concept

[image: modern building with glass facade and green spaces]

The design emphasizes sustainable materials and natural light.

## Site Plan

Our site responds to the urban context through strategic massing.
```

### 2. Generate Your Video

**Placeholder Mode (No API Key Required):**

```bash
python -m arch_video --script examples/project.md --output presentation.mp4
```

**DALL-E Mode (Requires OpenAI API Key):**

```bash
# Set your OpenAI API key
set OPENAI_API_KEY=sk-your-key-here  # Windows
export OPENAI_API_KEY=sk-your-key-here  # Linux/Mac

# Generate with AI images
python -m arch_video --script examples/project.md --output presentation.mp4 --dalle
```

**With Background Music:**

```bash
python -m arch_video --script examples/project.md --output presentation.mp4 --music background.mp3
```

## Command-Line Options

```
usage: arch-video --script SCRIPT --output OUTPUT [OPTIONS]

Required Arguments:
  --script SCRIPT       Path to markdown script file
  --output OUTPUT       Path to output video file (e.g., final.mp4)

Optional Arguments:
  --resolution WxH      Video resolution (default: 1920x1080)
                        Examples: 1920x1080, 1280x720, 3840x2160
  
  --music MUSIC         Path to background music file (MP3, WAV, etc.)
  
  --dalle               Enable DALL-E image generation
                        Requires OPENAI_API_KEY environment variable
  
  --duration SECONDS    Duration for each clip in seconds (default: 5.0)
  
  --help               Show this help message
  --version            Show version information
```

## Script Format

### Basic Structure

Each `##` heading creates a new section with two clips:
1. Title card (black background with white text)
2. Content image (with text overlay)

```markdown
## Section Title

Section content text appears as overlay on the content image.
This text will be wrapped and displayed at the bottom of the frame.
```

### Custom Image Prompts

Specify custom DALL-E prompts using `[image: prompt]` syntax:

```markdown
## Sustainable Design

[image: eco-friendly building with solar panels and green roof]

Our design incorporates sustainable materials and renewable energy systems.
```

**Note:** Image prompts are only used when `--dalle` flag is enabled. In placeholder mode, they are ignored.

## Examples

### Example 1: Basic Video

```bash
python -m arch_video --script examples/project.md --output basic.mp4
```

Creates a video with placeholder images and default settings.

### Example 2: HD Video with Music

```bash
python -m arch_video --script examples/project.md --output hd.mp4 --resolution 1920x1080 --music bgmusic.mp3
```

### Example 3: AI-Generated Images

```bash
set OPENAI_API_KEY=sk-your-key-here
python -m arch_video --script examples/project.md --output ai.mp4 --dalle --duration 6
```

Each section will have AI-generated architectural visualizations.

### Example 4: 4K Production

```bash
python -m arch_video --script examples/project.md --output 4k.mp4 --resolution 3840x2160 --music background.mp3 --dalle
```

## Project Structure

```
arch-video-workflow/
├── arch_video/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Module entry point
│   ├── cli.py               # Command-line interface
│   ├── parser.py            # Markdown parsing
│   ├── generator.py         # Image generation (title cards, DALL-E)
│   └── assembler.py         # Video assembly with moviepy
├── examples/
│   └── project.md           # Sample architectural presentation
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Dependencies

- **moviepy** (>=1.0.3): Video editing and assembly
- **Pillow** (>=10.0.0): Image generation and manipulation
- **openai** (>=1.0.0): DALL-E API integration (optional)

## Troubleshooting

### "No sections found in script"

Make sure your markdown file uses `##` (double hash) for section headings:

```markdown
## Correct Section Heading

This works!
```

### Font Issues on Windows

The tool tries to use Arial font by default. If you encounter font errors, install common fonts or the tool will fall back to the default system font.

### DALL-E API Errors

- Verify your API key is set: `echo %OPENAI_API_KEY%` (Windows)
- Check your OpenAI account has available credits
- The tool will automatically fall back to placeholder mode if DALL-E fails

### Video Codec Issues

If you encounter codec errors, ensure ffmpeg is installed:

**Windows:**
- Download from: https://www.gyan.dev/ffmpeg/builds/
- Add to PATH environment variable

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

## Advanced Usage

### Custom Styling

Modify `arch_video/generator.py` to customize:
- Title card colors and fonts
- Placeholder image color palettes
- Text overlay styling
- DALL-E prompt templates

### Extending the Tool

The modular architecture allows easy extensions:

- **Custom parsers**: Add support for other input formats
- **Image sources**: Integrate additional AI image generators
- **Effects**: Add transitions, animations, or filters
- **Audio**: Implement text-to-speech narration

## Performance Notes

- **Placeholder mode**: Very fast, ~1-2 minutes for typical project
- **DALL-E mode**: Slower due to API calls, ~30-60 seconds per section
- **4K rendering**: Significantly slower than 1080p

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please feel free to submit issues or pull requests.

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

## Credits

Built with:
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing
- [Pillow](https://python-pillow.org/) - Image processing
- [OpenAI API](https://platform.openai.com/) - DALL-E integration
