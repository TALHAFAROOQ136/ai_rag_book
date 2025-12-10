"""
Subagent Orchestrator
======================
Master controller for coordinating all four subagents

This module provides a unified interface to:
- Load and activate subagents
- Coordinate cross-agent workflows
- Manage skill loading (Matrix-style)
- Track project progress
"""

import sys
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import subagents
sys.path.append(str(Path(__file__).parent))

# Import all subagent classes
try:
    from BookWriter.agent import BookWriterAgent
    from RAGEngineer.agent import RAGEngineerAgent
    from FrontendDev.agent import FrontendDevAgent
    from APIBuilder.agent import APIBuilderAgent
except ImportError as e:
    print(f"Warning: Could not import all subagents: {e}")
    print("Make sure you're running from the subagents directory")


class SubagentOrchestrator:
    """
    Master Orchestrator for All Subagents
    
    Capabilities:
    - Load and manage multiple subagents
    - Coordinate multi-agent workflows
    - Track project progress across agents
    - Handle inter-agent communication
    """
    
    def __init__(self, project_root: str = "../../"):
        self.project_root = Path(project_root).resolve()
        self.agents = {}
        self.active_agent = None
        self.workflow_history = []
        self.project_status = {
            "phase": 0,
            "started_at": datetime.utcnow().isoformat(),
            "completed_tasks": []
        }
        
        print("="*70)
        print("SUBAGENT ORCHESTRATOR - Matrix-Style Agent Management")
        print("="*70)
    
    def activate_agent(self, agent_name: str) -> bool:
        """
        Activate (load) a subagent
        
        Args:
            agent_name: BookWriter | RAGEngineer | FrontendDev | APIBuilder
            
        Returns:
            bool: Success status
        """
        if agent_name in self.agents:
            self.active_agent = agent_name
            print(f"✓ Agent '{agent_name}' already loaded, now active")
            return True
        
        try:
            if agent_name == "BookWriter":
                self.agents[agent_name] = BookWriterAgent(str(self.project_root))
            elif agent_name == "RAGEngineer":
                self.agents[agent_name] = RAGEngineerAgent(str(self.project_root))
            elif agent_name == "FrontendDev":
                self.agents[agent_name] = FrontendDevAgent(str(self.project_root))
            elif agent_name == "APIBuilder":
                self.agents[agent_name] = APIBuilderAgent(str(self.project_root))
            else:
                print(f"✗ Unknown agent: {agent_name}")
                return False
            
            self.active_agent = agent_name
            print(f"✓ Agent '{agent_name}' loaded and activated")
            return True
            
        except Exception as e:
            print(f"✗ Error loading agent '{agent_name}': {e}")
            return False
    
    def load_skill_for_agent(self, agent_name: str, skill_name: str) -> bool:
        """
        Load a skill into a specific agent (Matrix-style)
        
        Args:
            agent_name: Target agent
            skill_name: Skill to load (e.g., "docusaurus-setup")
            
        Returns:
            bool: Success status
        """
        if agent_name not in self.agents:
            print(f"Agent '{agent_name}' not loaded. Activating...")
            if not self.activate_agent(agent_name):
                return False
        
        agent = self.agents[agent_name]
        return agent.load_skill(skill_name)
    
    def execute_workflow(self, workflow_name: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a multi-agent workflow
        
        Args:
            workflow_name: Name of the workflow to execute
            params: Workflow-specific parameters
            
        Returns:
            Dict: Workflow execution results
        """
        params = params or {}
        result = {
            "workflow": workflow_name,
            "started_at": datetime.utcnow().isoformat(),
            "steps": [],
            "status": "running"
        }
        
        try:
            if workflow_name == "phase_1_book_generation":
                result = self._execute_phase_1(params)
            elif workflow_name == "phase_2_backend_setup":
                result = self._execute_phase_2(params)
            elif workflow_name == "phase_3_integration":
                result = self._execute_phase_3(params)
            else:
                result["status"] = "error"
                result["error"] = f"Unknown workflow: {workflow_name}"
        
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        result["completed_at"] = datetime.utcnow().isoformat()
        self.workflow_history.append(result)
        
        return result
    
    def _execute_phase_1(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Phase 1: Book Development"""
        print("\n" + "="*70)
        print("WORKFLOW: Phase 1 - Book Development")
        print("="*70)
        
        result = {
            "workflow": "phase_1_book_generation",
            "steps": [],
            "status": "success"
        }
        
        # Step 1: Activate FrontendDev
        print("\n[Step 1/4] Activating FrontendDev...")
        self.activate_agent("FrontendDev")
        self.load_skill_for_agent("FrontendDev", "docusaurus-setup")
        result["steps"].append({"step": 1, "action": "FrontendDev activated"})
        
        # Step 2: Configure Docusaurus
        print("\n[Step 2/4] Configuring Docusaurus...")
        frontend = self.agents["FrontendDev"]
        config_result = frontend.execute_task({
            "action": "configure_docusaurus",
            "params": params.get("docusaurus_config", {
                "project_name": "AI Book with RAG",
                "base_url": "/",
                "organization_name": "yourusername"
            })
        })
        result["steps"].append({"step": 2, "result": config_result})
        
        # Step 3: Activate BookWriter
        print("\n[Step 3/4] Activating BookWriter...")
        self.activate_agent("BookWriter")
        result["steps"].append({"step": 3, "action": "BookWriter activated"})
        
        # Step 4: Generate content outline
        print("\n[Step 4/4] Generating content outline...")
        bookwriter = self.agents["BookWriter"]
        outline_result = bookwriter.execute_task({
            "action": "generate_outline",
            "params": params.get("outline_params", {
                "book_topic": "Introduction to RAG",
                "num_chapters": 4
            })
        })
        result["steps"].append({"step": 4, "result": outline_result})
        
        print("\n✓ Phase 1 workflow complete")
        return result
    
    def _execute_phase_2(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Phase 2: Backend Setup"""
        print("\n" + "="*70)
        print("WORKFLOW: Phase 2 - Backend Setup")
        print("="*70)
        
        result = {
            "workflow": "phase_2_backend_setup",
            "steps": [],
            "status": "success"
        }
        
        # Step 1: Activate RAGEngineer
        print("\n[Step 1/4] Activating RAGEngineer...")
        self.activate_agent("RAGEngineer")
        self.load_skill_for_agent("RAGEngineer", "qdrant-integration")
        result["steps"].append({"step": 1, "action": "RAGEngineer activated"})
        
        # Step 2: Set up Qdrant collection
        print("\n[Step 2/4] Setting up Qdrant collection...")
        rag_engineer = self.agents["RAGEngineer"]
        collection_result = rag_engineer.execute_task({
            "action": "setup_collection",
            "params": params.get("collection_config", {
                "collection_name": "book_chunks",
                "vector_size": 1536
            })
        })
        result["steps"].append({"step": 2, "result": collection_result})
        
        # Step 3: Activate APIBuilder
        print("\n[Step 3/4] Activating APIBuilder...")
        self.activate_agent("APIBuilder")
        self.load_skill_for_agent("APIBuilder", "openai-agent-builder")
        result["steps"].append({"step": 3, "action": "APIBuilder activated"})
        
        # Step 4: Create RAG agent
        print("\n[Step 4/4] Creating RAG agent...")
        api_builder = self.agents["APIBuilder"]
        agent_result = api_builder.execute_task({
            "action": "create_agent",
            "params": params.get("agent_config", {
                "book_title": "Introduction to RAG",
                "model": "gpt-4o-mini"
            })
        })
        result["steps"].append({"step": 4, "result": agent_result})
        
        print("\n✓ Phase 2 workflow complete")
        return result
    
    def _execute_phase_3(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Phase 3: Integration"""
        print("\n" + "="*70)
        print("WORKFLOW: Phase 3 - Integration")
        print("="*70)
        
        result = {
            "workflow": "phase_3_integration",
            "steps": [],
            "status": "success"
        }
        
        # Step 1: Use FrontendDev to create ChatBot
        print("\n[Step 1/2] Creating ChatBot component...")
        if "FrontendDev" not in self.agents:
            self.activate_agent("FrontendDev")
        
        frontend = self.agents["FrontendDev"]
        self.load_skill_for_agent("FrontendDev", "text-selection-handler")
        
        chatbot_result = frontend.execute_task({
            "action": "create_chatbot",
            "params": params.get("chatbot_config", {
                "backend_url": "https://your-backend.vercel.app",
                "floating_button": True
            })
        })
        result["steps"].append({"step": 1, "result": chatbot_result})
        
        # Step 2: Create text selector
        print("\n[Step 2/2] Creating text selection handler...")
        selector_result = frontend.execute_task({
            "action": "create_text_selector"
        })
        result["steps"].append({"step": 2, "result": selector_result})
        
        print("\n✓ Phase 3 workflow complete")
        return result
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        status = {
            "orchestrator_active": True,
            "active_agent": self.active_agent,
            "loaded_agents": list(self.agents.keys()),
            "agent_count": len(self.agents),
            "workflow_history_count": len(self.workflow_history),
            "project_phase": self.project_status["phase"],
            "agents_detail": {}
        }
        
        for name, agent in self.agents.items():
            status["agents_detail"][name] = agent.get_status()
        
        return status
    
    def print_status_report(self):
        """Print formatted status report"""
        status = self.get_system_status()
        
        print("\n" + "="*70)
        print("SYSTEM STATUS REPORT")
        print("="*70)
        print(f"Active Agent: {status['active_agent'] or 'None'}")
        print(f"Loaded Agents: {', '.join(status['loaded_agents']) if status['loaded_agents'] else 'None'}")
        print(f"Workflows Executed: {status['workflow_history_count']}")
        print(f"Current Phase: {status['project_phase']}")
        
        if status['agents_detail']:
            print("\n--- Agent Details ---")
            for name, details in status['agents_detail'].items():
                print(f"\n{name}:")
                print(f"  Status: {details['status']}")
                print(f"  Capabilities: {len(details['capabilities'])}")
                print(f"  Loaded Skills: {', '.join(details['loaded_skills']) if details['loaded_skills'] else 'None'}")


def main():
    """Example usage of Subagent Orchestrator"""
    
    # Initialize orchestrator
    orchestrator = SubagentOrchestrator()
    
    print("\n" + "="*70)
    print("DEMONSTRATION: Multi-Agent Workflow")
    print("="*70)
    
    # Execute Phase 1 workflow
    print("\n>>> Executing Phase 1: Book Development")
    phase1_result = orchestrator.execute_workflow(
        "phase_1_book_generation",
        params={
            "docusaurus_config": {
                "project_name": "Introduction to RAG",
                "organization_name": "yourname"
            },
            "outline_params": {
                "book_topic": "Introduction to RAG (Retrieval-Augmented Generation)",
                "num_chapters": 4
            }
        }
    )
    print(f"\nPhase 1 Status: {phase1_result['status']}")
    print(f"Steps Completed: {len(phase1_result['steps'])}")
    
    # Execute Phase 2 workflow
    print("\n>>> Executing Phase 2: Backend Setup")
    phase2_result = orchestrator.execute_workflow(
        "phase_2_backend_setup",
        params={
            "collection_config": {
                "collection_name": "book_chunks",
                "vector_size": 1536
            },
            "agent_config": {
                "book_title": "Introduction to RAG",
                "model": "gpt-4o-mini",
                "temperature": 0.3
            }
        }
    )
    print(f"\nPhase 2 Status: {phase2_result['status']}")
    print(f"Steps Completed: {len(phase2_result['steps'])}")
    
    # Execute Phase 3 workflow
    print("\n>>> Executing Phase 3: Integration")
    phase3_result = orchestrator.execute_workflow(
        "phase_3_integration",
        params={
            "chatbot_config": {
                "backend_url": "https://your-backend.vercel.app",
                "floating_button": True,
                "stream_enabled": True
            }
        }
    )
    print(f"\nPhase 3 Status: {phase3_result['status']}")
    print(f"Steps Completed: {len(phase3_result['steps'])}")
    
    # Print final status report
    orchestrator.print_status_report()
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nAll subagents have been successfully loaded and demonstrated.")
    print("This showcases the Matrix-style skill loading and multi-agent coordination.")


if __name__ == "__main__":
    main()
