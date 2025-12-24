# ADR-006: Statistical Methods for Tournament Analysis

## Status
Accepted

## Date
2025-01-15

## Context

The AI Agent League Competition System generates tournament results that need to be analyzed to:
1. Compare player strategy effectiveness
2. Identify statistically significant differences
3. Provide confidence intervals for win rates
4. Generate publication-quality statistical reports

We need to decide on the statistical methods and tools to use for this analysis.

## Decision

We will use the following statistical methodology:

### 1. Descriptive Statistics
- Mean, median, standard deviation for win rates
- Frequency distributions for match outcomes
- Summary tables with sample sizes

### 2. Inferential Statistics

#### Win Rate Comparisons
- **Two-sample t-tests** for pairwise comparisons
- **ANOVA** for overall significance across multiple strategies
- **Bonferroni correction** for multiple comparisons

#### Effect Size Measures
- **Cohen's d** for standardized effect sizes
  - Small: d = 0.2
  - Medium: d = 0.5
  - Large: d = 0.8

#### Confidence Intervals
- **95% confidence intervals** for all estimates
- Bootstrap methods for non-normal distributions

### 3. Tools and Libraries
- **Python scipy.stats** for statistical tests
- **statsmodels** for advanced analysis
- **pandas** for data manipulation
- **matplotlib/seaborn** for visualization

### 4. Significance Markers
```
*   p < 0.05
**  p < 0.01
*** p < 0.001
```

### 5. Results Format

| Comparison | Mean Diff | 95% CI | t-stat | p-value | Cohen's d | Sig |
|------------|-----------|--------|--------|---------|-----------|-----|
| A vs B     | +X.X%     | [L, H] | X.XX   | 0.XXX   | X.XX      | **  |

## Alternatives Considered

### Alternative 1: Non-parametric Tests Only
- **Pros**: No normality assumptions
- **Cons**: Less statistical power, harder to interpret
- **Rejected**: Our sample sizes are large enough for t-tests

### Alternative 2: Bayesian Analysis
- **Pros**: More interpretable probability statements
- **Cons**: More complex, requires prior specification
- **Rejected**: Added complexity not needed for this use case

### Alternative 3: Machine Learning Classification
- **Pros**: Could find non-linear patterns
- **Cons**: Overkill for simple comparisons, black box
- **Rejected**: Traditional statistics sufficient

### Alternative 4: Simple Win/Loss Counts
- **Pros**: Easy to understand
- **Cons**: No uncertainty quantification
- **Rejected**: Need statistical rigor

## Consequences

### Positive
- Rigorous statistical analysis with p-values and effect sizes
- Reproducible results with standard methods
- Publication-quality output
- Clear interpretation guidelines
- Multiple comparison correction prevents false positives

### Negative
- Requires statistical expertise to implement correctly
- Additional dependencies (scipy, statsmodels)
- Analysis may be slower than simple counting
- Need sufficient sample sizes for valid tests

### Risks
- Risk of p-hacking if running many tests
- Mitigation: Pre-register analysis plan, use correction methods

## Implementation Notes

### Sample Size Requirements
- Minimum 30 matches per strategy for t-tests
- Power analysis: 80% power to detect medium effects

### Assumptions to Check
1. Independence of matches
2. Approximate normality (or use large sample approximations)
3. Homogeneity of variance (for pooled t-tests)

### Code Example

```python
from scipy import stats
import numpy as np

def compare_strategies(wins_a, total_a, wins_b, total_b):
    """Compare two strategy win rates."""
    rate_a = wins_a / total_a
    rate_b = wins_b / total_b
    
    # Two-proportion z-test
    pooled = (wins_a + wins_b) / (total_a + total_b)
    se = np.sqrt(pooled * (1 - pooled) * (1/total_a + 1/total_b))
    z = (rate_a - rate_b) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    
    # Effect size (Cohen's h for proportions)
    h = 2 * (np.arcsin(np.sqrt(rate_a)) - np.arcsin(np.sqrt(rate_b)))
    
    return {
        'rate_diff': rate_a - rate_b,
        'z_stat': z,
        'p_value': p_value,
        'effect_size': h
    }
```

## References

1. Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences.
2. Bonferroni, C. E. (1936). Teoria statistica delle classi e calcolo delle probabilità.
3. Student (1908). The probable error of a mean. Biometrika.
4. Fisher, R. A. (1925). Statistical Methods for Research Workers.

## Related Decisions

- ADR-001: Three-Layer Architecture
- ADR-004: File-Based Persistence (affects data format)

---

*Decision made by: Development Team*
*Reviewed by: Course Instructor*
