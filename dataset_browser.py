#!/usr/bin/env python3
"""
Enhanced Chord Dataset Browser and Generator
Interfaces with the BiMMuDa 1.2M+ chord progression dataset
"""

import sys
import os
import json
import pickle
import random
import argparse
from typing import List, Dict, Any, Optional

def load_chord_dataset(pickle_path: str) -> List[tuple]:
    """Load the chord progression dataset from pickle file."""
    try:
        with open(pickle_path, 'rb') as f:
            data = pickle.load(f)
        
        # Convert set to list if necessary
        if isinstance(data, set):
            data = list(data)
            
        print(f"✅ Loaded dataset with {len(data)} progressions")
        return data
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return []

def midi_notes_to_chord_name(notes_tuple):
    """Convert MIDI note numbers to chord name."""
    if not notes_tuple:
        return "Rest"

    # try using music21 for advanced chord recognition and full-symbol display
    try:
        from music21 import chord as m21chord
        from music21.harmony import chordSymbolFigureFromChord
        m21_chord = m21chord.Chord(notes_tuple)
        symbol = chordSymbolFigureFromChord(m21_chord)
        if symbol:
            return symbol
    except ImportError:
        # music21 not installed or outdated, fallback to basic logic
        pass
    except Exception:
        # any chord parsing errors, fallback
        pass

    notes = sorted(list(notes_tuple))
    
    # Convert MIDI numbers to note names
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    
    # Get the root (lowest note)
    root_note = notes[0] % 12
    root_name = note_names[root_note]
    
    # Simple chord quality detection based on intervals
    if len(notes) == 1:
        return root_name
    elif len(notes) == 2:
        interval = (notes[1] - notes[0]) % 12
        if interval == 7:
            return root_name + "5"  # Perfect fifth
        else:
            return root_name + "2"  # Generic interval
    elif len(notes) >= 3:
        # Get intervals from root (remove duplicates and sort)
        intervals = sorted(list(set([(note - notes[0]) % 12 for note in notes[1:]])))
        
        # Enhanced chord recognition
        has_maj3 = 4 in intervals   # Major third
        has_min3 = 3 in intervals   # Minor third
        has_p5 = 7 in intervals     # Perfect fifth
        has_dim5 = 6 in intervals   # Diminished fifth / tritone
        has_aug5 = 8 in intervals   # Augmented fifth
        has_min7 = 10 in intervals  # Minor seventh
        has_maj7 = 11 in intervals  # Major seventh
        has_9 = 2 in intervals      # 9th (same as 2nd)
        has_11 = 5 in intervals     # 11th (same as 4th)
        has_13 = 9 in intervals     # 13th (same as 6th)
        
        # Build chord name step by step
        chord_name = root_name
        
        # Determine basic quality (major/minor/diminished/augmented)
        if has_min3 and has_dim5:
            chord_name += "dim"
        elif has_min3:
            chord_name += "m"
        elif has_maj3 and has_aug5:
            chord_name += "aug"
        elif has_maj3 and has_p5:
            pass  # Major chord, no modifier needed
        elif has_maj3 and has_dim5:
            chord_name += "7"  # Dominant (tritone substitution)
        elif not has_maj3 and not has_min3:
            # No third, might be sus or quartal
            if has_11:  # 4th instead of 3rd
                chord_name += "sus4"
            elif has_9:  # 2nd instead of 3rd
                chord_name += "sus2"
        
        # Add 7th extensions
        if has_maj7:
            if "m" in chord_name:
                chord_name += "maj7"
            else:
                chord_name += "maj7"
        elif has_min7:
            chord_name += "7"
        
        # Add upper extensions (9th, 11th, 13th)
        extensions = []
        if has_13:
            extensions.append("13")
        elif has_11:
            extensions.append("11")
        elif has_9:
            extensions.append("9")
        
        if extensions:
            # Remove "7" if we're adding higher extensions
            if chord_name.endswith("7") and not chord_name.endswith("maj7"):
                chord_name = chord_name[:-1]
            chord_name += extensions[0]  # Use highest extension
        
        # Handle special cases where our analysis might be incomplete
        if len(intervals) > 5:  # Very complex chord
            return f"{chord_name}({len(notes)})"
        
        return chord_name
    
    return root_name

def midi_notes_to_note_names(notes_tuple):
    """Convert MIDI note numbers to readable note names with octaves."""
    if not notes_tuple:
        return []
    
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    result = []
    
    for midi_note in sorted(notes_tuple):
        octave = (midi_note // 12) - 1  # MIDI octave calculation
        note_name = note_names[midi_note % 12]
        result.append(f"{note_name}{octave}")
    
    return result

def get_chord_analysis(notes_tuple):
    """Get detailed chord analysis including name and constituent notes."""
    chord_name = midi_notes_to_chord_name(notes_tuple)
    note_names = midi_notes_to_note_names(notes_tuple)
    
    return {
        "chord_name": chord_name,
        "notes": note_names,
        "midi_notes": list(sorted(notes_tuple)) if notes_tuple else [],
        "note_count": len(notes_tuple) if notes_tuple else 0
    }

def convert_progression_to_chords(progression) -> List[str]:
    """Convert progression of MIDI note tuples to chord names."""
    chords = []
    for chord_tuple in progression:
        chord_name = midi_notes_to_chord_name(chord_tuple)
        chords.append(chord_name)
    return chords

def analyze_progression(progression) -> Dict[str, Any]:
    """Analyze a chord progression for complexity, patterns, etc."""
    chord_names = convert_progression_to_chords(progression)
    
    # Calculate complexity based on chord variety and note density
    note_counts = [len(chord_tuple) for chord_tuple in progression]
    avg_notes = sum(note_counts) / len(note_counts) if note_counts else 0
    unique_chords = len(set(chord_names))
    
    complexity_score = min(int(unique_chords * 1.5 + avg_notes), 10)
    
    analysis = {
        "chord_count": len(progression),
        "unique_chords": unique_chords,
        "chord_names": chord_names,
        "complexity_score": complexity_score,
        "average_notes_per_chord": round(avg_notes, 1),
        "note_counts": note_counts,
        "midi_data": progression  # Keep original MIDI data
    }
    
    # Simple pattern detection
    patterns = []
    if len(chord_names) >= 4:
        # Look for repeated chords
        if chord_names[0] == chord_names[-1]:
            patterns.append("Returns to root")
        
        # Look for common progressions (very basic)
        chord_str = " ".join(chord_names[:4])
        if "C F G" in chord_str:
            patterns.append("Contains I-IV-V pattern")
        if any(name.endswith("m") for name in chord_names):
            patterns.append("Contains minor chords")
    
    analysis["common_patterns"] = patterns
    
    return analysis

def browse_dataset(dataset: List[tuple], page: int = 1, items_per_page: int = 10,
                  search_query: str = "", min_length: int = 0) -> Dict[str, Any]:
    """Browse the dataset with pagination and filtering."""
    
    # Apply filters
    filtered_data = dataset
    
    if min_length > 0:
        filtered_data = [prog for prog in filtered_data if len(prog) >= min_length]
    
    # Simple search implementation (searches in converted chord names)
    if search_query:
        search_results = []
        for prog in filtered_data:
            chord_names = convert_progression_to_chords(prog)
            if any(search_query.lower() in chord.lower() for chord in chord_names):
                search_results.append(prog)
        filtered_data = search_results
    
    # Pagination
    total_items = len(filtered_data)
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_data = filtered_data[start_idx:end_idx]
    
    # Convert to displayable format
    progressions = []
    for i, prog in enumerate(page_data):
        analysis = analyze_progression(prog)
        progressions.append({
            "id": start_idx + i,
            "raw_progression": prog,
            "chords": analysis["chord_names"],
            "chord_count": analysis["chord_count"],
            "complexity": analysis["complexity_score"],
            "patterns": analysis["common_patterns"]
        })
    
    return {
        "progressions": progressions,
        "page": page,
        "items_per_page": items_per_page,
        "total_items": total_items,
        "total_pages": (total_items + items_per_page - 1) // items_per_page,
        "has_next": end_idx < total_items,
        "has_previous": page > 1
    }

def generate_similar_progression(template_progression: tuple, dataset: List[tuple]) -> tuple:
    """Generate a progression similar to the template."""
    template_length = len(template_progression)
    
    # Find progressions with similar length
    similar_length = [prog for prog in dataset if abs(len(prog) - template_length) <= 2]
    
    if similar_length:
        return random.choice(similar_length)
    else:
        return random.choice(dataset)

def export_lua_index(dataset: List[tuple], output_path: str, limit: int = 1000) -> None:
    """
    Export a Lua table of chord progressions for use in a ReaScript panel.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('-- Generated chord progression index\n')
            f.write('CHORD_INDEX = {\n')
            for i, prog in enumerate(dataset[:limit]):
                chords = convert_progression_to_chords(prog)
                # Get detailed analysis for each chord
                chord_details = []
                for chord_tuple in prog:
                    analysis = get_chord_analysis(chord_tuple)
                    chord_details.append(analysis)
                
                # escape quotes
                chord_list = ', '.join(f'"{c}"' for c in chords)
                
                # Build note details with proper escaping
                note_details_parts = []
                for cd in chord_details:
                    notes_str = ', '.join(f'"{n}"' for n in cd["notes"])
                    midi_str = ', '.join(str(m) for m in cd["midi_notes"])
                    detail_str = f'{{ name = "{cd["chord_name"]}", notes = {{ {notes_str} }}, midi = {{ {midi_str} }} }}'
                    note_details_parts.append(detail_str)
                note_details = ', '.join(note_details_parts)
                
                f.write(f'  {{ id = {i}, chords = {{ {chord_list} }}, details = {{ {note_details} }} }},\n')
            f.write('}\n')
        print(f"✅ Exported Lua index with {min(limit, len(dataset))} entries to {output_path}")
    except Exception as e:
        print(f"❌ Failed to export Lua index: {e}")

def main():
    """Main CLI interface for dataset operations."""
    parser = argparse.ArgumentParser(description='Enhanced Chord Dataset Browser')
    parser.add_argument('command', choices=['browse', 'analyze', 'generate', 'stats', 'export-lua-index'], 
                       help='Command to execute')
    parser.add_argument('--dataset-path', type=str,
                        help='Path to the chord progression pickle file (optional)')
    parser.add_argument('--page', type=int, default=1, help='Page number for browsing')
    parser.add_argument('--items', type=int, default=10, help='Items per page')
    parser.add_argument('--search', type=str, default='', help='Search query')
    parser.add_argument('--min-length', type=int, default=0, help='Minimum progression length')
    parser.add_argument('--progression-id', type=int, help='Progression ID for analysis')
    parser.add_argument('--template-id', type=int, help='Template progression ID for generation')
    parser.add_argument('--output-path', type=str, help='File path to write Lua index to')
    
    args = parser.parse_args()
    
    # Determine dataset path (fallback if not provided)
    dataset_path = args.dataset_path or (
        r'C:\Users\CraftAuto-Sales\Downloads\Tegridy-MIDI-Dataset-master\Tegridy-MIDI-Dataset-master\Chords-Progressions\pitches_chords_progressions_5_3_15.pickle'
    )
    print(f"🔍 Using dataset at: {dataset_path}")
    # If dataset file missing, try to reconstruct from split ZIP parts
    if not os.path.exists(dataset_path):
        zip_dir = os.path.dirname(dataset_path)
        # find part files ending .zip.001, .zip.002
        # gather all split zip parts (e.g. .zip.001, .zip.002, etc.)
        parts = [f for f in os.listdir(zip_dir)
                 if f.startswith('Pitches-Chords-Progressions') and '.zip.' in f]
        if parts:
            parts = sorted(parts, key=lambda x: int(x.split('.zip.')[-1]))
            combined_zip = os.path.join(zip_dir, 'combined_chords.zip')
            print(f"🛠 Reconstructing ZIP from parts: {parts}")
            with open(combined_zip, 'wb') as out:
                for part in parts:
                    with open(os.path.join(zip_dir, part), 'rb') as pf:
                        out.write(pf.read())
            # unzip archive
            try:
                import zipfile
                with zipfile.ZipFile(combined_zip, 'r') as z:
                    z.extractall(zip_dir)
                print(f"✅ Unzipped combined archive to {zip_dir}")
            except Exception as uz:
                print(f"❌ Failed to unzip archive: {uz}")
            finally:
                os.remove(combined_zip)
    dataset = load_chord_dataset(dataset_path)
    
    if not dataset:
        print("❌ Failed to load dataset")
        return
    
    if args.command == 'browse':
        result = browse_dataset(dataset, args.page, args.items, args.search, args.min_length)
        print(json.dumps(result, indent=2))
    
    elif args.command == 'stats':
        total = len(dataset)
        lengths = [len(prog) for prog in dataset]
        avg_length = sum(lengths) / len(lengths)
        
        stats = {
            "total_progressions": total,
            "average_length": round(avg_length, 2),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "dataset_loaded": True
        }
        print(json.dumps(stats, indent=2))
    
    elif args.command == 'analyze' and args.progression_id is not None:
        if 0 <= args.progression_id < len(dataset):
            progression = dataset[args.progression_id]
            analysis = analyze_progression(progression)
            print(json.dumps(analysis, indent=2))
        else:
            print(f"❌ Invalid progression ID: {args.progression_id}")
    
    elif args.command == 'generate':
        if args.template_id is not None and 0 <= args.template_id < len(dataset):
            template = dataset[args.template_id]
            new_progression = generate_similar_progression(template, dataset)
        else:
            new_progression = random.choice(dataset)
        
        analysis = analyze_progression(new_progression)
        result = {
            "generated_progression": new_progression,
            "analysis": analysis
        }
        print(json.dumps(result, indent=2))
    
    elif args.command == 'export-lua-index':
        output = args.output_path or 'chord_dataset_index.lua'
        export_lua_index(dataset, output)

if __name__ == "__main__":
    main()
