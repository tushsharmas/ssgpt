# Contributing to ssgpt

Thanks for your interest in contributing to ssgpt! This project combines StockGPT (stock market analysis) and TravelEva (AI travel assistant) built with Streamlit and Python.

## Getting Started

### Prerequisites
* Python 3.8+
* Git

### Setup Instructions

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/ssgpt.git
   cd ssgpt
   ```

2. **Create Virtual Environment**
   ```bash
   # Using uv (recommended by this project)
   pip install uv
   uv venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   
   # Or using standard Python
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   uv pip install -r requirements.txt
   # Or: pip install -r requirements.txt
   ```

4. **Test the Applications**
   ```bash
   # Test StockGPT
   streamlit run tr2.py
   
   # Test TravelEva
   streamlit run traveleva.py
   ```

## Project Structure

Based on the repository, the main files are:
* `tr2.py` - Advanced StockGPT application (main version)
* `tr.py` - Basic StockGPT application  
* `tr3.py` - StockGPT with history features
* `traveleva.py` - TravelEva AI Travel Assistant
* `requirements.txt` - Python dependencies
* Database files (auto-created): `stock_history.db`, `traveleva_history.db`

## Ways to Contribute

You can help by:
* Reporting bugs or suggesting features
* Improving code quality
* Adding documentation
* Fixing issues
* Enhancing user experience

Check the [issues page](https://github.com/tushsharmas/ssgpt/issues) to see current needs and priorities.

## Development Guidelines

### Creating Your Branch
```bash
git checkout -b your-branch-name
```

### Code Style
* Follow the existing code patterns in the project
* Use meaningful variable names
* Handle exceptions properly
* The project uses Streamlit and caching with `@st.cache_data`

### Testing Your Changes
Before submitting:
* Ensure both applications start without errors
* Test core functionality works
* Check for any console errors
* Verify your changes don't break existing features

### Submitting Changes
```bash
git add .
git commit -m "Clear description of changes"
git push origin your-branch-name
```

Then create a pull request on GitHub with a description of what you changed.

## Reporting Issues

When reporting bugs, please include:
* Which application (StockGPT or TravelEva)  
* Steps to reproduce the issue
* What you expected to happen
* What actually happened
* Your environment (Python version, OS, browser)
* Any error messages or screenshots

## Code of Conduct

Please be respectful and professional in all interactions. We want this to be a welcoming environment for contributors of all experience levels.

## Contact

* Open an issue on GitHub for questions or bug reports
* Check existing issues before creating new ones
* Comment on issues if you want to work on them

Thanks for contributing! 
