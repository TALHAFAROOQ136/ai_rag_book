"""
BookWriter Subagent
===================
Content Generation and Structure specialist

Capabilities:
- Generate technical book content
- Organize content into logical chapters
- Create code examples with explanations
- Develop cross-references and metadata
- Ensure consistent terminology and style

Matrix-Style Skill Loading:
- Can dynamically load skills like "Docusaurus Setup" for understanding file structure
"""

import os
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class BookWriterAgent:
    """
    BookWriter Subagent - Content Generation Specialist
    
    Responsibilities:
    - Generate comprehensive technical content
    - Organize content into chapters and sections
    - Create code examples and diagrams
    - Maintain consistent style and terminology
    """
    
    def __init__(self, project_root: str):
        self.agent_name = "BookWriter"
        self.project_root = Path(project_root)
        self.loaded_skills = {}
        self.capabilities = [
            "content_generation",
            "code_example_creation",
            "metadata_generation",
            "cross_reference_creation",
            "style_consistency_check"
        ]
        self.status = "initialized"
        
    def load_skill(self, skill_name: str) -> bool:
        """
        Matrix-style skill loading
        
        Args:
            skill_name: Name of skill to load (e.g., "docusaurus-setup")
            
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
            return True
        else:
            print(f"✗ Skill '{skill_name}' not found")
            return False
    
    def generate_chapter_outline(
        self,
        book_topic: str,
        num_chapters: int = 4,
        target_audience: str = "developers"
    ) -> Dict[str, Any]:
        """
        Generate book outline
        
        Input:
            book_topic: Main topic (e.g., "Introduction to RAG")
            num_chapters: Number of chapters (default: 4)
            target_audience: Target reader level
            
        Output:
            Dict with chapter structure and page estimates
        """
        outline = {
            "book_title": book_topic,
            "target_audience": target_audience,
            "chapters": [],
            "estimated_pages": 0,
            "generated_at": datetime.utcnow().isoformat()
        }
        
        # Chapter templates for RAG topic (example)
        if "rag" in book_topic.lower():
            chapters = [
                {
                    "number": 1,
                    "title": "Introduction to RAG",
                    "sections": ["What is RAG?", "Why RAG Matters", "Prerequisites"],
                    "estimated_pages": 3
                },
                {
                    "number": 2,
                    "title": "Core Concepts",
                    "sections": ["Vector Embeddings", "Similarity Search", "Context Augmentation"],
                    "estimated_pages": 4
                },
                {
                    "number": 3,
                    "title": "Implementation",
                    "sections": ["Building the Pipeline", "Tools and Libraries", "Best Practices"],
                    "estimated_pages": 3
                },
                {
                    "number": 4,
                    "title": "Advanced Topics",
                    "sections": ["Optimization", "Real-World Applications", "Further Resources"],
                    "estimated_pages": 2
                }
            ]
        else:
            # Generic structure
            chapters = [
                {"number": i+1, "title": f"Chapter {i+1}", "sections": [], "estimated_pages": 3}
                for i in range(num_chapters)
            ]
        
        outline["chapters"] = chapters
        outline["estimated_pages"] = sum(ch["estimated_pages"] for ch in chapters)
        
        return outline
    
    def generate_page_content(
        self,
        chapter_num: int,
        chapter_title: str,
        section_title: str,
        context: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate content for a specific page
        
        Input:
            chapter_num: Chapter number
            chapter_title: Chapter title
            section_title: Section within chapter
            context: Additional context for generation
            
        Output:
            Dict with markdown content and metadata
        """
        # This is a template - in real implementation, would use LLM
        content = f"""---
id: chapter-{chapter_num}-{section_title.lower().replace(' ', '-')}
title: {section_title}
sidebar_position: {chapter_num}
---

# {section_title}

{context or 'Content will be generated here based on the topic.'}

## Overview

This section covers the fundamental concepts of {section_title.lower()}.

## Key Points

- Point 1
- Point 2
- Point 3

## Example

```python
# Example code for {section_title}
def example_function():
    return "Generated content"
```

## Summary

In this section, we covered...

---

**Next**: [Continue to next section](#)
"""
        
        return {
            "content": content,
            "filename": f"chapter{chapter_num}-{section_title.lower().replace(' ', '-')}.md",
            "chapter": chapter_num,
            "title": section_title,
            "word_count": len(content.split()),
            "has_code": True,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def create_category_metadata(
        self,
        chapter_num: int,
        chapter_title: str,
        description: str
    ) -> Dict[str, Any]:
        """
        Create _category_.json for Docusaurus
        
        Input:
            chapter_num: Chapter number
            chapter_title: Chapter title
            description: Chapter description
            
        Output:
            Dict ready to be written as JSON
        """
        return {
            "label": chapter_title,
            "position": chapter_num,
            "link": {
                "type": "generated-index",
                "description": description
            }
        }
    
    def validate_content_quality(
        self,
        content: str
    ) -> Dict[str, Any]:
        """
        Validate content quality
        
        Input:
            content: Markdown content to validate
            
        Output:
            Validation report with scores and issues
        """
        report = {
            "word_count": len(content.split()),
            "has_code_blocks": "```" in content,
            "has_headings": "#" in content,
            "has_links": "[" in content and "]" in content,
            "estimated_read_time_minutes": len(content.split()) / 200,
            "quality_score": 0.0,
            "issues": []
        }
        
        # Quality scoring
        score = 0
        if report["word_count"] >= 200:
            score += 25
        else:
            report["issues"].append(f"Content too short: {report['word_count']} words")
        
        if report["has_code_blocks"]:
            score += 25
        
        if report["has_headings"]:
            score += 25
        
        if report["has_links"]:
            score += 25
        
        report["quality_score"] = score
        
        return report
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main task execution interface
        
        Input:
            task: {
                "action": "generate_outline" | "generate_content" | "validate",
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
            if action == "generate_outline":
                result["data"] = self.generate_chapter_outline(**params)
                result["status"] = "success"
                
            elif action == "generate_content":
                result["data"] = self.generate_page_content(**params)
                result["status"] = "success"
                
            elif action == "validate":
                result["data"] = self.validate_content_quality(params.get("content", ""))
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
            "skill_count": len(self.loaded_skills)
        }


def main():
    """Example usage of BookWriter agent"""
    print("="*60)
    print("BookWriter Subagent - Example Usage")
    print("="*60)
    
    # Initialize agent
    agent = BookWriterAgent(project_root="../../")
    print(f"\n✓ {agent.agent_name} initialized")
    
    # Load skill (Matrix-style)
    print("\n--- Loading Skill ---")
    agent.load_skill("docusaurus-setup")
    
    # Generate outline
    print("\n--- Generating Outline ---")
    task = {
        "action": "generate_outline",
        "params": {
            "book_topic": "Introduction to RAG (Retrieval-Augmented Generation)",
            "num_chapters": 4,
            "target_audience": "developers with Python knowledge"
        }
    }
    result = agent.execute_task(task)
    print(f"Status: {result['status']}")
    print(f"Chapters: {len(result['data']['chapters'])}")
    print(f"Estimated Pages: {result['data']['estimated_pages']}")
    
    # Generate content
    print("\n--- Generating Page Content ---")
    task = {
        "action": "generate_content",
        "params": {
            "chapter_num": 1,
            "chapter_title": "Introduction to RAG",
            "section_title": "What is RAG?",
            "context": "RAG combines retrieval and generation for better AI responses."
        }
    }
    result = agent.execute_task(task)
    print(f"Status: {result['status']}")
    print(f"Filename: {result['data']['filename']}")
    print(f"Word Count: {result['data']['word_count']}")
    
    # Validate content
    print("\n--- Validating Content ---")
    task = {
        "action": "validate",
        "params": {
            "content": result['data']['content']
        }
    }
    validation = agent.execute_task(task)
    print(f"Quality Score: {validation['data']['quality_score']}/100")
    print(f"Issues: {validation['data']['issues']}")
    
    # Get status
    print("\n--- Agent Status ---")
    status = agent.get_status()
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
