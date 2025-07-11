# MIDI Processing and Chord Extraction Project

A comprehensive Python project for processing MIDI files, extracting chord information, and seamless REAPER DAW integration. Features complete Chordify.net integration for instant song-to-arrangement workflow.

## 🌟 Major Features

### 🎵 Core MIDI Processing

- 🎹 MIDI file processing with `mido` and `pretty-midi`
- 🎵 Chord extraction from audio and MIDI files using `chord-extractor`
- 📊 Music analysis and visualization with `matplotlib`
- 🔢 Numerical computations with `numpy`

### 🎛️ REAPER DAW Integration

- 📜 ReaScript generation and automation
- 🎨 Project templates and workflow setup
- 🎧 Track routing and effect configuration
- 📋 Chord marker placement and arrangement tools

### 🌐 **NEW: Chordify.net Integration**

- 🔍 **Search Chordify.net** directly from REAPER
- 📥 **Automatic MIDI download** from song database
- ⚡ **One-click workflow**: Search → Download → Analyze → REAPER Project
- 🖥️ **ImGui panel interface** integrated with REAPER toolkit
- 📁 **Smart file management** and organization

## Requirements

- **Python Version**: 3.6 ≤ version < 3.9 (required for chord-extractor compatibility)
- **Operating System**: macOS, Linux, Windows

## Installation

### 1. Python Environment Setup

This project requires Python 3.8 (or any version between 3.6-3.9). If you don't have the correct Python version:

```bash
# Install pyenv (if not already installed)
curl https://pyenv.run | bash

# Add to your shell configuration (~/.zshrc for zsh, ~/.bashrc for bash)
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Restart your shell or source the configuration
source ~/.zshrc  # or ~/.bashrc

# Install Python 3.8
pyenv install 3.8.19

# Create virtual environment
pyenv virtualenv 3.8.19 chord-extractor-env

# Set local environment for this project
pyenv local chord-extractor-env
```

### 2. Package Installation

```bash
# Install all required packages
pip install -r requirements.txt
```

## Dependencies

- `chord-extractor==0.1.2` - Chord extraction from audio/MIDI
- `mido>=1.2.0` - MIDI file I/O and manipulation
- `pretty-midi>=0.2.8` - MIDI analysis and processing
- `music21>=5.0.0` - Music analysis toolkit
- `numpy>=1.16.0` - Numerical computations
- `matplotlib>=3.0.0` - Plotting and visualization

## Usage

### Basic Usage

```bash
# Run the main script
python main.py
```

### In VS Code

1. Open the project in VS Code
2. Select the correct Python interpreter: `Cmd+Shift+P` → "Python: Select Interpreter"
3. Choose the pyenv environment: `/Users/[username]/.pyenv/versions/chord-extractor-env/bin/python`
4. Run the script with F5 or use the terminal

### REAPER Integration

```bash
# Run the complete REAPER workflow demo
python reaper_workflow_demo.py

# Or use the integration module directly
python reaper_integration.py
```

**REAPER Integration Features:**

- 📜 **ReaScript Generation**: Automatically create Lua scripts for REAPER
- 🏗️ **Project Templates**: Pre-configured REAPER projects for chord analysis
- 🎵 **MIDI Export**: Convert processed MIDI for REAPER import
- 🎯 **Chord Markers**: Automatic chord progression markers in timeline
- 🔄 **Workflow Automation**: Complete analysis-to-DAW pipeline

## Project Structure

```text
python2/
├── main.py                      # Main application script
├── reaper_integration.py        # REAPER DAW integration module
├── reaper_workflow_demo.py      # Complete REAPER workflow demonstration
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── sample_chord.mid             # Generated sample MIDI file
├── temp_reaper_files/           # Temporary files for REAPER integration
├── .github/
│   └── copilot-instructions.md  # Copilot configuration
└── .vscode/
    └── tasks.json               # VS Code tasks
```

## 🌐 Chordify.net Integration

## 🌐 Chordify.net Integration

### 🔑 **How It Actually Works**

Since **Chordify.net does not provide a public API**, this integration uses a different approach:

#### � **Web Scraping Approach**

- ✅ **Search Chordify.net** - Scrape search results from web pages  
- ✅ **Extract chord progressions** - Parse chord data from song pages
- ✅ **Generate MIDI from chords** - Create MIDI files from scraped progression data
- ✅ **REAPER integration** - Full project creation with generated files
- 📊 **Rate limiting** - Respectful scraping with delays

#### � **What This Means for Users**

**All Chordify users (free or paid) get the same integration features:**

- ✅ **Search any song** on Chordify.net
- ✅ **View chord progressions** from the website  
- ✅ **Generate realistic MIDI** from chord data
- ✅ **Create REAPER projects** with chord markers and arrangements
- ✅ **No subscription required** - works with free Chordify access

> **🎯 Result**: You get a complete song-to-REAPER workflow by leveraging Chordify's chord analysis and generating high-quality MIDI files from that data.

### ⚡ Quick Start

```bash
# Interactive setup (configure scraping vs examples)
python chordify_setup.py

# Run the complete integration demo
python chordify_complete_demo.py

# Or run interactively
python chordify_complete_demo.py --interactive
```

### 🔍 Search and Generate MIDI

```python
from chordify_integration import ChordifyIntegration

# Initialize integration
chordify = ChordifyIntegration()

# Search for songs (tries web scraping, falls back to examples)
results = chordify.search_songs("Wonderwall Oasis")



### 🎼 Workflow Features

1. **Chord Progression Analysis**: Extracts or generates chord progressions
2. **MIDI Generation**: Creates realistic MIDI files from chord data
3. **Project Template Generation**: Creates ready-to-use REAPER projects

## Features Demo

The `main.py` script demonstrates:

1. **Environment Verification**: Checks Python version compatibility
2. **Library Testing**: Verifies all dependencies are properly installed
3. **MIDI Creation**: Generates a sample C major chord MIDI file
4. **Chord Processing**: Ready for chord extraction from audio/MIDI files

## Troubleshooting

### chord-extractor Installation Issues

If you encounter issues installing `chord-extractor==0.1.2`:

1. Verify Python version: `python --version` (should be 3.6-3.9)
2. Upgrade pip: `pip install --upgrade pip`
3. Install from source if needed


### VAMP Plugin Warning

You may see a warning about VAMP_PATH. To fully use Chordino features:

1. Download the [VAMP Plugin Pack](https://code.soundsoftware.ac.uk/projects/vamp-plugin-pack)
2. Install and set the VAMP_PATH environment variable

## Contributing

1. Ensure you're using Python 3.6-3.9
2. Install dependencies with `pip install -r requirements.txt`
3. Follow PEP 8 style guidelines
4. Add type hints where appropriate
5. Include tests for new features

## License

This project is open source. Please check individual package licenses for dependencies.

---

🎵 **Ready for MIDI processing, music analysis, ** 🎵
