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
        # Get intervals from root
        intervals = [(note - notes[0]) % 12 for note in notes[1:]]
        
        # Basic chord recognition
        if 4 in intervals and 7 in intervals:  # Major third + perfect fifth
            if 10 in intervals:  # Minor seventh
                return root_name + "7"
            elif 11 in intervals:  # Major seventh
                return root_name + "maj7"
            else:
                return root_name  # Major
        elif 3 in intervals and 7 in intervals:  # Minor third + perfect fifth
            if 10 in intervals:  # Minor seventh
                return root_name + "m7"
            else:
                return root_name + "m"  # Minor
        elif 4 in intervals and 6 in intervals:  # Major third + tritone
            return root_name + "7"  # Dominant 7 (simplified)
        else:
            # Complex chord - just show root with number of notes
            return f"{root_name}({len(notes)})"
    
    return root_name

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

def main():
    """Main CLI interface for dataset operations."""
    parser = argparse.ArgumentParser(description='Enhanced Chord Dataset Browser')
    parser.add_argument('command', choices=['browse', 'analyze', 'generate', 'stats'], 
                       help='Command to execute')
    parser.add_argument('--page', type=int, default=1, help='Page number for browsing')
    parser.add_argument('--items', type=int, default=10, help='Items per page')
    parser.add_argument('--search', type=str, default='', help='Search query')
    parser.add_argument('--min-length', type=int, default=0, help='Minimum progression length')
    parser.add_argument('--progression-id', type=int, help='Progression ID for analysis')
    parser.add_argument('--template-id', type=int, help='Template progression ID for generation')
    
    args = parser.parse_args()
    
    # Load dataset
    dataset_path = "/Users/Matthew/git/BiMMuDa/Tegridy-MIDI-Dataset/Chords-Progressions/pitches_chords_progressions_5_3_15.pickle"
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

if __name__ == "__main__":
    main()
