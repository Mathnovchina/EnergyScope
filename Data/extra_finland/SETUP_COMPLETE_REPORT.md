# Finland Calibration Setup - Complete Report

**Date:** January 23, 2026  
**Status:** ✅ COMPLETE - All data files ready for testing

---

## Executive Summary

Successfully extracted and configured all required data files for Finland calibration from the MultiCell EnergyScope version. All three target years (2017, 2035, 2050) now have complete datasets ready for model execution.

### 📊 Critical Fixes Applied

1. **NUCLEAR CAPACITY CORRECTION** ⚠️ CRITICAL
   - **Problem:** MultiCell data showed 0 GW for Finland nuclear (completely wrong!)
   - **Fix Applied:**
     - 2017: 2.76 GW (Olkiluoto 1+2 only - OL3 not yet operational)
     - 2035: 4.36-5.0 GW (OL1+2+3, expansion allowed)
     - 2050: 4.36-5.0 GW (OL1+2+3, expansion allowed)
   - **Source:** Historical data + Finnish nuclear program

2. **2017 RENEWABLE CAPACITIES ADJUSTED**
   - Wind Onshore: 1.5 GW actual (vs 2035 projection of 30.77 GW max)
   - Wind Offshore: 0 GW in 2017 (no offshore wind yet)
   - PV: Minimal deployment (~0.02 GW)
   - Hydro River: 3.264 GW (fixed existing infrastructure)

---

## Files Created/Modified

### Data Folders
```
Data/FI_2017/  ✓ 11 files (complete)
Data/FI_2035/  ✓ 11 files (complete)  
Data/FI_2050/  ✓ 11 files (complete)
```

### New Documentation
- **Finland_Calibration_Tracker.xlsx** (5 sheets)
  - Technologies_2017: 9 capacity changes documented
  - Misc_Parameters: 29 parameters across years
  - Nuclear_Capacity: Critical fix summary
  - Data_Sources: 10 data sources tracked
  - Next_Steps: 5 priority tasks

### Scripts Created
- `setup_finland_data.py` - Initial extraction
- `final_setup_finland.py` - Complete configuration
- `extract_finland_data.py` - Original extraction tool (from docs)

---

## Data Sources Used

| Data Type | Source | Status |
|-----------|--------|--------|
| Time Series 2017 | MC exogenous_data/regions/Time_series_2017.csv | ✅ Extracted FI columns (117-129) |
| Technologies 2035/2050 | MC Data/{year}/FI/Technologies.csv | ✅ Copied + nuclear corrected |
| Demands 2035/2050 | MC Data/{year}/FI/Demands.csv | ✅ Copied |
| Resources 2035/2050 | MC Data/{year}/FI/Resources.csv | ✅ Copied |
| Misc 2035/2050 | MC Data/{year}/FI/Misc.json | ✅ Copied + updated |
| Storage files | MC Data/2035/00_INDEP/ | ✅ Copied (country-independent) |
| Layers | MC Data/2035/00_INDEP/Layers_in_out.csv | ✅ Copied |
| 2017 baseline | Belgium 2015 + Finland adjustments | ⚠️ Needs validation |

---

## Technology Capacity Changes (2017)

| Technology | Old (Belgium) | New (Finland 2017) | Rationale |
|------------|---------------|-------------------|-----------|
| **NUCLEAR** | 5.925 GW | **2.76 GW** | Olkiluoto 1+2 only |
| WIND_ONSHORE | 1.25 GW | 1.5-5.0 GW | Historical ~1.5 GW installed |
| WIND_OFFSHORE | 0.71 GW | 0.0 GW | No offshore wind in 2017 |
| HYDRO_RIVER | 0.115 GW | 3.264 GW | Finland has much more hydro |
| GEOTHERMAL | 0 GW | 0-0.3 GW | From FI MC data |
| PV_ROOFTOP | N/A | 0.02-2.0 GW | Very small deployment |
| PV_UTILITY | N/A | 0-1.0 GW | Minimal utility PV |

---

## Misc.json Parameters Updated

### Key Finland-Specific Parameters
```json
{
  "i_rate": 0.05,
  "re_share_primary": 0.41,
  "solar_area": 338000,
  "power_density_pv": 0.085,
  "power_density_solar_thermal": 0.026,
  "elec_import_capacity": 3.0,
  "elec_export_capacity": 3.0
}
```

### Parameter Comparison Across Years
- **2017**: 24 parameters (includes Belgium baseline)
- **2035**: 13 parameters (Finland MC)
- **2050**: 13 parameters (Finland MC)

See `Finland_Calibration_Tracker.xlsx` → Sheet "Misc_Parameters" for full comparison.

---

## Important Notes & Assumptions

### ⚠️ Critical Issues
1. **2017 Demands.csv** currently uses 2035 as baseline
   - Needs adjustment to actual 2017 demand levels
   - Finland 2017 total energy: ~85 TWh electricity
   - Must collect validation data from Statistics Finland

2. **Demand Structure Difference**
   - Belgium: ELECTRICITY split into baseload + LIGHTING
   - Finland MC: Combined ELECTRICITY + new categories (COOLING, AVIATION, SHIPPING)
   - Current setup: Using Finland MC structure
   - **Decision needed:** Keep MC structure or convert to Belgium format?

3. **END_USES_CATEGORIES**
   - Currently using Belgium/country-independent version
   - May need adjustment if Finland has different categories

### ✅ Validated
- All 11 required files present in each year folder
- Nuclear capacity corrected to realistic values
- Time series properly extracted (8760 hours × 13 variables)
- Storage and layer files copied from country-independent sources

---

## Next Steps (Priority Order)

### 🔴 HIGH PRIORITY - Week 1

1. **Test Run with FI_2035**
   ```bash
   cd case_studies/ref_run
   # Update ESTD_main.run to point to ../../Data/FI_2035/
   ampl ESTD_main.run
   ```
   - If errors: Document and fix iteratively
   - Expected issues: Demand categories, technology naming

2. **Review Generated Excel Tracker**
   - File: `Data/extra_finland/Finland_Calibration_Tracker.xlsx`
   - Verify all changes make sense
   - Add any missing assumptions

3. **Decide on Demand Structure**
   - Option A: Convert Finland Demands to Belgium format (split ELECTRICITY)
   - Option B: Keep Finland format, ensure model supports new categories
   - Recommendation: Check `es_model.mod` for END_USES_TYPES

### 🟡 MEDIUM PRIORITY - Weeks 2-3

4. **Collect 2017 Validation Data**
   Sources:
   - Statistics Finland (stat.fi)
   - Finnish Energy (energia.fi)
   - IEA Finland statistics
   
   Required data:
   - Total electricity production by technology
   - Total GHG emissions
   - Energy consumption by sector
   - Technology installed capacities

5. **Adjust 2017 Demands.csv**
   - Scale down from 2035 baseline to 2017 actual
   - Verify against collected validation data
   - Adjust sector breakdowns if needed

6. **Run Constrained 2017 Validation**
   - Set f_min = f_max = actual 2017 capacities
   - Set f_max = 0 for technologies not yet deployed
   - Compare model output with real 2017 data
   - Acceptance criteria: ±10% GHG, ±5% electricity

### 🟢 LOW PRIORITY - Weeks 4-6

7. **Create Intermediate Years (if needed)**
   - Interpolate 2020, 2025, 2030, 2040, 2045
   - Linear interpolation for most parameters
   - Check technology deployment trajectories

8. **Full Scenario Runs**
   - Execute all years successfully
   - Verify year-to-year consistency
   - Check technology transitions are realistic

9. **Final Documentation**
   - Document all calibration decisions
   - List data sources with URLs/dates
   - Note assumptions and limitations
   - Create validation report

---

## File Verification Checklist

### FI_2017 ✅
- [x] Demand.csv (or Demands.csv)
- [x] END_USES_CATEGORIES.csv
- [x] Layers_in_out.csv
- [x] misc.json (updated with Finland params)
- [x] Resources.csv
- [x] Storage_characteristics.csv
- [x] Storage_eff_in.csv
- [x] Storage_eff_out.csv
- [x] Technologies.csv (Belgium template + Finland limits)
- [x] Time_series.csv (extracted FI columns, 8760 rows)

### FI_2035 ✅
- [x] All 10 files present
- [x] NUCLEAR corrected: 4.36-5.0 GW
- [x] misc.json updated

### FI_2050 ✅
- [x] All 10 files present
- [x] NUCLEAR corrected: 4.36-5.0 GW
- [x] misc.json updated

---

## Known Limitations & Gaps

### Data Gaps
1. **2017 Historical Validation Data** - Not yet collected
   - Need actual technology capacities
   - Need actual production/consumption
   - Need actual costs and emissions

2. **Intermediate Years** - Not created yet
   - Years 2020, 2025, 2030, 2040, 2045
   - Can be interpolated or run with only 3 years

3. **Finland-Specific Cost Data** - Using defaults
   - Investment costs: Need Finland-specific values?
   - Maintenance costs: Currency conversion needed?
   - Fuel costs: Finland market prices?

### Assumptions Made
1. **2017 Demands** = 2035 baseline (temporary)
2. **Cost parameters** = Belgium values (need verification)
3. **Efficiency parameters** = Country-independent (should be OK)
4. **Time series** = 2017 actual (validated from MC data)

---

## Validation Strategy

### Phase 1: Model Execution Test (Week 1)
- Run FI_2035 to check for syntax/compatibility errors
- Fix any model-code mismatches
- Ensure all technologies are properly defined

### Phase 2: 2017 Constrained Validation (Week 2-3)
- Set actual 2017 capacities as constraints
- Run model in "validation mode"
- Compare outputs:
  - Total electricity: ~85 TWh (±5%)
  - GHG emissions: ~55 Mt CO2eq (±10%)
  - Nuclear production: ~22 TWh
  - Hydro production: ~13-15 TWh
  - Wind production: ~4-5 TWh

### Phase 3: Calibration Adjustments (Week 3-4)
- If validation errors > thresholds:
  - Adjust efficiency parameters
  - Adjust demand profiles
  - Adjust cost parameters (if needed)
- Document all adjustments
- Re-run validation

### Phase 4: Future Scenarios (Week 5-6)
- Run 2035 and 2050 scenarios
- Check technology mix evolution is reasonable
- Verify emissions targets are achievable
- Compare with Finland national energy plans

---

## Commands Reference

### Run EnergyScope
```bash
cd case_studies/ref_run
# Edit ESTD_main.run to change data path
ampl ESTD_main.run
```

### Re-run Setup Scripts (if needed)
```bash
# Extract data from MultiCell
python extract_finland_data.py --year 2035
python extract_finland_data.py --year 2050
python extract_finland_data.py --year 2017

# Complete setup with all fixes
python setup_finland_data.py

# Final configuration
.venv\Scripts\python.exe final_setup_finland.py
```

### Check File Contents
```bash
# View first lines of key files
Get-Content Data/FI_2035/Technologies.csv -Head 20
Get-Content Data/FI_2035/misc.json

# Check nuclear capacity
Select-String "NUCLEAR" Data/FI_2035/Technologies.csv
```

---

## Success Criteria

### Week 1 (Immediate)
- [ ] FI_2035 runs without errors
- [ ] Output files generated successfully
- [ ] No missing technology definitions

### Week 2-3 (Validation)
- [ ] 2017 validation data collected
- [ ] Constrained 2017 run completed
- [ ] Validation metrics within acceptable ranges

### Week 4-6 (Calibration)
- [ ] All three years run successfully
- [ ] Technology evolution looks reasonable
- [ ] Emissions trajectories align with policy targets
- [ ] Costs are within expected ranges

---

## Contact & Resources

### Data Sources
- **Statistics Finland:** https://stat.fi/en
- **Finnish Energy:** https://energia.fi/en
- **IEA Finland:** https://www.iea.org/countries/finland
- **Fingrid (TSO):** https://www.fingrid.fi/en/

### Documentation
- Main guide: `FINLAND_CALIBRATION_GUIDE.md`
- Checklist: `FINLAND_CALIBRATION_CHECKLIST.md`
- Tracker: `Finland_Calibration_Tracker.xlsx`

### Model Documentation
- EnergyScope docs: `Docs/` folder
- Model equations: `energyscope/energy_model/es_model.mod`

---

## Change Log

| Date | Action | Status |
|------|--------|--------|
| 2026-01-23 | Extracted 2017 time series | ✅ Complete |
| 2026-01-23 | Copied MC Finland data (2035/2050) | ✅ Complete |
| 2026-01-23 | Fixed nuclear capacity (CRITICAL) | ✅ Complete |
| 2026-01-23 | Updated misc.json parameters | ✅ Complete |
| 2026-01-23 | Created calibration tracker Excel | ✅ Complete |
| 2026-01-23 | Adjusted 2017 technology capacities | ✅ Complete |

---

**🎯 READY FOR FIRST TEST RUN WITH FI_2035 DATA!**

Next command:
```bash
cd case_studies/ref_run
# Update ESTD_main.run to point to ../../Data/FI_2035/
ampl ESTD_main.run
```

---

*Generated: January 23, 2026*  
*Setup Scripts: setup_finland_data.py, final_setup_finland.py*
