"""
ReaScript integration helper for Reaper DAW.

Provides functions to launch and communicate with the MIDI Chord Progression panel.
"""
from typing import Any

try:
    import reapy
except ImportError:
    reapy = None


def show_chord_progression_panel() -> None:
    """
    Launch the ReaScript UI panel for MIDI chord progression.
    """
    if reapy is None:
        raise RuntimeError(
            "reapy library not installed. Please install with `pip install reapy`."
        )
    # TODO: implement panel launch logic using reapy or custom IPC
    pass


if __name__ == "__main__":
    show_chord_progression_panel()
