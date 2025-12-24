# Contributing to AI Agent League Competition System

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

---

## Code of Conduct

This project follows a standard code of conduct. Please be respectful and constructive in all interactions.

- Be welcoming and inclusive
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what is best for the community

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip package manager

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/LLMs-and-Multi-Agent-Orchestration---Assignment7.git
   cd LLMs-and-Multi-Agent-Orchestration---Assignment7
   ```
3. Add upstream remote:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/LLMs-and-Multi-Agent-Orchestration---Assignment7.git
   ```

---

## Development Setup

### Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Verify Installation

```bash
# Run tests
pytest tests/ -v

# Check imports work
python -c "import SHARED.league_sdk; print('OK')"
```

---

## Making Changes

### Branch Naming

Use descriptive branch names:
- `feature/add-new-strategy` - New features
- `fix/timeout-handling` - Bug fixes
- `docs/update-readme` - Documentation
- `refactor/player-module` - Code refactoring
- `test/add-edge-cases` - Test additions

### Commit Messages

Follow conventional commit format:
```
type(scope): brief description

Longer description if needed.

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(player): add adaptive strategy implementation`
- `fix(referee): handle timeout edge case`
- `docs(readme): update installation instructions`

---

## Pull Request Process

1. **Update your fork**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature
   ```

3. **Make changes** following coding standards

4. **Run tests**:
   ```bash
   pytest tests/ -v --cov=SHARED --cov-fail-under=70
   ```

5. **Run linting**:
   ```bash
   pylint SHARED/ agents/ api/ --fail-under=8.0
   ```

6. **Push and create PR**:
   ```bash
   git push origin feature/your-feature
   ```

7. **Fill out PR template** with:
   - Description of changes
   - Related issues
   - Testing performed
   - Screenshots (if UI changes)

---

## Coding Standards

### File Size Limit

**CRITICAL**: No file may exceed 150 lines. Break large files into modules.

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Maximum line length: 120 characters
- Use Google-style docstrings

### Docstring Example

```python
def calculate_win_rate(wins: int, total: int) -> float:
    """Calculate win rate as a percentage.
    
    Args:
        wins: Number of wins
        total: Total number of games
        
    Returns:
        Win rate as percentage (0-100)
        
    Raises:
        ValueError: If total is zero or negative
        
    Example:
        >>> calculate_win_rate(7, 10)
        70.0
    """
    if total <= 0:
        raise ValueError("Total must be positive")
    return (wins / total) * 100
```

### Import Organization

```python
# Standard library
import json
from typing import Dict, List

# Third-party
import httpx
from fastapi import FastAPI

# Local
from SHARED.constants import Field, MessageType
from SHARED.contracts import build_message
```

---

## Testing Guidelines

### Test Requirements

- Minimum 70% code coverage
- All new features must have tests
- All bug fixes must have regression tests

### Test Structure

```python
class TestFeatureName:
    """Tests for feature_name module."""
    
    def test_basic_functionality(self):
        """Test basic case works correctly."""
        result = function_under_test(input)
        assert result == expected
    
    def test_edge_case(self):
        """Test edge case handling."""
        ...
    
    def test_error_handling(self):
        """Test error cases raise appropriate exceptions."""
        with pytest.raises(ValueError):
            function_under_test(invalid_input)
```

### Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=SHARED --cov-report=html

# Specific test file
pytest tests/test_game_logic.py -v

# Specific test
pytest tests/test_game_logic.py::test_determine_winner -v
```

---

## Documentation

### When to Update Docs

- New features: Update relevant docs
- API changes: Update API.md
- Architecture changes: Update ARCHITECTURE.md
- New ADRs: Add to doc/ADRs/

### Documentation Standards

- Use Markdown format
- Include code examples
- Keep documentation up-to-date with code
- Add diagrams where helpful (Mermaid format)

---

## Questions?

If you have questions:
1. Check existing documentation in `doc/`
2. Search existing issues
3. Open a new issue with the `question` label

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
