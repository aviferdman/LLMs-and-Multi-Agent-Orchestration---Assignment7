# Visualization Quality Standards

**Document Version**: 1.0  
**Last Updated**: December 2025

---

## Overview

This document defines the visualization quality standards for charts, diagrams, and graphical outputs in the AI Agent League Competition System.

---

## Publication Standards

### Resolution Requirements

| Output Type | Minimum DPI | Recommended DPI |
|-------------|-------------|-----------------|
| Web Display | 72 | 96 |
| Print/PDF | 300 | 300-600 |
| Presentations | 150 | 200 |

### Typography

- **Font Family**: Sans-serif (Arial, Helvetica, or system default)
- **Title Size**: 14-16pt bold
- **Axis Labels**: 10-12pt regular
- **Legend Text**: 9-11pt regular
- **Annotations**: 8-10pt italic

### Color Palette

**Primary Palette** (Colorblind-Friendly):
| Color Name | Hex Code | RGB | Usage |
|------------|----------|-----|-------|
| Blue | #0077BB | (0, 119, 187) | Player 1, Primary data |
| Orange | #EE7733 | (238, 119, 51) | Player 2, Secondary data |
| Green | #009988 | (0, 153, 136) | Player 3, Success states |
| Magenta | #CC3311 | (204, 51, 17) | Player 4, Error states |
| Cyan | #33BBEE | (51, 187, 238) | Highlights |
| Grey | #BBBBBB | (187, 187, 187) | Neutral/background |

**Why Colorblind-Friendly?**
- ~8% of males and ~0.5% of females have color vision deficiency
- Above palette distinguishes well in grayscale
- Passes WCAG 2.1 contrast requirements

---

## Chart-Specific Standards

### Bar Charts (Standings)

- **Bar Width**: Consistent across all bars
- **Spacing**: 50% of bar width between bars
- **Value Labels**: Display on or above bars
- **Axis**: Start Y-axis at 0 to avoid misleading visuals
- **Grid Lines**: Horizontal, light gray, dashed

### Line Charts (Progress)

- **Line Width**: 2-3pt for primary, 1-2pt for secondary
- **Markers**: Use distinct shapes (circle, square, triangle)
- **Legend**: Position outside plot area
- **Grid Lines**: Both horizontal and vertical, light

### Pie Charts (Distribution)

- **Maximum Slices**: 6 (use "Other" for additional)
- **Labels**: Show percentage values
- **Start Angle**: 90° (12 o'clock position)
- **Explode**: Only for emphasis on specific slice

### State Machine Diagrams

- **Node Shape**: Rounded rectangles for states
- **Arrow Style**: Single-headed, medium weight
- **Labels**: On arrows for transitions
- **Colors**: 
  - Initial state: Green border
  - Final state: Double border
  - Error states: Red border

---

## Quality Checklist

### Pre-Publication Review

- [ ] All text is legible at intended display size
- [ ] Colors pass colorblind simulation test
- [ ] Axis labels present and descriptive
- [ ] Title accurately describes content
- [ ] Legend explains all data series
- [ ] Units specified where applicable
- [ ] No truncated text or overlapping elements
- [ ] Consistent style across all figures

### Accessibility Standards

- [ ] Color is not the only means of conveying information
- [ ] Sufficient contrast ratio (≥4.5:1 for text)
- [ ] Alternative text descriptions provided
- [ ] Patterns/shapes supplement color coding
- [ ] Font sizes meet minimum requirements

### Technical Quality

- [ ] Vector format for diagrams (SVG preferred)
- [ ] Raster format for complex visualizations (PNG)
- [ ] Appropriate resolution for output medium
- [ ] File size optimized (<500KB for web)
- [ ] Transparent background where appropriate

---

## Tools and Libraries

### Recommended Tools

| Purpose | Tool | Notes |
|---------|------|-------|
| Charts | Matplotlib, Plotly | Python-based |
| Diagrams | Draw.io, Mermaid | Architecture diagrams |
| Icons | Font Awesome | Consistent iconography |
| Color Check | Coblis | Colorblind simulator |

### Matplotlib Configuration

```python
import matplotlib.pyplot as plt

# Publication-quality settings
plt.rcParams.update({
    'figure.dpi': 300,
    'font.family': 'sans-serif',
    'font.size': 10,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.figsize': (8, 6),
})
```

---

## Diagram Inventory

### Required Diagrams

| Diagram | File | Location | Format |
|---------|------|----------|--------|
| System Architecture | architecture.svg | doc/diagrams/ | SVG |
| Message Flow | messageflow.svg | doc/diagrams/ | SVG |
| State Machine | statemachine.svg | doc/diagrams/ | SVG |

### Status

- [x] architecture.svg - Complete
- [x] messageflow.svg - Complete
- [ ] statemachine.svg - Required (game state machine)

---

**Document Owner**: Assignment 7 Team  
**Status**: ✅ Complete
