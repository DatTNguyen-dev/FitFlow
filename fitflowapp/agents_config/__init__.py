"""
Agents configuration for FitFlow
"""
from .agent_manager import (
    FitnessAgentManager,
    FitnessAgent,
    initialize_gemini_model,
    load_prompt_template,
    agent_manager,
    create_exercise_plan_tool,
    create_schedule_tool,
    create_progress_tracking_tool,
    create_assessment_tool,
)

__all__ = [
    'FitnessAgentManager',
    'FitnessAgent',
    'initialize_gemini_model',
    'load_prompt_template',
    'agent_manager',
    'create_exercise_plan_tool',
    'create_schedule_tool',
    'create_progress_tracking_tool',
    'create_assessment_tool',
]
