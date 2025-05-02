from setuptools import setup, find_packages

setup(
    name="kernel_analyzer",
    version="0.1.0",
    description="A tool for analyzing OpenCL compute kernels for performance characteristics",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="OpenCL Kernel Performance Analyzer Contributors",
    author_email="maintainer@example.com",
    url="https://github.com/your-organization/kernel-analyzer",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "matplotlib>=3.5.0",
        "PyQt5>=5.15.0",
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.3.0",
            "flake8>=4.0.0",
            "isort>=5.10.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "kernel-analyzer=kernel_analyzer.cli.analyzer_cli:main",
            "kernel-analyzer-gui=kernel_analyzer.gui.kernel_analyzer_gui:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="opencl, gpu, kernel, performance, analysis",
    project_urls={
        "Documentation": "https://github.com/your-organization/kernel-analyzer/docs",
        "Source": "https://github.com/your-organization/kernel-analyzer",
        "Tracker": "https://github.com/your-organization/kernel-analyzer/issues",
    },
    include_package_data=True,
) 