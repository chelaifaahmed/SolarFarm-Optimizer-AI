"""
Sunlight and shadow prediction
"""
import numpy as np
import cv2
from typing import Dict, Tuple
from datetime import datetime, timedelta
import math
from utils.logger import vision_logger


class SunlightPredictor:
    """Predict sunlight hours and shadow patterns"""
    
    def __init__(self, latitude: float = 40.7128, longitude: float = -74.0060):
        self.latitude = latitude
        self.longitude = longitude
        vision_logger.info(f"Initialized SunlightPredictor for lat={latitude}, lon={longitude}")
    
    def calculate_sun_position(
        self,
        date: datetime,
        hour: int
    ) -> Tuple[float, float]:
        """
        Calculate sun azimuth and elevation angles
        
        Returns:
            Tuple of (azimuth, elevation) in degrees
        """
        # Day of year
        day_of_year = date.timetuple().tm_yday
        
        # Declination angle
        declination = 23.45 * math.sin(math.radians((360/365) * (day_of_year - 81)))
        
        # Hour angle (15 degrees per hour from solar noon)
        hour_angle = 15 * (hour - 12)
        
        # Convert to radians
        lat_rad = math.radians(self.latitude)
        dec_rad = math.radians(declination)
        hour_rad = math.radians(hour_angle)
        
        # Elevation angle
        elevation = math.degrees(math.asin(
            math.sin(lat_rad) * math.sin(dec_rad) +
            math.cos(lat_rad) * math.cos(dec_rad) * math.cos(hour_rad)
        ))
        
        # Azimuth angle
        azimuth = math.degrees(math.atan2(
            math.sin(hour_rad),
            math.cos(hour_rad) * math.sin(lat_rad) - math.tan(dec_rad) * math.cos(lat_rad)
        ))
        
        return azimuth, elevation
    
    def predict_shadow_map(
        self,
        terrain_segments: Dict,
        image_shape: Tuple[int, int]
    ) -> np.ndarray:
        """
        Predict shadow areas based on terrain and sun position
        
        Returns:
            Shadow probability map (0-1)
        """
        vision_logger.info("Predicting shadow map")
        
        h, w = image_shape[:2]
        shadow_map = np.zeros((h, w), dtype=np.float32)
        
        # Get current date and time
        now = datetime.now()
        
        # Calculate average shadow throughout the day
        for hour in range(6, 20):  # 6 AM to 8 PM
            azimuth, elevation = self.calculate_sun_position(now, hour)
            
            # Skip nighttime (sun below horizon)
            if elevation < 0:
                continue
            
            # Calculate shadow direction
            shadow_length = 1.0 / max(math.tan(math.radians(elevation)), 0.1)
            shadow_dx = shadow_length * math.cos(math.radians(azimuth))
            shadow_dy = shadow_length * math.sin(math.radians(azimuth))
            
            # Cast shadows from obstacles
            if 'building' in terrain_segments:
                for building in terrain_segments['building']:
                    center = building['center']
                    # Simple shadow projection
                    shadow_center_x = int(center[0] + shadow_dx * 50)
                    shadow_center_y = int(center[1] + shadow_dy * 50)
                    
                    # Draw shadow ellipse
                    if 0 <= shadow_center_x < w and 0 <= shadow_center_y < h:
                        cv2.ellipse(
                            shadow_map,
                            (shadow_center_x, shadow_center_y),
                            (30, 20),
                            0, 0, 360,
                            0.1,
                            -1
                        )
        
        # Add existing shadows from terrain classification
        if 'shadow' in terrain_segments:
            for shadow in terrain_segments['shadow']:
                bbox = shadow['bbox']
                shadow_map[bbox[1]:bbox[3], bbox[0]:bbox[2]] += 0.3
        
        # Normalize to [0, 1]
        shadow_map = np.clip(shadow_map, 0, 1)
        
        return shadow_map
    
    def calculate_annual_sunlight_hours(
        self,
        shadow_map: np.ndarray
    ) -> np.ndarray:
        """
        Calculate estimated annual sunlight hours for each pixel
        
        Returns:
            Array with annual sunlight hours per pixel
        """
        vision_logger.info("Calculating annual sunlight hours")
        
        # Maximum possible sunlight hours per year
        # Assuming 12 hours average daylight per day
        max_hours_per_year = 12 * 365
        
        # Reduce by shadow probability
        sunlight_hours = max_hours_per_year * (1 - shadow_map)
        
        return sunlight_hours
    
    def generate_sunlight_heatmap(
        self,
        sunlight_hours: np.ndarray
    ) -> np.ndarray:
        """
        Generate color-coded heatmap of sunlight hours
        
        Returns:
            RGB heatmap image
        """
        # Normalize to 0-255
        normalized = ((sunlight_hours / sunlight_hours.max()) * 255).astype(np.uint8)
        
        # Apply colormap (hot: red = high sunlight, blue = low sunlight)
        heatmap = cv2.applyColorMap(normalized, cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        
        return heatmap
    
    def analyze_sunlight(
        self,
        image: np.ndarray,
        terrain_segments: Dict
    ) -> Dict:
        """
        Complete sunlight analysis
        
        Returns:
            Dictionary with sunlight analysis results
        """
        vision_logger.info("Starting sunlight analysis")
        
        # Predict shadow map
        shadow_map = self.predict_shadow_map(terrain_segments, image.shape)
        
        # Calculate sunlight hours
        sunlight_hours = self.calculate_annual_sunlight_hours(shadow_map)
        
        # Generate heatmap
        heatmap = self.generate_sunlight_heatmap(sunlight_hours)
        
        # Calculate statistics
        mean_sunlight = float(np.mean(sunlight_hours))
        max_sunlight = float(np.max(sunlight_hours))
        min_sunlight = float(np.min(sunlight_hours))
        std_sunlight = float(np.std(sunlight_hours))
        
        # Find optimal zones (>80% of max sunlight)
        optimal_threshold = max_sunlight * 0.8
        optimal_zones = sunlight_hours > optimal_threshold
        optimal_area_percentage = float(np.sum(optimal_zones) / optimal_zones.size * 100)
        
        vision_logger.info(f"Mean annual sunlight: {mean_sunlight:.2f} hours")
        vision_logger.info(f"Optimal area coverage: {optimal_area_percentage:.2f}%")
        
        return {
            'shadow_map': shadow_map,
            'sunlight_hours': sunlight_hours,
            'heatmap': heatmap,
            'statistics': {
                'mean': mean_sunlight,
                'max': max_sunlight,
                'min': min_sunlight,
                'std': std_sunlight,
                'optimal_area_percentage': optimal_area_percentage
            },
            'optimal_zones': optimal_zones
        }
