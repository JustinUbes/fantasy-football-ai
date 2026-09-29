# Repository Agents

This repository uses workspace-local customization agents:

- [Work Item Assistant](agents/work-item-assistant.agent.md)
- [Work Planning Assistant](agents/work-planning-assistant.agent.md)
- [Vulnerability Responder](agents/vulnerability-responder.agent.md)

Repository-wide guidance is also defined in [copilot-instructions.md](copilot-instructions.md).

Use the work item assistant when you want to turn a feature, improvement, bug fix, or task into a well-defined GitHub Issue draft for this project.

The Work Item Assistant is best for:
- GitHub issues for features, bugs, and follow-up work
- acceptance criteria and definition of done
- breaking larger work into smaller actionable items
- scope refinement and implementation sequencing
- MVP planning grounded in the current repo

Use the Work Planning Assistant when you have a larger initiative or idea and want it broken into milestones, phases, and a tractable sequence of GitHub Issues.

The Work Planning Assistant is best for:
- turning broad concepts into phased delivery plans
- breaking a big idea into smaller actionable items for the tracker
- sequencing work by dependencies, risk, and value
- proposing MVP-first planning before implementation begins
- creating a backlog from specs, docs, and repository goals

The Vulnerability Responder agent is best for:
- triaging `pip-audit` findings
- responding to Dependabot or GitHub security alerts
- finding the smallest safe dependency remediation
- validating vulnerability fixes with focused checks