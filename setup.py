"""
JurisRank: Advanced Legal AI Platform
=====================================

A revolutionary legal AI platform that democratizes access to jurisprudential
analysis through cutting-edge artificial intelligence and machine learning.

Copyright (c) 2025 Ignacio Adrián Lerer
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    """Read README.md file for long description."""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Advanced Legal AI Platform for jurisprudential analysis"

# Read requirements
def read_requirements():
    """Read requirements.txt file."""
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f 
                   if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return [
            "requests>=2.31.0",
            "pandas>=2.0.0", 
            "numpy>=1.24.0",
            "nltk>=3.8.1",
            "scikit-learn>=1.3.0",
            "pydantic>=2.0.0"
        ]

setup(
    name="jurisrank",
    version="1.0.0",
    author="Ignacio Adrián Lerer",
    author_email="contact@jurisrank.io",
    description="Advanced Legal AI Platform for jurisprudential analysis",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/adrianlerer/jurisrank-core",
    project_urls={
        "Homepage": "https://jurisrank.io",
        "Documentation": "https://docs.jurisrank.net", 
        "Repository": "https://github.com/adrianlerer/jurisrank-core",
        "Bug Tracker": "https://github.com/adrianlerer/jurisrank-core/issues",
        "API Documentation": "https://api.jurisrank.io/docs"
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Developers", 
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Legal",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Natural Language :: Spanish"
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "isort>=5.12.0", 
            "flake8>=6.0.0",
            "mypy>=1.4.0"
        ],
        "docs": [
            "mkdocs>=1.5.0",
            "mkdocs-material>=9.1.0"
        ],
        "full": [
            "transformers>=4.30.0",
            "spacy>=3.6.0",
            "lightgbm>=3.3.5",
            "xgboost>=1.7.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "jurisrank=jurisrank.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "jurisrank": ["data/*.json", "configs/*.yaml", "templates/*.txt"]
    },
    keywords=[
        "legal", "ai", "artificial intelligence", "jurisprudence", 
        "law", "legal-tech", "nlp", "machine learning", "legal analysis",
        "court decisions", "legal research", "patent pending"
    ],
    license="MIT",
    zip_safe=False
)
