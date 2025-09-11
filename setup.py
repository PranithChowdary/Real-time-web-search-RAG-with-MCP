from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rag-mcp-assistant",
    version="1.0.0",
    author="Pranith Chowdary",
    author_email="pranithtpm@gmail.com",
    description="Real-time Web Search & RAG Assistant with MCP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PranithChowdary/Real-time-web-search-RAG-with-MCP",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain>=0.1.0",
        "openai>=1.12.0",
        "faiss-cpu>=1.7.4",
        "sentence-transformers>=2.2.2",
        "fastapi>=0.108.0",
        "uvicorn>=0.25.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
)