# Installation Guide for Shelf Vision Audit Tool

This guide provides multiple methods to install the dependencies for the Shelf Vision Audit Tool.

## Method 1: Using the Installation Script

The easiest way to install all dependencies is to use the provided installation script:

```bash
# Make the script executable (if not already)
chmod +x install_dependencies.sh

# Run the installation script
./install_dependencies.sh
```

## Method 2: Using Conda Environment

If you have Anaconda or Miniconda installed, you can create a new environment with all the required dependencies:

```bash
# Create and activate a new conda environment
conda env create -f environment.yml
conda activate shelf-vision
```

## Method 3: Manual Installation

If you prefer to install dependencies manually, follow these steps:

1. Update pip to the latest version:
   ```bash
   pip install --upgrade pip
   ```

2. Install tokenizers first (to avoid compilation issues):
   ```bash
   pip install tokenizers==0.13.3 --no-build-isolation
   ```

3. Install the remaining dependencies:
   ```bash
   pip install flask==2.3.3 werkzeug==2.3.7 pillow==10.0.0 numpy>=1.26.0
   pip install opencv-python==4.8.0.76 transformers==4.32.1
   pip install torch>=2.0.1 python-dotenv==1.0.0 flask-wtf==1.1.1
   ```

## Minimal Installation (No Transformers)

If you're having issues with the transformers library or tokenizers, you can use the minimal version of the application:

```bash
# Make the script executable
chmod +x install_minimal.sh

# Run the minimal installation script
./install_minimal.sh
```

Then run the application using:

```bash
python run_minimal.py
```

This version uses only OpenCV for image processing and doesn't require transformers or PyTorch.

## Troubleshooting

### Rust Compiler Error

If you encounter an error about missing Rust compiler when installing tokenizers, try one of these solutions:

1. Install Rust:
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   source $HOME/.cargo/env
   ```

2. Or use a pre-built wheel:
   ```bash
   pip install tokenizers==0.13.3 --no-build-isolation
   ```

3. Or use the minimal version of the application (see above).

### CUDA Issues

If you encounter CUDA-related errors with PyTorch, you can install a CPU-only version:

```bash
pip install torch>=2.0.1 --index-url https://download.pytorch.org/whl/cpu
```

Or use the provided CPU-only installation script:

```bash
./install_dependencies_cpu.sh
```

## Running the Application

After installing all dependencies, you can run the application:

```bash
# Full version
python run.py

# Minimal version (if using minimal installation)
python run_minimal.py
```

The application will be accessible at http://localhost:5000. 