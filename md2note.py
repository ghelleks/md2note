#!/usr/bin/env python3
"""
Main entry point for the Markdown to Apple Notes converter.
"""
import argparse
import logging
import sys
from src.app import MD2Note

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Markdown files to Apple Notes"
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Source directory containing Markdown files"
    )
    parser.add_argument(
        "--clean",
        help="Directory to move processed files to (default: source/clean)"
    )
    
    # Folder organization options (mutually exclusive)
    folder_group = parser.add_mutually_exclusive_group()
    folder_group.add_argument(
        "--folder",
        help="Folder name to place notes in Apple Notes"
    )
    folder_group.add_argument(
        "--auto-folder",
        action="store_true",
        help="Auto-generate unique folder name for this import batch"
    )
    
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    try:
        app = MD2Note(
            source_dir=args.source, 
            clean_dir=args.clean,
            folder=args.folder,
            auto_folder=args.auto_folder
        )
        app.run()
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 