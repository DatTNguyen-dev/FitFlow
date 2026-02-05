import os
import json
from typing import Any, Dict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Khởi tạo Gemini 2.5 Flash Model
def initialize_gemini_model():
    """Khởi tạo model Gemini 2.5 Flash"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=api_key,
        temperature=0.7,
        max_tokens=2048
    )
    return llm


def load_prompt_template(prompt_file_path: str) -> str:
    """Tải prompt từ file Markdown"""
    try:
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {prompt_file_path}")


class FitnessAgentManager:
    """Quản lý các agent fitness"""
    
    def __init__(self):
        self.llm = initialize_gemini_model()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agents = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Khởi tạo tất cả các agent"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        prompts_path = os.path.join(base_path, 'prompts')
        
        # Master Agent
        master_prompt = load_prompt_template(os.path.join(prompts_path, 'master_agent_prompt.md'))
        self.agents['master'] = FitnessAgent(
            name='Master Agent',
            role='coordinator',
            prompt_template=master_prompt,
            llm=self.llm,
            memory=self.memory
        )
        
        # Planning Agent
        planning_prompt = load_prompt_template(os.path.join(prompts_path, 'planning_agent_prompt.md'))
        self.agents['planning'] = FitnessAgent(
            name='Planning Agent',
            role='planning',
            prompt_template=planning_prompt,
            llm=self.llm,
            memory=self.memory
        )
        
        # Schedule Agent
        schedule_prompt = load_prompt_template(os.path.join(prompts_path, 'schedule_agent_prompt.md'))
        self.agents['schedule'] = FitnessAgent(
            name='Schedule Agent',
            role='scheduling',
            prompt_template=schedule_prompt,
            llm=self.llm,
            memory=self.memory
        )
        
        # Tracking Agent
        tracking_prompt = load_prompt_template(os.path.join(prompts_path, 'tracking_agent_prompt.md'))
        self.agents['tracking'] = FitnessAgent(
            name='Tracking Agent',
            role='tracking',
            prompt_template=tracking_prompt,
            llm=self.llm,
            memory=self.memory
        )
    
    def get_agent(self, agent_type: str) -> 'FitnessAgent':
        """Lấy agent theo loại"""
        if agent_type not in self.agents:
            raise ValueError(f"Unknown agent type: {agent_type}")
        return self.agents[agent_type]
    
    def process_request(self, user_input: Dict[str, Any], agent_type: str = 'master') -> Dict[str, Any]:
        """Xử lý yêu cầu từ người dùng"""
        agent = self.get_agent(agent_type)
        response = agent.run(user_input)
        return response


class FitnessAgent:
    """Agent cho fitness coaching"""
    
    def __init__(self, name: str, role: str, prompt_template: str, llm, memory):
        self.name = name
        self.role = role
        self.prompt_template = prompt_template
        self.llm = llm
        self.memory = memory
    
    def run(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Chạy agent với input từ người dùng"""
        context = self._prepare_context(user_input)
        
        # Tạo prompt với context
        full_prompt = f"{self.prompt_template}\n\n## User Input:\n{json.dumps(user_input, indent=2)}\n\n## Context:\n{context}"
        
        # Gọi LLM
        response = self.llm.invoke(full_prompt)
        
        # Xử lý response
        result = self._parse_response(response)
        
        return result
    
    def _prepare_context(self, user_input: Dict[str, Any]) -> str:
        """Chuẩn bị context cho agent"""
        context = f"Agent Role: {self.role}\n"
        context += f"Agent Name: {self.name}\n"
        
        if self.memory.chat_history:
            context += "Chat History:\n"
            for msg in self.memory.chat_history[-3:]:  # Lấy 3 tin nhắn gần nhất
                context += f"- {msg}\n"
        
        return context
    
    def _parse_response(self, response) -> Dict[str, Any]:
        """Phân tích response từ LLM"""
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        result = {
            'success': True,
            'agent': self.name,
            'role': self.role,
            'response': response_text,
            'timestamp': self._get_timestamp()
        }
        
        # Cố gắng extract JSON nếu có
        try:
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result['data'] = json.loads(json_match.group())
        except (json.JSONDecodeError, AttributeError):
            pass
        
        return result
    
    def _get_timestamp(self) -> str:
        """Lấy timestamp hiện tại"""
        from datetime import datetime
        return datetime.now().isoformat()


# Tools cho Agent
def create_exercise_plan_tool(llm) -> Tool:
    """Tool tạo kế hoạch tập luyện"""
    def create_plan(user_profile: str) -> str:
        prompt = f"Based on user profile: {user_profile}, create a detailed exercise plan"
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    
    return Tool(
        name="CreateExercisePlan",
        func=create_plan,
        description="Creates a detailed exercise plan based on user profile"
    )


def create_schedule_tool(llm) -> Tool:
    """Tool tạo lịch tập luyện"""
    def schedule_workouts(exercise_plan: str, personal_timetable: str) -> str:
        prompt = f"Schedule these workouts: {exercise_plan} into this timetable: {personal_timetable}"
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    
    return Tool(
        name="ScheduleWorkouts",
        func=schedule_workouts,
        description="Schedules workouts into a personal timetable"
    )


def create_progress_tracking_tool(llm) -> Tool:
    """Tool theo dõi tiến độ"""
    def track_progress(user_id: str, metrics: str) -> str:
        prompt = f"Track progress for user {user_id} with metrics: {metrics}"
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    
    return Tool(
        name="TrackProgress",
        func=track_progress,
        description="Tracks and analyzes user's progress"
    )


def create_assessment_tool(llm) -> Tool:
    """Tool tạo báo cáo đánh giá"""
    def create_assessment(progress_data: str, weak_areas: str) -> str:
        prompt = f"Create an assessment report based on progress: {progress_data} with weak areas: {weak_areas}"
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    
    return Tool(
        name="CreateAssessment",
        func=create_assessment,
        description="Creates an assessment report identifying areas for improvement"
    )


# Khởi tạo toàn cục
try:
    agent_manager = FitnessAgentManager()
except Exception as e:
    print(f"Warning: Failed to initialize agent manager: {e}")
    agent_manager = None
