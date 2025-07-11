<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Copilot Instructions for MIDI Processing Project

This is a Python project focused on MIDI processing and chord extraction. 

## Key Requirements:
- **Python Version**: Must use Python >= 3.6 and < 3.9 for chord-extractor compatibility
- **Main Libraries**: chord-extractor, mido, pretty-midi, music21
- **Purpose**: MIDI file processing, chord extraction, music analysis, and REAPER DAW integration

## Code Guidelines:
- Use type hints where appropriate
- Follow PEP 8 style guidelines  
- Include docstrings for functions and classes
- Handle MIDI file errors gracefully
- Use virtual environments for dependency management
- Consider REAPER workflow compatibility when designing features

## Common Tasks:
- Loading and processing MIDI files
- Extracting chord progressions from audio/MIDI
- Converting between different music representations
- Analyzing musical patterns and structures
- Generating ReaScript files for REAPER automation
- Creating REAPER project templates
- Exporting MIDI data for DAW integration
