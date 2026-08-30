"""
Chapter 10: Workflows — Minimal Example

See the shared framework modules for the implementation:
  src/agentic_patterns/workflows/

Run:
    python book-code/ch10-open-source-models/minimal/main.py
"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../src"))

from agentic_patterns.utils.logging.logger import get_logger
logger = get_logger(__name__)

if __name__ == "__main__":
    print(f"Chapter 10 — workflows: configure .env then see README.md for usage.")
