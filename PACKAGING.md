# Packaging Skills Guide

This guide explains how to package the `skills` directory into a distributable Python library.

## Prerequisites

- Python 3.8+
- pip
- setuptools, wheel

## 1. Build the Package

Open a terminal in the project root:

```bash
# Install build tools
pip install --upgrade setuptools wheel

# Build source distribution and wheel
python setup.py sdist bdist_wheel
```

This will create a `dist/` directory containing:
- `matrix-skills-0.1.0.tar.gz` (Source)
- `matrix_skills-0.1.0-py3-none-any.whl` (Wheel - Precompiled)

## 2. Install in Another Project

You can install the package directly from the wheel file.

**Copy the wheel file to your new project and run:**

```bash
pip install matrix_skills-0.1.0-py3-none-any.whl
```

Or install directly from the source folder (development mode):

```bash
pip install -e /path/to/ai_book/
```

## 3. Usage in Code

Once installed, you can import skills directly:

```python
from skills import QdrantIntegration, OpenAIAgentBuilder

# Initialize standard Qdrant skill
qdrant = QdrantIntegration(url="...", api_key="...")

# Initialize OpenAI Agent skill
agent_builder = OpenAIAgentBuilder(api_key="...")
```

## 4. Publishing to PyPI (Optional)

If you want to share with the world:

1. Create account on [pypi.org](https://pypi.org)
2. Install twine: `pip install twine`
3. Upload: `twine upload dist/*`

Now anyone can install with: `pip install matrix-skills`

## Troubleshooting

- **ImportError**: Ensure `__init__.py` files exist (we created them).
- **Dependencies**: Check `install_requires` in `setup.py` matches your needs.
