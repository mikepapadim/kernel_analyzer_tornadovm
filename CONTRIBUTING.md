# Contributing to OpenCL Kernel Analyzer

Thank you for considering contributing to the OpenCL Kernel Analyzer! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Making Contributions](#making-contributions)
  - [Bug Reports](#bug-reports)
  - [Feature Requests](#feature-requests)
  - [Pull Requests](#pull-requests)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Review Process](#review-process)
- [Community](#community)

## Code of Conduct

This project adheres to a Code of Conduct that sets expectations for participation in our community. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up your development environment** (see [Development Environment](#development-environment))
4. **Create a branch** for your contribution
5. **Make your changes** following our [Coding Standards](#coding-standards)
6. **Write tests** for your changes (see [Testing](#testing))
7. **Update documentation** as needed
8. **Submit a pull request** (see [Pull Requests](#pull-requests))

## Development Environment

### Prerequisites

- Python 3.7 or newer
- pip (Python package installer)
- Git

### Setting Up

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/opencl-kernel-analyzer.git
cd opencl-kernel-analyzer

# Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### GUI Development Requirements

For GUI development, you'll also need:

- PyQt5 (installed with the dev dependencies)
- Qt Designer (optional, for UI design)

## Making Contributions

### Bug Reports

When filing a bug report, please include:

1. **Clear title and description** of the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** and what actually happened
4. **Environment details**: Python version, OS, etc.
5. **Relevant logs or screenshots**

### Feature Requests

Feature requests should include:

1. **Clear description** of the feature
2. **Rationale** for adding the feature
3. **Example use cases** showing how users would interact with the feature
4. **Implementation ideas** (optional)

### Pull Requests

When submitting a pull request:

1. **Reference related issues** or feature requests
2. **Describe your changes** and the problem they solve
3. **Include screenshots or examples** for UI changes
4. **Ensure all tests pass**
5. **Add or update documentation** as needed

## Coding Standards

We follow these coding standards:

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use 4 spaces for indentation
- Maximum line length of 100 characters
- Use meaningful variable and function names
- Add type hints to function signatures

### Documentation

- Use docstrings for modules, classes, and functions
- Follow [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Keep docstrings up-to-date with code changes

### Code Organization

- Organize code logically into modules
- Keep functions and methods focused on a single responsibility
- Limit class inheritance depth
- Use proper encapsulation

## Testing

We use pytest for testing. All new features and bug fixes should include tests.

### Running Tests

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/test_specific_file.py

# Run with coverage
pytest --cov=kernel_analyzer
```

### Test Guidelines

- Write both unit tests and integration tests
- Mock external dependencies
- Test edge cases and error conditions
- Aim for high code coverage, but prioritize meaningful tests over coverage percentage

## Documentation

Documentation is as important as code. When contributing:

- Update README.md if you change user-facing functionality
- Update docstrings and comments for code changes
- Add or update examples for new features
- Consider adding or updating tutorial documentation

## Review Process

All submissions require review before merging:

1. **Automated checks** will verify code style and tests
2. **Maintainers will review** your code for:
   - Code quality and style
   - Test coverage
   - Documentation
   - Overall design and implementation
3. **Address review feedback** by making requested changes
4. Once approved, maintainers will merge your contribution

## Community

Join our community:

- **GitHub Discussions**: Ask questions and share ideas
- **GitHub Issues**: Report bugs and request features
- **Pull Requests**: Contribute code and documentation

## Areas for Contribution

We're particularly interested in contributions in these areas:

1. **Analyzer Improvements**:
   - Support for more OpenCL features
   - Enhanced performance analysis
   - Better vectorization detection

2. **GUI Enhancements**:
   - Improved visualization
   - Usability improvements
   - New analysis views

3. **Documentation and Examples**:
   - Better user guides
   - More example kernels
   - Optimization case studies

4. **Testing Infrastructure**:
   - More comprehensive test suite
   - Performance benchmarks
   - Test coverage improvements

Thank you for contributing to the OpenCL Kernel Analyzer! 