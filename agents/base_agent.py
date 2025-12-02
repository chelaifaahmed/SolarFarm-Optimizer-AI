"""
Base Agent class for all specialized agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from utils.logger import agent_logger
import time


class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str, role: str, goal: str):
        self.name = name
        self.role = role
        self.goal = goal
        self.status = "idle"
        self.execution_time = 0.0
        self.results = None
        agent_logger.info(f"Initialized {name} agent")
    
    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent task"""
        pass
    
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Run agent with timing and status tracking"""
        agent_logger.info(f"{self.name} starting execution")
        self.status = "running"
        start_time = time.time()
        
        try:
            self.results = self.execute(inputs)
            self.status = "completed"
            agent_logger.info(f"{self.name} completed successfully")
        except Exception as e:
            self.status = "failed"
            agent_logger.error(f"{self.name} failed: {str(e)}")
            raise
        finally:
            self.execution_time = time.time() - start_time
            agent_logger.info(f"{self.name} execution time: {self.execution_time:.2f}s")
        
        return self.results
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            'name': self.name,
            'role': self.role,
            'status': self.status,
            'execution_time': self.execution_time
        }
