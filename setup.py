from pathlib import Path

from setuptools import find_packages, setup

setup(
    name="agentmem",
    version="0.1.0",
    author="Mukunda Rao Katta",
    author_email="mukunda.vjcs6@gmail.com",
    description="Lightweight, pluggable memory management for AI agents",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/MukundaKatta/agentmem",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[],
    extras_require={
        "dev": ["pytest", "pytest-asyncio", "ruff"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
