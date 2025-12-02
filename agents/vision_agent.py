"""
Vision Agent - Performs image analysis using computer vision
"""
from typing import Dict, Any
import numpy as np
from .base_agent import BaseAgent
from vision import ImagePreprocessor, TerrainSegmenter, ObstacleDetector, SunlightPredictor
from utils.logger import agent_logger


class VisionAgent(BaseAgent):
    """Agent responsible for vision AI processing"""
    
    def __init__(self):
        super().__init__(
            name="VisionAgent",
            role="Computer Vision Specialist",
            goal="Analyze satellite imagery to identify terrain features, obstacles, and sunlight patterns"
        )
        
        # Initialize vision components
        self.preprocessor = ImagePreprocessor()
        self.segmenter = TerrainSegmenter()
        self.detector = ObstacleDetector()
        self.sunlight_predictor = None  # Will be initialized with geo data
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute vision AI pipeline
        
        Expected inputs:
            - raw_image: Input image to analyze
            - geospatial_data: Geographic information
            
        Returns:
            - processed_image: Preprocessed image
            - terrain_segments: Segmented terrain classes
            - obstacles: Detected obstacles
            - sunlight_analysis: Sunlight and shadow prediction
        """
        agent_logger.info("VisionAgent: Starting image analysis")
        
        raw_image = inputs.get('raw_image')
        geospatial_data = inputs.get('geospatial_data', {})
        
        if raw_image is None:
            raise ValueError("raw_image is required")
        
        # Step 1: Preprocess image
        agent_logger.info("VisionAgent: Preprocessing image")
        processed_image, features = self.preprocessor.preprocess(
            raw_image,
            enhance=True,
            denoise_img=False
        )
        
        # Step 2: Segment terrain
        agent_logger.info("VisionAgent: Segmenting terrain")
        segmentation_result = self.segmenter.segment_image(processed_image)
        
        # Step 3: Detect obstacles
        agent_logger.info("VisionAgent: Detecting obstacles")
        detection_result = self.detector.detect_obstacles(processed_image)
        
        # Step 4: Analyze sunlight
        agent_logger.info("VisionAgent: Analyzing sunlight patterns")
        
        # Initialize sunlight predictor with coordinates
        coords = geospatial_data.get('coordinates', {})
        self.sunlight_predictor = SunlightPredictor(
            latitude=coords.get('latitude', 40.7128),
            longitude=coords.get('longitude', -74.0060)
        )
        
        sunlight_analysis = self.sunlight_predictor.analyze_sunlight(
            processed_image,
            segmentation_result['terrain_classes']
        )
        
        agent_logger.info("VisionAgent: Analysis complete")
        
        return {
            'processed_image': processed_image,
            'image_features': features,
            'terrain_segments': segmentation_result['terrain_classes'],
            'segmentation_visualization': segmentation_result['visualization'],
            'obstacles': detection_result['detections'],
            'obstacle_visualization': detection_result['visualization'],
            'obstacle_density': detection_result['obstacle_density'],
            'sunlight_analysis': sunlight_analysis,
            'status': 'success'
        }
