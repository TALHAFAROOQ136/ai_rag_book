# Skills Packaging Guide (Roman Urdu)

Ye guide aapko batayegi ke `skills` folder ko ek python library kese banate hain taake kisi aur project mein use kar sakein.

## Pre-requisites (Zaroori Cheezein)

- Python 3.8+ hona chahiye
- Terminal mein `pip` install hona chahiye

## 1. Package Build Karna

Sabse pehle project folder mein terminal khol kar ye commands run karein:

```bash
# Build tools update karein
pip install --upgrade setuptools wheel

# Package create karein
python setup.py sdist bdist_wheel
```

Is se ek naya `dist/` folder ban jayega jismein ye file hogi:
- `matrix_skills-0.1.0-py3-none-any.whl` (Ye apki main file hai)

## 2. Kisi Aur Project Mein Install Karna

Ab agar aapko ye skills kisi doosre project mein use karni hain:

1. `dist/` folder se `.whl` file copy karein.
2. Apne naye project ke folder mein paste karein.
3. Terminal mein ye command run karein:

```bash
pip install matrix_skills-0.1.0-py3-none-any.whl
```

## 3. Code Mein Use Karna

Install karne ke baad, aap direct import kar sakte hain:

```python
from skills import QdrantIntegration, OpenAIAgentBuilder

# Qdrant skill use karein
qdrant = QdrantIntegration(url="...", api_key="...")

# OpenAI Agent skill use karein
agent_builder = OpenAIAgentBuilder(api_key="...")
```

## Troubleshooting (Masle Hal Karna)

- **Agar install na ho**: Check karein ke aapne pehle `python setup.py ...` wali command run ki hai ya nahi.
- **Dependencies**: `openai` aur `qdrant-client` khud hi install ho jayenge.
