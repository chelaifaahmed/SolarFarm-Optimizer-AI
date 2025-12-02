"""
Solar Farm Optimizer - Streamlit Dashboard
Production-ready multi-agent AI system for optimal solar panel placement
"""

import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
import sys
import time
from PIL import Image
import io

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents import AgentOrchestrator
from utils.visualizer import SolarFarmVisualizer
from utils.config import config

# Page configuration
st.set_page_config(
    page_title="Solar Farm Optimizer",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark mode glassmorphism design
st.markdown("""
<style>
    /* Dark theme */
    .stApp {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
    }
    
    /* Glassmorphism cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F7B801 !important;
        font-weight: 700;
    }
    
    /* Metrics */
    .stMetric {
        background: rgba(247, 184, 1, 0.1);
        border-radius: 10px;
        padding: 15px;
    }
    
    .stMetric label {
        color: #F5F5F5 !important;
    }
    
    .stMetric value {
        color: #F7B801 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #FF6B35 0%, #F7B801 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(255, 107, 53, 0.4);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #2A9D8F 0%, #F7B801 100%);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: rgba(26, 26, 46, 0.8);
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed #F7B801;
        border-radius: 10px;
        padding: 20px;
    }
    
    /* Success/Info boxes */
    .stSuccess {
        background: rgba(42, 157, 143, 0.2);
        border-left: 4px solid #2A9D8F;
    }
    
    .stInfo {
        background: rgba(0, 78, 137, 0.2);
        border-left: 4px solid #004E89;
    }
    
    .stWarning {
        background: rgba(231, 111, 81, 0.2);
        border-left: 4px solid #E76F51;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'pipeline_results' not in st.session_state:
        st.session_state.pipeline_results = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = AgentOrchestrator()
    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = SolarFarmVisualizer()


def render_header():
    """Render application header"""
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='font-size: 3em; margin-bottom: 0;'>☀️ Solar Farm Optimizer</h1>
            <p style='color: #F5F5F5; font-size: 1.2em; margin-top: 10px;'>
                Multi-Agent AI System for Optimal Solar Panel Placement
            </p>
        </div>
        """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar with controls and settings"""
    st.sidebar.markdown("## ⚙️ Configuration")
    
    # File upload
    uploaded_file = st.sidebar.file_uploader(
        "Upload Satellite Image",
        type=['png', 'jpg', 'jpeg', 'tif'],
        help="Upload satellite imagery for analysis"
    )
    
    # Geographic coordinates
    st.sidebar.markdown("### 📍 Location")
    latitude = st.sidebar.number_input("Latitude", value=40.7128, format="%.4f")
    longitude = st.sidebar.number_input("Longitude", value=-74.0060, format="%.4f")
    
    # Algorithm parameters
    st.sidebar.markdown("### 🔧 Algorithm Parameters")
    population_size = st.sidebar.slider(
        "Population Size",
        min_value=100,
        max_value=2000,
        value=1000,
        step=100
    )
    
    top_n = st.sidebar.slider(
        "Top N Sites",
        min_value=5,
        max_value=20,
        value=10
    )
    
    # Field report upload (optional)
    field_report = st.sidebar.file_uploader(
        "Upload Field Report (Optional)",
        type=['csv'],
        help="Upload field validation data for reality gap analysis"
    )
    
    # Process button
    process_button = st.sidebar.button(
        "🚀 Start Analysis",
        disabled=uploaded_file is None,
        use_container_width=True
    )
    
    return {
        'uploaded_file': uploaded_file,
        'latitude': latitude,
        'longitude': longitude,
        'population_size': population_size,
        'top_n': top_n,
        'field_report': field_report,
        'process_button': process_button
    }


def run_pipeline(params):
    """Run the multi-agent pipeline"""
    
    # Save uploaded file temporarily
    temp_image_path = project_root / "data" / "temp_image.png"
    temp_image_path.parent.mkdir(exist_ok=True)
    
    with open(temp_image_path, "wb") as f:
        f.write(params['uploaded_file'].getbuffer())
    
    # Save field report if provided
    field_report_path = None
    if params['field_report'] is not None:
        field_report_path = project_root / "data" / "field_report.csv"
        with open(field_report_path, "wb") as f:
            f.write(params['field_report'].getbuffer())
    
    # Update configuration
    st.session_state.orchestrator.optimizer_agent.population_size = params['population_size']
    st.session_state.orchestrator.optimizer_agent.top_n = params['top_n']
    
    # Run pipeline
    results = st.session_state.orchestrator.run_pipeline(
        image_path=str(temp_image_path),
        coordinates={
            'latitude': params['latitude'],
            'longitude': params['longitude']
        },
        field_report_path=str(field_report_path) if field_report_path else None
    )
    
    return results


def render_agent_status(execution_log):
    """Render agent execution status"""
    st.markdown("## 🤖 Multi-Agent Execution Status")
    
    cols = st.columns(4)
    
    agent_icons = {
        'DataAgent': '📊',
        'VisionAgent': '👁️',
        'OptimizerAgent': '🎯',
        'ValidatorAgent': '✅'
    }
    
    for i, log in enumerate(execution_log):
        with cols[i]:
            icon = agent_icons.get(log['name'], '🤖')
            st.markdown(f"""
            <div class='glass-card' style='text-align: center;'>
                <h2 style='font-size: 2.5em; margin: 0;'>{icon}</h2>
                <h3 style='font-size: 1.2em; margin: 10px 0;'>{log['name']}</h3>
                <p style='color: #2A9D8F; font-size: 1.5em; margin: 5px 0;'>✓</p>
                <p style='color: #F5F5F5; margin: 5px 0;'>{log['execution_time']:.2f}s</p>
            </div>
            """, unsafe_allow_html=True)


def render_results(results):
    """Render analysis results"""
    
    # Extract key results
    vision_results = results['vision']
    optimization_results = results['optimization']
    validation_results = results['validation']
    
    candidate_sites = optimization_results['candidate_sites']
    validation_data = validation_results['validation_results']
    reality_gap = validation_results['reality_gap_analysis']
    
    # Key metrics
    st.markdown("## 📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Top Sites Found",
            len(candidate_sites),
            help="Number of optimal sites identified"
        )
    
    with col2:
        avg_score = np.mean([s['score'] for s in candidate_sites])
        st.metric(
            "Avg Score",
            f"{avg_score:.3f}",
            help="Average optimization score"
        )
    
    with col3:
        avg_confidence = reality_gap.get('average_confidence', 0) * 100
        st.metric(
            "Avg Confidence",
            f"{avg_confidence:.1f}%",
            help="Average validation confidence"
        )
    
    with col4:
        error_reduction = reality_gap.get('error_reduction_vs_baseline', 0)
        st.metric(
            "Error Reduction",
            f"{error_reduction:.1f}%",
            delta=f"{error_reduction:.1f}%",
            help="Improvement vs baseline"
        )
    
    # Tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🗺️ Site Map",
        "📊 Rankings",
        "🌞 Sunlight Analysis",
        "✅ Validation",
        "📄 Detailed Report"
    ])
    
    with tab1:
        render_site_map_tab(results)
    
    with tab2:
        render_rankings_tab(candidate_sites)
    
    with tab3:
        render_sunlight_tab(vision_results)
    
    with tab4:
        render_validation_tab(validation_data, reality_gap)
    
    with tab5:
        render_report_tab(results)


def render_site_map_tab(results):
    """Render site map visualization"""
    st.markdown("### 📍 Optimal Site Locations")
    
    # Get visualizer
    viz = st.session_state.visualizer
    
    # Overlay sites on image
    processed_image = results['vision']['processed_image']
    candidate_sites = results['optimization']['candidate_sites']
    
    overlay_image = viz.overlay_sites_on_image(processed_image, candidate_sites)
    
    st.image(overlay_image, caption="Top 10 Recommended Sites", width=800)
    
    # Show Folium map
    st.markdown("### 🗺️ Interactive Map")
    coords = results['data']['geospatial_data']['coordinates']
    folium_map = viz.create_folium_map(
        candidate_sites,
        center_lat=coords.get('latitude', 40.7128),
        center_lon=coords.get('longitude', -74.0060)
    )
    
    # Save and display map
    from streamlit_folium import st_folium
    try:
        st_folium(folium_map, width=1200, height=600)
    except:
        st.info("Install streamlit-folium for interactive maps: pip install streamlit-folium")


def render_rankings_tab(candidate_sites):
    """Render site rankings"""
    st.markdown("### 🏆 Top 10 Candidate Sites")
    
    viz = st.session_state.visualizer
    
    # Comparison chart
    comparison_chart = viz.create_site_comparison_chart(candidate_sites)
    st.plotly_chart(comparison_chart, use_container_width=True)
    
    # Detailed table
    st.markdown("### 📋 Detailed Rankings")
    
    table_data = []
    for i, site in enumerate(candidate_sites[:10]):
        table_data.append({
            'Rank': i + 1,
            'Site ID': site['id'],
            'Total Score': f"{site['score']:.3f}",
            'Area (m²)': f"{site.get('area', 0):.0f}",
            'Sunlight Score': f"{site.get('score_components', {}).get('sunlight', 0):.3f}",
            'Terrain Score': f"{site.get('score_components', {}).get('terrain', 0):.3f}",
            'Obstacle Score': f"{site.get('score_components', {}).get('obstacles', 0):.3f}"
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)


def render_sunlight_tab(vision_results):
    """Render sunlight analysis"""
    st.markdown("### ☀️ Sunlight Analysis")
    
    viz = st.session_state.visualizer
    sunlight_analysis = vision_results['sunlight_analysis']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sunlight heatmap
        heatmap = viz.create_heatmap(sunlight_analysis['sunlight_hours'])
        st.plotly_chart(heatmap, use_container_width=True)
    
    with col2:
        # Statistics
        stats = sunlight_analysis['statistics']
        st.markdown("### 📊 Sunlight Statistics")
        st.metric("Mean Annual Hours", f"{stats['mean']:.0f}")
        st.metric("Max Annual Hours", f"{stats['max']:.0f}")
        st.metric("Optimal Area %", f"{stats['optimal_area_percentage']:.1f}%")
    
    # Show visualizations
    col3, col4 = st.columns(2)
    
    with col3:
        st.image(
            vision_results['segmentation_visualization'],
            caption="Terrain Segmentation",
            use_container_width=True
        )
    
    with col4:
        st.image(
            vision_results['obstacle_visualization'],
            caption="Obstacle Detection",
            use_container_width=True
        )


def render_validation_tab(validation_data, reality_gap):
    """Render validation results"""
    st.markdown("### ✅ Validation & Reality Gap Analysis")
    
    viz = st.session_state.visualizer
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Reality gap chart
        gap_chart = viz.create_reality_gap_chart(validation_data)
        st.plotly_chart(gap_chart, use_container_width=True)
    
    with col2:
        # Confidence gauge
        confidence_gauge = viz.create_confidence_gauge(validation_data)
        st.plotly_chart(confidence_gauge, use_container_width=True)
    
    # Metrics
    st.markdown("### 📊 Gap Metrics")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.metric(
            "Avg Sunlight Error",
            f"{reality_gap.get('average_sunlight_error', 0):.1f}%"
        )
    
    with col4:
        st.metric(
            "Avg Cost Error",
            f"{reality_gap.get('average_cost_error', 0):.1f}%"
        )
    
    with col5:
        st.metric(
            "Error Reduction",
            f"{reality_gap.get('error_reduction_vs_baseline', 0):.1f}%",
            delta=f"{reality_gap.get('error_reduction_vs_baseline', 0):.1f}%"
        )
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    recommendations = validation_data[0].get('recommendations', []) if validation_data else []
    
    # Use validation_results recommendations
    from agents import ValidatorAgent
    validator = ValidatorAgent()
    recommendations = validator._generate_recommendations(reality_gap)
    
    for rec in recommendations:
        st.info(rec)


def render_report_tab(results):
    """Render detailed report"""
    st.markdown("### 📄 Comprehensive Report")
    
    candidate_sites = results['optimization']['candidate_sites']
    validation_results = results['validation']['validation_results']
    
    # Create downloadable report
    report_data = []
    for site in candidate_sites[:10]:
        # Find validation data
        validation = next(
            (v for v in validation_results if v['site_id'] == site['id']),
            {}
        )
        
        report_data.append({
            'Site ID': site['id'],
            'Score': site['score'],
            'Area (m²)': site.get('area', 0),
            'Confidence': validation.get('confidence', 0),
            'Feasibility': validation.get('overall_feasibility', 'Unknown'),
            'Sunlight Score': site.get('score_components', {}).get('sunlight', 0),
            'Terrain Score': site.get('score_components', {}).get('terrain', 0),
            'Obstacle Score': site.get('score_components', {}).get('obstacles', 0),
            'Access Road': validation.get('access_road_quality', 'Unknown'),
            'Soil Stability': validation.get('soil_stability', 0)
        })
    
    df_report = pd.DataFrame(report_data)
    
    st.dataframe(df_report, use_container_width=True, hide_index=True)
    
    # Download buttons
    col1, col2 = st.columns(2)
    
    with col1:
        csv = df_report.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV Report",
            data=csv,
            file_name="solar_farm_recommendations.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # Excel download
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_report.to_excel(writer, index=False, sheet_name='Recommendations')
        
        st.download_button(
            label="📥 Download Excel Report",
            data=buffer.getvalue(),
            file_name="solar_farm_recommendations.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


def main():
    """Main application entry point"""
    
    initialize_session_state()
    render_header()
    
    # Sidebar controls
    params = render_sidebar()
    
    # Info section
    if st.session_state.pipeline_results is None:
        st.info("""
        👋 **Welcome to Solar Farm Optimizer!**
        
        This multi-agent AI system analyzes satellite imagery to recommend optimal solar panel placements.
        
        **How to use:**
        1. Upload a satellite image in the sidebar
        2. Set your location coordinates
        3. Adjust algorithm parameters
        4. Click "Start Analysis" to begin
        
        The system will:
        - 📊 Analyze terrain and obstacles
        - 👁️ Predict sunlight hours and shadows
        - 🎯 Optimize site selection using genetic algorithms
        - ✅ Validate predictions against field data
        """)
    
    # Process pipeline
    if params['process_button']:
        st.session_state.processing = True
        
        with st.spinner("🚀 Running multi-agent pipeline..."):
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate progress updates
            phases = [
                "📊 Phase 1/4: Data Acquisition",
                "👁️ Phase 2/4: Vision AI Analysis",
                "🎯 Phase 3/4: Site Optimization",
                "✅ Phase 4/4: Validation"
            ]
            
            for i, phase in enumerate(phases):
                status_text.text(phase)
                progress_bar.progress((i + 1) * 25)
                
                if i == 0:
                    # Actually run the pipeline in background
                    if i == 0:
                        try:
                            results = run_pipeline(params)
                            st.session_state.pipeline_results = results
                        except Exception as e:
                            st.error(f"❌ Pipeline error: {str(e)}")
                            st.session_state.processing = False
                            return
                
                time.sleep(0.5)
            
            status_text.text("✅ Pipeline Complete!")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
        
        st.session_state.processing = False
        st.success("🎉 Analysis complete! See results below.")
    
    # Display results
    if st.session_state.pipeline_results is not None:
        results = st.session_state.pipeline_results
        
        # Agent status
        render_agent_status(results['execution_log'])
        
        st.markdown("---")
        
        # Results
        render_results(results)


if __name__ == "__main__":
    main()
