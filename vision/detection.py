"""
Obstacle detection using YOLO
"""
import cv2
import numpy as np
from typing import List, Dict, Tuple
from pathlib import Path
from utils.logger import vision_logger


class ObstacleDetector:
    """YOLO-based obstacle detection for solar farm planning"""
    
    # COCO class names relevant to solar farm planning
    OBSTACLE_CLASSES = {
        'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
        'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
        'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe',
        'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
        'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
        'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
        'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
        'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
        'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
        'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
        'toothbrush'
    }
    
    def __init__(self, model_path: str = "yolov8x.pt", confidence: float = 0.5):
        self.model_path = model_path
        self.confidence = confidence
        self.model = None
        vision_logger.info("Initializing ObstacleDetector")
        
    def load_model(self):
        """Load YOLO model - using OpenCV DNN as fallback"""
        vision_logger.info("Loading obstacle detection model")
        
        try:
            # Try to use ultralytics YOLO
            from ultralytics import YOLO
            self.model = YOLO(self.model_path)
            vision_logger.info("Loaded YOLO model successfully")
        except Exception as e:
            vision_logger.warning(f"Could not load YOLO model: {e}. Using fallback detector")
            self.model = None
    
    def detect_with_traditional_cv(self, image: np.ndarray) -> List[Dict]:
        """Fallback detection using traditional CV methods"""
        vision_logger.info("Using traditional CV for obstacle detection")
        
        detections = []
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Filter and classify contours
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            
            # Filter small contours
            if area < 500:
                continue
            
            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)
            
            # Calculate aspect ratio
            aspect_ratio = float(w) / h if h > 0 else 0
            
            # Simple classification based on shape
            if 0.8 < aspect_ratio < 1.2:
                class_name = "building"
            elif aspect_ratio > 2:
                class_name = "road"
            else:
                class_name = "unknown_obstacle"
            
            detections.append({
                'class': class_name,
                'confidence': 0.7,  # Mock confidence
                'bbox': [int(x), int(y), int(x + w), int(y + h)],
                'center': [int(x + w/2), int(y + h/2)],
                'area': int(area),
                'aspect_ratio': float(aspect_ratio)
            })
        
        vision_logger.info(f"Detected {len(detections)} obstacles using CV")
        return detections
    
    def detect_obstacles(self, image: np.ndarray) -> Dict:
        """
        Detect obstacles in image
        
        Returns:
            Dictionary with detection results
        """
        if self.model is None:
            self.load_model()
        
        vision_logger.info("Starting obstacle detection")
        
        detections = []
        
        if self.model is not None and hasattr(self.model, 'predict'):
            try:
                # Use YOLO model
                results = self.model.predict(
                    image,
                    conf=self.confidence,
                    verbose=False
                )
                
                # Parse results
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        conf = float(box.conf[0])
                        cls = int(box.cls[0])
                        class_name = result.names[cls]
                        
                        detections.append({
                            'class': class_name,
                            'confidence': conf,
                            'bbox': [int(x1), int(y1), int(x2), int(y2)],
                            'center': [int((x1 + x2) / 2), int((y1 + y2) / 2)],
                            'area': int((x2 - x1) * (y2 - y1))
                        })
                
                vision_logger.info(f"YOLO detected {len(detections)} obstacles")
            except Exception as e:
                vision_logger.error(f"YOLO detection failed: {e}. Using fallback.")
                detections = self.detect_with_traditional_cv(image)
        else:
            # Use fallback
            detections = self.detect_with_traditional_cv(image)
        
        # Create visualization
        visualization = self.visualize_detections(image, detections)
        
        # Calculate obstacle density
        obstacle_density = self._calculate_density(detections, image.shape)
        
        return {
            'detections': detections,
            'visualization': visualization,
            'total_obstacles': len(detections),
            'obstacle_density': obstacle_density
        }
    
    def visualize_detections(
        self,
        image: np.ndarray,
        detections: List[Dict]
    ) -> np.ndarray:
        """Draw bounding boxes on image"""
        
        vis_image = image.copy()
        
        for detection in detections:
            bbox = detection['bbox']
            class_name = detection['class']
            confidence = detection.get('confidence', 0.0)
            
            # Draw bounding box
            cv2.rectangle(
                vis_image,
                (bbox[0], bbox[1]),
                (bbox[2], bbox[3]),
                (255, 0, 0),
                2
            )
            
            # Draw label
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(
                vis_image,
                label,
                (bbox[0], bbox[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                2
            )
        
        return vis_image
    
    def _calculate_density(
        self,
        detections: List[Dict],
        image_shape: Tuple[int, int, int]
    ) -> float:
        """Calculate obstacle density per square meter"""
        h, w = image_shape[:2]
        total_area = h * w
        
        if total_area == 0:
            return 0.0
        
        obstacle_area = sum(d.get('area', 0) for d in detections)
        return obstacle_area / total_area
