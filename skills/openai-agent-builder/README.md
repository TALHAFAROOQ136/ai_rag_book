# OpenAI Agent Builder Skill

**Version**: 1.0.0  
**Category**: AI / Backend  
**Reusability**: High (works with any conversational AI project)

## Purpose

Create and configure OpenAI Agents using the Swarm framework for conversational AI applications, including RAG-optimized agents.

## Inputs

- `agent_name`: Name of the agent
- `system_prompt`: Agent's system instructions
- `model`: OpenAI model (default: gpt-4o-mini)
- `temperature`: Creativity level (0.0-2.0, default: 0.7)
- `streaming`: Enable response streaming (default: true)

## Outputs

- Configured OpenAI Agent instance
- Wrapper functions for chat and streaming
- Context management utilities
- Token counting and cost estimation
- RAGAgent class (specialized for Q&A)

## Usage

See [skills.spec.md](../../skills.spec.md#skill-3-openai-agent-builder) for complete implementation with code examples.

## Status

**Phase 0**: ✅ Skill defined and documented  
**Phase 2**: ⏳ Ready for use by APIBuilder subagent
