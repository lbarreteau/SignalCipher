# 🤝 Contribution Guidelines

Merci de vouloir contribuer à **SignalCipher** ! Voici les guidelines pour contribuer efficacement.

---

## 📋 Code of Conduct

Ce projet adhère à un code de conduite. En participant, vous vous engagez à maintenir un environnement respectueux et inclusif.

### Nos Engagements
- 🤝 Être accueillant et inclusif
- 🎯 Se concentrer sur ce qui est meilleur pour la communauté
- 💡 Accepter les critiques constructives
- 🚫 Zéro tolérance pour le harcèlement

---

## 🚀 Comment Contribuer

### Types de Contributions

1. **🐛 Bug Reports**
   - Utiliser le template d'issue bug
   - Inclure les étapes de reproduction
   - Fournir logs et screenshots si possible

2. **✨ Feature Requests**
   - Décrire clairement la feature
   - Expliquer le use case
   - Proposer une implémentation (optionnel)

3. **📝 Documentation**
   - Améliorer README, docs, comments
   - Ajouter des exemples
   - Corriger typos

4. **💻 Code Contributions**
   - Nouvelles features
   - Bug fixes
   - Optimisations de performance
   - Tests

---

## 🔧 Setup Development Environment

### 1. Fork & Clone

```bash
# Fork sur GitHub, puis clone
git clone https://github.com/YOUR_USERNAME/SignalCipher.git
cd SignalCipher

# Ajouter upstream remote
git remote add upstream https://github.com/lbarreteau/SignalCipher.git
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Install Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

### 4. Create Feature Branch

```bash
git checkout -b feature/amazing-feature
```

---

## 📝 Coding Standards

### Style Guide

Nous suivons **PEP 8** avec quelques extensions.

#### Formatter: Black
```bash
black .
```

#### Linter: Flake8
```bash
flake8 .
```

#### Type Hints: MyPy
```bash
mypy .
```

### Code Structure

```python
"""Module docstring explaining purpose."""

import standard_library
import third_party
import local_module


class MyClass:
    """Class docstring.
    
    Attributes:
        attr1: Description
        attr2: Description
    """
    
    def __init__(self, param: str):
        """Initialize with param.
        
        Args:
            param: Description
        """
        self.attr = param
    
    def method(self, arg: int) -> bool:
        """Method description.
        
        Args:
            arg: Description
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: When something goes wrong
        """
        # Implementation
        return True
```

### Naming Conventions

```python
# Variables & Functions: snake_case
user_name = "John"
def calculate_total():
    pass

# Classes: PascalCase
class MoneyFlowClassifier:
    pass

# Constants: UPPER_CASE
MAX_RETRIES = 3
API_ENDPOINT = "https://api.binance.com"

# Private: _leading_underscore
_internal_variable = 42
def _private_function():
    pass
```

---

## 🧪 Testing

### Writing Tests

```python
# tests/test_indicators.py
import pytest
from indicators.money_flow import calculate_mfi


def test_mfi_calculation():
    """Test MFI calculation with known values."""
    # Arrange
    data = create_sample_data()
    
    # Act
    result = calculate_mfi(data, period=14)
    
    # Assert
    assert len(result) == len(data)
    assert 0 <= result.iloc[-1] <= 100


def test_mfi_oversold():
    """Test MFI oversold detection."""
    data = create_oversold_data()
    mfi = calculate_mfi(data)
    
    assert mfi.iloc[-1] < 20, "MFI should be in oversold zone"
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=. --cov-report=html

# Specific file
pytest tests/test_indicators.py

# Specific test
pytest tests/test_indicators.py::test_mfi_calculation

# Verbose
pytest -v

# Stop at first failure
pytest -x
```

### Test Coverage

Nous visons **>80% code coverage**.

```bash
# Generate coverage report
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

---

## 📚 Documentation

### Docstrings

Utiliser le format **Google Style**.

```python
def fetch_ohlcv(symbol: str, timeframe: str, limit: int = 1000) -> pd.DataFrame:
    """Fetch OHLCV data from Binance.
    
    Args:
        symbol: Trading pair (e.g., 'BTC/USDT')
        timeframe: Candle timeframe (e.g., '1h', '1d')
        limit: Maximum number of candles (default: 1000)
        
    Returns:
        DataFrame with columns: timestamp, open, high, low, close, volume
        
    Raises:
        APIError: If Binance API returns an error
        ValueError: If timeframe is invalid
        
    Example:
        >>> df = fetch_ohlcv('BTC/USDT', '1h', limit=100)
        >>> print(df.head())
    """
    pass
```

### Type Hints

Toujours utiliser type hints.

```python
from typing import List, Dict, Optional, Union, Tuple

def process_signals(
    data: pd.DataFrame,
    symbols: List[str],
    config: Optional[Dict[str, any]] = None
) -> Tuple[List[str], Dict[str, float]]:
    """Process trading signals."""
    pass
```

---

## 🔀 Git Workflow

### Branch Naming

```
feature/add-new-indicator
bugfix/fix-mfi-calculation
hotfix/critical-api-error
docs/update-readme
refactor/optimize-scanner
test/add-wave-trend-tests
```

### Commit Messages

Format: **Conventional Commits**

```
type(scope): short description

Longer description if needed.

Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples:**

```bash
git commit -m "feat(indicators): add wave trend oscillator calculation"

git commit -m "fix(scanner): resolve race condition in multi-threading"

git commit -m "docs(readme): update installation instructions"

git commit -m "test(ml_models): add unit tests for money flow classifier"
```

### Pull Request Process

1. **Update from upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

3. **Open Pull Request**
   - Use PR template
   - Link related issues
   - Request review

4. **Address Review Comments**
   ```bash
   # Make changes
   git add .
   git commit -m "fix: address review comments"
   git push origin feature/amazing-feature
   ```

5. **Merge**
   - Maintainer will merge after approval

---

## 📋 Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] Added new tests
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings

## Related Issues
Fixes #123
Related to #456

## Screenshots (if applicable)
```

---

## 🐛 Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## To Reproduce
1. Step 1
2. Step 2
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10.5]
- SignalCipher version: [e.g., 0.1.0]

## Logs
```
Paste relevant logs here
```

## Additional Context
Any other relevant information
```

---

## ✨ Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Use Case
Explain why this feature is needed

## Proposed Solution
How you think it should be implemented

## Alternatives Considered
Other approaches you've thought about

## Additional Context
Any other relevant information
```

---

## 🏆 Recognition

Contributors will be recognized in:
- README.md Contributors section
- CHANGELOG.md for significant contributions
- Special badge on Discord (if applicable)

---

## 📞 Questions?

- 💬 **Discord:** [Join our server](#)
- 📧 **Email:** contribute@signalcipher.com
- 📖 **Docs:** [Read the docs](#)

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to SignalCipher! 🚀**
