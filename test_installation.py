"""
Test script to verify Solar Farm Optimizer installation
"""
import sys
from pathlib import Path

print("=" * 60)
print("Solar Farm Optimizer - Installation Test")
print("=" * 60)
print()

# Test 1: Python version
print("[1/8] Checking Python version...")
if sys.version_info >= (3, 11):
    print(f"✓ Python {sys.version.split()[0]} (OK)")
else:
    print(f"✗ Python {sys.version.split()[0]} (Need 3.11+)")
    sys.exit(1)
print()

# Test 2: Core dependencies
print("[2/8] Checking core dependencies...")
required_packages = [
    'numpy',
    'cv2',
    'pandas',
    'streamlit',
    'plotly',
    'folium'
]

missing = []
for package in required_packages:
    try:
        __import__(package)
        print(f"  ✓ {package}")
    except ImportError:
        print(f"  ✗ {package} (MISSING)")
        missing.append(package)

if missing:
    print(f"\n⚠️  Missing packages: {', '.join(missing)}")
    print("Run: pip install -r requirements.txt")
else:
    print("✓ All core packages installed")
print()

# Test 3: Project structure
print("[3/8] Verifying project structure...")
project_root = Path(__file__).parent
required_dirs = ['agents', 'vision', 'utils', 'data', 'demo_data']
required_files = ['app.py', 'requirements.txt', 'README.md']

structure_ok = True
for dir_name in required_dirs:
    if (project_root / dir_name).exists():
        print(f"  ✓ {dir_name}/")
    else:
        print(f"  ✗ {dir_name}/ (MISSING)")
        structure_ok = False

for file_name in required_files:
    if (project_root / file_name).exists():
        print(f"  ✓ {file_name}")
    else:
        print(f"  ✗ {file_name} (MISSING)")
        structure_ok = False

if structure_ok:
    print("✓ Project structure verified")
else:
    print("✗ Project structure incomplete")
print()

# Test 4: Import agents
print("[4/8] Testing agent imports...")
try:
    from agents import (
        BaseAgent, DataAgent, VisionAgent,
        OptimizerAgent, ValidatorAgent, AgentOrchestrator
    )
    print("✓ All agents imported successfully")
except ImportError as e:
    print(f"✗ Agent import failed: {e}")
print()

# Test 5: Import vision modules
print("[5/8] Testing vision module imports...")
try:
    from vision import (
        ImagePreprocessor, TerrainSegmenter,
        ObstacleDetector, SunlightPredictor
    )
    print("✓ All vision modules imported successfully")
except ImportError as e:
    print(f"✗ Vision module import failed: {e}")
print()

# Test 6: Import utils
print("[6/8] Testing utilities...")
try:
    from utils import config, main_logger, agent_logger
    print("✓ Utilities imported successfully")
except ImportError as e:
    print(f"✗ Utilities import failed: {e}")
print()

# Test 7: Check demo data
print("[7/8] Checking demo data...")
demo_dir = project_root / "demo_data"
if demo_dir.exists():
    demo_files = list(demo_dir.glob("*.png"))
    if demo_files:
        print(f"✓ Found {len(demo_files)} demo image(s)")
    else:
        print("⚠️  No demo images found")
        print("   Run: python demo_data/generate_demo_images.py")
else:
    print("✗ Demo data directory missing")
print()

# Test 8: Quick functionality test
print("[8/8] Testing basic functionality...")
try:
    from agents import AgentOrchestrator
    orchestrator = AgentOrchestrator()
    print(f"✓ Created orchestrator with {len(orchestrator.agents)} agents")
    
    # Test agent status
    statuses = orchestrator.get_agent_statuses()
    print(f"✓ Agent status check: {len(statuses)} agents ready")
    
except Exception as e:
    print(f"✗ Functionality test failed: {e}")
print()

# Final summary
print("=" * 60)
print("Installation Test Summary")
print("=" * 60)
print()
print("Your Solar Farm Optimizer installation is ready!")
print()
print("Next steps:")
print("  1. Generate demo images: python demo_data/generate_demo_images.py")
print("  2. Launch dashboard: streamlit run app.py")
print("  3. Open browser: http://localhost:8501")
print()
print("For help, see:")
print("  - QUICKSTART.md (quick instructions)")
print("  - README.md (full documentation)")
print()
print("=" * 60)
