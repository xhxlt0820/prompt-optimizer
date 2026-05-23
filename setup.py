from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prompt-optimizer",
    version="1.0.0",
    author="xhxlt0820",
    author_email="xiaohuxian@gmail.com",
    description="AI Prompt Quality Analyzer & Optimizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xhxlt0820/prompt-optimizer",
    py_modules=["prompt_optimizer"],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "prompt-optimizer=prompt_optimizer:main",
            "prompt_opt=prompt_optimizer:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
)
