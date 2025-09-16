#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TfidfLangID - TF-IDF based language detection model.

This module provides a simple interface for language detection using
a pre-trained TF-IDF model with character n-grams.
"""

import os
import sys
import unicodedata
from typing import List, Dict, Optional

try:
    import joblib
except ImportError:
    joblib = None
    import pickle

try:
    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import LinearSVC
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import LabelEncoder
    from sklearn.calibration import CalibratedClassifierCV
    import numpy as np
except ImportError as e:
    raise ImportError(
        "scikit-learn and numpy are required for language detection.\n"
        "Install with: pip install scikit-learn numpy joblib"
    ) from e


def _softmax(x: "np.ndarray") -> "np.ndarray":
    """Apply softmax normalization to decision function outputs."""
    x = x - x.max(axis=1, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=1, keepdims=True)


class TfidfLangID:
    """
    TF-IDF based language identification model.
    
    This class provides methods to load a pre-trained model and predict
    the language of input text.
    """
    
    def __init__(
        self,
        ngram_min: int = 1,
        ngram_max: int = 5,
        classifier: str = 'svm',
        C: float = 1.0,
        max_features: Optional[int] = None,
        min_df: int = 1,
        lowercase: bool = True,
        sublinear_tf: bool = True,
        calibrate: bool = False,
        calibration_method: str = 'sigmoid',
        calibration_cv: int = 3,
    ) -> None:
        """
        Initialize TfidfLangID model.
        
        Args:
            ngram_min: Minimum character n-gram size
            ngram_max: Maximum character n-gram size
            classifier: Classifier type ('svm' or 'logreg')
            C: Regularization strength
            max_features: Maximum number of features
            min_df: Minimum document frequency
            lowercase: Convert to lowercase
            sublinear_tf: Use sublinear TF scaling
            calibrate: Use probability calibration
            calibration_method: Calibration method ('sigmoid' or 'isotonic')
            calibration_cv: Number of CV folds for calibration
        """
        self.ngram_min = ngram_min
        self.ngram_max = ngram_max
        self.classifier_name = classifier
        self.C = C
        self.max_features = max_features
        self.min_df = min_df
        self.lowercase = lowercase
        self.sublinear_tf = sublinear_tf
        self.calibrate = calibrate
        self.calibration_method = calibration_method
        self.calibration_cv = calibration_cv

        self.pipeline: Optional[Pipeline] = None
        self.le: Optional[LabelEncoder] = None

    @staticmethod
    def _normalize(text: str) -> str:
        """Normalize Unicode text."""
        return unicodedata.normalize('NFKC', text)

    def predict(self, texts: List[str], top_k: int = 3) -> List[Dict]:
        """
        Predict language for a list of texts.
        
        Args:
            texts: List of input texts
            top_k: Number of top predictions to return
            
        Returns:
            List of dictionaries with language predictions
        """
        if not self.pipeline or not self.le:
            raise RuntimeError('Model is not loaded. Call load() first.')
            
        Xn = [self._normalize(t) for t in texts]
        clf = self.pipeline.named_steps['clf']
        
        # Try probability prediction; fallback to decision function + softmax
        has_proba = hasattr(clf, 'predict_proba')
        if has_proba:
            proba = clf.predict_proba(self.pipeline.named_steps['tfidf'].transform(Xn))
        else:
            df = clf.decision_function(self.pipeline.named_steps['tfidf'].transform(Xn))
            if df.ndim == 1:
                df = df.reshape(-1, 1)
            proba = _softmax(df)

        results: List[Dict] = []
        for row in proba:
            idxs = row.argsort()[::-1]
            langs = self.le.inverse_transform(idxs)
            confs = row[idxs]
            results.append({
                'language': langs[0],
                'confidence': float(confs[0]),
                'top_k': list(zip(langs[:top_k].tolist(), [float(c) for c in confs[:top_k]]))
            })
        return results

    def predict_one(self, text: str, top_k: int = 3) -> Dict:
        """
        Predict language for a single text.
        
        Args:
            text: Input text
            top_k: Number of top predictions to return
            
        Returns:
            Dictionary with language prediction
        """
        return self.predict([text], top_k=top_k)[0]

    def load(self, model_path: str) -> "TfidfLangID":
        """
        Load a pre-trained model from file.
        
        Args:
            model_path: Path to the model file
            
        Returns:
            Self for method chaining
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
            
        if joblib is not None:
            payload = joblib.load(model_path)
        else:
            with open(model_path, 'rb') as f:
                payload = pickle.load(f)

        # Update instance attributes
        self.ngram_min = payload['ngram_min']
        self.ngram_max = payload['ngram_max']
        self.classifier_name = payload['classifier_name']
        self.C = payload['C']
        self.max_features = payload['max_features']
        self.min_df = payload['min_df']
        self.lowercase = payload['lowercase']
        self.sublinear_tf = payload['sublinear_tf']
        
        self.le = payload['le']
        self.pipeline = payload['pipeline']
        
        return self

    @classmethod
    def load_from_package(cls, model_name: str = "tfidf_langid.joblib") -> "TfidfLangID":
        """
        Load model from the package's model directory, or from env override.
        
        Args:
            model_name: Name of the model file
            
        Returns:
            Loaded TfidfLangID instance
        """
        # Resolve default packaged path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        default_path = os.path.join(current_dir, 'model', model_name)

        # Allow overriding via environment variable if packaged model isn't present
        env_path = os.environ.get('MYLANGDETECT_MODEL_PATH')
        if os.path.exists(default_path):
            model_path = default_path
        elif env_path and os.path.exists(env_path):
            model_path = env_path
        else:
            hint = (
                f"Model file not found. Expected at '{default_path}'. "
                f"You can set environment variable MYLANGDETECT_MODEL_PATH to point to '{model_name}'."
            )
            raise FileNotFoundError(hint)

        instance = cls()
        return instance.load(model_path)
