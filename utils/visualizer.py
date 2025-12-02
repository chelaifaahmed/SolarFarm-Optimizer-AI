"""
Visualization utilities for solar farm optimization
"""
import numpy as np
import cv2
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import folium
from typing import Dict, Any, List
from pathlib import Path


class SolarFarmVisualizer:
    """Create interactive visualizations for results"""
    
    def __init__(self):
        self.color_scheme = {
            'primary': '#FF6B35',
            'secondary': '#004E89',
            'accent': '#F7B801',
            'success': '#2A9D8F',
            'warning': '#E76F51',
            'dark': '#1A1A2E',
            'light': '#F5F5F5'
        }
    
    def create_heatmap(
        self,
        sunlight_hours: np.ndarray,
        title: str = "Annual Sunlight Hours Heatmap"
    ) -> go.Figure:
        """Create interactive sunlight heatmap"""
        
        fig = go.Figure(data=go.Heatmap(
            z=sunlight_hours,
            colorscale='YlOrRd',
            colorbar=dict(title="Hours/Year"),
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            plot_bgcolor=self.color_scheme['dark'],
            paper_bgcolor=self.color_scheme['dark'],
            font=dict(color=self.color_scheme['light']),
            height=600
        )
        
        return fig
    
    def create_site_comparison_chart(
        self,
        candidate_sites: List[Dict]
    ) -> go.Figure:
        """Create bar chart comparing top candidate sites"""
        
        # Extract data
        site_ids = [f"Site {s['id']}" for s in candidate_sites[:10]]
        scores = [s['score'] for s in candidate_sites[:10]]
        
        # Extract score components if available
        sunlight_scores = [s.get('score_components', {}).get('sunlight', 0) for s in candidate_sites[:10]]
        terrain_scores = [s.get('score_components', {}).get('terrain', 0) for s in candidate_sites[:10]]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Total Score',
            x=site_ids,
            y=scores,
            marker_color=self.color_scheme['primary']
        ))
        
        fig.update_layout(
            title="Top 10 Candidate Sites Comparison",
            xaxis_title="Site",
            yaxis_title="Score",
            plot_bgcolor=self.color_scheme['dark'],
            paper_bgcolor=self.color_scheme['dark'],
            font=dict(color=self.color_scheme['light']),
            height=500,
            barmode='group'
        )
        
        return fig
    
    def create_score_breakdown_chart(
        self,
        candidate_sites: List[Dict],
        site_index: int = 0
    ) -> go.Figure:
        """Create pie chart showing score component breakdown"""
        
        if site_index >= len(candidate_sites):
            site_index = 0
        
        site = candidate_sites[site_index]
        components = site.get('score_components', {})
        
        labels = list(components.keys())
        values = list(components.values())
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.3,
            marker=dict(colors=[
                self.color_scheme['primary'],
                self.color_scheme['success'],
                self.color_scheme['accent'],
                self.color_scheme['secondary'],
                self.color_scheme['warning']
            ])
        )])
        
        fig.update_layout(
            title=f"Score Breakdown - Site {site['id']}",
            plot_bgcolor=self.color_scheme['dark'],
            paper_bgcolor=self.color_scheme['dark'],
            font=dict(color=self.color_scheme['light']),
            height=400
        )
        
        return fig
    
    def create_reality_gap_chart(
        self,
        validation_results: List[Dict]
    ) -> go.Figure:
        """Create chart showing prediction vs reality"""
        
        site_ids = [f"Site {v['site_id']}" for v in validation_results]
        predicted = [v['predicted_score'] for v in validation_results]
        adjusted = [v['adjusted_score'] for v in validation_results]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Predicted Score',
            x=site_ids,
            y=predicted,
            marker_color=self.color_scheme['primary']
        ))
        
        fig.add_trace(go.Bar(
            name='Adjusted Score (After Validation)',
            x=site_ids,
            y=adjusted,
            marker_color=self.color_scheme['success']
        ))
        
        fig.update_layout(
            title="Prediction vs Reality Analysis",
            xaxis_title="Site",
            yaxis_title="Score",
            plot_bgcolor=self.color_scheme['dark'],
            paper_bgcolor=self.color_scheme['dark'],
            font=dict(color=self.color_scheme['light']),
            height=500,
            barmode='group'
        )
        
        return fig
    
    def create_confidence_gauge(
        self,
        validation_results: List[Dict]
    ) -> go.Figure:
        """Create gauge chart for average confidence"""
        
        avg_confidence = np.mean([v['confidence'] for v in validation_results])
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_confidence * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Average Confidence", 'font': {'color': self.color_scheme['light']}},
            delta={'reference': 70},
            gauge={
                'axis': {'range': [None, 100], 'tickcolor': self.color_scheme['light']},
                'bar': {'color': self.color_scheme['primary']},
                'steps': [
                    {'range': [0, 50], 'color': self.color_scheme['warning']},
                    {'range': [50, 75], 'color': self.color_scheme['accent']},
                    {'range': [75, 100], 'color': self.color_scheme['success']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            plot_bgcolor=self.color_scheme['dark'],
            paper_bgcolor=self.color_scheme['dark'],
            font=dict(color=self.color_scheme['light']),
            height=400
        )
        
        return fig
    
    def create_folium_map(
        self,
        candidate_sites: List[Dict],
        center_lat: float = 40.7128,
        center_lon: float = -74.0060
    ) -> folium.Map:
        """Create interactive Folium map with candidate sites"""
        
        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=13,
            tiles='OpenStreetMap'
        )
        
        # Add markers for each candidate site
        for i, site in enumerate(candidate_sites[:10]):
            # Convert pixel coordinates to lat/lon (simplified)
            # In production, you would use actual georeferencing
            lat_offset = (site['center'][1] - 512) / 10000
            lon_offset = (site['center'][0] - 512) / 10000
            
            lat = center_lat + lat_offset
            lon = center_lon + lon_offset
            
            # Color based on score
            score = site['score']
            if score > 0.8:
                color = 'green'
            elif score > 0.6:
                color = 'orange'
            else:
                color = 'red'
            
            # Create popup
            popup_html = f"""
            <div style="font-family: Arial; width: 200px;">
                <h4>Site {site['id']}</h4>
                <p><b>Score:</b> {score:.3f}</p>
                <p><b>Area:</b> {site.get('area', 0):.0f} m²</p>
            </div>
            """
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=10,
                popup=folium.Popup(popup_html, max_width=250),
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(m)
        
        return m
    
    def overlay_sites_on_image(
        self,
        image: np.ndarray,
        candidate_sites: List[Dict],
        show_top_n: int = 10
    ) -> np.ndarray:
        """Overlay candidate sites on satellite image"""
        
        overlay = image.copy()
        
        for i, site in enumerate(candidate_sites[:show_top_n]):
            center = site['center']
            width = site.get('width', 50)
            height = site.get('height', 50)
            
            # Calculate rectangle corners
            x1 = int(center[0] - width / 2)
            y1 = int(center[1] - height / 2)
            x2 = int(center[0] + width / 2)
            y2 = int(center[1] + height / 2)
            
            # Color based on rank
            if i < 3:
                color = (0, 255, 0)  # Green for top 3
            elif i < 6:
                color = (255, 255, 0)  # Yellow for 4-6
            else:
                color = (255, 165, 0)  # Orange for 7-10
            
            # Draw rectangle
            cv2.rectangle(overlay, (x1, y1), (x2, y2), color, 3)
            
            # Draw label
            label = f"#{i+1}"
            cv2.putText(
                overlay,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color,
                2
            )
        
        return overlay
