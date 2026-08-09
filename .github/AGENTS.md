# Repository Agents

This repository uses workspace-local customization agents:

- [Work Item Assistant](agents/work-item-assistant.agent.md)
- [Vulnerability Responder](agents/vulnerability-responder.agent.md)

Repository-wide guidance is also defined in [copilot-instructions.md](copilot-instructions.md).

Use the work item assistant when you want to turn a feature, improvement, bug fix, or task into a well-defined GitHub Issue draft for this project.

The Work Item Assistant is best for:
- GitHub issues for features, bugs, and follow-up work
- acceptance criteria and definition of done
- breaking larger work into smaller actionable items
- scope refinement and implementation sequencing
- MVP planning grounded in the current repo

The Vulnerability Responder agent is best for:
- triaging `pip-audit` findings
- responding to Dependabot or GitHub security alerts
- finding the smallest safe dependency remediation
- validating vulnerability fixes with focused checks