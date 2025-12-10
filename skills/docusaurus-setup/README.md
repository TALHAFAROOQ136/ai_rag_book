# Docusaurus Setup Skill

**Version**: 1.0.0  
**Category**: Frontend / Documentation  
**Reusability**: High (works with any documentation project)

## Purpose

Initialize and configure a Docusaurus project with TypeScript, search, dark mode, and optimal settings for technical documentation.

## Inputs

- `project_name`: Name of the project (kebab-case)
- `typescript`: Use TypeScript (default: true)
- `search`: Search type (local/algolia/none, default: local)
- `theme`: Docusaurus theme (default: classic)
- `plugins`: Additional plugins to install

## Outputs

- Complete Docusaurus project directory
- `docusaurus.config.ts` with optimized settings
- Initial content structure (docs/)
- Package.json with scripts
- README.md with setup instructions

## Usage

See [skills.spec.md](../../skills.spec.md#skill-1-docusaurus-setup) for complete implementation guide.

## Status

**Phase 0**: ✅ Skill defined and documented  
**Phase 1**: ⏳ Ready for use by FrontendDev subagent
