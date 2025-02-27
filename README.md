# Shelf Vision Audit Tool

A Flask web application for auditing output photos from vision machine learning models that analyze store shelves.

## Features

- Upload and process shelf photos
- Upload and parse metadata files (txt format)
- Automatic detection of anomalies:
  - Poor image quality
  - Missing products in metadata
  - Misaligned product information
  - Other inconsistencies

## Installation

There are multiple ways to install the dependencies for this application. Choose the method that works best for your environment:

### Quick Installation

Use one of the provided installation scripts:

```bash
# For systems with CUDA support
./install_dependencies.sh

# For CPU-only systems
./install_dependencies_cpu.sh
```

### Detailed Installation

For more detailed installation instructions and troubleshooting, see [INSTALL.md](INSTALL.md).

## Usage

1. Navigate to the web interface (default: http://localhost:5000)
2. Upload a shelf photo
3. Upload the corresponding metadata file (txt format)
4. View the analysis results with highlighted anomalies

## File Format

The metadata file should be in txt format with information about products on the shelf, including:
- SKU numbers
- Prices
- Section locations
- Other product details

Example format:
```
SKU123456 $19.99 A1 Cereal_Box_Large
SKU789012 $24.99 B2 Pasta_Premium_Brand
```

## Technologies Used

- Flask (Web Framework)
- OpenCV (Image Processing)
- Transformers (AI Vision Models)
- HTML/CSS/JavaScript (Frontend)

## Running the Application

After installing all dependencies, run the application:

```bash
python run.py
```

The application will be accessible at http://localhost:5000. # Shelf-Vision-Audit-Tool
