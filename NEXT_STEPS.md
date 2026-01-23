# Finland Calibration - Next Steps

**Date:** January 23, 2026  
**Current Status:** Phase 1 Complete, Ready for Phase 2 (Model Testing)

---

## 🎯 IMMEDIATE PRIORITIES (Today)

### 1. Investigate Layers_in_out.csv Row Mismatch 🔍 **URGENT**

**Problem:**
- Technologies.csv: 123 rows (121 technologies + 2 header)
- Layers_in_out.csv: 167 rows (166 technology entries + 1 header)
- **Mismatch: 45 extra rows**

**Action Required:**
```python
# Extract and compare technology names
import pandas as pd

# Get Technologies list
tech = pd.read_csv('Data/FI_2017/Technologies.csv', sep=';', skiprows=2)
tech_names = tech['Technologies param'].tolist()
print(f"Technologies.csv: {len(tech_names)} technologies")

# Get Layers list
layers = pd.read_csv('Data/FI_2017/Layers_in_out.csv', sep=';')
layers_names = layers.iloc[:, 0].tolist()  # First column = tech names
print(f"Layers_in_out.csv: {len(layers_names)} rows")

# Find differences
extra_in_layers = set(layers_names) - set(tech_names)
missing_in_layers = set(tech_names) - set(layers_names)

print(f"\nExtra in Layers (not in Technologies): {len(extra_in_layers)}")
print(extra_in_layers)
print(f"\nMissing from Layers (in Technologies): {len(missing_in_layers)}")
print(missing_in_layers)
```

**Expected Outcomes:**
- **If duplicates:** Remove duplicate rows from Layers_in_out.csv
- **If missing technologies:** Add to Technologies.csv with appropriate parameters
- **If obsolete entries:** Remove from Layers_in_out.csv

**Timeline:** 1-2 hours

---

### 2. Investigate Electricity Demand Discrepancy 🔍 **URGENT**

**Problem:**
- Model shows: 42,912 GWh (FI_2017)
- Statistics Finland 2017 actual: ~85,000 GWh
- **Factor of 2 difference!**

**Possible Explanations:**
1. **Useful energy vs final energy:** Model uses energy after conversion losses
2. **Sector coverage:** Electric heating may be in HEAT demands, not ELECTRICITY
3. **Data source:** MC exogenous data may have wrong year/region

**Action Required:**
```python
# Check Belgium for comparison
belgium_elec = 81_478  # GWh from Belgium 2015 Demands.csv
belgium_actual_2015 = 83_000  # GWh actual (Elia/Eurostat)
ratio_belgium = belgium_elec / belgium_actual_2015
print(f"Belgium ratio (model/actual): {ratio_belgium:.2f}")

# If Belgium ratio ~1.0 → Finland extraction error
# If Belgium ratio ~0.5 → systematic (useful energy convention)
```

**Timeline:** 30 minutes

---

### 3. Verify PV Capacity Values 🔍 **HIGH**

**Problem:**
- Model shows: 3.845 GW (FI_2017)
- IEA 2017 actual: ~50 MW (0.05 GW)
- **Factor of 77 difference!**

**Likely Cause:** Copy-paste from Belgium (Belgium 2015 had ~3 GW PV)

**Action Required:**
- Check if MC uses "technology availability" vs "installed capacity"
- Update FI_2017: f_min=0.05, f_max=0.05 (or reasonable expansion limit)
- Check FI_2035/FI_2050 for more realistic future values

**Timeline:** 15 minutes

---

## 🚀 PHASE 2: FIRST MODEL RUN (After Investigations)

### Step 1: Update ESTD_main.run

**File:** `case_studies/ref_run/ESTD_main.run`

**Change:**
```ampl
# OLD:
param DataFolder symbolic := "../../Data/2015/";

# NEW:
param DataFolder symbolic := "../../Data/FI_2035/";
```

**Rationale:** Start with 2035 (more complete future scenario, less constrained than 2017)

---

### Step 2: Execute First Test Run

**Command:**
```bash
cd case_studies/ref_run
ampl ESTD_main.run > ../../output_FI_2035_run1.log 2>&1
```

**Monitor for:**
- ✅ **Success:** Model runs, produces solution → proceed to validation
- ⚠️ **Warnings:** Dimension mismatches, unused parameters → document
- ❌ **Errors:** Fatal crashes → troubleshoot iteratively

**Expected Runtime:** 5-30 minutes (depends on problem size)

---

### Step 3: Analyze Outputs

**If Successful:**
```
Check outputs:
- output/sankey.txt (energy flows)
- output/year_balance.txt (annual energy balance)
- output/Losses.txt (conversion losses)
- output/gwp_breakdown.txt (emissions)
```

**If Errors:**
Document exact error messages:
- "set TECHNOLOGIES[tech_name] undefined" → Layers mismatch not fixed
- "dimension mismatch" → Array size issues
- "infeasible" → Supply/demand balance problem
- "unbounded" → Missing constraints

---

## 📊 PHASE 3: VALIDATION (Week 2)

### Collect 2017 Finland Statistics

**Sources:**
- Statistics Finland (stat.fi): Energy consumption, production
- Fingrid (fingrid.fi): Electricity generation, demand
- Finnish Energy (energia.fi): District heating, fuel mix
- IAEA PRIS: Nuclear generation

**Target Metrics:**
| Metric | 2017 Actual | Model Target | Tolerance |
|--------|-------------|--------------|-----------|
| Total electricity consumption | ~85 TWh | 85 TWh | ±5% |
| Nuclear generation | ~22 TWh | 22 TWh | ±5% |
| Hydro generation | 13-15 TWh | 14 TWh | ±10% |
| Wind generation | ~4-5 TWh | 4.5 TWh | ±15% |
| Total GHG emissions | ~55 Mt CO2-eq | 55 Mt | ±10% |
| Biomass consumption | ~280 PJ | 280 PJ | ±15% |

---

### Run Constrained 2017 Validation

**Approach:**
1. Fix all technologies at 2017 actual capacities (f_min = f_max = actual)
2. Run model in "validation mode" (reproduces 2017 with real constraints)
3. Compare outputs with collected statistics
4. If errors > tolerance → calibrate efficiency parameters

---

## 📅 TIMELINE

### Week 1 (This Week)
- **Day 1 (Today):** 
  - ✅ Documentation cleanup (DONE)
  - 🔍 Investigate 3 critical issues (Layers, electricity, PV)
  - 🚀 First test run (FI_2035)
  
- **Day 2-3:**
  - 🐛 Troubleshoot errors from first run
  - 🔄 Iterate fixes until clean run
  - 📊 Test all 3 years (2017, 2035, 2050)

- **Day 4-5:**
  - 📈 Begin collecting 2017 statistics
  - 📝 Document model assumptions
  - 🎯 Prepare validation framework

### Week 2-3: Validation & Calibration
- Run 2017 constrained validation
- Compare with real data
- Adjust parameters iteratively
- Document calibration choices

### Week 4-6: Scenarios & Finalization
- Run 2035/2050 policy scenarios
- Sensitivity analysis
- Final documentation
- Reproducibility package

---

## 🎯 SUCCESS CRITERIA

### Phase 1 Complete ✅
- [x] All 30 files present
- [x] Belgium format compatibility verified
- [x] Critical fixes applied (headers, columns, structure)
- [x] Documentation consolidated

### Phase 2 Success (This Week)
- [ ] Layers_in_out row mismatch resolved
- [ ] Model runs without fatal errors (all 3 years)
- [ ] Outputs reasonable (no negative values, bounded)
- [ ] All errors documented with solutions

### Phase 3 Success (Weeks 2-3)
- [ ] 2017 validation errors <10% for key metrics
- [ ] Nuclear generation matches actual (~22 TWh)
- [ ] Total GHG within ±15% of actual
- [ ] Biomass use within availability constraints

### Phase 4 Success (Final)
- [ ] All 3 years run cleanly
- [ ] Results published/documented
- [ ] Reproducibility tested
- [ ] Model ready for policy analysis

---

## 📞 SUPPORT RESOURCES

**Documentation:**
- STRUCTURE_DISCREPANCIES.md - All Belgium vs Finland differences
- PROJECT_STATUS.md - Overall progress tracking
- Finland_Calibration_MASTER.xlsx - Data tracker

**Data Sources:**
- MC folder: Data/2035/FI/, Data/2050/FI/
- MC exogenous: Data/exogenous_data/regions/
- Belgium baseline: Data/2015/

**Model Files:**
- AMPL model: case_studies/ref_run/es_model.mod
- Run file: case_studies/ref_run/ESTD_main.run
- Outputs: case_studies/ref_run/output/

---

**Last Updated:** January 23, 2026  
**Next Review:** After first successful model run
