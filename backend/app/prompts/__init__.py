"""
backend/app/prompts/__init__.py
==============================
Autonomous prompt selection system for the phone booth.
"""

from .registry import prompt_registry, PromptTemplate

__all__ = ["prompt_registry", "PromptTemplate"]

