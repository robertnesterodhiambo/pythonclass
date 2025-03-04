import subprocess

# List of packages to install
packages = [
    "huggingface_hub",
    "langchain",
    "langchain-community",
    "llama-cpp-python",
    "fitz",
    "tools",
    "pymupdf",
    "pypdf",
    "chromadb"
]

# Install each package
for package in packages:
    subprocess.run(["pip", "install", "--break-system-packages", package], check=True)

print("All packages installed successfully!")
