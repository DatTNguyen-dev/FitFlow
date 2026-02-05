"""
Main agents module for FitFlow
Imports and exposes agent functionality
"""
from fitflowapp.agents_config.agent_manager import (
    FitnessAgentManager,
    FitnessAgent,
    initialize_gemini_model,
    agent_manager,
)

__all__ = [
    'FitnessAgentManager',
    'FitnessAgent',
    'initialize_gemini_model',
    'agent_manager',
]
