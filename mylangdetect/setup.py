#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for MyLangDetect package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "MyLangDetect - Simple language detection library"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return [
        'scikit-learn>=1.0.0',
        'numpy>=1.20.0',
        'joblib>=1.0.0'
    ]

setup(
    name="mylangdetect",
    version="1.0.0",
    author="MyLangDetect Team",
    author_email="info@mylangdetect.com",
    description="Simple language detection library using TF-IDF and character n-grams",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mylangdetect",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    include_package_data=True,
    package_data={
        'mylangdetect': ['model/*.joblib'],
    },
    entry_points={
        'console_scripts': [
            'mylang-detect=mylangdetect.cli:main',
        ]
    },
    keywords="language detection, nlp, machine learning, tf-idf, text analysis",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/mylangdetect/issues",
        "Source": "https://github.com/yourusername/mylangdetect",
        "Documentation": "https://github.com/yourusername/mylangdetect#readme",
    },
)
