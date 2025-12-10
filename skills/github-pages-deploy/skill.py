"""
GitHub Pages Deploy Skill
==========================
Set up automated deployment to GitHub Pages

This skill provides GitHub Actions workflow generation and
repository configuration for automated static site deployment.

Matrix-Style Loading: ✓
Self-Contained: ✓
Importable: ✓
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path


class GitHubPagesDeploy:
    """
    GitHub Pages Deploy Skill
    
    Capabilities:
    - Generate GitHub Actions workflows
    - Configure repository settings
    - Support multiple static site generators
    - Custom domain configuration
    - Optimize deployment caching
    """
    
    def __init__(self):
        self.skill_name = "GitHub Pages Deploy"
        self.version = "1.0.0"
    
    def create_deployment_workflow(
        self,
        site_generator: str = "docusaurus",
        node_version: str = "18",
        build_command: str = "npm run build",
        build_dir: str = "./build",
        working_directory: Optional[str] = None,
        custom_domain: Optional[str] = None
    ) -> str:
        """
        Generate GitHub Actions workflow for deployment
        
        Args:
            site_generator: Type of site (docusaurus, vite, nextjs, etc.)
            node_version: Node.js version to use
            build_command: Command to build the site
            build_dir: Directory containing built files
            working_directory: Working directory for commands (if nested)
            custom_domain: Custom domain name (optional)
            
        Returns:
            YAML workflow content
        """
        # Build working directory prefix for commands
        wd_prefix = ""
        if working_directory:
            wd_prefix = f"\n        working-directory: {working_directory}"
        
        # Custom domain step
        cname_step = ""
        if custom_domain:
            cname_step = f"""
      - name: Add CNAME for custom domain
        run: echo '{custom_domain}' > {build_dir}/CNAME{wd_prefix}
"""
        
        workflow = f"""name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{{{ steps.deployment.outputs.page_url }}}}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: {node_version}
          cache: npm{wd_prefix if working_directory else f"\n          cache-dependency-path: {working_directory}/package-lock.json" if working_directory else ""}
      
      - name: Install dependencies
        run: npm ci{wd_prefix}
      
      - name: Build website
        run: {build_command}{wd_prefix}
{cname_step}      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: {build_dir}
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""
        return workflow
    
    def create_prebuild_workflow(
        self,
        checks: List[str] = None
    ) -> str:
        """
        Create pre-build validation workflow
        
        Args:
            checks: List of checks to run (lint, test, etc.)
            
        Returns:
            YAML workflow for CI checks
        """
        checks = checks or ["lint", "test"]
        
        check_steps = []
        if "lint" in checks:
            check_steps.append("""      - name: Run linter
        run: npm run lint
        continue-on-error: true""")
        
        if "test" in checks:
            check_steps.append("""      - name: Run tests
        run: npm test
        continue-on-error: true""")
        
        if "typecheck" in checks:
            check_steps.append("""      - name: Type check
        run: npm run typecheck
        continue-on-error: true""")
        
        workflow = f"""name: CI Checks

on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [develop]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: npm
      
      - name: Install dependencies
        run: npm ci
      
{chr(10).join(check_steps)}
"""
        return workflow
    
    def create_repository_config(
        self,
        enable_pages: bool = True,
        branch: str = "main",
        custom_domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate repository settings configuration
        
        Args:
            enable_pages: Enable GitHub Pages
            branch: Source branch for Pages
            custom_domain: Custom domain (optional)
            
        Returns:
            Configuration instructions dict
        """
        config = {
            "github_pages": {
                "enabled": enable_pages,
                "source": {
                    "branch": branch,
                    "path": "/"
                },
                "custom_domain": custom_domain
            },
            "instructions": [
                "1. Go to repository Settings → Pages",
                f"2. Set Source to 'GitHub Actions'",
                "3. Save the settings"
            ]
        }
        
        if custom_domain:
            config["instructions"].extend([
                f"4. Add custom domain: {custom_domain}",
                "5. Configure DNS records at your domain provider:",
                "   - Add A records pointing to GitHub Pages IPs",
                "   - Or add CNAME record pointing to <username>.github.io"
            ])
        
        return config
    
    def create_deployment_checklist(
        self,
        project_type: str = "docusaurus"
    ) -> List[str]:
        """
        Generate deployment checklist
        
        Args:
            project_type: Type of project being deployed
            
        Returns:
            List of checklist items
        """
        common_checklist = [
            "✓ Repository is public (or you have GitHub Pro for private repos)",
            "✓ package.json exists with build script",
            "✓ Build succeeds locally (npm run build)",
            "✓ Build output directory is correct",
            "✓ GitHub Actions workflow file in .github/workflows/",
            "✓ Repository Settings → Pages is configured",
            "✓ First deployment workflow has run successfully"
        ]
        
        if project_type == "docusaurus":
            common_checklist.extend([
                "✓ docusaurus.config.ts has correct url and baseUrl",
                "✓ Static assets are in static/ directory",
                "✓ All internal links use relative paths"
            ])
        
        if project_type == "vite":
            common_checklist.extend([
                "✓ vite.config.ts has correct base path",
                "✓ Public assets are in public/ directory"
            ])
        
        return common_checklist
    
    def troubleshoot_deployment(
        self,
        error_type: str
    ) -> Dict[str, Any]:
        """
        Provide troubleshooting guidance for common issues
        
        Args:
            error_type: Type of error (build_failed, 404, assets_missing, etc.)
            
        Returns:
            Troubleshooting guide
        """
        guides = {
            "build_failed": {
                "issue": "Build fails in GitHub Actions",
                "causes": [
                    "Missing dependencies in package.json",
                    "Build script not defined",
                    "Environment-specific code (window, document) in SSR",
                    "Node version mismatch"
                ],
                "solutions": [
                    "Run 'npm run build' locally to reproduce",
                    "Check package.json has all dependencies",
                    "Use dynamic imports for client-only code",
                    "Match Node version in workflow to local version"
                ]
            },
            "404_error": {
                "issue": "Site shows 404 after deployment",
                "causes": [
                    "Incorrect baseUrl in config",
                    "Wrong build directory specified",
                    "Pages source not set to GitHub Actions"
                ],
                "solutions": [
                    "Check baseUrl matches repository name (e.g., '/my-repo/')",
                    "Verify build directory in workflow matches actual output",
                    "Go to Settings → Pages and select 'GitHub Actions' as source"
                ]
            },
            "assets_missing": {
                "issue": "CSS/JS/images not loading",
                "causes": [
                    "Absolute paths instead of relative",
                    "Incorrect public path configuration",
                    "Assets not included in build output"
                ],
                "solutions": [
                    "Use relative paths for all assets",
                    "Check build output includes all required files",
                    "Verify publicPath or base configuration"
                ]
            },
            "slow_builds": {
                "issue": "Deployment takes too long",
                "causes": [
                    "No caching of dependencies",
                    "Heavy dependencies installed every time",
                    "Large build output"
                ],
                "solutions": [
                    "Enable npm caching in workflow (already included)",
                    "Use 'npm ci' instead of 'npm install'",
                    "Optimize bundle size with code splitting"
                ]
            }
        }
        
        return guides.get(error_type, {
            "issue": "Unknown error",
            "solutions": ["Check GitHub Actions logs for specific error messages"]
        })


# Example usage
def main():
    """Example usage of GitHub Pages Deploy Skill"""
    print("="*60)
    print("GitHub Pages Deploy Skill - Example Usage")
    print("="*60)
    
    skill = GitHubPagesDeploy()
    
    # Example 1: Create deployment workflow
    print("\n[Example 1] Create Deployment Workflow (Docusaurus)")
    workflow = skill.create_deployment_workflow(
        site_generator="docusaurus",
        node_version="18",
        build_command="npm run build",
        build_dir="./build",
        working_directory="./book",
        custom_domain="mybook.example.com"
    )
    print(f"✓ Workflow created ({len(workflow)} chars)")
    print(f"  Node version: 18")
    print(f"  Custom domain: mybook.example.com")
    
    # Example 2: Create CI workflow
    print("\n[Example 2] Create Pre-Build CI Workflow")
    ci_workflow = skill.create_prebuild_workflow(
        checks=["lint", "test", "typecheck"]
    )
    print(f"✓ CI workflow created ({len(ci_workflow)} chars)")
    print(f"  Checks: lint, test, typecheck")
    
    # Example 3: Repository configuration
    print("\n[Example 3] Repository Configuration Guide")
    config = skill.create_repository_config(
        enable_pages=True,
        branch="main",
        custom_domain="mybook.example.com"
    )
    print(f"✓ Configuration guide created")
    print("  Instructions:")
    for instruction in config["instructions"]:
        print(f"    {instruction}")
    
    # Example 4: Deployment checklist
    print("\n[Example 4] Deployment Checklist")
    checklist = skill.create_deployment_checklist("docusaurus")
    print(f"✓ Checklist items: {len(checklist)}")
    for item in checklist[:3]:
        print(f"  {item}")
    print(f"  ... and {len(checklist) - 3} more")
    
    # Example 5: Troubleshooting
    print("\n[Example 5] Troubleshooting Guide")
    guide = skill.troubleshoot_deployment("404_error")
    print(f"✓ Issue: {guide['issue']}")
    print(f"  Causes: {len(guide['causes'])}")
    print(f"  Solutions: {len(guide['solutions'])}")
    
    print("\n" + "="*60)
    print("Skill demonstration complete")
    print("="*60)


if __name__ == "__main__":
    main()
