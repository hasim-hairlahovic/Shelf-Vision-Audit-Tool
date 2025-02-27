/**
 * Shelf Vision Audit Tool - Main JavaScript
 * Enhanced with AI-specific functionality
 */

// Initialize when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // File input validation
    const imageInput = document.getElementById('image');
    const metadataInput = document.getElementById('metadata');
    const uploadForm = document.getElementById('upload-form');
    
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Validate image file
            if (imageInput && imageInput.files.length > 0) {
                const file = imageInput.files[0];
                const fileType = file.type;
                const validImageTypes = ['image/jpeg', 'image/jpg', 'image/png'];
                
                if (!validImageTypes.includes(fileType)) {
                    alert('Please select a valid image file (JPG, JPEG, or PNG)');
                    isValid = false;
                }
                
                if (file.size > 16 * 1024 * 1024) { // 16MB
                    alert('Image file size must be less than 16MB');
                    isValid = false;
                }
            }
            
            // Validate metadata file
            if (metadataInput && metadataInput.files.length > 0) {
                const file = metadataInput.files[0];
                const fileName = file.name.toLowerCase();
                
                if (!fileName.endsWith('.txt')) {
                    alert('Metadata file must be a .txt file');
                    isValid = false;
                }
                
                if (file.size > 5 * 1024 * 1024) { // 5MB
                    alert('Metadata file size must be less than 5MB');
                    isValid = false;
                }
            }
            
            if (!isValid) {
                event.preventDefault();
            } else {
                // Show loading indicator
                const submitBtn = uploadForm.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Processing...';
                    submitBtn.disabled = true;
                }
            }
        });
    }
    
    // Adjust highlight boxes on results page
    const analyzedImage = document.getElementById('analyzed-image');
    const highlightBoxes = document.querySelectorAll('.highlight-box');
    
    if (analyzedImage && highlightBoxes.length > 0) {
        function adjustHighlightBoxes() {
            const imageRect = analyzedImage.getBoundingClientRect();
            const imageNaturalWidth = analyzedImage.naturalWidth;
            const imageNaturalHeight = analyzedImage.naturalHeight;
            const scaleX = imageRect.width / imageNaturalWidth;
            const scaleY = imageRect.height / imageNaturalHeight;
            
            highlightBoxes.forEach(box => {
                const x = parseInt(box.dataset.x) * scaleX;
                const y = parseInt(box.dataset.y) * scaleY;
                const width = parseInt(box.dataset.width) * scaleX;
                const height = parseInt(box.dataset.height) * scaleY;
                
                box.style.left = `${x}px`;
                box.style.top = `${y}px`;
                box.style.width = `${width}px`;
                box.style.height = `${height}px`;
            });
        }
        
        // Adjust boxes when image loads
        analyzedImage.addEventListener('load', adjustHighlightBoxes);
        
        // Also adjust on window resize
        window.addEventListener('resize', adjustHighlightBoxes);
        
        // Initial adjustment
        if (analyzedImage.complete) {
            adjustHighlightBoxes();
        }
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-info)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add animation to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});

/**
 * Toggle highlight visibility
 */
function toggleHighlights() {
    const highlightBoxes = document.querySelectorAll('.highlight-box');
    highlightBoxes.forEach(box => {
        box.classList.toggle('d-none');
    });
    
    // Update button text
    const btn = document.querySelector('button[onclick="toggleHighlights()"]');
    if (btn) {
        if (highlightBoxes[0] && highlightBoxes[0].classList.contains('d-none')) {
            btn.innerHTML = '<i class="bi bi-eye"></i> Show Highlights';
        } else {
            btn.innerHTML = '<i class="bi bi-eye-slash"></i> Hide Highlights';
        }
    }
}

/**
 * Export results as JSON
 */
function exportResults() {
    // Get results data from the page
    const resultsData = window.resultsData;
    
    if (!resultsData) {
        alert('No results data available to export');
        return;
    }
    
    // Create a blob and download link
    const dataStr = JSON.stringify(resultsData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    
    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(dataBlob);
    downloadLink.download = 'shelf_analysis_results.json';
    
    // Trigger download
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

/**
 * Filter anomalies by severity
 */
function filterAnomaliesBySeverity(severity) {
    const anomalyItems = document.querySelectorAll('.anomaly-card');
    
    if (severity === 'all') {
        anomalyItems.forEach(item => {
            item.style.display = 'block';
        });
    } else {
        anomalyItems.forEach(item => {
            const itemSeverity = item.querySelector('small').textContent.toLowerCase();
            if (itemSeverity === severity) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }
}

/**
 * Zoom in on a specific product or anomaly
 */
function zoomToElement(x, y, width, height) {
    const imageContainer = document.querySelector('.image-container');
    const image = document.getElementById('analyzed-image');
    
    if (!imageContainer || !image) return;
    
    // Calculate the scale
    const imageRect = image.getBoundingClientRect();
    const imageNaturalWidth = image.naturalWidth;
    const imageNaturalHeight = image.naturalHeight;
    const scaleX = imageRect.width / imageNaturalWidth;
    const scaleY = imageRect.height / imageNaturalHeight;
    
    // Calculate the position
    const scaledX = x * scaleX;
    const scaledY = y * scaleY;
    const scaledWidth = width * scaleX;
    const scaledHeight = height * scaleY;
    
    // Create a highlight effect
    const highlight = document.createElement('div');
    highlight.style.position = 'absolute';
    highlight.style.left = `${scaledX}px`;
    highlight.style.top = `${scaledY}px`;
    highlight.style.width = `${scaledWidth}px`;
    highlight.style.height = `${scaledHeight}px`;
    highlight.style.border = '3px solid #ffc107';
    highlight.style.backgroundColor = 'rgba(255, 193, 7, 0.3)';
    highlight.style.zIndex = '100';
    highlight.style.animation = 'pulse 1s infinite';
    
    // Add to container
    imageContainer.appendChild(highlight);
    
    // Remove after 3 seconds
    setTimeout(() => {
        highlight.remove();
    }, 3000);
    
    // Scroll to the element
    imageContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
} 