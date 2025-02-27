import numpy as np
import cv2
import os

# Create directory if it doesn't exist
os.makedirs('app/static/sample', exist_ok=True)

# Create a blank image (800x600, RGB)
img = np.ones((600, 800, 3), dtype=np.uint8) * 255

# Draw some rectangles to simulate products on a shelf
colors = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (128, 0, 0),    # Maroon
    (0, 128, 0),    # Dark Green
    (0, 0, 128),    # Navy
    (128, 128, 0)   # Olive
]

# Draw shelves (horizontal lines)
for i in range(1, 5):
    y = i * 120
    cv2.line(img, (0, y), (800, y), (200, 200, 200), 5)

# Draw products on shelves
product_positions = [
    (50, 30, 100, 80),    # (x, y, width, height)
    (200, 30, 120, 80),
    (370, 30, 90, 80),
    (510, 30, 110, 80),
    (670, 30, 80, 80),
    (50, 150, 100, 80),
    (200, 150, 120, 80),
    (370, 150, 90, 80),
    (510, 150, 110, 80),
    (670, 150, 80, 80),
    (50, 270, 100, 80),
    (200, 270, 120, 80),
    (370, 270, 90, 80),
    (510, 270, 110, 80),
    (670, 270, 80, 80),
    (50, 390, 100, 80),
    (200, 390, 120, 80),
    (370, 390, 90, 80),
    (510, 390, 110, 80),
    (670, 390, 80, 80),
    (50, 510, 100, 80),
    (200, 510, 120, 80),
    (370, 510, 90, 80),
    (510, 510, 110, 80),
    (670, 510, 80, 80)
]

for i, (x, y, w, h) in enumerate(product_positions):
    color = colors[i % len(colors)]
    cv2.rectangle(img, (x, y), (x+w, y+h), color, -1)
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 0), 2)
    
    # Add some text to simulate product labels
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, f'P{i+1}', (x+w//2-10, y+h//2+5), font, 0.7, (255, 255, 255), 2)

# Add some text
cv2.putText(img, 'Sample Shelf Image', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

# Save the image
cv2.imwrite('app/static/sample/shelf_image.jpg', img)
print("Sample image created at app/static/sample/shelf_image.jpg") 