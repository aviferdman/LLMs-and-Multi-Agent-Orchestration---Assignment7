# Mathematical Foundations

**Document Version**: 1.0  
**Last Updated**: December 2025

---

## Overview

This document presents the mathematical foundations underlying the Even-Odd game competition system, including probability calculations, ranking algorithms, and statistical analysis methods.

---

## 1. Even-Odd Game Theory

### Basic Probability

The Even-Odd game has the following characteristics:
- Random number drawn: $n \in \{1, 2, 3, 4, 5, 6, 7, 8, 9, 10\}$
- Even numbers: $\{2, 4, 6, 8, 10\}$ → 5 outcomes
- Odd numbers: $\{1, 3, 5, 7, 9\}$ → 5 outcomes

$$P(\text{even}) = P(\text{odd}) = \frac{5}{10} = 0.5$$

### Win Probability

For a player choosing parity $c \in \{\text{even}, \text{odd}\}$:

$$P(\text{win} | c) = P(\text{drawn parity} = c) = 0.5$$

Against an opponent choosing uniformly at random:

$$P(\text{win against random}) = P(\text{correct guess}) = 0.5$$

---

## 2. Strategy Analysis

### Random Strategy

Expected win rate over $n$ matches:

$$E[\text{wins}] = 0.5n$$

Variance:
$$\text{Var}(\text{wins}) = np(1-p) = 0.25n$$

Standard deviation:
$$\sigma = 0.5\sqrt{n}$$

### Frequency Strategy

If opponent chooses "even" with probability $p$:
- Frequency strategy detects $p > 0.5$ or $p < 0.5$
- Counters with opposite choice

Expected win rate against biased opponent:
$$E[\text{win rate}] = \max(p, 1-p)$$

### Pattern Strategy

For pattern length $k=3$ with history length $h$:
- Possible patterns: $2^k = 8$
- Pattern matches expected: $\frac{h-k}{2^k}$

If pattern $\pi$ predicts next choice with accuracy $a > 0.5$:
$$E[\text{win rate}] = a$$

---

## 3. Ranking Calculations

### Points System

| Outcome | Points Awarded |
|---------|----------------|
| Win | 2 |
| Draw | 1 |
| Loss | 0 |

Total points for player $i$ after $n$ matches:
$$P_i = 2W_i + D_i$$

where $W_i$ = wins, $D_i$ = draws.

### Win Rate

$$\text{Win Rate}_i = \frac{W_i}{n_i}$$

where $n_i$ = total matches played.

### Ranking Algorithm

Players ranked by:
1. **Primary**: Total points (descending)
2. **Secondary**: Win count (descending)
3. **Tertiary**: Head-to-head record

---

## 4. Round-Robin Schedule

### Number of Matches

For $n$ players in a round-robin tournament:

$$\text{Total Matches} = \binom{n}{2} = \frac{n(n-1)}{2}$$

For $n=4$ players:
$$\text{Total Matches} = \frac{4 \times 3}{2} = 6$$

### Number of Rounds

Each player faces every other player once:
$$\text{Rounds} = n - 1 = 3$$

Matches per round:
$$\text{Matches per Round} = \frac{n}{2} = 2$$

---

## 5. Statistical Analysis

### Confidence Intervals

For win rate $\hat{p}$ over $n$ matches, 95% confidence interval:

$$\hat{p} \pm 1.96\sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$$

### Effect Size (Cohen's d)

For comparing two strategies:

$$d = \frac{\bar{x}_1 - \bar{x}_2}{s_{\text{pooled}}}$$

where:
$$s_{\text{pooled}} = \sqrt{\frac{(n_1-1)s_1^2 + (n_2-1)s_2^2}{n_1+n_2-2}}$$

Interpretation:
| |d| | Effect Size |
|-----|-------------|
| < 0.2 | Small |
| 0.2 - 0.8 | Medium |
| > 0.8 | Large |

### Chi-Square Test for Strategy Differences

$$\chi^2 = \sum_i \frac{(O_i - E_i)^2}{E_i}$$

where $O_i$ = observed wins, $E_i$ = expected wins under null hypothesis.

---

## 6. Expected Tournament Outcomes

### Random vs Random

Both players choose uniformly: $P(\text{any outcome}) = 0.5$

Expected standings after complete tournament are uniformly distributed.

### Adaptive vs Random

Adaptive strategies (Frequency, Pattern) converge to baseline performance against truly random opponents.

### Adaptive vs Biased

If opponent has exploitable bias, adaptive strategy expected win rate:
$$E[\text{win rate}] > 0.5$$

---

## 7. Timeout Probability

Let $T$ be the timeout threshold (30 seconds) and response time $X$ be normally distributed:

$$X \sim N(\mu, \sigma^2)$$

Timeout probability:
$$P(\text{timeout}) = P(X > T) = 1 - \Phi\left(\frac{T-\mu}{\sigma}\right)$$

For reliable agents with $\mu = 1s$, $\sigma = 0.5s$:
$$P(\text{timeout}) \approx 0$$

---

**Document Owner**: Assignment 7 Team  
**Status**: ✅ Complete
