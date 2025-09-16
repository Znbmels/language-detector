#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MyLangDetect - Simple language detection library.

This package provides a simple interface for detecting the language of text
using a pre-trained TF-IDF model with character n-grams.

Example:
    from mylangdetect import detect_language
    
    result = detect_language("Hello world")
    print(result)  # "EN"
    
    # With confidence scores
    from mylangdetect import TfidfLangID
    detector = TfidfLangID.load_from_package()
    result = detector.predict_one("Hello world")
    print(result)  # {"language": "EN", "confidence": 0.95, ...}
"""

import os
from typing import Dict, Optional

from .detector import TfidfLangID

# Global detector instance for simple API
_detector: Optional[TfidfLangID] = None


def _get_detector() -> TfidfLangID:
    """Get or create the global detector instance."""
    global _detector
    if _detector is None:
        _detector = TfidfLangID.load_from_package()
    return _detector


def detect_language(text: str, top_k: int = 1) -> str:
    """
    Detect the language of the given text.
    
    This is a simple function that returns just the language code.
    For more detailed results (confidence scores, top-k predictions),
    use the TfidfLangID class directly.
    
    Args:
        text: Input text to analyze
        top_k: Number of top predictions to consider (default: 1)
        
    Returns:
        Language code (e.g., "EN", "RU", "KK") of the most likely language
        
    Example:
        >>> detect_language("Hello world")
        "EN"
        >>> detect_language("Привет мир")
        "RU"
        >>> detect_language("Сәлем дүние")
        "KK"
    """
    detector = _get_detector()
    result = detector.predict_one(text, top_k=top_k)
    return result['language']


def detect_language_detailed(text: str, top_k: int = 3) -> Dict:
    """
    Detect the language of the given text with detailed results.
    
    Args:
        text: Input text to analyze
        top_k: Number of top predictions to return
        
    Returns:
        Dictionary containing:
        - language: Most likely language code
        - confidence: Confidence score (0.0 to 1.0)
        - top_k: List of (language, confidence) tuples
        
    Example:
        >>> detect_language_detailed("Hello world")
        {
            "language": "EN",
            "confidence": 0.95,
            "top_k": [("EN", 0.95), ("FR", 0.03), ("DE", 0.02)]
        }
    """
    detector = _get_detector()
    return detector.predict_one(text, top_k=top_k)


def get_supported_languages() -> list:
    """
    Get list of supported language codes.
    
    Returns:
        List of supported language codes (e.g., ["EN", "RU", "KK", ...])
    """
    detector = _get_detector()
    if detector.le is None:
        raise RuntimeError("Model not loaded properly")
    return sorted(detector.le.classes_.tolist())


# Version information
__version__ = "1.0.0"
__author__ = "MyLangDetect Team"
__email__ = "info@mylangdetect.com"

# Public API
__all__ = [
    'TfidfLangID',
    'detect_language',
    'detect_language_detailed', 
    'get_supported_languages',
    '__version__',
    '__author__',
    '__email__'
]
