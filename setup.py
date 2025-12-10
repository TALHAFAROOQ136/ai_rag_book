from setuptools import setup, find_packages

setup(
    name="matrix-skills",
    version="0.1.0",
    description="Reusable Matrix-style capabilities for AI agents",
    author="AI Book Project",
    packages=find_packages(include=['skills', 'skills.*']),
    install_requires=[
        "openai>=1.0.0",
        "qdrant-client>=1.7.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0"
    ],
    python_requires=">=3.8",
)
