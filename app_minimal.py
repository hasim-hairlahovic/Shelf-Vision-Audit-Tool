import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import cv2
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
            template_folder='app/templates',
            static_folder='app/static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_testing')
app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'txt'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(filename):
    """Generate a unique filename with timestamp and UUID"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    return f"{unique_name}.{ext}" if ext else unique_name

def parse_metadata_file(file_path):
    """Parse the metadata txt file into a structured format"""
    metadata = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    # Simple parsing logic - adjust based on actual format
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Assuming tab or space-separated values
        parts = line.split()
        if len(parts) >= 3:  # At minimum: SKU, price, section
            item = {
                'sku': parts[0],
                'price': parts[1],
                'section': parts[2],
                'additional_info': parts[3:] if len(parts) > 3 else []
            }
            metadata.append(item)
    
    return metadata

def analyze_image_quality(image_path):
    """Analyze image quality and return issues"""
    img = cv2.imread(image_path)
    issues = []
    
    # Check for blurriness
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    if laplacian_var < 100:  # Threshold for blurriness
        issues.append({
            'type': 'blur',
            'severity': 'high' if laplacian_var < 50 else 'medium',
            'description': 'Image appears to be blurry'
        })
    
    # Check for poor lighting
    brightness = np.mean(gray)
    if brightness < 50:
        issues.append({
            'type': 'lighting',
            'severity': 'medium',
            'description': 'Image appears to be too dark'
        })
    elif brightness > 200:
        issues.append({
            'type': 'lighting',
            'severity': 'medium',
            'description': 'Image appears to be too bright'
        })
    
    # Check for low resolution
    height, width = img.shape[:2]
    if width < 800 or height < 600:
        issues.append({
            'type': 'resolution',
            'severity': 'medium',
            'description': f'Low resolution image ({width}x{height})'
        })
    
    return issues

def detect_products_in_image(image_path):
    """
    Detect products in the image using computer vision
    This is a simplified version using basic OpenCV techniques
    """
    # For demonstration, we'll use a simple approach
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Use edge detection to find potential product boundaries
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours by size to eliminate noise
    min_contour_area = 1000
    product_regions = []
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_contour_area:
            x, y, w, h = cv2.boundingRect(contour)
            product_regions.append({
                'x': x,
                'y': y,
                'width': w,
                'height': h,
                'area': area
            })
    
    return product_regions

def compare_metadata_with_image(metadata, detected_products, image_path):
    """Compare metadata with detected products to find anomalies"""
    anomalies = []
    
    # Count products in metadata
    metadata_product_count = len(metadata)
    
    # Count detected products
    detected_product_count = len(detected_products)
    
    # Check for count mismatch
    if metadata_product_count != detected_product_count:
        anomalies.append({
            'type': 'count_mismatch',
            'severity': 'high',
            'description': f'Metadata has {metadata_product_count} products, but {detected_product_count} were detected in the image',
            'metadata_count': metadata_product_count,
            'detected_count': detected_product_count
        })
    
    # Additional checks could be implemented here
    # For example, checking if product positions match metadata sections
    
    return anomalies

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'image' not in request.files or 'metadata' not in request.files:
        flash('Both image and metadata files are required')
        return redirect(request.url)
    
    image_file = request.files['image']
    metadata_file = request.files['metadata']
    
    if image_file.filename == '' or metadata_file.filename == '':
        flash('No selected files')
        return redirect(request.url)
    
    if not (allowed_file(image_file.filename) and allowed_file(metadata_file.filename)):
        flash('Invalid file type')
        return redirect(request.url)
    
    # Save image file
    image_filename = generate_unique_filename(secure_filename(image_file.filename))
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image_file.save(image_path)
    
    # Save metadata file
    metadata_filename = generate_unique_filename(secure_filename(metadata_file.filename))
    metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], metadata_filename)
    metadata_file.save(metadata_path)
    
    # Process files and analyze
    return redirect(url_for('analyze', image=image_filename, metadata=metadata_filename))

@app.route('/analyze')
def analyze():
    image_filename = request.args.get('image')
    metadata_filename = request.args.get('metadata')
    
    if not image_filename or not metadata_filename:
        flash('Missing files for analysis')
        return redirect(url_for('index'))
    
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], metadata_filename)
    
    # Parse metadata
    metadata = parse_metadata_file(metadata_path)
    
    # Analyze image quality
    quality_issues = analyze_image_quality(image_path)
    
    # Detect products in image
    detected_products = detect_products_in_image(image_path)
    
    # Compare metadata with detected products
    anomalies = compare_metadata_with_image(metadata, detected_products, image_path)
    
    # Prepare results for display
    results = {
        'image_url': url_for('static', filename=f'uploads/{image_filename}'),
        'metadata': metadata,
        'quality_issues': quality_issues,
        'detected_products': detected_products,
        'anomalies': anomalies
    }
    
    return render_template('results.html', results=results)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for programmatic analysis"""
    if 'image' not in request.files or 'metadata' not in request.files:
        return jsonify({'error': 'Both image and metadata files are required'}), 400
    
    image_file = request.files['image']
    metadata_file = request.files['metadata']
    
    if image_file.filename == '' or metadata_file.filename == '':
        return jsonify({'error': 'No selected files'}), 400
    
    if not (allowed_file(image_file.filename) and allowed_file(metadata_file.filename)):
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Save image file
    image_filename = generate_unique_filename(secure_filename(image_file.filename))
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image_file.save(image_path)
    
    # Save metadata file
    metadata_filename = generate_unique_filename(secure_filename(metadata_file.filename))
    metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], metadata_filename)
    metadata_file.save(metadata_path)
    
    # Parse metadata
    metadata = parse_metadata_file(metadata_path)
    
    # Analyze image quality
    quality_issues = analyze_image_quality(image_path)
    
    # Detect products in image
    detected_products = detect_products_in_image(image_path)
    
    # Compare metadata with detected products
    anomalies = compare_metadata_with_image(metadata, detected_products, image_path)
    
    # Prepare results
    results = {
        'image_url': url_for('static', filename=f'uploads/{image_filename}', _external=True),
        'metadata': metadata,
        'quality_issues': quality_issues,
        'detected_products': detected_products,
        'anomalies': anomalies
    }
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=os.environ.get('DEBUG', 'False').lower() == 'true') 