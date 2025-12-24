# 🚀 START HERE - Project Guide

**Status**: Production Ready ✅  
**Last Updated**: December 24, 2025  
**Total Cost**: $0.00 (No external APIs required)

---

## Quick Navigation

### 📖 For Overview & Context
Start here if you want to understand what was built:
1. **[README.md](README.md)** - Project overview and key features (10 min)
2. **[doc/PROJECT_REPORT.md](doc/PROJECT_REPORT.md)** - Consolidated project report (15 min)
3. **[doc/RESULTS.md](doc/RESULTS.md)** - Experimental results and findings (10 min)

### 🔬 For Understanding the Architecture
If you want to understand the system design:
1. **[doc/ARCHITECTURE.md](doc/ARCHITECTURE.md)** - Three-layer architecture (15 min)
2. **[doc/DESIGN_DOCUMENT.md](doc/DESIGN_DOCUMENT.md)** - Design decisions (20 min)
3. **[doc/ADRs/](doc/ADRs/)** - Architectural Decision Records (30 min)

### 🎮 For Running the System
If you want to run the league:
1. **[doc/INSTALLATION.md](doc/INSTALLATION.md)** - Setup instructions (5 min)
2. **[doc/RUNNING.md](doc/RUNNING.md)** - Running the system (10 min)
3. **[doc/GUI_QUICK_START.md](doc/GUI_QUICK_START.md)** - Using the GUI (5 min)

### 📊 For Seeing Results
If you want to see what was accomplished:
1. **[doc/RESULTS.md](doc/RESULTS.md)** - Tournament results (10 min)
2. **[doc/STATISTICAL_ANALYSIS.md](doc/STATISTICAL_ANALYSIS.md)** - Statistical analysis (15 min)
3. **[doc/results/](doc/results/)** - Raw result files

### 🧪 For Testing & Quality
If you want to verify quality:
1. **[doc/TESTING.md](doc/TESTING.md)** - Test strategy (10 min)
2. **[doc/TEST_COVERAGE_REPORT.md](doc/TEST_COVERAGE_REPORT.md)** - Coverage report (5 min)
3. **[doc/ISO_25010_COMPLIANCE.md](doc/ISO_25010_COMPLIANCE.md)** - Quality compliance (15 min)

---

## 🎯 System at a Glance

### What Is This?
A **Multi-Agent Even-Odd Game Competition System** where autonomous AI agents compete in tournaments.

**Every agent is an MCP (Model Context Protocol) server** - including the League Manager, Referees, and Players. All inter-agent communication happens via HTTP POST requests to `/mcp` endpoints using the `league.v2` protocol.

### Key Components

| Component | Description | Port |
|-----------|-------------|------|
| **League Manager** | Tournament orchestration | 8000 |
| **Referee 01** | Match execution | 8001 |
| **Referee 02** | Match execution | 8002 |
| **Player 01-04** | Game participants | 8101-8104 |
| **API Server** | REST API & WebSocket | 8080 |
| **GUI Dashboard** | Streamlit interface | 8501 |

### Three-Layer Architecture

```
┌─────────────────────────────────────┐
│   ORCHESTRATION (League Manager)    │
│   - Tournament management           │
│   - Standings calculation           │
└─────────────────┬───────────────────┘
                  │
┌─────────────────┴───────────────────┐
│   EXECUTION (Referees)              │
│   - Match execution                 │
│   - Rule enforcement                │
└─────────────────┬───────────────────┘
                  │
┌─────────────────┴───────────────────┐
│   PARTICIPATION (Players)           │
│   - Strategy execution              │
│   - Game participation              │
└─────────────────────────────────────┘
```

---

## 🚀 30-Second Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt && pip install -e .

# 2. Start API server (Terminal 1)
python run_api.py

# 3. Start GUI (Terminal 2)
python run_gui.py

# 4. Open browser to http://localhost:8501
```

---

## 📂 Key Documents

| Document | Purpose | Audience | Time |
|----------|---------|----------|------|
| **[README.md](README.md)** | Project overview | Everyone | 10 min |
| **[doc/ARCHITECTURE.md](doc/ARCHITECTURE.md)** | System design | Developers | 15 min |
| **[doc/PRD.md](doc/PRD.md)** | Requirements | Stakeholders | 20 min |
| **[doc/AGENT_STRATEGY.md](doc/AGENT_STRATEGY.md)** | Player strategies | Researchers | 15 min |
| **[doc/protocol_spec.md](doc/protocol_spec.md)** | Protocol details | Developers | 20 min |
| **[doc/TESTING.md](doc/TESTING.md)** | Test strategy | QA | 10 min |
| **[doc/EDGE_CASES.md](doc/EDGE_CASES.md)** | Edge case handling | Developers | 15 min |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Contribution guide | Contributors | 10 min |

---

## 📊 Key Metrics

| Metric | Value |
|--------|-------|
| **Test Count** | 228 tests |
| **Test Pass Rate** | 100% |
| **Code Coverage** | 70%+ |
| **Documentation Files** | 30+ |
| **ADRs** | 10+ |
| **Protocol Version** | league.v2 |
| **Player Strategies** | 3 (Random, Frequency, Pattern) |
| **Total Lines of Code** | ~8,000 |
| **File Size Compliance** | 100% (<150 lines) |

---

## 🎮 Player Strategies Explained

| Strategy | Description | Win Rate |
|----------|-------------|----------|
| **Random** | Pure random selection | ~50% |
| **Frequency** | Tracks opponent patterns | ~55-60% |
| **Pattern** | Detects sequential patterns | ~55-60% |

---

## ✅ Project Completion Status

### Core Features (100% Complete)
- [x] Three-layer agent architecture
- [x] Protocol-driven communication (league.v2)
- [x] Round-robin tournament scheduling
- [x] Real-time GUI dashboard
- [x] REST API with WebSocket support
- [x] JSONL logging system
- [x] Statistical analysis

### Quality Assurance (100% Complete)
- [x] 228 automated tests
- [x] CI/CD pipeline (GitHub Actions)
- [x] Type hints throughout
- [x] Comprehensive documentation
- [x] ISO 25010 compliance audit

### Documentation (100% Complete)
- [x] Architecture documentation
- [x] API documentation
- [x] Protocol specification
- [x] Installation guide
- [x] User guide (GUI)
- [x] Testing documentation
- [x] ADRs (10+ decisions)

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Import Errors
```bash
# Reinstall in development mode
pip install -e .
```

### Tests Failing
```bash
# Run tests with verbose output
pytest tests/ -v --tb=short
```

---

## 📞 Quick Reference

### Essential Commands

```bash
# Run full test suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=SHARED --cov=agents --cov=api

# Start API server
python run_api.py

# Start GUI
python run_gui.py

# Run tournament (CLI)
python run_league.py
```

### Key Files

| File | Purpose |
|------|---------|
| `run_api.py` | Start REST API server |
| `run_gui.py` | Start Streamlit GUI |
| `run_league.py` | Run CLI tournament |
| `agents/generic_player.py` | Player agent code |
| `agents/generic_referee.py` | Referee agent code |
| `SHARED/contracts/` | Protocol contracts |
| `SHARED/league_sdk/` | Shared utilities |

---

## 🚀 Next Steps

1. **Start Here**: Run the GUI demo with `python run_gui.py`
2. **Explore**: Check the dashboard at http://localhost:8501
3. **Dive Deep**: Read [ARCHITECTURE.md](doc/ARCHITECTURE.md)
4. **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

<div align="center">

**Production Ready ✅ | 228 Tests Passing ✅ | 70%+ Coverage ✅**

**Built with 💙 for Multi-Agent Orchestration**

</div>
