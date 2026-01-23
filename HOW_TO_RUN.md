# EnergyScope Model - User Guide

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Running the Model](#running-the-model)
4. [Main Inputs](#main-inputs)
5. [Main Outputs](#main-outputs)
6. [Configuration](#configuration)

---

## Overview

EnergyScope is an open-source energy system optimization model that helps design regional energy systems. It optimizes the energy system configuration (technologies, resources, storage) to meet energy demands while minimizing total system cost and respecting CO2 emission limits.

**Key Features:**
- Hourly linear programming (LP) optimization
- Typical days clustering to reduce computational complexity
- Multi-sector energy system (electricity, heat, mobility, industry)
- Technology investment and operation decisions
- Resource consumption and GWP (greenhouse gas) emissions tracking

---

## Installation

### 1. Prerequisites
- Python >= 3.7
- AMPL solver (Gurobi, CPLEX, or other)
- Git (optional, for cloning)

### 2. Setup Steps

```powershell
# Navigate to the EnergyScope directory
cd c:\Users\borde\OneDrive\Bureau\model\EnergyScope\EnergyScope

# Create and activate virtual environment (optional but recommended)
python -m venv .venv
.venv\Scripts\activate

# Install the package with dependencies
pip install -e .
```

**Required Python packages** (automatically installed):
- numpy
- pandas
- matplotlib
- plotly
- pyyaml

### 3. AMPL Solver Configuration
- Install AMPL with a solver (Gurobi or CPLEX recommended)
- Update `AMPL_path` in config file if AMPL is not in your PATH environment variables

---

## Running the Model

### Quick Start

```powershell
# Navigate to scripts directory
cd scripts

# Run the model with default configuration
python run_energyscope.py
```

### What Happens During Execution

1. **Data Import**: Loads input data from CSV files
2. **Typical Days Selection**: Performs k-medoid clustering to select representative days
3. **Data Printing**: Generates `.dat` files for AMPL optimization
4. **Optimization**: Runs the AMPL solver to find optimal energy system design
5. **Output Generation**: Saves results and generates plots

### Execution Time
- Typical days clustering: ~5-10 seconds
- Optimization (12 typical days): ~15-30 seconds
- Total runtime: ~1-2 minutes (depending on system and solver)

---

## Main Inputs

All input data is located in the `Data/` directory, organized by year (e.g., `Data/2050/`).

### 1. **Demand.csv**
Defines end-use energy demands for different sectors.

**Columns:**
- `Category`: Energy type (Electricity, Heat, Mobility, Non-energy)
- `Subcategory`: Demand category
- `parameter name`: AMPL parameter name
- `HOUSEHOLDS`, `SERVICES`, `INDUSTRY`, `TRANSPORTATION`: Demand values by sector
- `Units`: Units of measurement (GWh, Mpkm, Mtkm)

**Example:**
```csv
Category;Subcategory;parameter name;HOUSEHOLDS;SERVICES;INDUSTRY;TRANSPORTATION;Units
Electricity;baseload;ELECTRICITY;9212.6;12814.7;51287.5;0.0;[GWh]
Heat;space heating;HEAT_LOW_T_SH;45360.0;32023.1;14753.0;0.0;[GWh]
Mobility;passenger;MOBILITY_PASSENGER;0.0;0.0;0.0;159270.5;[Mpkm]
```

### 2. **Technologies.csv**
Contains all available energy conversion technologies with their technical and economic parameters.

**Key Parameters:**
- `c_inv`: Investment cost [EUR/kW]
- `c_maint`: Maintenance cost [EUR/kW/year]
- `lifetime`: Technology lifetime [years]
- `c_p`: Operation cost [EUR/MWh]
- `gwp_constr`: Construction emissions [kgCO2/kW]
- `f_min`, `f_max`: Min/max installed capacity [GW]

### 3. **Resources.csv**
Defines primary energy resources (coal, gas, biomass, solar, wind, etc.).

**Key Parameters:**
- `avail`: Maximum availability [GWh/year or GW]
- `c_op`: Resource cost [EUR/MWh]
- `gwp_op`: Operational emissions [kgCO2/MWh]

### 4. **Layers_in_out.csv**
Specifies input/output layers for each technology (energy conversion matrix).

**Example:** A natural gas boiler takes ELECTRICITY (small amount) and GAS as inputs, outputs HEAT_LOW_T_DECEN

### 5. **Storage_characteristics.csv**, **Storage_eff_in.csv**, **Storage_eff_out.csv**
Define storage technologies (batteries, thermal storage, pumped hydro, etc.) with efficiencies and characteristics.

### 6. **Time_series.csv**
Hourly profiles (8760 hours) for variable resources and demands:
- Solar irradiation profiles
- Wind capacity factors
- Temperature profiles
- Electricity demand variations
- Heating demand variations

### 7. **END_USES_CATEGORIES.csv**
Categorizes end-uses for output processing and visualization.

### 8. **misc.json**
Miscellaneous parameters:
- `GWP_limit`: CO2 emission constraint [ktCO2/year]
- `i_rate`: Interest rate for annualization
- Other system-wide parameters

### Input Data Map and Processing Flow

- **Data folder**: `Data/<year>/` (e.g., `Data/2050/`)
   - Read by `es.import_data()` in [energyscope/preprocessing/es_pre/es_read_data.py](energyscope/preprocessing/es_pre/es_read_data.py#L70-L115)
   - Loaded into `config['all_data']` (pandas DataFrames + misc dict)
- **Clustering (typical days)**: uses `Time_series.csv` + `Demand.csv`
   - Function: `build_td_of_days()` in [energyscope/preprocessing/td_selection/td_selection.py](energyscope/preprocessing/td_selection/td_selection.py#L15-L80)
   - Output: `energyscope/preprocessing/td_selection/td_of_days.out`
- **Printed AMPL inputs** (generated, not edited):
   - `case_studies/<case_study>/ESTD_data.dat` (core data)
   - `case_studies/<case_study>/ESTD_<nbr_td>TD.dat` (time slices) if `printing_td: True`
   - Produced by `es.print_data()` in [energyscope/preprocessing/es_pre/es_write_energy_model_data.py](energyscope/preprocessing/es_pre/es_write_energy_model_data.py#L19-L120)
- **Model files**: `energyscope/energy_model/`
   - `es_model.mod` (AMPL model), copied to `case_studies/<case_study>/`
   - Run script template `run/print_*.run` combined by `es.run_es()` in [energyscope/energy_model/es_run.py](energyscope/energy_model/es_run.py#L12-L70)
- **Config file**: `scripts/config_ref.yaml`
   - Paths (`data_dir`, `cs_path`, `es_path`, `step1_path`), solver options, flags (`print_hourly_data`, `print_sankey`), emission cap, typical days count

**Processing sequence (run_energyscope.py):**
1) `load_config()` → expand relative paths to absolute
2) `import_data()` → read CSV/JSON inputs into memory
3) `build_td_of_days()` → cluster typical days
4) `print_data()` → emit AMPL `.dat` files into `case_studies/<case_study>/`
5) `run_es()` → copy `es_model.mod`, compose `.run`, call AMPL solver
6) `read_outputs()` + plotting helpers → populate `output/` and `output/plots/`

---

## Main Outputs

All outputs are saved in `case_studies/<case_study_name>/output/`

### 1. **cost_breakdown.txt**
Total system cost breakdown.

**Components:**
- `C_inv`: Investment costs (annualized)
- `C_maint`: Maintenance costs
- `C_op`: Operation costs
- `TotalCost`: Sum of all costs [MEUR/year]

### 2. **resources_breakdown.txt**
Primary energy resources used in the system.

**Columns:**
- Resource name
- `Used`: Annual consumption [GWh/year]
- `Potential`: Maximum availability [GWh/year]

### 3. **gwp_breakdown.txt**
Greenhouse gas emissions breakdown.

**Components:**
- `GWP_constr`: Construction emissions [ktCO2-eq]
- `GWP_op`: Operational emissions [ktCO2-eq/year]
- Total GWP

### 4. **assets.txt**
Installed capacity for all technologies [GW or appropriate unit].

**Key Information:**
- `f`: Installed capacity of each technology
- `f_min`, `f_max`: Technology bounds
- `%_min`, `%_max`: Percentage of bounds used

### 5. **sto_year.txt**
Annual storage operations.

**Columns:**
- Storage technology name
- Energy stored/discharged over the year

### 6. **year_balance.txt**
Annual energy balance by layer (electricity, heat, fuels, etc.).

**Shows:**
- Total production by layer
- Total consumption by layer
- Network losses

### 7. **losses.txt**
Network distribution losses by layer [GWh/year].

### 8. **hourly_data/** (if `print_hourly_data: True`)
Detailed hourly results for typical days:
- `cost_year.txt`: Hourly costs
- `layer_*.txt`: Hourly layer balances (e.g., `layer_ELECTRICITY.txt`)
- `sto_level_*.txt`: Storage level evolution

### 9. **sankey/** (if `print_sankey: True`)
Data for Sankey diagram visualization:
- `input2sankey.csv`: Energy flows for Sankey diagram
- Can be visualized using `es.drawSankey()` function

### 10. **plots/**
Generated visualization plots:
- `primary_energy_used.png`: Primary resources consumption
- `electricity_assets.png`: Electricity generation capacities
- `layer_electricity.png`: Hourly electricity balance for typical days
- `layer_heat_low_t_decen.png`: Hourly heat balance for typical days

### 11. **log.txt**
AMPL solver log with optimization details:
- Problem size (variables, constraints)
- Solver iterations
- Solution status
- Objective value

---

## Configuration

### Configuration File: `scripts/config_ref.yaml`

#### Key Parameters:

```yaml
# Case study name (creates directory: case_studies/<case_study>/)
'case_study': 'ref_run'

# Number of typical days (4, 10, 12 common choices)
# More days = more accurate but slower
'nbr_td': 12

# CO2 emissions limit [ktCO2-eq/year]
'GWP_limit': 1000

# Data directory path
'data_dir': 'Data/2050'

# AMPL path (set to null if AMPL is in PATH)
'AMPL_path': null

# Solver options
'ampl_options':
  'solver': 'gurobi'  # or 'cplex', 'cbc', etc.
  'gurobi_options': 'predual=-1 method=2 crossover=0 barconvtol=1e-6'

# Output detail level
'print_hourly_data': True  # Save hourly results
'print_sankey': True       # Generate Sankey diagram data
```

#### Modifying Scenarios:

To create different scenarios:
1. Copy `config_ref.yaml` to `config_<scenario_name>.yaml`
2. Modify parameters (e.g., different `GWP_limit`, `data_dir`, `case_study` name)
3. Update `run_energyscope.py` to load your config:
   ```python
   config = es.load_config(config_fn='config_<scenario_name>.yaml')
   ```

#### Solver Selection:

**Gurobi** (recommended, commercial):
- Fast for large problems
- Requires license (free academic license available)

**CPLEX** (commercial):
- Similar performance to Gurobi
- Requires license

**CBC** (open-source):
- Free but slower
- May struggle with large problems

---

## Tips and Troubleshooting

### Common Issues:

1. **Module not found errors**
   ```powershell
   pip install -e .
   ```

2. **AMPL not found**
   - Add AMPL to PATH, or
   - Set `AMPL_path` in config file

3. **Solver errors**
   - Check solver is properly installed
   - Verify license (for commercial solvers)
   - Try different solver

4. **Infeasible solution**
   - Check if `GWP_limit` is too restrictive
   - Verify input data consistency
   - Check `f_min`/`f_max` technology bounds

### Performance Optimization:

- Use fewer typical days (`nbr_td: 4`) for faster testing
- Use `predual=-1` and barrier method for Gurobi
- Increase `barconvtol` for faster but less precise solutions
- Disable `print_hourly_data` if not needed

---

## Quick Reference Commands

```powershell
# Standard run
cd scripts
python run_energyscope.py

# Run with different Python
C:\path\to\python.exe run_energyscope.py

# Check installed packages
pip list

# View results
cd ../case_studies/ref_run/output
# Open cost_breakdown.txt, assets.txt, etc.
```

---

## Additional Resources

- **Documentation**: https://energyscope.readthedocs.io
- **Repository**: https://github.com/energyscope/EnergyScope
- **Contact**: moret.stefano@gmail.com, gauthierLimpens@gmail.com

---

**Last Updated**: January 2026
