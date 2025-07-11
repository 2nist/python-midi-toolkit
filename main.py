"""
MIDI Processing and Chord Extraction Project

This project provides tools for processing MIDI files and extracting chord information.
Requires Python version >= 3.6 and < 3.9 for chord-extractor compatibility.
"""

import sys
import mido
import pretty_midi
import numpy as np
try:
    from chord_extractor.extractors import Chordino
    CHORD_EXTRACTOR_AVAILABLE = True
except ImportError:
    print("Warning: chord_extractor not available")
    CHORD_EXTRACTOR_AVAILABLE = False

def main():
    """Main function demonstrating chord extraction from MIDI."""
    print("MIDI Processing and Chord Extraction Tool")
    print(f"Python version: {sys.version}")
    print(f"Running on Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check if we meet the requirements
    if sys.version_info >= (3, 6) and sys.version_info < (3, 9):
        print("✅ Python version compatible with chord-extractor")
    else:
        print("❌ Python version not compatible with chord-extractor (requires >=3.6,<3.9)")
    
    if CHORD_EXTRACTOR_AVAILABLE:
        print("✅ chord-extractor is available")
        print("✅ Ready for chord extraction from audio/MIDI files!")
    else:
        print("❌ chord-extractor not available")
    
    print("✅ mido library loaded for MIDI processing")
    print("✅ pretty-midi library loaded for MIDI analysis")
    print("✅ numpy loaded for numerical computations")
    
    print("\n🎵 Ready for MIDI processing and analysis!")

def create_sample_midi():
    """Create a simple MIDI file for testing."""
    # Create a simple C major chord progression
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # C major chord (C, E, G)
    track.append(mido.Message('program_change', program=0, time=0))
    track.append(mido.Message('note_on', channel=0, note=60, velocity=64, time=0))  # C
    track.append(mido.Message('note_on', channel=0, note=64, velocity=64, time=0))  # E
    track.append(mido.Message('note_on', channel=0, note=67, velocity=64, time=0))  # G
    track.append(mido.Message('note_off', channel=0, note=60, velocity=64, time=480))
    track.append(mido.Message('note_off', channel=0, note=64, velocity=64, time=0))
    track.append(mido.Message('note_off', channel=0, note=67, velocity=64, time=0))
    
    return mid

if __name__ == "__main__":
    main()
    
    # Demonstrate MIDI creation
    print("\n🎹 Creating sample MIDI file...")
    sample_midi = create_sample_midi()
    sample_midi.save('/Users/Matthew/git/python2/sample_chord.mid')
    print("✅ Sample MIDI file saved as 'sample_chord.mid'")
