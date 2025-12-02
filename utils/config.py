"""
Configuration management for Solar Farm Optimizer
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

# Load environment variables
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DEMO_DATA_DIR = PROJECT_ROOT / "demo_data"
MODELS_DIR = PROJECT_ROOT / "models"

# Create directories if they don't exist
for directory in [DATA_DIR, DEMO_DATA_DIR, MODELS_DIR]:
    directory.mkdir(exist_ok=True)


class VisionConfig(BaseModel):
    """Vision AI configuration"""
    sam_checkpoint: str = str(MODELS_DIR / "sam_vit_h_4b8939.pth")
    yolo_model: str = "yolov8x.pt"
    image_size: int = 1024
    confidence_threshold: float = 0.5
    iou_threshold: float = 0.45


class OptimizationConfig(BaseModel):
    """Optimization algorithm configuration"""
    population_size: int = 1000
    generations: int = 50
    mutation_rate: float = 0.1
    crossover_rate: float = 0.8
    top_n_sites: int = 10
    min_site_area: float = 1000.0  # square meters
    max_site_area: float = 50000.0  # square meters


class AgentConfig(BaseModel):
    """Multi-agent system configuration"""
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    use_groq: bool = os.getenv("USE_GROQ", "False").lower() == "true"
    model_name: str = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    max_iterations: int = int(os.getenv("MAX_ITERATIONS", "100"))


class GeospatialConfig(BaseModel):
    """Geospatial data configuration"""
    osm_endpoint: str = os.getenv("OSM_API_ENDPOINT", "https://overpass-api.de/api/interpreter")
    default_bbox: list = [40.7128, -74.0060, 40.7228, -73.9960]  # NYC area
    tile_size: int = 256
    zoom_level: int = 18


class AppConfig(BaseModel):
    """Main application configuration"""
    vision: VisionConfig = VisionConfig()
    optimization: OptimizationConfig = OptimizationConfig()
    agent: AgentConfig = AgentConfig()
    geospatial: GeospatialConfig = GeospatialConfig()
    processing_timeout: int = int(os.getenv("PROCESSING_TIMEOUT", "300"))
    enable_caching: bool = True
    debug_mode: bool = False


# Global configuration instance
config = AppConfig()


def get_config() -> AppConfig:
    """Get global configuration"""
    return config


def update_config(**kwargs):
    """Update configuration values"""
    global config
    for key, value in kwargs.items():
        if hasattr(config, key):
            setattr(config, key, value)
