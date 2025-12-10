"""
FrontendDev Subagent
====================
UI/UX and Client-Side Integration specialist

Capabilities:
- Configure Docusaurus projects
- Integrate chat UI components
- Implement text selection handlers
- Optimize frontend performance
- Deploy to GitHub Pages

Matrix-Style Skill Loading:
- Can load "Docusaurus Setup", "Text Selection Handler", "GitHub Pages Deploy"
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class FrontendDevAgent:
    """
    FrontendDev Subagent - UI/UX Specialist
    
    Responsibilities:
    - Docusaurus configuration and customization
    - ChatKit SDK integration
    - Text selection functionality
    - Performance optimization
    - GitHub Pages deployment
    """
    
    def __init__(self, project_root: str):
        self.agent_name = "FrontendDev"
        self.project_root = Path(project_root)
        self.loaded_skills = {}
        self.capabilities = [
            "docusaurus_setup",
            "chatkit_integration",
            "text_selection",
            "performance_optimization",
            "deployment_automation",
            "responsive_design"
        ]
        self.status = "initialized"
        self.docusaurus_config = None
        
    def load_skill(self, skill_name: str) -> bool:
        """
        Matrix-style skill loading
        
        Args:
            skill_name: Name of skill (e.g., "docusaurus-setup")
            
        Returns:
            bool: Success status
        """
        skill_path = self.project_root / "skills" / skill_name / "README.md"
        
        if skill_path.exists():
            with open(skill_path, 'r', encoding='utf-8') as f:
                skill_content = f.read()
            
            self.loaded_skills[skill_name] = {
                "loaded_at": datetime.utcnow().isoformat(),
                "documentation": skill_content,
                "status": "active"
            }
            print(f"✓ Skill '{skill_name}' loaded into {self.agent_name}")
            
            # Activate skill-specific capabilities
            if skill_name == "docusaurus-setup":
                self._activate_docusaurus_tools()
            elif skill_name == "text-selection-handler":
                self._activate_text_selection()
            
            return True
        else:
            print(f"✗ Skill '{skill_name}' not found")
            return False
    
    def _activate_docusaurus_tools(self):
        """Activate Docusaurus-related tools"""
        print("  → Docusaurus configuration tools loaded")
        print("  → Sidebar generation ready")
        print("  → Theme customization enabled")
    
    def _activate_text_selection(self):
        """Activate text selection capabilities"""
        print("  → Text selection event handlers ready")
        print("  → Context menu integration enabled")
    
    def create_docusaurus_config(
        self,
        project_name: str,
        base_url: str = "/",
        organization_name: str = "yourusername",
        theme_color: str = "#2e8555"
    ) -> Dict[str, Any]:
        """
        Generate Docusaurus configuration
        
        Input:
            project_name: Name of the project
            base_url: Base URL for deployment
            organization_name: GitHub organization/username
            theme_color: Primary theme color
            
        Output:
            Configuration dict (to be written as TypeScript)
        """
        config = {
            "title": project_name,
            "tagline": "AI-Generated Technical Documentation",
            "url": f"https://{organization_name}.github.io",
            "baseUrl": base_url,
            "onBrokenLinks": "throw",
            "onBrokenMarkdownLinks": "warn",
            "favicon": "img/favicon.ico",
            "organizationName": organization_name,
            "projectName": project_name,
            
            "presets": [
                [
                    "classic",
                    {
                        "docs": {
                            "sidebarPath": "./sidebars.ts",
                            "routeBasePath": "/"
                        },
                        "blog": False,
                        "theme": {
                            "customCss": "./src/css/custom.css"
                        }
                    }
                ]
            ],
            
            "themeConfig": {
                "navbar": {
                    "title": project_name,
                    "logo": {"src": "img/logo.svg"},
                    "items": [
                        {"type": "search", "position": "right"}
                    ]
                },
                "footer": {
                    "style": "dark",
                    "copyright": f"Copyright © {datetime.now().year}"
                },
                "colorMode": {
                    "defaultMode": "light",
                    "disableSwitch": False,
                    "respectPrefersColorScheme": True
                },
                "prism": {
                    "theme": "github",
                    "darkTheme": "dracula",
                    "additionalLanguages": ["python", "typescript", "bash"]
                }
            }
        }
        
        self.docusaurus_config = config
        return config
    
    def generate_sidebar_config(
        self,
        chapters: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate sidebar configuration from chapters
        
        Input:
            chapters: List of chapter data with structure
            
        Output:
            Sidebar configuration
        """
        sidebar_items = []
        
        for chapter in chapters:
            item = {
                "type": "category",
                "label": chapter["title"],
                "items": [
                    {
                        "type": "doc",
                        "id": section["id"]
                    }
                    for section in chapter.get("sections", [])
                ]
            }
            sidebar_items.append(item)
        
        return {
            "tutorialSidebar": sidebar_items
        }
    
    def create_chatbot_component(
        self,
        backend_url: str,
        floating_button: bool = True,
        stream_enabled: bool = True
    ) -> Dict[str, str]:
        """
        Generate ChatBot component code
        
        Input:
            backend_url: URL of the FastAPI backend
            floating_button: Whether to show floating button
            stream_enabled: Enable streaming responses
            
        Output:
            Dict with component code files
        """
        chatbot_tsx = f"""import React, {{ useState, useEffect }} from 'react';
import './ChatBot.css';

interface Message {{
  role: 'user' | 'assistant';
  content: string;
}}

interface ChatBotProps {{
  backendUrl: string;
  isOpen: boolean;
  onClose: () => void;
}}

export const ChatBot: React.FC<ChatBotProps> = ({{ backendUrl, isOpen, onClose }}) => {{
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {{
    if (!input.trim()) return;

    const userMessage: Message = {{ role: 'user', content: input }};
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {{
      {'// Streaming implementation' if stream_enabled else '// Non-streaming implementation'}
      const response = await fetch(`${{backendUrl}}/api/chat`, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ question: input }})
      }});

      const data = await response.json();
      const assistantMessage: Message = {{ 
        role: 'assistant', 
        content: data.answer 
      }};
      setMessages(prev => [...prev, assistantMessage]);
    }} catch (error) {{
      console.error('Error:', error);
    }} finally {{
      setLoading(false);
    }}
  }};

  if (!isOpen) return null;

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h3>Ask About This Book</h3>
        <button onClick={{onClose}}>×</button>
      </div>
      <div className="chatbot-messages">
        {{messages.map((msg, i) => (
          <div key={{i}} className={{`message message-${{msg.role}}`}}>
            {{msg.content}}
          </div>
        ))}}
        {{loading && <div className="loading">Thinking...</div>}}
      </div>
      <div className="chatbot-input">
        <input
          value={{input}}
          onChange={{e => setInput(e.target.value)}}
          onKeyPress={{e => e.key === 'Enter' && sendMessage()}}
          placeholder="Ask a question..."
        />
        <button onClick={{sendMessage}}>Send</button>
      </div>
    </div>
  );
}};
"""
        
        floating_button_tsx = """import React, { useState } from 'react';
import { ChatBot } from './ChatBot';
import './FloatingButton.css';

export const FloatingChatButton: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <button 
        className="floating-chat-button"
        onClick={() => setIsOpen(!isOpen)}
      >
        💬
      </button>
      <ChatBot 
        backendUrl={process.env.CHATBOT_API_URL || 'http://localhost:8000'}
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
      />
    </>
  );
};
"""
        
        return {
            "ChatBot.tsx": chatbot_tsx,
            "FloatingButton.tsx": floating_button_tsx,
            "info": {
                "backend_url": backend_url,
                "stream_enabled": stream_enabled,
                "components": ["ChatBot", "FloatingButton"]
            }
        }
    
    def create_text_selector(self) -> str:
        """
        Generate text selection handler component
        
        Output:
            TypeScript code for text selection
        """
        code = """import { useState, useEffect, useCallback } from 'react';

interface SelectionPosition {
  x: number;
  y: number;
}

export const useTextSelection = (minLength: number = 10) => {
  const [selectedText, setSelectedText] = useState('');
  const [position, setPosition] = useState<SelectionPosition | null>(null);

  const clearSelection = useCallback(() => {
    setSelectedText('');
    setPosition(null);
  }, []);

  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection?.toString().trim() || '';

      if (text.length >= minLength) {
        const range = selection?.getRangeAt(0);
        const rect = range?.getBoundingClientRect();

        if (rect) {
          setSelectedText(text);
          setPosition({
            x: rect.left + rect.width / 2,
            y: rect.bottom + window.scrollY
          });
        }
      } else {
        clearSelection();
      }
    };

    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('selectionchange', handleSelection);

    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('selectionchange', handleSelection);
    };
  }, [minLength, clearSelection]);

  return { selectedText, position, clearSelection };
};
"""
        return code
    
    def optimize_performance(
        self,
        config: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """
        Generate performance optimization recommendations
        
        Input:
            config: Current Docusaurus config
            
        Output:
            Optimization recommendations by category
        """
        recommendations = {
            "build_optimization": [
                "Enable webpack code splitting",
                "Minimize CSS and JS bundles",
                "Use dynamic imports for heavy components"
            ],
            "image_optimization": [
                "Convert images to WebP format",
                "Implement lazy loading for images",
                "Use @docusaurus/plugin-ideal-image"
            ],
            "loading_performance": [
                "Preload critical resources",
                "Defer non-critical JavaScript",
                "Minimize third-party scripts"
            ],
            "caching": [
                "Configure service worker for offline access",
                "Set proper cache headers",
                "Use CDN for static assets"
            ]
        }
        
        return recommendations
    
    def create_deployment_workflow(
        self,
        project_name: str,
        node_version: str = "18"
    ) -> str:
        """
        Generate GitHub Actions deployment workflow
        
        Input:
            project_name: Name of the project
            node_version: Node.js version to use
            
        Output:
            YAML workflow configuration
        """
        workflow = f"""name: Deploy {project_name} to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{{{ steps.deployment.outputs.page_url }}}}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: {node_version}
          cache: npm
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build website
        run: npm run build
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./build
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
        return workflow
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main task execution interface
        
        Input:
            task: {
                "action": "configure" | "create_component" | "optimize" | "deploy",
                "params": {...}
            }
            
        Output:
            Task result with status and data
        """
        action = task.get("action")
        params = task.get("params", {})
        
        result = {
            "agent": self.agent_name,
            "action": action,
            "status": "pending",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            if action == "configure_docusaurus":
                result["data"] = self.create_docusaurus_config(**params)
                result["status"] = "success"
                
            elif action == "create_chatbot":
                result["data"] = self.create_chatbot_component(**params)
                result["status"] = "success"
                
            elif action == "create_text_selector":
                result["data"] = {
                    "code": self.create_text_selector(),
                    "filename": "TextSelector.tsx"
                }
                result["status"] = "success"
                
            elif action == "optimize":
                result["data"] = self.optimize_performance(params.get("config", {}))
                result["status"] = "success"
                
            elif action == "create_deployment":
                result["data"] = {
                    "workflow": self.create_deployment_workflow(**params),
                    "filename": "deploy.yml"
                }
                result["status"] = "success"
                
            elif action == "load_skill":
                success = self.load_skill(params.get("skill_name"))
                result["status"] = "success" if success else "failed"
                result["data"] = {"loaded": success}
                
            else:
                result["status"] = "error"
                result["error"] = f"Unknown action: {action}"
                
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """Get current agent status"""
        return {
            "agent": self.agent_name,
            "status": self.status,
            "capabilities": self.capabilities,
            "loaded_skills": list(self.loaded_skills.keys()),
            "docusaurus_configured": self.docusaurus_config is not None
        }


def main():
    """Example usage of FrontendDev agent"""
    print("="*60)
    print("FrontendDev Subagent - Example Usage")
    print("="*60)
    
    # Initialize agent
    agent = FrontendDevAgent(project_root="../../")
    print(f"\n✓ {agent.agent_name} initialized")
    
    # Load skills (Matrix-style)
    print("\n--- Loading Skills ---")
    agent.load_skill("docusaurus-setup")
    agent.load_skill("text-selection-handler")
    
    # Configure Docusaurus
    print("\n--- Configuring Docusaurus ---")
    task = {
        "action": "configure_docusaurus",
        "params": {
            "project_name": "AI Book with RAG",
            "base_url": "/ai-book-rag/",
            "organization_name": "yourusername"
        }
    }
    result = agent.execute_task(task)
    print(f"Status: {result['status']}")
    print(f"Config Keys: {list(result['data'].keys())}")
    
    # Create ChatBot component
    print("\n--- Creating ChatBot Component ---")
    task = {
        "action": "create_chatbot",
        "params": {
            "backend_url": "https://your-backend.vercel.app",
            "floating_button": True,
            "stream_enabled": True
        }
    }
    result = agent.execute_task(task)
    print(f"Status: {result['status']}")
    print(f"Components: {result['data']['info']['components']}")
    
    # Create text selector
    print("\n--- Creating Text Selector ---")
    task = {"action": "create_text_selector", "params": {}}
    result = agent.execute_task(task)
    print(f"Status: {result['status']}")
    print(f"Filename: {result['data']['filename']}")
    
    # Get optimization recommendations
    print("\n--- Performance Optimization ---")
    task = {"action": "optimize", "params": {"config": {}}}
    result = agent.execute_task(task)
    print(f"Status: {result['status']}")
    print("Recommendations:")
    for category, recs in result['data'].items():
        print(f"  {category}: {len(recs)} items")
    
    # Get status
    print("\n--- Agent Status ---")
    status = agent.get_status()
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
