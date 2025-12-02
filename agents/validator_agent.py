"""
Validator Agent - Validates predictions against field data
"""
import csv
from typing import Dict, Any, List
import numpy as np
from pathlib import Path
from .base_agent import BaseAgent
from utils.logger import agent_logger


class ValidatorAgent(BaseAgent):
    """Agent responsible for validation and reality gap analysis"""
    
    def __init__(self):
        super().__init__(
            name="ValidatorAgent",
            role="Validation Specialist",
            goal="Validate predictions against field reports and quantify reality gaps"
        )
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute validation and reality gap analysis
        
        Expected inputs:
            - candidate_sites: Top N recommended sites
            - field_report_path: Path to field validation CSV (optional)
            
        Returns:
            - validation_results: Comparison results
            - reality_gap_analysis: Gap metrics and recommendations
        """
        agent_logger.info("ValidatorAgent: Starting validation")
        
        candidate_sites = inputs.get('candidate_sites', [])
        field_report_path = inputs.get('field_report_path')
        
        # Load or generate field reports
        if field_report_path and Path(field_report_path).exists():
            field_reports = self._load_field_reports(field_report_path)
        else:
            agent_logger.info("No field report found, generating simulated data")
            field_reports = self._generate_simulated_field_reports(candidate_sites)
        
        # Validate each candidate against field data
        validation_results = self._validate_candidates(candidate_sites, field_reports)
        
        # Calculate reality gap metrics
        reality_gap = self._calculate_reality_gap(validation_results)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(reality_gap)
        
        agent_logger.info("ValidatorAgent: Validation complete")
        
        return {
            'validation_results': validation_results,
            'field_reports': field_reports,
            'reality_gap_analysis': reality_gap,
            'recommendations': recommendations,
            'status': 'success'
        }
    
    def _load_field_reports(self, file_path: str) -> List[Dict]:
        """Load field reports from CSV"""
        agent_logger.info(f"Loading field reports from {file_path}")
        reports = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                for key, value in row.items():
                    try:
                        if '.' in value:
                            row[key] = float(value)
                        else:
                            row[key] = int(value)
                    except ValueError:
                        pass
                reports.append(row)
        return reports
    
    def _generate_simulated_field_reports(
        self,
        candidate_sites: List[Dict]
    ) -> List[Dict]:
        """Generate simulated field validation data"""
        
        agent_logger.info("Generating simulated field reports")
        
        reports = []
        for site in candidate_sites:
            # Simulate field measurements with some noise/variance
            predicted_score = site['score']
            
            # Add realistic variance (±10-30%)
            actual_sunlight = predicted_score * np.random.uniform(0.7, 1.1)
            
            # Simulate field observations
            report = {
                'site_id': site['id'],
                'access_road_quality': np.random.choice(['excellent', 'good', 'fair', 'poor']),
                'soil_stability': np.random.uniform(0.5, 1.0),
                'actual_sunlight_hours': actual_sunlight * 4000,  # Annual hours
                'predicted_sunlight_hours': predicted_score * 4000,
                'obstacles_found': np.random.randint(0, 5),
                'terrain_difficulty': np.random.choice(['easy', 'moderate', 'difficult']),
                'grid_connection_distance': np.random.uniform(0.5, 5.0),  # km
                'environmental_concerns': np.random.choice([True, False], p=[0.2, 0.8]),
                'actual_cost_estimate': np.random.uniform(50000, 200000),
                'predicted_cost_estimate': np.random.uniform(40000, 180000)
            }
            
            reports.append(report)
        
        return reports
    
    def _validate_candidates(
        self,
        candidate_sites: List[Dict],
        field_reports: List[Dict]
    ) -> List[Dict]:
        """Validate candidates against field reports"""
        
        validation_results = []
        
        for site in candidate_sites:
            site_id = site['id']
            
            # Find corresponding field report
            report = next((r for r in field_reports if r['site_id'] == site_id), None)
            
            if not report:
                agent_logger.warning(f"No field report for site {site_id}")
                continue
            
            # Calculate errors
            sunlight_error = abs(
                report['actual_sunlight_hours'] - 
                report['predicted_sunlight_hours']
            ) / report['predicted_sunlight_hours']
            
            cost_error = abs(
                report['actual_cost_estimate'] - 
                report['predicted_cost_estimate']
            ) / report['predicted_cost_estimate']
            
            # Adjust score based on field reality
            adjusted_score = site['score'] * (1 - sunlight_error * 0.5)
            
            # Calculate confidence
            confidence = 1.0 - (sunlight_error + cost_error) / 2
            confidence = max(0.0, min(1.0, confidence))
            
            validation_results.append({
                'site_id': site_id,
                'predicted_score': site['score'],
                'adjusted_score': adjusted_score,
                'confidence': confidence,
                'sunlight_error_percent': sunlight_error * 100,
                'cost_error_percent': cost_error * 100,
                'access_road_quality': report['access_road_quality'],
                'soil_stability': report['soil_stability'],
                'environmental_concerns': report['environmental_concerns'],
                'overall_feasibility': self._calculate_feasibility(report, adjusted_score)
            })
        
        return validation_results
    
    def _calculate_feasibility(self, report: Dict, adjusted_score: float) -> str:
        """Calculate overall feasibility rating"""
        
        feasibility_score = adjusted_score
        
        # Adjust based on field observations
        if report['access_road_quality'] == 'poor':
            feasibility_score *= 0.8
        if report['soil_stability'] < 0.6:
            feasibility_score *= 0.9
        if report['environmental_concerns']:
            feasibility_score *= 0.85
        if report['grid_connection_distance'] > 3:
            feasibility_score *= 0.9
        
        if feasibility_score > 0.8:
            return 'Highly Feasible'
        elif feasibility_score > 0.6:
            return 'Feasible'
        elif feasibility_score > 0.4:
            return 'Moderately Feasible'
        else:
            return 'Low Feasibility'
    
    def _calculate_reality_gap(self, validation_results: List[Dict]) -> Dict[str, Any]:
        """Calculate reality gap metrics"""
        
        if not validation_results:
            return {}
        
        sunlight_errors = [v['sunlight_error_percent'] for v in validation_results]
        cost_errors = [v['cost_error_percent'] for v in validation_results]
        confidences = [v['confidence'] for v in validation_results]
        
        gap_analysis = {
            'average_sunlight_error': np.mean(sunlight_errors),
            'max_sunlight_error': np.max(sunlight_errors),
            'min_sunlight_error': np.min(sunlight_errors),
            'average_cost_error': np.mean(cost_errors),
            'max_cost_error': np.max(cost_errors),
            'min_cost_error': np.min(cost_errors),
            'average_confidence': np.mean(confidences),
            'high_confidence_sites': sum(1 for c in confidences if c > 0.7),
            'low_confidence_sites': sum(1 for c in confidences if c < 0.5)
        }
        
        # Calculate improvement potential
        baseline_error = 35.0  # Assume 35% baseline error
        current_error = gap_analysis['average_sunlight_error']
        improvement = ((baseline_error - current_error) / baseline_error) * 100
        
        gap_analysis['error_reduction_vs_baseline'] = improvement
        
        return gap_analysis
    
    def _generate_recommendations(self, reality_gap: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on reality gap"""
        
        recommendations = []
        
        avg_error = reality_gap.get('average_sunlight_error', 0)
        
        if avg_error > 25:
            recommendations.append(
                "High sunlight prediction error detected. Consider improving shadow prediction model."
            )
        
        if avg_error > 20:
            recommendations.append(
                "Recommend on-site validation before final site selection."
            )
        
        cost_error = reality_gap.get('average_cost_error', 0)
        if cost_error > 30:
            recommendations.append(
                "Significant cost estimation variance. Update cost models with local market data."
            )
        
        low_conf_sites = reality_gap.get('low_confidence_sites', 0)
        if low_conf_sites > 0:
            recommendations.append(
                f"{low_conf_sites} sites have low confidence. Conduct detailed site surveys."
            )
        
        if reality_gap.get('error_reduction_vs_baseline', 0) > 15:
            recommendations.append(
                "Strong performance vs baseline. Multi-agent approach is effective."
            )
        
        if not recommendations:
            recommendations.append("All predictions within acceptable ranges. Proceed with implementation.")
        
        return recommendations
