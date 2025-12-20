# Next Steps - Action Plan

**Date**: 2025-12-20  
**Purpose**: Prioritized action plan for completing the assignment  
**Current Status**: 75% complete (9/12 phases)

---

## 🎯 Quick Summary

**What's Done** ✅:
- ✅ All core implementation (Phases 1-7)
- ✅ 139/139 tests passing
- ✅ 54% code coverage
- ✅ 100% line count compliance
- ✅ 100% protocol compliance
- ✅ Complete documentation suite (10 guides)

**What's Left** ⚠️:
- ⚠️ Phase 8: End-to-End Testing (manual tournament run)
- ⚠️ Phase 9: Code quality tools (optional linting)
- ⚠️ Phase 10: Research & Analysis (**required for assignment**)
- ⚠️ Phases 11-12: Polish & submission

---

## 🚀 Priority 1: End-to-End Testing (Phase 8)

**Goal**: Verify the complete system works in a real tournament scenario

### 8.1 Manual Testing
**Estimated Time**: 30 minutes

**Steps**:
1. Open 7 terminal windows
2. Start agents in order:
   ```bash
   # Terminal 1: League Manager
   python agents/league_manager/main.py
   
   # Terminal 2-3: Referees
   python agents/launch_referee_01.py
   python agents/launch_referee_02.py
   
   # Terminal 4-7: Players
   python agents/launch_player_01.py
   python agents/launch_player_02.py
   python agents/launch_player_03.py
   python agents/launch_player_04.py
   ```
3. Wait 10 seconds for all agents to register
4. Run tournament launcher:
   ```bash
   python run_league.py
   ```
5. Monitor execution:
   - Watch console output for all agents
   - Verify 3 rounds execute
   - Verify 6 matches complete
   - Verify agents shut down gracefully

**Success Criteria**:
- ✅ All agents start without errors
- ✅ All agents register with League Manager
- ✅ Tournament completes all 3 rounds
- ✅ All 6 matches execute successfully
- ✅ Final standings generated
- ✅ All agents shut down gracefully
- ✅ No timeout errors
- ✅ No protocol errors

**Output Files to Check**:
- `SHARED/data/leagues/league_2025_even_odd_standings.json` - Final standings
- `SHARED/data/matches/*.json` - 6 match result files
- `SHARED/logs/league/*.jsonl` - League manager logs
- `SHARED/logs/agents/*.jsonl` - Agent logs

**Troubleshooting**:
- If agents don't start: Check port conflicts
- If registration fails: Increase wait time in `run_league.py`
- If matches fail: Check referee/player logs
- If shutdown hangs: Kill processes manually (Ctrl+C)

### 8.2 Create Automated Test Script
**Estimated Time**: 1 hour

**Task**: Create `scripts/run_full_tournament.py`

**Features**:
- Start all agents programmatically
- Wait for registration (10 seconds)
- Send START_LEAGUE message
- Monitor tournament progress
- Collect final results
- Generate summary report
- Clean shutdown

**Example Structure**:
```python
#!/usr/bin/env python3
"""Automated tournament runner."""

import asyncio
import subprocess
import time
import json
from pathlib import Path

async def run_tournament():
    """Run a complete tournament automatically."""
    print("🏁 Starting automated tournament...")
    
    # 1. Start all agents
    processes = []
    # ... start league manager, referees, players ...
    
    # 2. Wait for registration
    await asyncio.sleep(10)
    
    # 3. Trigger tournament
    # ... send START_LEAGUE ...
    
    # 4. Monitor progress
    # ... watch for completion ...
    
    # 5. Collect results
    results = load_results()
    
    # 6. Generate report
    print_report(results)
    
    # 7. Cleanup
    for proc in processes:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(run_tournament())
```

**Acceptance Criteria**:
- ✅ Script runs tournament end-to-end
- ✅ No manual intervention needed
- ✅ Results printed to console
- ✅ Exit code 0 on success
- ✅ Exit code 1 on failure

### 8.3 Run Multiple Tournaments
**Estimated Time**: 30 minutes

**Task**: Verify consistency

**Steps**:
1. Run automated script 10 times
2. Verify all complete successfully
3. Check for any errors/warnings
4. Document any issues found

**Expected Results**:
- 10/10 tournaments complete successfully
- Consistent behavior across runs
- No memory leaks
- No resource exhaustion

---

## 🔬 Priority 2: Research & Analysis (Phase 10) - **REQUIRED**

**Goal**: Analyze strategy performance across 100 tournaments

### 10.1 Data Collection
**Estimated Time**: 2-3 hours

**Task**: Run 100 tournaments and collect data

**Script to Create**: `scripts/run_research_tournaments.py`

**Features**:
- Run 100 tournaments automatically
- Randomize strategy assignments for each run
- Collect match results
- Save to `doc/research_data/tournament_{n}.json`
- Track:
  - Win rates per strategy
  - Match outcomes (win/loss/draw)
  - Average points per strategy
  - Head-to-head performance

**Data Structure**:
```json
{
  "tournament_id": 1,
  "players": {
    "P01": {"strategy": "Random", "wins": 2, "losses": 0, "draws": 1},
    "P02": {"strategy": "Frequency", "wins": 1, "losses": 1, "draws": 1},
    "P03": {"strategy": "Pattern", "wins": 1, "losses": 2, "draws": 0},
    "P04": {"strategy": "Random", "wins": 1, "losses": 2, "draws": 0}
  },
  "matches": [...],
  "final_standings": [...]
}
```

### 10.2 Statistical Analysis
**Estimated Time**: 2 hours

**Task**: Analyze collected data

**Script to Create**: `scripts/analyze_results.py`

**Analyses**:
1. **Win Rate by Strategy**
   - Calculate mean win rate for each strategy
   - Calculate standard deviation
   - Calculate 95% confidence intervals

2. **Statistical Significance**
   - Use t-tests to compare strategies
   - Calculate p-values
   - Determine if differences are significant (p < 0.05)

3. **Effect Sizes**
   - Calculate Cohen's d for pairwise comparisons
   - Interpret effect sizes (small/medium/large)

4. **Match Outcome Distribution**
   - Count wins/losses/draws per strategy
   - Create frequency tables
   - Chi-square test for independence

**Python Libraries**:
```python
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
```

**Example Analysis**:
```python
def analyze_strategy_performance(data):
    """Analyze strategy performance from 100 tournaments."""
    df = pd.DataFrame(data)
    
    # Calculate win rates
    win_rates = df.groupby('strategy')['wins'].mean()
    
    # Statistical tests
    strategies = df['strategy'].unique()
    for s1, s2 in combinations(strategies, 2):
        wins_s1 = df[df['strategy'] == s1]['wins']
        wins_s2 = df[df['strategy'] == s2]['wins']
        t_stat, p_value = stats.ttest_ind(wins_s1, wins_s2)
        cohen_d = calculate_cohens_d(wins_s1, wins_s2)
        
    return results
```

### 10.3 Visualizations
**Estimated Time**: 1 hour

**Task**: Create publication-quality plots (300 DPI)

**Visualizations to Create**:

1. **Strategy Win Rate Bar Chart**
   - X-axis: Strategies (Random, Frequency, Pattern)
   - Y-axis: Average Win Rate (%)
   - Error bars: 95% confidence intervals
   - Save as: `doc/results/win_rates.png`

2. **Match Outcome Distribution**
   - Stacked bar chart or grouped bar chart
   - X-axis: Strategies
   - Y-axis: Count
   - Categories: Wins (green), Losses (red), Draws (yellow)
   - Save as: `doc/results/outcomes.png`

3. **Performance Heatmap**
   - Head-to-head win rates between strategies
   - Color: Win rate (0-100%)
   - Annotations: Exact percentages
   - Save as: `doc/results/heatmap.png`

**Example Code**:
```python
import matplotlib.pyplot as plt
import seaborn as sns

def create_win_rate_plot(data):
    """Create bar chart of win rates with error bars."""
    plt.figure(figsize=(10, 6), dpi=300)
    
    strategies = ['Random', 'Frequency', 'Pattern']
    win_rates = [data['Random']['mean'], ...]
    errors = [data['Random']['ci'], ...]
    
    plt.bar(strategies, win_rates, yerr=errors, capsize=10)
    plt.xlabel('Strategy', fontsize=14)
    plt.ylabel('Win Rate (%)', fontsize=14)
    plt.title('Strategy Performance (100 Tournaments)', fontsize=16)
    plt.ylim(0, 100)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('doc/results/win_rates.png', dpi=300, bbox_inches='tight')
    plt.close()
```

### 10.4 Research Report
**Estimated Time**: 2 hours

**Task**: Write `doc/RESULTS.md`

**Sections**:

1. **Abstract** (200 words)
   - Brief summary of research question, methods, and findings

2. **Introduction**
   - Research question: "Which strategy performs best in Even-Odd game?"
   - Hypotheses:
     - H1: Adaptive strategies outperform random
     - H2: Pattern-based performs best
     - H0: No significant difference

3. **Methodology**
   - Tournament setup (4 players, 3 rounds, 6 matches)
   - Strategy descriptions (Random, Frequency, Pattern)
   - Data collection (100 tournaments, randomized assignments)
   - Statistical methods (t-tests, effect sizes, CI)

4. **Results**
   - Overall win rates table
   - Statistical significance table (p-values)
   - Effect sizes table (Cohen's d)
   - Visualizations (3 plots)

5. **Discussion**
   - Interpretation of findings
   - Comparison to hypotheses
   - Limitations of study
   - Potential biases

6. **Conclusions**
   - Summary of key findings
   - Practical implications
   - Future research directions

**Example Structure**:
```markdown
# Research Results: Strategy Performance in Even-Odd Game

## Abstract
This study analyzed the performance of three strategies...
[200 words]

## 1. Introduction

### 1.1 Research Question
Which strategy performs best in the Even-Odd number guessing game?

### 1.2 Hypotheses
- H1: Adaptive strategies (Frequency, Pattern) outperform Random
- H2: Pattern-based strategy performs best
- H0: No significant difference between strategies

## 2. Methodology

### 2.1 Tournament Setup
- 4 players per tournament
- 3 rounds (6 matches total)
- Round-robin format
- Scoring: Win=3, Draw=1, Loss=0

### 2.2 Strategies Tested
1. **Random**: Chooses "even" or "odd" randomly (50/50)
2. **Frequency**: Tracks opponent's history, picks most likely
3. **Pattern**: Detects patterns in opponent's choices

### 2.3 Data Collection
- 100 tournaments executed
- Strategy assignments randomized
- Total: 600 matches analyzed

### 2.4 Statistical Methods
- Independent samples t-tests
- Cohen's d effect sizes
- 95% confidence intervals
- Alpha level: 0.05

## 3. Results

### 3.1 Overall Performance
| Strategy | Win Rate | Std Dev | 95% CI |
|----------|----------|---------|--------|
| Random   | 33.2%    | 12.5%   | [30.7, 35.7] |
| Frequency| 38.7%    | 11.8%   | [36.4, 41.0] |
| Pattern  | 41.1%    | 13.2%   | [38.5, 43.7] |

### 3.2 Statistical Significance
| Comparison | t-statistic | p-value | Cohen's d | Significant? |
|------------|-------------|---------|-----------|--------------|
| Freq vs Random | 2.34 | 0.021 | 0.47 | ✅ Yes (p<0.05) |
| Pattern vs Random | 3.12 | 0.002 | 0.61 | ✅ Yes (p<0.05) |
| Pattern vs Freq | 1.21 | 0.229 | 0.19 | ❌ No |

### 3.3 Visualizations
[Include 3 plots here]

## 4. Discussion

### 4.1 Key Findings
Pattern-based strategy showed the highest win rate...

### 4.2 Hypothesis Testing
- H1: SUPPORTED - Both adaptive strategies outperformed Random
- H2: PARTIALLY SUPPORTED - Pattern showed highest rate but not significantly different from Frequency
- H0: REJECTED - Significant differences found

### 4.3 Limitations
- Small sample (100 tournaments)
- Only 3 strategies tested
- Simple game dynamics

## 5. Conclusions
Adaptive strategies demonstrate clear advantage...

## References
[Statistical methods, game theory papers, etc.]
```

---

## 🛠️ Priority 3: Code Quality Tools (Phase 9.1) - **OPTIONAL**

**Goal**: Run linting and formatting tools

**Estimated Time**: 1-2 hours

### Tasks:
1. **Install tools**:
   ```bash
   pip install pylint black isort
   ```

2. **Run black formatter**:
   ```bash
   black SHARED/ agents/ tests/
   ```

3. **Run isort**:
   ```bash
   isort SHARED/ agents/ tests/
   ```

4. **Run pylint**:
   ```bash
   pylint SHARED/ agents/ --rcfile=.pylintrc
   ```
   - Target: ≥8.5/10 score
   - Fix issues as needed

**Note**: This is optional. System already works correctly and has comprehensive tests.

---

## ✨ Priority 4: Final Polish (Phases 11-12)

**Goal**: Prepare for submission

**Estimated Time**: 2-3 hours

### 11.1 Documentation Review
- [ ] Proofread all documents
- [ ] Fix typos and formatting
- [ ] Verify all links work
- [ ] Update README.md with latest info

### 11.2 Final Testing
- [ ] Run full test suite one last time
- [ ] Run full tournament one last time
- [ ] Verify all outputs correct

### 11.3 Submission Package
- [ ] Create zip archive
- [ ] Test on clean machine (if possible)
- [ ] Verify README instructions
- [ ] Double-check requirements

---

## 📊 Time Estimates

| Phase | Task | Time | Priority |
|-------|------|------|----------|
| 8.1 | Manual E2E test | 30 min | 🔴 High |
| 8.2 | Automated test script | 1 hour | 🟡 Medium |
| 8.3 | Multiple test runs | 30 min | 🟡 Medium |
| 10.1 | Data collection | 2-3 hours | 🔴 High |
| 10.2 | Statistical analysis | 2 hours | 🔴 High |
| 10.3 | Visualizations | 1 hour | 🔴 High |
| 10.4 | Research report | 2 hours | 🔴 High |
| 9.1 | Code quality tools | 1-2 hours | 🟢 Low |
| 11-12 | Final polish | 2-3 hours | 🟡 Medium |

**Total Estimated Time**: 12-16 hours

---

## 🎯 Recommended Work Order

### Session 1 (2-3 hours): **Phase 8 - Verification**
1. Manual E2E test (30 min)
2. Fix any issues found (30 min)
3. Create automated test script (1 hour)
4. Run multiple tests (30 min)

**Deliverable**: Verified working system

### Session 2 (3-4 hours): **Phase 10 Part 1 - Data Collection**
1. Create tournament runner script (1 hour)
2. Run 100 tournaments (2 hours)
3. Verify data collected correctly (30 min)

**Deliverable**: Complete dataset (100 tournaments)

### Session 3 (3-4 hours): **Phase 10 Part 2 - Analysis**
1. Create analysis script (1 hour)
2. Run statistical analyses (1 hour)
3. Create visualizations (1 hour)
4. Write research report (2 hours)

**Deliverable**: Complete research analysis

### Session 4 (2-3 hours): **Final Polish**
1. Run code quality tools (optional)
2. Review all documentation
3. Final testing
4. Create submission package

**Deliverable**: Ready for submission

---

## 📋 Success Criteria

Before submission, verify:

- ✅ All 139 tests passing
- ✅ E2E tournament runs successfully
- ✅ 100 tournaments completed
- ✅ Statistical analysis complete
- ✅ 3 visualizations created (300 DPI)
- ✅ Research report written
- ✅ All documentation updated
- ✅ README has clear instructions
- ✅ Submission package created

---

## 🚨 Potential Blockers

1. **E2E Test Fails**
   - Solution: Check logs, fix bugs, re-test
   - Fallback: Document issues, continue with research

2. **Tournament Runner Hangs**
   - Solution: Add timeouts, improve error handling
   - Fallback: Run tournaments manually (slower but works)

3. **Statistical Analysis Issues**
   - Solution: Consult statistics documentation
   - Fallback: Use simpler analyses (mean/median comparison)

4. **Visualization Problems**
   - Solution: Use matplotlib examples
   - Fallback: Use simpler chart types

---

## 📞 Need Help?

- **Technical Issues**: Review logs in `SHARED/logs/`
- **Documentation**: Refer to existing guides in `doc/`
- **Testing**: Check test examples in `tests/`
- **Research**: Consult statistics textbooks/online resources

---

**Document Created**: 2025-12-20  
**Last Updated**: 2025-12-20  
**Status**: Ready to proceed with Phase 8

---

## Quick Start - Next Action

**To continue right now**:

```bash
# 1. Open 7 terminals
# 2. Start agents (see Phase 8.1 above)
# 3. Run tournament
python run_league.py
# 4. Check results
cat SHARED/data/leagues/league_2025_even_odd_standings.json
```

**Expected Duration**: 30 minutes  
**Success**: Tournament completes, standings generated  
**Next**: Create automated script for Phase 10
