"""
Orchestrator - Coordinates all agents in the pipeline
"""
from typing import Dict, Any, List
from .base_agent import BaseAgent
from .data_agent import DataAgent
from .vision_agent import VisionAgent
from .optimizer_agent import OptimizerAgent
from .validator_agent import ValidatorAgent
from utils.logger import agent_logger
import time


class AgentOrchestrator:
    """Orchestrates the multi-agent pipeline"""
    
    def __init__(self):
        self.data_agent = DataAgent()
        self.vision_agent = VisionAgent()
        self.optimizer_agent = OptimizerAgent()
        self.validator_agent = ValidatorAgent()
        
        self.agents = [
            self.data_agent,
            self.vision_agent,
            self.optimizer_agent,
            self.validator_agent
        ]
        
        self.pipeline_results = {}
        self.execution_log = []
        
        agent_logger.info("AgentOrchestrator initialized with 4 agents")
    
    def run_pipeline(
        self,
        image_path: str,
        coordinates: Dict = None,
        field_report_path: str = None
    ) -> Dict[str, Any]:
        """
        Run the complete multi-agent pipeline
        
        Args:
            image_path: Path to satellite image
            coordinates: Optional geographic coordinates
            field_report_path: Optional path to field validation data
            
        Returns:
            Complete pipeline results
        """
        agent_logger.info("="*60)
        agent_logger.info("STARTING MULTI-AGENT PIPELINE")
        agent_logger.info("="*60)
        
        start_time = time.time()
        
        try:
            # Phase 1: Data Acquisition
            agent_logger.info("\n[PHASE 1/4] Data Acquisition")
            data_results = self.data_agent.run({
                'image_path': image_path,
                'coordinates': coordinates
            })
            self._log_agent_completion(self.data_agent)
            
            # Phase 2: Vision Analysis
            agent_logger.info("\n[PHASE 2/4] Vision AI Analysis")
            vision_results = self.vision_agent.run({
                'raw_image': data_results['raw_image'],
                'geospatial_data': data_results['geospatial_data']
            })
            self._log_agent_completion(self.vision_agent)
            
            # Phase 3: Site Optimization
            agent_logger.info("\n[PHASE 3/4] Site Optimization")
            optimizer_results = self.optimizer_agent.run({
                'processed_image': vision_results['processed_image'],
                'terrain_segments': vision_results['terrain_segments'],
                'obstacles': vision_results['obstacles'],
                'sunlight_analysis': vision_results['sunlight_analysis'],
                'geospatial_data': data_results['geospatial_data']
            })
            self._log_agent_completion(self.optimizer_agent)
            
            # Phase 4: Validation
            agent_logger.info("\n[PHASE 4/4] Validation & Reality Check")
            validation_results = self.validator_agent.run({
                'candidate_sites': optimizer_results['candidate_sites'],
                'field_report_path': field_report_path
            })
            self._log_agent_completion(self.validator_agent)
            
            # Compile results
            total_time = time.time() - start_time
            
            pipeline_results = {
                'data': data_results,
                'vision': vision_results,
                'optimization': optimizer_results,
                'validation': validation_results,
                'execution_log': self.execution_log,
                'total_execution_time': total_time,
                'status': 'success'
            }
            
            agent_logger.info("="*60)
            agent_logger.info(f"PIPELINE COMPLETED in {total_time:.2f} seconds")
            agent_logger.info("="*60)
            
            return pipeline_results
            
        except Exception as e:
            agent_logger.error(f"Pipeline failed: {str(e)}")
            raise
    
    def _log_agent_completion(self, agent: BaseAgent):
        """Log agent completion"""
        status = agent.get_status()
        self.execution_log.append(status)
        agent_logger.info(
            f"✓ {agent.name} completed in {status['execution_time']:.2f}s"
        )
    
    def get_agent_statuses(self) -> List[Dict[str, Any]]:
        """Get status of all agents"""
        return [agent.get_status() for agent in self.agents]
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get execution summary"""
        if not self.execution_log:
            return {'message': 'No executions yet'}
        
        total_time = sum(log['execution_time'] for log in self.execution_log)
        
        return {
            'total_agents': len(self.agents),
            'total_execution_time': total_time,
            'agent_breakdown': self.execution_log
        }
