# Claude Ecosystem Configuration

## Navigation Guide for Agents, Skills, and Commands

This directory contains the configuration for the Claude ecosystem that streamlines the AI Agent League Competition project development.

---

## 📋 Quick Navigation

### 🤖 Agents (`.claude/agents/`)

Specialized AI agents that handle different aspects of the project:

| Agent | Purpose | Key Outputs |
|-------|---------|------------|
| [@code-reviewer](agents/code-reviewer.md) | Code review and quality assurance | Review feedback, suggestions |
| [@fullstack-developer](agents/fullstack-developer.md) | Full-stack development | Features, bug fixes |
| [@qa-expert](agents/qa-expert.md) | Testing and quality assurance | Test cases, coverage reports |
| [@ui-designer](agents/ui-designer.md) | UI/UX design | GUI components, layouts |
| [@protocol-architect](agents/protocol-architect.md) | Protocol design | Message schemas, contracts |
| [@agent-developer](agents/agent-developer.md) | Agent implementation | Player/Referee agents |

### 🔧 Skills (`.claude/skills/`)

Reusable capabilities available throughout the project:

| Skill | Purpose | Use Cases |
|-------|---------|-----------|
| [protocol_validation](skills/protocol_validation.md) | Validate message schemas | Check league.v2 compliance |
| [test_generation](skills/test_generation.md) | Generate test cases | Unit tests, edge cases |
| [metrics_calculation](skills/metrics_calculation.md) | Calculate statistics | Win rates, performance |
| [agent_communication](skills/agent_communication.md) | Inter-agent messaging | HTTP, JSON handling |
| [logging_analysis](skills/logging_analysis.md) | Analyze JSONL logs | Debug, audit trail |

### ⚡ Commands (`.claude/commands/`)

Quick-access shortcuts for common tasks:

| Command | Purpose | Example |
|---------|---------|---------|
| [/run-tests](commands/run_tests.md) | Execute test suite | `/run-tests` |
| [/validate-protocol](commands/validate_protocol.md) | Validate message | `/validate-protocol message.json` |
| [/check-coverage](commands/check_coverage.md) | Check test coverage | `/check-coverage` |
| [/start-league](commands/start_league.md) | Start tournament | `/start-league` |
| [/analyze-logs](commands/analyze_logs.md) | Analyze log files | `/analyze-logs LM01` |

---

## 🚀 Typical Workflows

### Development Workflow

```
@fullstack-developer implements feature
├── Creates agent code
├── Adds protocol contracts
└── Updates documentation

@qa-expert tests implementation
├── Generates test cases
├── Runs test suite
└── Checks coverage

@code-reviewer reviews changes
├── Reviews code quality
├── Checks style compliance
└── Suggests improvements
```

### Protocol Development Workflow

```
@protocol-architect designs messages
├── Defines message schema
├── Creates contract file
└── Documents in protocol_spec.md

/validate-protocol checks compliance
├── Validates JSON structure
├── Checks required fields
└── Verifies protocol version
```

### Testing Workflow

```
/run-tests executes suite
├── Unit tests
├── Integration tests
└── Edge case tests

/check-coverage reports metrics
├── Line coverage
├── Branch coverage
└── Missing coverage
```

---

## 📖 Reference Guide

### Using Agents

Agents are referenced with the `@` symbol:

```
@code-reviewer: Please review the new player strategy
@fullstack-developer: Implement timeout handling
@qa-expert: Generate edge case tests for referee
@protocol-architect: Design MATCH_TIMEOUT message
```

### Using Skills

Skills are automatically available throughout the project:

```
Use protocol_validation to check message compliance
Use test_generation for creating test cases
Use metrics_calculation for win rate analysis
Use agent_communication for HTTP client patterns
Use logging_analysis to debug issues
```

### Using Commands

Commands provide quick access to common tasks:

```
/run-tests [pattern]
/validate-protocol [file]
/check-coverage [module]
/start-league [config]
/analyze-logs [agent-id]
```

---

## 🎯 Success Checklist

### Setup Phase
- [x] .claude/ directory created
- [x] 6 agent files created
- [x] 5 skill files created
- [x] 5 command files created
- [x] INDEX.md (this file) created

### Project Phases
- [x] Can reference agents with @agent-name syntax
- [x] Can invoke commands with /command-name syntax
- [x] All agents have clear responsibilities
- [x] All skills have documented use cases
- [x] All commands have working implementations

---

## 📚 Documentation Structure

```
.claude/
├── INDEX.md                      # This file - navigation guide
├── settings.local.json           # Local settings
├── agents/
│   ├── code-reviewer.md          # Code review expert
│   ├── fullstack-developer.md    # Full-stack developer
│   ├── qa-expert.md              # QA and testing expert
│   ├── ui-designer.md            # UI/UX designer
│   ├── protocol-architect.md     # Protocol design expert
│   └── agent-developer.md        # Agent implementation expert
├── skills/
│   ├── protocol_validation.md    # Message validation
│   ├── test_generation.md        # Test case creation
│   ├── metrics_calculation.md    # Statistics
│   ├── agent_communication.md    # HTTP/JSON handling
│   └── logging_analysis.md       # Log analysis
└── commands/
    ├── run_tests.md              # Test execution
    ├── validate_protocol.md      # Protocol validation
    ├── check_coverage.md         # Coverage reporting
    ├── start_league.md           # Tournament start
    └── analyze_logs.md           # Log analysis
```

---

## 🔄 Integration with Main Documentation

This ecosystem integrates with the main project documentation:

- **PRD.md**: Define what to build (requirements, features)
- **ARCHITECTURE.md**: Define how to build (design, patterns)
- **README.md**: Define how to use (setup, running)
- **.claude/**: Define who helps (agents, skills, commands)

---

## ✨ Key Features

- **Specialized Agents**: Each agent has a specific role and expertise
- **Reusable Skills**: Skills are available across all agents
- **Quick Commands**: Common tasks have shortcuts
- **Clear Responsibilities**: Each agent documents what it handles
- **Workflow Examples**: Typical workflows shown for each phase
- **Integrated Design**: Ecosystem references throughout docs

---

## 🎓 Learning Path

1. **Start here**: Read this INDEX.md
2. **Understand agents**: Review all agent files
3. **Understand skills**: Review all skill files
4. **Understand commands**: Review all command files
5. **Review workflows**: Check example workflows above
6. **Get started**: Use agents and commands in development

---

## 📞 Next Steps

### Use the Ecosystem

```bash
# Throughout the project:
@qa-expert generates test cases
/run-tests executes suite
@code-reviewer reviews changes
/check-coverage reports metrics
@protocol-architect designs messages
```

---

**Status**: Ready for use  
**Last Updated**: December 24, 2025
