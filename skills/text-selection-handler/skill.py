"""
Text Selection Handler Skill
=============================
Capture and process user text selections in web pages

This skill provides browser-based text selection detection
and context menu integration for enhanced UX.

Matrix-Style Loading: ✓
Self-Contained: ✓
Importable: ✓
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class TextSelectionHandler:
    """
    Text Selection Handler Skill
    
    Capabilities:
    - Detect text selections in browser
    - Create custom context menus
    - Handle selection events
    - Extract selection metadata
    - Integrate with chat interfaces
    
    Note: This generates TypeScript/React code for browser use
    """
    
    def __init__(self):
        self.skill_name = "Text Selection Handler"
        self.version = "1.0.0"
    
    def create_selection_hook(
        self,
        min_length: int = 10,
        enable_position_tracking: bool = True
    ) -> str:
        """
        Generate React hook for text selection
        
        Args:
            min_length: Minimum selection length to trigger
            enable_position_tracking: Track selection position for UI placement
            
        Returns:
            TypeScript React hook code
        """
        code = f"""import {{ useState, useEffect, useCallback }} from 'react';

interface SelectionPosition {{
  x: number;
  y: number;
  width: number;
  height: number;
}}

interface UseTextSelectionReturn {{
  selectedText: string;
  position: SelectionPosition | null;
  clearSelection: () => void;
  isActive: boolean;
}}

/**
 * Custom hook to handle text selection in the document
 * 
 * @param minLength - Minimum number of characters to consider a valid selection
 * @returns Selected text, position, and control functions
 */
export const useTextSelection = (
  minLength: number = {min_length}
): UseTextSelectionReturn => {{
  const [selectedText, setSelectedText] = useState<string>('');
  const [position, setPosition] = useState<SelectionPosition | null>(null);

  const clearSelection = useCallback(() => {{
    setSelectedText('');
    setPosition(null);
    window.getSelection()?.removeAllRanges();
  }}, []);

  useEffect(() => {{
    const handleSelection = () => {{
      const selection = window.getSelection();
      const text = selection?.toString().trim() || '';

      if (text.length >= minLength) {{
        setSelectedText(text);
        
{'        // Track position for UI placement' if enable_position_tracking else ''}
{'        const range = selection?.getRangeAt(0);' if enable_position_tracking else ''}
{'        const rect = range?.getBoundingClientRect();' if enable_position_tracking else ''}
{'        ' if enable_position_tracking else ''}
{'        if (rect) {' if enable_position_tracking else ''}
{'          setPosition({' if enable_position_tracking else ''}
{'            x: rect.left + rect.width / 2,' if enable_position_tracking else ''}
{'            y: rect.bottom + window.scrollY,' if enable_position_tracking else ''}
{'            width: rect.width,' if enable_position_tracking else ''}
{'            height: rect.height' if enable_position_tracking else ''}
{'          });' if enable_position_tracking else ''}
{'        }' if enable_position_tracking else ''}
      }} else {{
        clearSelection();
      }}
    }};

    // Listen to mouseup for selection completion
    document.addEventListener('mouseup', handleSelection);
    
    // Listen to selectionchange for real-time updates
    document.addEventListener('selectionchange', handleSelection);

    return () => {{
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('selectionchange', handleSelection);
    }};
  }}, [minLength, clearSelection]);

  return {{
    selectedText,
    position,
    clearSelection,
    isActive: selectedText.length > 0
  }};
}};
"""
        return code
    
    def create_context_menu_component(
        self,
        actions: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate context menu component for selections
        
        Args:
            actions: List of action configs with label and handler name
            
        Returns:
            TypeScript React component code
        """
        default_actions = actions or [
            {"label": "Ask about this", "handler": "onAskAbout"},
            {"label": "Copy", "handler": "onCopy"}
        ]
        
        action_items = "\n".join([
            f"""        <button
          onClick={() => {action['handler']}(selectedText)}}
          className="selection-menu-item"
        >
          {action['label']}
        </button>"""
            for action in default_actions
        ])
        
        code = f"""import React from 'react';
import './SelectionMenu.css';

interface SelectionMenuProps {{
  selectedText: string;
  position: {{ x: number; y: number }} | null;
  onAskAbout: (text: string) => void;
  onCopy: (text: string) => void;
  onClose: () => void;
}}

/**
 * Context menu that appears when text is selected
 */
export const SelectionMenu: React.FC<SelectionMenuProps> = ({{
  selectedText,
  position,
  onAskAbout,
  onCopy,
  onClose
}}) => {{
  if (!position || !selectedText) return null;

  return (
    <div
      className="selection-menu"
      style={{{{
        position: 'absolute',
        left: `${{position.x}}px`,
        top: `${{position.y}}px`,
        transform: 'translateX(-50%)'
      }}}}
    >
{action_items}
      <button
        onClick={{onClose}}
        className="selection-menu-close"
      >
        ✕
      </button>
    </div>
  );
}};
"""
        return code
    
    def create_context_menu_styles(self) -> str:
        """
        Generate CSS for context menu
        
        Returns:
            CSS code
        """
        css = """.selection-menu {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 8px;
  z-index: 9999;
  display: flex;
  gap: 4px;
  animation: fadeIn 0.2s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

.selection-menu-item {
  background: transparent;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #2d3748;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.selection-menu-item:hover {
  background-color: #edf2f7;
}

.selection-menu-close {
  background: transparent;
  border: none;
  padding: 4px 8px;
  cursor: pointer;
  color: #718096;
  font-size: 16px;
  margin-left: 4px;
}

.selection-menu-close:hover {
  color: #2d3748;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .selection-menu {
    background: #2d3748;
    border-color: #4a5568;
  }
  
  .selection-menu-item {
    color: #e2e8f0;
  }
  
  .selection-menu-item:hover {
    background-color: #4a5568;
  }
  
  .selection-menu-close {
    color: #a0aec0;
  }
  
  .selection-menu-close:hover {
    color: #e2e8f0;
  }
}
"""
        return css
    
    def create_integration_example(self) -> str:
        """
        Generate example integration with chat component
        
        Returns:
            TypeScript example code
        """
        code = """import React, { useState } from 'react';
import { useTextSelection } from './hooks/useTextSelection';
import { SelectionMenu } from './components/SelectionMenu';
import { ChatBot } from './components/ChatBot';

/**
 * Example: Integrate text selection with chat component
 */
export const BookPageWithChat: React.FC = () => {
  const [chatOpen, setChatOpen] = useState(false);
  const [initialQuestion, setInitialQuestion] = useState('');
  
  const { selectedText, position, clearSelection, isActive } = useTextSelection();

  const handleAskAbout = (text: string) => {
    // Pre-populate chat with selected text
    setInitialQuestion(`Can you explain this: "${text}"`);
    setChatOpen(true);
    clearSelection();
  };

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    clearSelection();
  };

  return (
    <div className="book-page">
      {/* Book content here */}
      <article>
        {/* User can select any text in this area */}
      </article>

      {/* Selection menu appears when text is selected */}
      {isActive && (
        <SelectionMenu
          selectedText={selectedText}
          position={position}
          onAskAbout={handleAskAbout}
          onCopy={handleCopy}
          onClose={clearSelection}
        />
      )}

      {/* Chat component */}
      <ChatBot
        isOpen={chatOpen}
        onClose={() => setChatOpen(false)}
        initialQuestion={initialQuestion}
      />
    </div>
  );
};
"""
        return code
    
    def create_usage_instructions(self) -> Dict[str, Any]:
        """
        Generate usage instructions
        
        Returns:
            Installation and usage guide
        """
        return {
            "installation": {
                "steps": [
                    "1. Copy useTextSelection.tsx to src/hooks/",
                    "2. Copy SelectionMenu.tsx to src/components/",
                    "3. Copy SelectionMenu.css to src/components/",
                    "4. Import and use in your page components"
                ]
            },
            "basic_usage": {
                "description": "Minimal implementation",
                "code": """const { selectedText, position } = useTextSelection();

// Use selectedText and position in your UI
if (selectedText) {
  console.log('User selected:', selectedText);
}"""
            },
            "advanced_usage": {
                "description": "Integration with chat",
                "code": """const { selectedText, clearSelection } = useTextSelection();

const handleAskAbout = (text: string) => {
  openChat({ context: text });
  clearSelection();
};"""
            },
            "customization": {
                "min_length": "Change minimum selection length",
                "actions": "Customize context menu actions",
                "styling": "Modify SelectionMenu.css for your theme"
            }
        }


# Example usage
def main():
    """Example usage of Text Selection Handler Skill"""
    print("="*60)
    print("Text Selection Handler Skill - Example Usage")
    print("="*60)
    
    skill = TextSelectionHandler()
    
    # Example 1: Create selection hook
    print("\n[Example 1] Create Text Selection Hook")
    hook_code = skill.create_selection_hook(
        min_length=15,
        enable_position_tracking=True
    )
    print(f"✓ Hook created ({len(hook_code)} chars)")
    print(f"  Min length: 15 characters")
    print(f"  Position tracking: Enabled")
    
    # Example 2: Create context menu
    print("\n[Example 2] Create Context Menu Component")
    actions = [
        {"label": "Ask AI about this", "handler": "onAskAI"},
        {"label": "Search in book", "handler": "onSearch"},
        {"label": "Copy", "handler": "onCopy"}
    ]
    menu_code = skill.create_context_menu_component(actions)
    print(f"✓ Context menu created ({len(menu_code)} chars)")
    print(f"  Actions: {len(actions)}")
    
    # Example 3: Generate styles
    print("\n[Example 3] Generate CSS Styles")
    css = skill.create_context_menu_styles()
    print(f"✓ Styles created ({len(css)} chars)")
    print(f"  Dark mode support: Yes")
    
    # Example 4: Integration example
    print("\n[Example 4] Create Integration Example")
    integration = skill.create_integration_example()
    print(f"✓ Integration example created ({len(integration)} chars)")
    
    # Example 5: Usage instructions
    print("\n[Example 5] Generate Usage Instructions")
    instructions = skill.create_usage_instructions()
    print(f"✓ Instructions created")
    print(f"  Installation steps: {len(instructions['installation']['steps'])}")
    print(f"  Usage examples: {len([k for k in instructions.keys() if 'usage' in k])}")
    
    print("\n" + "="*60)
    print("Skill demonstration complete")
    print("="*60)


if __name__ == "__main__":
    main()
