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
        description="Convert Markdown files to Apple Notes or Google Docs"
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
    parser.add_argument(
        "--export-to",
        choices=["apple_notes", "google_docs"],
        default="apple_notes",
        help="Export destination: apple_notes or google_docs (default: apple_notes)"
    )
    parser.add_argument(
        "--gdocs-folder",
        help="Google Drive folder name for Google Docs export (optional)"
    )
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    try:
        app = MD2Note(
            source_dir=args.source,
            clean_dir=args.clean,
            export_type=args.export_to,
            gdocs_folder=args.gdocs_folder
        )
        app.run()
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
