"""Setup configuration for AI Agent League Competition System."""

from setuptools import find_packages, setup

setup(
    name="league_sdk",
    version="1.0.0",
    description="SDK for AI Agent League Competition System",
    author="Assignment 7 Team",
    packages=find_packages(where="SHARED"),
    package_dir={"": "SHARED"},
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "httpx>=0.25.0",
        "pydantic>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "pylint>=3.0.0",
            "isort>=5.12.0",
        ],
    },
)
