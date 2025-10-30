#!/usr/bin/env python3
"""
Setup script for SignalCipher project.
Creates directory structure and initializes the project.
"""

import os
from pathlib import Path


def create_directory_structure():
    """Create the complete directory structure for the project."""
    
    directories = [
        # Data directories
        "data/raw",
        "data/processed",
        "data/training",
        
        # Source code directories
        "indicators",
        "ml_models",
        "data_collection",
        "training",
        "scanner",
        "backtesting",
        "utils",
        "dashboard",
        
        # Other directories
        "tests",
        "notebooks",
        "models",
        "logs",
        "docs",
    ]
    
    print("🏗️  Creating directory structure...")
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}/")
        
        # Create __init__.py for Python packages
        if directory not in ["data", "tests", "notebooks", "models", "logs", "docs", "config"]:
            if not directory.startswith("data/"):
                init_file = path / "__init__.py"
                if not init_file.exists():
                    init_file.write_text('"""Package initialization."""\n')
                    
        # Create .gitkeep for empty directories
        if directory in ["data/raw", "data/processed", "data/training", "models", "logs"]:
            gitkeep = path / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.touch()
    
    print("\n✨ Directory structure created successfully!")


def create_env_file():
    """Create .env file from .env.example if it doesn't exist."""
    
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("\n⚠️  .env file already exists. Skipping...")
    elif env_example.exists():
        print("\n📝 Creating .env file from template...")
        env_file.write_text(env_example.read_text())
        print("✅ .env file created! Please edit it with your API keys.")
    else:
        print("\n❌ .env.example not found!")


def create_gitignore():
    """Create .gitignore file."""
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local

# Data files
data/raw/*.csv
data/raw/*.parquet
data/processed/*.csv
data/processed/*.parquet
data/training/*.csv
data/training/*.parquet

# Models
models/*.pkl
models/*.joblib
models/*.h5
models/*.pt
models/*.pth

# Logs
logs/*.log
logs/*.txt

# Jupyter Notebook
.ipynb_checkpoints
*.ipynb

# Distribution / packaging
.Python
build/
dist/
*.egg-info/

# Testing
.coverage
.pytest_cache/
htmlcov/
.tox/

# OS
.DS_Store
Thumbs.db

# Redis dump
dump.rdb

# Database
*.db
*.sqlite
*.sqlite3
"""
    
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        print("\n📝 Creating .gitignore file...")
        gitignore_path.write_text(gitignore_content)
        print("✅ .gitignore file created!")
    else:
        print("\n⚠️  .gitignore already exists. Skipping...")


def print_next_steps():
    """Print next steps for the user."""
    
    print("\n" + "="*60)
    print("🎉 SignalCipher Project Setup Complete!")
    print("="*60)
    
    print("\n📋 Next Steps:\n")
    
    print("1️⃣  Create and activate virtual environment:")
    print("   python -m venv venv")
    print("   source venv/bin/activate  # Linux/Mac")
    print("   # or: venv\\Scripts\\activate  # Windows")
    
    print("\n2️⃣  Install dependencies:")
    print("   pip install --upgrade pip")
    print("   pip install -r requirements.txt")
    
    print("\n3️⃣  Configure environment variables:")
    print("   Edit .env file with your API keys")
    print("   nano .env  # or your favorite editor")
    
    print("\n4️⃣  Test API connection:")
    print("   python -c \"from data_collection.binance_client import test_connection; test_connection()\"")
    
    print("\n5️⃣  Collect sample data:")
    print("   python -m data_collection.data_fetcher --symbols BTC/USDT --days 30")
    
    print("\n6️⃣  Start developing:")
    print("   Check TODO.md for task list")
    print("   Read CONTRIBUTING.md for guidelines")
    
    print("\n📚 Documentation:")
    print("   - PROJECT_PLAN.md - Full project roadmap")
    print("   - TECHNICAL_SPECS.md - Technical specifications")
    print("   - README.md - Project overview")
    print("   - TODO.md - Task checklist")
    
    print("\n💡 Need help?")
    print("   - GitHub Issues: Report bugs or request features")
    print("   - GitHub Discussions: Ask questions")
    
    print("\n" + "="*60)
    print("Happy Coding! 🚀")
    print("="*60 + "\n")


def main():
    """Main setup function."""
    
    print("\n" + "="*60)
    print("🔐 SignalCipher - Project Setup")
    print("="*60 + "\n")
    
    # Create directory structure
    create_directory_structure()
    
    # Create .env from template
    create_env_file()
    
    # Create .gitignore
    create_gitignore()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()
