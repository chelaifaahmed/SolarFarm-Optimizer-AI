"""
Image preprocessing utilities for satellite imagery
"""
import cv2
import numpy as np
from typing import Tuple, Optional
from pathlib import Path
from utils.logger import vision_logger


class ImagePreprocessor:
    """Preprocessing pipeline for satellite images"""
    
    def __init__(self, target_size: int = 1024):
        self.target_size = target_size
        
    def load_image(self, image_path: Path) -> np.ndarray:
        """Load image from path"""
        vision_logger.info(f"Loading image from {image_path}")
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Failed to load image from {image_path}")
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    def resize_image(self, image: np.ndarray) -> np.ndarray:
        """Resize image to target size while maintaining aspect ratio"""
        h, w = image.shape[:2]
        
        # Calculate scaling factor
        scale = self.target_size / max(h, w)
        new_w, new_h = int(w * scale), int(h * scale)
        
        # Resize
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        # Pad to square
        delta_w = self.target_size - new_w
        delta_h = self.target_size - new_h
        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)
        
        padded = cv2.copyMakeBorder(
            resized, top, bottom, left, right,
            cv2.BORDER_CONSTANT, value=[0, 0, 0]
        )
        
        return padded
    
    def enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """Apply CLAHE for contrast enhancement"""
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        return cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
    
    def normalize(self, image: np.ndarray) -> np.ndarray:
        """Normalize image to [0, 1] range"""
        return image.astype(np.float32) / 255.0
    
    def denoise(self, image: np.ndarray) -> np.ndarray:
        """Apply denoising filter"""
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    
    def extract_features(self, image: np.ndarray) -> dict:
        """Extract basic image features"""
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Calculate statistics
        mean_brightness = np.mean(gray)
        std_brightness = np.std(gray)
        
        # Edge detection
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Color distribution
        hist_r = cv2.calcHist([image], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([image], [1], None, [256], [0, 256])
        hist_b = cv2.calcHist([image], [2], None, [256], [0, 256])
        
        return {
            'mean_brightness': float(mean_brightness),
            'std_brightness': float(std_brightness),
            'edge_density': float(edge_density),
            'color_variance': {
                'r': float(np.var(hist_r)),
                'g': float(np.var(hist_g)),
                'b': float(np.var(hist_b)),
            }
        }
    
    def preprocess(
        self,
        image: np.ndarray,
        enhance: bool = True,
        denoise_img: bool = False
    ) -> Tuple[np.ndarray, dict]:
        """
        Complete preprocessing pipeline
        
        Returns:
            Tuple of (processed_image, features)
        """
        vision_logger.info("Starting image preprocessing")
        
        # Resize
        processed = self.resize_image(image)
        
        # Optional denoising
        if denoise_img:
            processed = self.denoise(processed)
        
        # Optional contrast enhancement
        if enhance:
            processed = self.enhance_contrast(processed)
        
        # Extract features
        features = self.extract_features(processed)
        
        vision_logger.info(f"Preprocessing complete. Image shape: {processed.shape}")
        return processed, features
