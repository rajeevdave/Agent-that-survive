"""
Chapter 03: Model-Selection — Minimal Example

See the shared framework modules for the implementation:
  src/agentic_patterns/model_selection/

Run:
    python book-code/ch03-isolation-problem/minimal/main.py
"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../src"))

from agentic_patterns.utils.logging.logger import get_logger
logger = get_logger(__name__)

if __name__ == "__main__":
    print(f"Chapter 03 — model-selection: configure .env then see README.md for usage.")
