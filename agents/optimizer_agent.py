"""
Optimizer Agent - Uses genetic algorithms to find optimal solar panel placements
"""
from typing import Dict, Any, List, Tuple
import numpy as np

from .base_agent import BaseAgent
from utils.logger import agent_logger


class OptimizerAgent(BaseAgent):
    """Agent responsible for optimization using genetic algorithms"""
    
    def __init__(self):
        super().__init__(
            name="OptimizerAgent",
            role="Optimization Specialist",
            goal="Find optimal solar panel placements maximizing energy yield while respecting constraints"
        )
        self.population_size = 1000
        self.max_generations = 50
        self.top_n = 10
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute optimization algorithm
        
        Expected inputs:
            - processed_image: Image for dimension reference
            - terrain_segments: Terrain classification results
            - obstacles: Detected obstacles
            - sunlight_analysis: Sunlight prediction results
            - geospatial_data: Geographic and environmental data
            
        Returns:
            - candidate_sites: List of top N candidate sites
            - optimization_metrics: Optimization performance metrics
        """
        agent_logger.info("OptimizerAgent: Starting site optimization")
        
        # Extract inputs
        processed_image = inputs.get('processed_image')
        terrain_segments = inputs.get('terrain_segments', {})
        obstacles = inputs.get('obstacles', [])
        sunlight_analysis = inputs.get('sunlight_analysis', {})
        geospatial_data = inputs.get('geospatial_data', {})
        
        if processed_image is None:
            raise ValueError("processed_image is required")
        
        # Generate candidate sites
        agent_logger.info("OptimizerAgent: Generating candidate sites")
        candidate_sites = self._generate_candidate_sites(
            processed_image.shape,
            self.population_size
        )
        
        # Score each candidate
        agent_logger.info("OptimizerAgent: Scoring candidates")
        scored_sites = self._score_candidates(
            candidate_sites,
            terrain_segments,
            obstacles,
            sunlight_analysis,
            geospatial_data,
            processed_image.shape
        )
        
        # Optimize using genetic algorithm
        agent_logger.info("OptimizerAgent: Running genetic optimization")
        optimized_sites = self._genetic_optimization(
            scored_sites,
            processed_image.shape
        )
        
        # Select top N sites
        top_sites = sorted(optimized_sites, key=lambda x: x['score'], reverse=True)[:self.top_n]
        
        agent_logger.info(f"OptimizerAgent: Selected top {len(top_sites)} sites")
        
        # Calculate metrics
        metrics = self._calculate_metrics(top_sites, scored_sites)
        
        return {
            'candidate_sites': top_sites,
            'all_candidates': scored_sites,
            'optimization_metrics': metrics,
            'status': 'success'
        }
    
    def _generate_candidate_sites(
        self,
        image_shape: Tuple[int, int, int],
        n_sites: int
    ) -> List[Dict[str, Any]]:
        """Generate random candidate sites"""
        
        h, w = image_shape[:2]
        sites = []
        
        for i in range(n_sites):
            # Random center point
            center_x = np.random.randint(50, w - 50)
            center_y = np.random.randint(50, h - 50)
            
            # Random area (1000 to 10000 square meters)
            area = np.random.uniform(1000, 10000)
            
            # Calculate width and height (assuming square to rectangular)
            aspect_ratio = np.random.uniform(0.8, 2.0)
            width = int(np.sqrt(area * aspect_ratio))
            height = int(area / width)
            
            sites.append({
                'id': i,
                'center': [center_x, center_y],
                'width': width,
                'height': height,
                'area': area,
                'rotation': np.random.uniform(0, 360)
            })
        
        return sites
    
    def _score_candidates(
        self,
        candidates: List[Dict],
        terrain_segments: Dict,
        obstacles: List[Dict],
        sunlight_analysis: Dict,
        geospatial_data: Dict,
        image_shape: Tuple[int, int, int]
    ) -> List[Dict]:
        """Score each candidate site"""
        
        sunlight_hours = sunlight_analysis.get('sunlight_hours', np.zeros(image_shape[:2]))
        
        scored = []
        
        for candidate in candidates:
            score_components = {}
            
            # 1. Sunlight score (40% weight)
            sunlight_score = self._calculate_sunlight_score(
                candidate, sunlight_hours
            )
            score_components['sunlight'] = sunlight_score
            
            # 2. Terrain suitability (25% weight)
            terrain_score = self._calculate_terrain_score(
                candidate, terrain_segments
            )
            score_components['terrain'] = terrain_score
            
            # 3. Obstacle avoidance (20% weight)
            obstacle_score = self._calculate_obstacle_score(
                candidate, obstacles
            )
            score_components['obstacles'] = obstacle_score
            
            # 4. Accessibility (10% weight)
            access_score = self._calculate_accessibility_score(
                candidate, geospatial_data
            )
            score_components['accessibility'] = access_score
            
            # 5. Cost efficiency (5% weight)
            cost_score = self._calculate_cost_score(
                candidate, geospatial_data
            )
            score_components['cost'] = cost_score
            
            # Calculate weighted total score
            total_score = (
                0.40 * sunlight_score +
                0.25 * terrain_score +
                0.20 * obstacle_score +
                0.10 * access_score +
                0.05 * cost_score
            )
            
            candidate['score'] = total_score
            candidate['score_components'] = score_components
            scored.append(candidate)
        
        return scored
    
    def _calculate_sunlight_score(
        self,
        site: Dict,
        sunlight_hours: np.ndarray
    ) -> float:
        """Calculate sunlight score for a site"""
        
        center = site['center']
        width = site['width']
        height = site['height']
        
        # Get bounding box
        x1 = max(0, center[0] - width // 2)
        x2 = min(sunlight_hours.shape[1], center[0] + width // 2)
        y1 = max(0, center[1] - height // 2)
        y2 = min(sunlight_hours.shape[0], center[1] + height // 2)
        
        # Calculate average sunlight in this area
        if x2 > x1 and y2 > y1:
            area_sunlight = sunlight_hours[y1:y2, x1:x2]
            avg_sunlight = np.mean(area_sunlight)
            max_sunlight = np.max(sunlight_hours)
            
            if max_sunlight > 0:
                return avg_sunlight / max_sunlight
        
        return 0.5
    
    def _calculate_terrain_score(
        self,
        site: Dict,
        terrain_segments: Dict
    ) -> float:
        """Calculate terrain suitability score"""
        
        # Prefer bare land and avoid water/buildings
        score = 0.7  # Default score
        
        center = site['center']
        
        # Check if site overlaps with good terrain
        for bare_land in terrain_segments.get('bare_land', []):
            if self._point_in_bbox(center, bare_land['bbox']):
                score = 0.9
                break
        
        # Penalize if overlapping with bad terrain
        for water in terrain_segments.get('water', []):
            if self._point_in_bbox(center, water['bbox']):
                score = 0.1
                break
        
        for building in terrain_segments.get('building', []):
            if self._point_in_bbox(center, building['bbox']):
                score = 0.2
                break
        
        return score
    
    def _calculate_obstacle_score(
        self,
        site: Dict,
        obstacles: List[Dict]
    ) -> float:
        """Calculate obstacle avoidance score"""
        
        center = site['center']
        min_distance = float('inf')
        
        for obstacle in obstacles:
            obs_center = obstacle['center']
            distance = np.sqrt(
                (center[0] - obs_center[0])**2 +
                (center[1] - obs_center[1])**2
            )
            min_distance = min(min_distance, distance)
        
        # Score decreases as we get closer to obstacles
        if min_distance == float('inf'):
            return 1.0
        
        return min(1.0, min_distance / 100.0)
    
    def _calculate_accessibility_score(
        self,
        site: Dict,
        geospatial_data: Dict
    ) -> float:
        """Calculate accessibility score"""
        
        # Use slope as a proxy for accessibility
        slope = geospatial_data.get('slope', 5)
        
        # Prefer flatter terrain (slope < 5 degrees)
        if slope < 5:
            return 1.0
        elif slope < 10:
            return 0.7
        elif slope < 15:
            return 0.4
        else:
            return 0.2
    
    def _calculate_cost_score(
        self,
        site: Dict,
        geospatial_data: Dict
    ) -> float:
        """Calculate cost efficiency score"""
        
        # Larger sites are more cost-efficient
        area = site['area']
        
        if area > 8000:
            return 1.0
        elif area > 5000:
            return 0.8
        elif area > 3000:
            return 0.6
        else:
            return 0.4
    
    def _genetic_optimization(
        self,
        candidates: List[Dict],
        image_shape: Tuple[int, int, int]
    ) -> List[Dict]:
        """Apply genetic algorithm to refine candidates"""
        
        agent_logger.info("Running genetic algorithm")
        
        # Simple genetic algorithm: selection, crossover, mutation
        population = candidates.copy()
        
        for generation in range(min(10, self.max_generations)):
            # Selection: Keep top 50%
            population.sort(key=lambda x: x['score'], reverse=True)
            survivors = population[:len(population)//2]
            
            # Crossover and mutation to create new generation
            offspring = []
            for i in range(len(population) - len(survivors)):
                # Select two random parents
                parent1 = survivors[np.random.randint(len(survivors))]
                parent2 = survivors[np.random.randint(len(survivors))]
                
                # Crossover
                child = {
                    'id': len(candidates) + i,
                    'center': [
                        int((parent1['center'][0] + parent2['center'][0]) / 2),
                        int((parent1['center'][1] + parent2['center'][1]) / 2)
                    ],
                    'width': int((parent1['width'] + parent2['width']) / 2),
                    'height': int((parent1['height'] + parent2['height']) / 2),
                    'area': (parent1['area'] + parent2['area']) / 2,
                    'rotation': (parent1['rotation'] + parent2['rotation']) / 2
                }
                
                # Mutation (10% chance)
                if np.random.random() < 0.1:
                    child['center'][0] += np.random.randint(-20, 20)
                    child['center'][1] += np.random.randint(-20, 20)
                
                # Rescore
                child['score'] = parent1['score'] * 0.95  # Approximate score
                
                offspring.append(child)
            
            population = survivors + offspring
        
        return population
    
    def _point_in_bbox(self, point: List[int], bbox: List[int]) -> bool:
        """Check if point is inside bounding box"""
        return (bbox[0] <= point[0] <= bbox[2] and
                bbox[1] <= point[1] <= bbox[3])
    
    def _calculate_metrics(
        self,
        top_sites: List[Dict],
        all_sites: List[Dict]
    ) -> Dict[str, Any]:
        """Calculate optimization metrics"""
        
        avg_score = np.mean([s['score'] for s in top_sites])
        min_score = np.min([s['score'] for s in top_sites])
        max_score = np.max([s['score'] for s in top_sites])
        
        return {
            'average_score': float(avg_score),
            'min_score': float(min_score),
            'max_score': float(max_score),
            'total_candidates_evaluated': len(all_sites),
            'top_candidates_selected': len(top_sites)
        }
