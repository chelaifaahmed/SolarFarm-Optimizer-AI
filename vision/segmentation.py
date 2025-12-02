"""
Terrain segmentation using Segment Anything Model (SAM)
"""
import numpy as np
import cv2
from typing import List, Dict, Optional, Tuple
from pathlib import Path
try:
    import torch
except ImportError:
    torch = None
from utils.logger import vision_logger


class TerrainSegmenter:
    """SAM-based terrain segmentation"""
    
    def __init__(self, checkpoint_path: Optional[str] = None):
        self.checkpoint_path = checkpoint_path
        if torch and torch.cuda.is_available():
            self.device = "cuda"
        else:
            self.device = "cpu"
        self.model = None
        vision_logger.info(f"Initializing TerrainSegmenter on {self.device}")
        
    def load_model(self):
        """Load SAM model - simplified version for demo"""
        vision_logger.info("Loading segmentation model (simplified)")
        # Note: Full SAM integration would require downloading the model
        # For this prototype, we'll use traditional CV methods as fallback
        self.model = "opencv_fallback"
        
    def segment_using_watershed(self, image: np.ndarray) -> np.ndarray:
        """Fallback segmentation using watershed algorithm"""
        vision_logger.info("Using watershed segmentation")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Apply Otsu's thresholding
        ret, thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )
        
        # Noise removal
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # Sure background area
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        
        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        
        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        
        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)
        
        # Add one to all labels so that sure background is not 0, but 1
        markers = markers + 1
        
        # Mark the region of unknown with zero
        markers[unknown == 255] = 0
        
        # Apply watershed
        image_copy = image.copy()
        markers = cv2.watershed(image_copy, markers)
        
        return markers
    
    def classify_segments(
        self,
        image: np.ndarray,
        segments: np.ndarray
    ) -> Dict[str, List[Dict]]:
        """
        Classify segments into terrain types based on color/texture
        
        Returns:
            Dictionary mapping terrain types to segment info
        """
        vision_logger.info("Classifying terrain segments")
        
        terrain_classes = {
            'vegetation': [],
            'water': [],
            'building': [],
            'road': [],
            'bare_land': [],
            'shadow': []
        }
        
        unique_segments = np.unique(segments)
        
        for seg_id in unique_segments:
            if seg_id <= 0:  # Skip background
                continue
            
            # Create mask for this segment
            mask = (segments == seg_id).astype(np.uint8)
            
            # Calculate area
            area = np.sum(mask)
            if area < 100:  # Skip very small segments
                continue
            
            # Extract segment pixels
            segment_pixels = image[mask > 0]
            
            # Calculate mean color
            mean_color = np.mean(segment_pixels, axis=0)
            std_color = np.std(segment_pixels, axis=0)
            
            # Calculate brightness
            brightness = np.mean(mean_color)
            
            # Get bounding box
            coords = np.column_stack(np.where(mask > 0))
            y_min, x_min = coords.min(axis=0)
            y_max, x_max = coords.max(axis=0)
            
            segment_info = {
                'id': int(seg_id),
                'area': int(area),
                'mean_color': mean_color.tolist(),
                'std_color': std_color.tolist(),
                'brightness': float(brightness),
                'bbox': [int(x_min), int(y_min), int(x_max), int(y_max)],
                'center': [int((x_min + x_max) / 2), int((y_min + y_max) / 2)]
            }
            
            # Simple classification based on color heuristics
            r, g, b = mean_color
            
            # Vegetation: High green
            if g > r and g > b and g > 100:
                terrain_classes['vegetation'].append(segment_info)
            
            # Water: High blue
            elif b > r and b > g and b > 80:
                terrain_classes['water'].append(segment_info)
            
            # Shadow: Low brightness
            elif brightness < 60:
                terrain_classes['shadow'].append(segment_info)
            
            # Road/Building: Gray tones (r≈g≈b)
            elif abs(r - g) < 20 and abs(g - b) < 20:
                if brightness > 120:
                    terrain_classes['building'].append(segment_info)
                else:
                    terrain_classes['road'].append(segment_info)
            
            # Bare land: Everything else
            else:
                terrain_classes['bare_land'].append(segment_info)
        
        # Log statistics
        for terrain_type, segments_list in terrain_classes.items():
            vision_logger.info(f"Found {len(segments_list)} {terrain_type} segments")
        
        return terrain_classes
    
    def segment_image(self, image: np.ndarray) -> Dict[str, any]:
        """
        Main segmentation method
        
        Returns:
            Dictionary with segmentation results
        """
        if self.model is None:
            self.load_model()
        
        vision_logger.info("Starting terrain segmentation")
        
        # Perform segmentation
        segments = self.segment_using_watershed(image)
        
        # Classify segments
        terrain_classes = self.classify_segments(image, segments)
        
        # Create visualization
        visualization = self.create_visualization(image, segments, terrain_classes)
        
        return {
            'segments': segments,
            'terrain_classes': terrain_classes,
            'visualization': visualization,
            'total_segments': len(np.unique(segments)) - 1  # Exclude background
        }
    
    def create_visualization(
        self,
        image: np.ndarray,
        segments: np.ndarray,
        terrain_classes: Dict[str, List[Dict]]
    ) -> np.ndarray:
        """Create colored visualization of segmented terrain"""
        
        # Define colors for each terrain type
        colors = {
            'vegetation': [34, 139, 34],      # Forest green
            'water': [0, 119, 190],           # Ocean blue
            'building': [178, 34, 34],        # Brick red
            'road': [128, 128, 128],          # Gray
            'bare_land': [210, 180, 140],     # Tan
            'shadow': [47, 79, 79]            # Dark slate gray
        }
        
        # Create color overlay
        overlay = image.copy()
        alpha = 0.4
        
        for terrain_type, segments_list in terrain_classes.items():
            color = colors.get(terrain_type, [255, 255, 255])
            for segment in segments_list:
                mask = (segments == segment['id']).astype(np.uint8)
                colored_mask = np.zeros_like(image)
                colored_mask[mask > 0] = color
                overlay = cv2.addWeighted(overlay, 1, colored_mask, alpha, 0)
        
        return overlay
