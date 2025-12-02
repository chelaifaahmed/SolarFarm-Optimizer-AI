"""
Data Agent - Handles geospatial data ingestion and preprocessing
"""
import numpy as np
from typing import Dict, Any
from pathlib import Path
from .base_agent import BaseAgent
from utils.logger import agent_logger


class DataAgent(BaseAgent):
    """Agent responsible for data acquisition and preprocessing"""
    
    def __init__(self):
        super().__init__(
            name="DataAgent",
            role="Geospatial Data Specialist",
            goal="Acquire and preprocess satellite imagery and geospatial data"
        )
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute data acquisition and preprocessing
        
        Expected inputs:
            - image_path: Path to satellite image
            - coordinates: Optional geo-coordinates
            
        Returns:
            - raw_image: Loaded image
            - metadata: Image metadata
            - geospatial_data: Extracted geospatial information
        """
        agent_logger.info("DataAgent: Starting data acquisition")
        
        image_path = inputs.get('image_path')
        if not image_path:
            raise ValueError("image_path is required")
        
        # Load image
        import cv2
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Failed to load image from {image_path}")
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Extract metadata
        metadata = self._extract_metadata(image, image_path)
        
        # Simulate geospatial data extraction
        geospatial_data = self._extract_geospatial_data(inputs.get('coordinates'))
        
        agent_logger.info(f"DataAgent: Loaded image {image.shape}")
        
        return {
            'raw_image': image,
            'metadata': metadata,
            'geospatial_data': geospatial_data,
            'status': 'success'
        }
    
    def _extract_metadata(self, image: np.ndarray, image_path: str) -> Dict[str, Any]:
        """Extract image metadata"""
        return {
            'shape': image.shape,
            'size': image.size,
            'dtype': str(image.dtype),
            'source': str(image_path),
            'channels': image.shape[2] if len(image.shape) > 2 else 1
        }
    
    def _extract_geospatial_data(self, coordinates: Any) -> Dict[str, Any]:
        """Extract or generate geospatial data"""
        
        # Default coordinates (NYC area) if not provided
        if coordinates is None:
            coordinates = {
                'latitude': 40.7128,
                'longitude': -74.0060,
                'bbox': [40.7028, -74.0160, 40.7228, -73.9960]
            }
        
        # Simulate population density data
        population_density = np.random.uniform(50, 500)
        
        # Simulate land use data
        land_use = {
            'residential': np.random.uniform(0.1, 0.4),
            'commercial': np.random.uniform(0.05, 0.2),
            'industrial': np.random.uniform(0.05, 0.15),
            'agricultural': np.random.uniform(0.2, 0.5),
            'undeveloped': np.random.uniform(0.1, 0.3)
        }
        
        return {
            'coordinates': coordinates,
            'population_density': population_density,
            'land_use': land_use,
            'elevation': np.random.uniform(0, 200),  # meters
            'slope': np.random.uniform(0, 15)  # degrees
        }
