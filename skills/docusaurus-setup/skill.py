"""
Docusaurus Setup Skill
======================
Initialize and configure Docusaurus projects with optimal settings

This skill is reusable across any documentation project and can be
imported by any subagent (primarily FrontendDev).

Matrix-Style Loading: ✓
Self-Contained: ✓
Importable: ✓
"""

import json
import subprocess
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime


class DocusaurusSetup:
    """
    Docusaurus Setup Skill
    
    Capabilities:
    - Initialize Docusaurus project
    - Generate configuration files
    - Set up custom themes
    - Configure search and navigation
    - Create initial content structure
    """
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.skill_name = "Docusaurus Setup"
        self.version = "1.0.0"
    
    def create_docusaurus_config(
        self,
        project_name: str,
        title: str,
        tagline: str,
        url: str,
        base_url: str = "/",
        organization_name: str = "yourusername",
        theme_color: str = "#2e8555",
        enable_search: bool = True,
        enable_dark_mode: bool = True
    ) -> str:
        """
        Generate docusaurus.config.ts content
        
        Args:
            project_name: Project name (kebab-case)
            title: Site title
            tagline: Site tagline
            url: Production URL
            base_url: Base URL path
            organization_name: GitHub org/username
            theme_color: Primary theme color
            enable_search: Enable local search
            enable_dark_mode: Enable dark mode toggle
            
        Returns:
            TypeScript configuration as string
        """
        config = f"""import {{themes as prismThemes}} from 'prism-react-renderer';
import type {{Config}} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {{
  title: '{title}',
  tagline: '{tagline}',
  favicon: 'img/favicon.ico',

  url: '{url}',
  baseUrl: '{base_url}',

  organizationName: '{organization_name}',
  projectName: '{project_name}',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {{
    defaultLocale: 'en',
    locales: ['en'],
  }},

  presets: [
    [
      'classic',
      {{
        docs: {{
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
        }},
        blog: false,
        theme: {{
          customCss: './src/css/custom.css',
        }},
      }} satisfies Preset.Options,
    ],
  ],

  themeConfig: {{
    image: 'img/social-card.jpg',
    navbar: {{
      title: '{title}',
      logo: {{
        alt: '{title} Logo',
        src: 'img/logo.svg',
      }},
      items: [
        {{'type': 'search', 'position': 'right'}} if enable_search else ''
      ],
    }},
    footer: {{
      style: 'dark',
      copyright: `Copyright © ${{new Date().getFullYear()}} {title}.`,
    }},
    prism: {{
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'typescript', 'bash', 'json'],
    }},
    colorMode: {{
      defaultMode: 'light',
      disableSwitch: {str(not enable_dark_mode).lower()},
      respectPrefersColorScheme: true,
    }},
  }} satisfies Preset.ThemeConfig,
}};

export default config;
"""
        return config
    
    def create_sidebar_config(
        self,
        chapters: List[Dict[str, Any]]
    ) -> str:
        """
        Generate sidebars.ts content
        
        Args:
            chapters: List of chapter structures
            
        Returns:
            TypeScript sidebar configuration
        """
        # Convert chapters to sidebar items
        sidebar_items = []
        for chapter in chapters:
            if chapter.get("sections"):
                # Category with items
                items = [f"'{section['id']}'" for section in chapter["sections"]]
                sidebar_items.append(f"""  {{
    type: 'category',
    label: '{chapter['title']}',
    items: [{', '.join(items)}],
  }}""")
            else:
                # Single document
                sidebar_items.append(f"  '{chapter['id']}'")
        
        config = f"""import type {{SidebarsConfig}} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {{
  tutorialSidebar: [
{',\\n'.join(sidebar_items)}
  ],
}};

export default sidebars;
"""
        return config
    
    def create_custom_css(
        self,
        primary_color: str = "#2e8555",
        secondary_color: str = "#2563eb"
    ) -> str:
        """
        Generate custom.css with theme variables
        
        Args:
            primary_color: Primary brand color
            secondary_color: Secondary accent color
            
        Returns:
            CSS content
        """
        css = f"""/**
 * Custom CSS for enhanced book styling
 */

:root {{
  --ifm-color-primary: {primary_color};
  --ifm-color-primary-dark: #26a55e;
  --ifm-color-primary-darker: #249556;
  --ifm-color-primary-darkest: #1e7b47;
  --ifm-color-primary-light: #32d673;
  --ifm-color-primary-lighter: #38de79;
  --ifm-color-primary-lightest: #4ce68a;
  
  --ifm-code-font-size: 95%;
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.1);
}}

[data-theme='dark'] {{
  --ifm-color-primary: #35d67a;
  --ifm-color-primary-dark: #24d066;
  --ifm-color-primary-darker: #1fc55e;
  --ifm-color-primary-darkest: #19a24d;
  --ifm-color-primary-light: #4ddc8e;
  --ifm-color-primary-lighter: #57df96;
  --ifm-color-primary-lightest: #75e5ab;
  
  --docusaurus-highlighted-code-line-bg: rgba(0, 0, 0, 0.3);
}}

/* Enhanced code blocks */
.theme-code-block {{
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}}

/* Better link styling */
article a:not(.hash-link) {{
  text-decoration: underline;
  text-decoration-color: var(--ifm-color-primary);
  text-decoration-thickness: 2px;
}}

article a:not(.hash-link):hover {{
  text-decoration-thickness: 3px;
}}

/* Improved heading anchors */
.hash-link {{
  opacity: 0;
  transition: opacity 0.2s;
}}

h1:hover .hash-link,
h2:hover .hash-link,
h3:hover .hash-link {{
  opacity: 0.6;
}}

.hash-link:hover {{
  opacity: 1 !important;
}}
"""
        return css
    
    def create_package_json(
        self,
        project_name: str,
        docusaurus_version: str = "3.0.0"
    ) -> str:
        """
        Generate package.json
        
        Args:
            project_name: Project name
            docusaurus_version: Docusaurus version
            
        Returns:
            JSON content as string
        """
        package = {
            "name": project_name,
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "docusaurus": "docusaurus",
                "start": "docusaurus start",
                "build": "docusaurus build",
                "swizzle": "docusaurus swizzle",
                "deploy": "docusaurus deploy",
                "clear": "docusaurus clear",
                "serve": "docusaurus serve",
                "write-translations": "docusaurus write-translations",
                "write-heading-ids": "docusaurus write-heading-ids"
            },
            "dependencies": {
                "@docusaurus/core": f"^{docusaurus_version}",
                "@docusaurus/preset-classic": f"^{docusaurus_version}",
                "@mdx-js/react": "^3.0.0",
                "clsx": "^2.0.0",
                "prism-react-renderer": "^2.1.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            },
            "devDependencies": {
                "@docusaurus/module-type-aliases": f"^{docusaurus_version}",
                "@docusaurus/types": f"^{docusaurus_version}",
                "typescript": "~5.2.0"
            },
            "engines": {
                "node": ">=18.0"
            }
        }
        
        return json.dumps(package, indent=2)
    
    def initialize_project(
        self,
        project_path: Path,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Complete project initialization
        
        Args:
            project_path: Path where to create project
            config: Configuration dictionary
            
        Returns:
            Result with created files and status
        """
        project_path = Path(project_path)
        project_path.mkdir(parents=True, exist_ok=True)
        
        result = {
            "project_path": str(project_path),
            "files_created": [],
            "status": "success",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            # Create docusaurus.config.ts
            config_content = self.create_docusaurus_config(**config.get("docusaurus", {}))
            config_file = project_path / "docusaurus.config.ts"
            config_file.write_text(config_content, encoding='utf-8')
            result["files_created"].append(str(config_file))
            
            # Create sidebars.ts
            sidebar_content = self.create_sidebar_config(config.get("chapters", []))
            sidebar_file = project_path / "sidebars.ts"
            sidebar_file.write_text(sidebar_content, encoding='utf-8')
            result["files_created"].append(str(sidebar_file))
            
            # Create custom.css
            css_dir = project_path / "src" / "css"
            css_dir.mkdir(parents=True, exist_ok=True)
            css_content = self.create_custom_css(
                config.get("primary_color", "#2e8555"),
                config.get("secondary_color", "#2563eb")
            )
            css_file = css_dir / "custom.css"
            css_file.write_text(css_content, encoding='utf-8')
            result["files_created"].append(str(css_file))
            
            # Create package.json
            package_content = self.create_package_json(
                config.get("project_name", "my-docusaurus-site")
            )
            package_file = project_path / "package.json"
            package_file.write_text(package_content, encoding='utf-8')
            result["files_created"].append(str(package_file))
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result


# Example usage
def main():
    """Example usage of Docusaurus Setup Skill"""
    print("="*60)
    print("Docusaurus Setup Skill - Example Usage")
    print("="*60)
    
    skill = DocusaurusSetup(project_root=Path("../../"))
    
    # Example 1: Generate config
    print("\n[Example 1] Generate Docusaurus Config")
    config = skill.create_docusaurus_config(
        project_name="ai-book-rag",
        title="AI Book with RAG",
        tagline="Learn RAG with AI-generated content",
        url="https://yourusername.github.io",
        base_url="/ai-book-rag/",
        organization_name="yourusername"
    )
    print(f"✓ Generated config ({len(config)} chars)")
    
    # Example 2: Generate sidebar
    print("\n[Example 2] Generate Sidebar Config")
    chapters = [
        {
            "id": "intro",
            "title": "Introduction",
            "sections": [
                {"id": "intro/welcome"},
                {"id": "intro/prerequisites"}
            ]
        },
        {
            "id": "chapter-1",
            "title": "Chapter 1: Basics",
            "sections": [
                {"id": "chapter-1/overview"},
                {"id": "chapter-1/concepts"}
            ]
        }
    ]
    sidebar = skill.create_sidebar_config(chapters)
    print(f"✓ Generated sidebar ({len(sidebar)} chars)")
    
    # Example 3: Generate custom CSS
    print("\n[Example 3] Generate Custom CSS")
    css = skill.create_custom_css("#2563eb", "#7c3aed")
    print(f"✓ Generated CSS ({len(css)} chars)")
    
    print("\n" + "="*60)
    print("Skill demonstration complete")
    print("="*60)


if __name__ == "__main__":
    main()
