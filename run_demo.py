"""
Standalone demo script for Solar Farm Optimizer
Demonstrates the complete pipeline without Streamlit
"""
import sys
from pathlib import Path
import time
import csv

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents import AgentOrchestrator



def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_section(text):
    """Print formatted section"""
    print(f"\n>>> {text}")
    print("-" * 70)


def run_demo():
    """Run complete demo"""
    
    print_header("☀️  SOLAR FARM OPTIMIZER - DEMO")
    
    print("This demo will:")
    print("  1. Load a sample satellite image")
    print("  2. Run multi-agent analysis pipeline")
    print("  3. Display optimization results")
    print("  4. Show validation metrics")
    print("  5. Export recommendations to CSV")
    print()
    
    # Check for demo image
    demo_image_path = project_root / "demo_data" / "satellite_sample.png"
    
    if not demo_image_path.exists():
        print("⚠️  Demo image not found!")
        print("Generating now...")
        import subprocess
        subprocess.run([
            sys.executable,
            str(project_root / "demo_data" / "generate_demo_images.py")
        ])
        print()
    
    if not demo_image_path.exists():
        print("❌ Could not generate demo image. Please run:")
        print("   python demo_data/generate_demo_images.py")
        return
    
    print(f"✓ Using demo image: {demo_image_path}")
    print()
    input("Press Enter to start analysis...")
    
    # Initialize orchestrator
    print_section("Initializing Multi-Agent System")
    orchestrator = AgentOrchestrator()
    print(f"✓ Created {len(orchestrator.agents)} specialized agents:")
    for agent in orchestrator.agents:
        print(f"  • {agent.name}: {agent.role}")
    print()
    
    # Run pipeline
    print_section("Running Analysis Pipeline")
    print("This will take ~15-20 seconds...")
    print()
    
    start_time = time.time()
    
    try:
        results = orchestrator.run_pipeline(
            image_path=str(demo_image_path),
            coordinates={
                'latitude': 40.7128,
                'longitude': -74.0060
            },
            field_report_path=str(project_root / "data" / "field_reports.csv")
        )
        
        elapsed_time = time.time() - start_time
        
        print()
        print(f"✅ Pipeline completed in {elapsed_time:.2f} seconds!")
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Display results
    print_section("📊 Key Metrics")
    
    candidate_sites = results['optimization']['candidate_sites']
    validation_results = results['validation']['validation_results']
    reality_gap = results['validation']['reality_gap_analysis']
    
    print(f"  Sites Found:        {len(candidate_sites)}")
    print(f"  Average Score:      {sum(s['score'] for s in candidate_sites) / len(candidate_sites):.3f}")
    print(f"  Best Site Score:    {candidate_sites[0]['score']:.3f}")
    print(f"  Avg Confidence:     {reality_gap.get('average_confidence', 0) * 100:.1f}%")
    print(f"  Error Reduction:    {reality_gap.get('error_reduction_vs_baseline', 0):.1f}%")
    print()
    
    # Top sites
    print_section("🏆 Top 5 Recommended Sites")
    print()
    print(f"{'Rank':<6} {'Site ID':<10} {'Score':<10} {'Area (m²)':<12} {'Feasibility':<20}")
    print("-" * 70)
    
    for i, site in enumerate(candidate_sites[:5]):
        validation = next((v for v in validation_results if v['site_id'] == site['id']), {})
        feasibility = validation.get('overall_feasibility', 'Unknown')
        
        print(f"{i+1:<6} {site['id']:<10} {site['score']:<10.3f} {site.get('area', 0):<12.0f} {feasibility:<20}")
    
    print()
    
    # Score breakdown
    print_section("📈 Score Components (Site #1)")
    site1 = candidate_sites[0]
    components = site1.get('score_components', {})
    
    for component, value in components.items():
        bar_length = int(value * 40)
        bar = "█" * bar_length + "▒" * (40 - bar_length)
        print(f"  {component.capitalize():<15} {bar} {value:.3f}")
    
    print()
    
    # Validation metrics
    print_section("✅ Validation Metrics")
    
    print(f"  Avg Sunlight Error: {reality_gap.get('average_sunlight_error', 0):.1f}%")
    print(f"  Avg Cost Error:     {reality_gap.get('average_cost_error', 0):.1f}%")
    print(f"  High Confidence:    {reality_gap.get('high_confidence_sites', 0)} sites")
    print(f"  Low Confidence:     {reality_gap.get('low_confidence_sites', 0)} sites")
    print()
    
    # Recommendations
    print_section("💡 Recommendations")
    
    recommendations = results['validation'].get('recommendations', [])
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    else:
        print("  No specific recommendations at this time.")
    
    print()
    
    # Agent execution times
    print_section("⏱️  Agent Execution Times")
    
    execution_log = results['execution_log']
    for log in execution_log:
        print(f"  {log['name']:<20} {log['execution_time']:>8.2f}s")
    
    print(f"\n  {'TOTAL':<20} {sum(log['execution_time'] for log in execution_log):>8.2f}s")
    print()
    
    # Export results
    print_section("📥 Exporting Results")
    
    export_data = []
    for site in candidate_sites:
        validation = next((v for v in validation_results if v['site_id'] == site['id']), {})
        
        export_data.append({
            'Site_ID': site['id'],
            'Rank': candidate_sites.index(site) + 1,
            'Total_Score': site['score'],
            'Area_m2': site.get('area', 0),
            'Confidence': validation.get('confidence', 0),
            'Feasibility': validation.get('overall_feasibility', 'Unknown'),
            'Sunlight_Score': site.get('score_components', {}).get('sunlight', 0),
            'Terrain_Score': site.get('score_components', {}).get('terrain', 0),
            'Obstacle_Score': site.get('score_components', {}).get('obstacles', 0),
            'Access_Road': validation.get('access_road_quality', 'Unknown'),
            'Soil_Stability': validation.get('soil_stability', 0)
        })
    
    output_path = project_root / "solar_farm_recommendations_demo.csv"
    
    if export_data:
        keys = export_data[0].keys()
        with open(output_path, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(export_data)
    
    print(f"✓ Saved recommendations to: {output_path}")
    print()
    
    # Summary
    print_header("✨ Demo Complete!")
    
    print("Summary:")
    print(f"  • Analyzed satellite image in {elapsed_time:.2f} seconds")
    print(f"  • Identified {len(candidate_sites)} optimal sites")
    print(f"  • Best site score: {candidate_sites[0]['score']:.3f}")
    print(f"  • Average confidence: {reality_gap.get('average_confidence', 0) * 100:.1f}%")
    print(f"  • Exported results to CSV")
    print()
    print("Next steps:")
    print("  1. Review the exported CSV file")
    print("  2. Run the full dashboard: streamlit run app.py")
    print("  3. Try with your own satellite images")
    print()
    print("For more information, see README.md and QUICKSTART.md")
    print()


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
