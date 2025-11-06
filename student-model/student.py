#!/usr/bin/env python3
"""
student.py - Student Model CLI Tool
Tracks conceptual knowledge mastery across learning sessions.
"""

import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Default data file location
DATA_FILE = Path.home() / "student_model.json"

# JSON Schema for student model
SCHEMA_VERSION = "1.0"

def get_default_model() -> Dict[str, Any]:
    """Return the default/empty student model structure."""
    return {
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "student_profile": ""
        },
        "concepts": {},
        "sessions": []
    }

def validate_model(model: Dict[str, Any]) -> bool:
    """Validate that model has required structure."""
    required_keys = ["metadata", "concepts", "sessions"]
    if not all(key in model for key in required_keys):
        return False
    
    required_metadata = ["created", "last_updated"]
    if not all(key in model["metadata"] for key in required_metadata):
        return False
    
    return True

def load_model() -> Dict[str, Any]:
    """
    Load the student model from disk with error handling.
    Creates a new model if file doesn't exist.
    """
    if not DATA_FILE.exists():
        print(f"ℹ️  No model found at {DATA_FILE}")
        print("   Run 'python student.py init' to create one")
        return get_default_model()
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            model = json.load(f)
        
        # Validate structure
        if not validate_model(model):
            print(f"⚠️  Model at {DATA_FILE} has invalid structure")
            
            # Check for backup
            backup = DATA_FILE.with_suffix('.json.backup')
            if backup.exists():
                print(f"   Attempting to restore from backup...")
                with open(backup, 'r', encoding='utf-8') as f:
                    model = json.load(f)
                if validate_model(model):
                    print("✅ Restored from backup successfully")
                    save_model(model)  # Save the good backup as main file
                    return model
            
            print("   Creating new model")
            return get_default_model()
        
        return model
    
    except json.JSONDecodeError as e:
        print(f"❌ Error: Corrupt JSON in {DATA_FILE}")
        print(f"   {str(e)}")
        
        # Try backup
        backup = DATA_FILE.with_suffix('.json.backup')
        if backup.exists():
            print(f"   Attempting to restore from backup...")
            try:
                with open(backup, 'r', encoding='utf-8') as f:
                    model = json.load(f)
                if validate_model(model):
                    print("✅ Restored from backup successfully")
                    save_model(model)
                    return model
            except:
                pass
        
        print("   Creating new model")
        return get_default_model()
    
    except Exception as e:
        print(f"❌ Unexpected error loading model: {str(e)}")
        return get_default_model()


def save_model(model: Dict[str, Any]) -> bool:
    """
    Save model to disk with atomic writes and backup.
    Returns True on success, False on failure.
    """
    try:
        # Validate before saving
        if not validate_model(model):
            print("❌ Error: Model structure is invalid, refusing to save")
            return False
        
        # Update timestamp
        model["metadata"]["last_updated"] = datetime.now().isoformat()
        
        # Backup existing file (before any write operations)
        if DATA_FILE.exists():
            backup = DATA_FILE.with_suffix('.json.backup')
            shutil.copy(DATA_FILE, backup)
        
        # Write to temp file first (atomic operation)
        temp = DATA_FILE.with_suffix('.json.tmp')
        with open(temp, 'w', encoding='utf-8') as f:
            json.dump(model, f, indent=2, ensure_ascii=False)
        
        # Atomic rename
        temp.replace(DATA_FILE)
        
        # Create backup after successful save (if it doesn't exist yet)
        backup = DATA_FILE.with_suffix('.json.backup')
        if not backup.exists():
            shutil.copy(DATA_FILE, backup)
        
        return True
    
    except Exception as e:
        print(f"❌ Error saving model: {str(e)}")
        return False

def initialize_model(profile: str = "") -> Dict[str, Any]:
    """
    Create a new student model and save it to disk.
    """
    if DATA_FILE.exists():
        response = input(f"⚠️  Model already exists at {DATA_FILE}. Overwrite? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Cancelled.")
            return load_model()
    
    model = get_default_model()
    if profile:
        model["metadata"]["student_profile"] = profile
    
    if save_model(model):
        print(f"✅ Initialized new student model at {DATA_FILE}")
        print(f"   Created: {model['metadata']['created']}")
        if profile:
            print(f"   Profile: {profile}")
    else:
        print("❌ Failed to initialize model")
    
    return model

def find_concept(model: Dict[str, Any], concept_name: str) -> Optional[str]:
    """
    Find a concept by name (case-insensitive).
    Returns the exact key from the model, or None if not found.
    """
    concept_lower = concept_name.lower()
    for key in model["concepts"].keys():
        if key.lower() == concept_lower:
            return key
    return None

# CLI Commands

def cmd_init(args):
    """Initialize a new student model."""
    initialize_model(args.profile if hasattr(args, 'profile') else "")

def cmd_info(args):
    """Show model metadata and statistics."""
    model = load_model()
    
    print("📊 Student Model Information")
    print(f"   Location:      {DATA_FILE}")
    print(f"   Created:       {model['metadata']['created'].split('T')[0]}")
    print(f"   Last Updated:  {model['metadata']['last_updated'].split('T')[0]}")
    
    if model['metadata'].get('student_profile'):
        print(f"   Profile:       {model['metadata']['student_profile']}")
    
    print(f"\n   Total Concepts: {len(model['concepts'])}")
    print(f"   Total Sessions: {len(model['sessions'])}")
    
    if model['concepts']:
        masteries = [c.get('mastery', 0) for c in model['concepts'].values()]
        avg_mastery = sum(masteries) / len(masteries)
        print(f"   Avg Mastery:    {avg_mastery:.1f}%")


"""
Phase 2 additions to student.py - Read Operations
Add these functions and command handlers to your existing student.py
"""

# Add these command handler functions after cmd_info()

def cmd_list(args):
    """List all concepts with summary info."""
    model = load_model()
    
    if not model['concepts']:
        print("📚 No concepts tracked yet.")
        print("   Add your first concept with: python student.py add \"Concept Name\" 50 medium")
        return
    
    print(f"📚 Tracked Concepts ({len(model['concepts'])} total)\n")
    
    # Sort by mastery (descending) for better overview
    sorted_concepts = sorted(
        model['concepts'].items(),
        key=lambda x: x[1].get('mastery', 0),
        reverse=True
    )
    
    for name, data in sorted_concepts:
        mastery = data.get('mastery', 0)
        confidence = data.get('confidence', 'unknown')
        last_reviewed = data.get('last_reviewed', 'never')
        
        # Format last reviewed date
        if last_reviewed != 'never':
            last_reviewed = last_reviewed.split('T')[0]
        
        # Mastery indicator
        if mastery >= 80:
            indicator = "✅"
        elif mastery >= 60:
            indicator = "🟡"
        elif mastery >= 40:
            indicator = "🟠"
        else:
            indicator = "🔴"
        
        # Confidence indicator
        conf_display = confidence
        if confidence == "low":
            conf_display = "⚠️  low"
        
        print(f"{indicator} {name:<40} {mastery:>3}%  {conf_display:<12} (last: {last_reviewed})")
    
    print(f"\nLegend: ✅ 80%+  🟡 60-79%  🟠 40-59%  🔴 <40%")


def cmd_show(args):
    """Show detailed information about a specific concept."""
    model = load_model()
    concept_key = find_concept(model, args.concept_name)
    
    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        print(f"   Run 'python student.py list' to see tracked concepts.")
        return
    
    concept = model['concepts'][concept_key]
    
    print(f"📊 Concept: {concept_key}")
    print(f"   Mastery:          {concept.get('mastery', 'N/A')}%")
    print(f"   Confidence:       {concept.get('confidence', 'N/A')}")
    
    # Dates
    first = concept.get('first_encountered', 'N/A')
    last = concept.get('last_reviewed', 'N/A')
    if first != 'N/A':
        first = first.split('T')[0]
    if last != 'N/A':
        last = last.split('T')[0]
    
    print(f"   First Encountered: {first}")
    print(f"   Last Reviewed:     {last}")
    
    # Struggles
    struggles = concept.get('struggles', [])
    if struggles:
        print(f"   ⚠️  Struggles:")
        for struggle in struggles:
            print(f"      - {struggle}")
    
    # Breakthroughs
    breakthroughs = concept.get('breakthroughs', [])
    if breakthroughs:
        print(f"   💡 Breakthroughs:")
        for breakthrough in breakthroughs:
            print(f"      - {breakthrough}")
    
    # Related concepts
    related = concept.get('related_concepts', [])
    if related:
        print(f"   🔗 Related Concepts:")
        for rel_name in related:
            rel_key = find_concept(model, rel_name)
            if rel_key and rel_key in model['concepts']:
                rel_data = model['concepts'][rel_key]
                rel_mastery = rel_data.get('mastery', 0)
                rel_last = rel_data.get('last_reviewed', 'never')
                if rel_last != 'never':
                    rel_last = rel_last.split('T')[0]
                
                # Flag low mastery prerequisites
                if rel_mastery < 60:
                    print(f"      - {rel_name} (Mastery: {rel_mastery}%, Last: {rel_last}) ⚠️ LOW")
                else:
                    print(f"      - {rel_name} (Mastery: {rel_mastery}%, Last: {rel_last}) ✓")
            else:
                print(f"      - {rel_name} (not tracked)")


def cmd_related(args):
    """Show concepts related to a specific concept."""
    model = load_model()
    concept_key = find_concept(model, args.concept_name)
    
    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        return
    
    concept = model['concepts'][concept_key]
    related = concept.get('related_concepts', [])
    
    if not related:
        print(f"🔗 No related concepts tracked for '{concept_key}'")
        print(f"   Link concepts with: python student.py link \"{concept_key}\" \"Related Concept\"")
        return
    
    print(f"🔗 Concepts related to '{concept_key}':")
    
    for rel_name in related:
        rel_key = find_concept(model, rel_name)
        if rel_key and rel_key in model['concepts']:
            rel_data = model['concepts'][rel_key]
            rel_mastery = rel_data.get('mastery', 0)
            rel_confidence = rel_data.get('confidence', 'unknown')
            rel_last = rel_data.get('last_reviewed', 'never')
            
            if rel_last != 'never':
                rel_last = rel_last.split('T')[0]
            
            # Status indicator
            if rel_mastery < 60:
                status = "⚠️ LOW"
            else:
                status = "✓"
            
            print(f"   - {rel_name:<40} {rel_mastery:>3}%  {rel_confidence:<10}  (last: {rel_last}) {status}")
        else:
            print(f"   - {rel_name} (not tracked yet)")


# Update the main() function to add new subparsers:

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Student Model CLI - Track conceptual knowledge mastery',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    parser_init = subparsers.add_parser('init', help='Initialize a new student model')
    parser_init.add_argument('--profile', type=str, default='', 
                            help='Student profile description')
    
    # Info command
    parser_info = subparsers.add_parser('info', help='Show model information')
    
    # List command (NEW)
    parser_list = subparsers.add_parser('list', help='List all tracked concepts')
    
    # Show command (NEW)
    parser_show = subparsers.add_parser('show', help='Show detailed concept information')
    parser_show.add_argument('concept_name', type=str, help='Name of the concept to show')
    
    # Related command (NEW)
    parser_related = subparsers.add_parser('related', help='Show related concepts')
    parser_related.add_argument('concept_name', type=str, help='Name of the concept')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Route to command handlers
    if args.command == 'init':
        cmd_init(args)
    elif args.command == 'info':
        cmd_info(args)
    elif args.command == 'list':
        cmd_list(args)
    elif args.command == 'show':
        cmd_show(args)
    elif args.command == 'related':
        cmd_related(args)


if __name__ == '__main__':
    main()
