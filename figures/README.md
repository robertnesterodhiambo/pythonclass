# Thermal Cycling Visualization

This package generates polished figures from thermal-cycling measurements.

## Figures
1. **Line plot** (`line_temperature_profile.png`)  
   Shows the full temperature profile across cycles (macro trends, step changes).  

2. **Histogram** (`hist_temperature_distribution.png`)  
   Distribution of peak temperatures.  

3. **Box plot** (`box_temperature_spread.png`)  
   Spread and thermal-stress outliers.  

4. **Scatter plot** (`scatter_cycle_vs_resistance.png`)  
   Correlates cycle number with resistance (secondary variable).  

## Requirements
- Python 3.11+
- pandas  
- seaborn  
- matplotlib  

Install dependencies:
```bash
pip install pandas seaborn matplotlib
