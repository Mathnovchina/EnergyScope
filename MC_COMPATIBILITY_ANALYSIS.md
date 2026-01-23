# MC vs Single-Cell Compatibility Analysis

**Date**: January 23, 2026  
**Status**: CRITICAL DECISION REQUIRED

---

## Executive Summary

Finland data was extracted from **EnergyScope Multi-Cell (MC) version** but we've been preparing to run it with the **Belgium single-cell model**. Analysis reveals:

- ✅ **Technologies**: 111 in both (SAME) - no compatibility issue
- ⚠️ **Layers**: 166 in Finland vs 115 in Belgium (63 extra) - likely compatible but unconfirmed
- ⚠️ **AMPL Model**: MC version has 551 lines vs single-cell 380 lines (+45%) - **SIGNIFICANT DIFFERENCES**

**Risk**: MEDIUM to HIGH - model may run but produce incorrect results or fail with subtle errors

---

## Detailed Comparison

### 1. Technology Sets ✅ COMPATIBLE
```
Belgium single-cell (2015): 111 technologies
Finland from MC (2017):     111 technologies
Common:                     111 (100% match)
Finland-only:               0
Belgium-only:               0
```

**Conclusion**: Technology lists are identical. No missing tech definitions.

### 2. Layers/Resources ⚠️ PARTIALLY COMPATIBLE
```
Belgium single-cell (2015): 115 layer entries
Finland from MC (2017):     166 layer entries
Common:                     103
Finland-only (MC):          63
Belgium-only:               12
```

**Finland-only layers (from MC):**

**New Energy Carriers** (renewable fuels):
- DIESEL_RE, GASOLINE_RE, JET_FUEL_RE, LFO_RE
- H2_NEW, H2_RETROFITTED, H2_NG
- AMMONIA, AMMONIA_RE, METHANOL_RE

**New Transport Technologies**:
- CARGO_AMMONIA, CARGO_LFO, CARGO_METHANOL, CARGO_LNG
- CARGO_FUELCELL_AMMONIA, CARGO_FUELCELL_LH2
- PLANE_H2_SHORT_HAUL, PLANE_LONG_HAUL, PLANE_SHORT_HAUL

**New Infrastructure**:
- GAS_PIPELINE, GAS_SUBSEA
- H2_SUBSEA_NEW, H2_SUBSEA_RETRO
- HVAC_LINE, HVDC_SUBSEA

**New Renewables**:
- PV_ROOFTOP, PV_UTILITY (split from single PV)
- PT_COLLECTOR, PT_HEAT, PT_POWER_BLOCK (parabolic trough)
- ST_COLLECTOR, ST_HEAT, ST_POWER_BLOCK (solar tower)
- TIDAL_RANGE, TIDAL_STREAM, WAVE

**New Biomass Pathways**:
- BIOMASS_TO_* (DIESEL, GASOLINE, JET_FUEL, LFO, METHANE, POWER)
- BIOWASTE_TO_* (DIESEL, GASOLINE, JET_FUEL, LFO, METHANE, METHANOL)
- BIOMETHANATION_BIOWASTE, BIOMETHANATION_WET_BIOMASS

**Conclusion**: MC has significantly expanded energy carrier set and biomass conversion pathways. These may require new balance equations in AMPL model.

### 3. AMPL Model Code ⚠️ SIGNIFICANT DIFFERENCES
```
Single-cell: energyscope/energy_model/es_model.mod (380 lines)
MC version:  EnergyScope_multi_cells/esmc/energy_model/ESMC_model_AMPL.mod (551 lines)
Difference:  +171 lines (+45%)
```

**Implications**: MC likely added:
- New balance equations for renewable fuels
- H2 infrastructure constraints
- Biomass conversion pathways
- Multi-cell exchange logic (though we're using single country)

**Risk**: Running Finland data (MC format) with Belgium model (single-cell) may:
1. Ignore new energy carriers → incorrect optimization
2. Miss biomass pathway constraints → infeasible or wrong results
3. Fail validation checks if MC added new constraints

---

## Decision Matrix

### OPTION A: Upgrade Single-Cell Model to MC Technology Set ⭐ **RECOMMENDED**

**Approach**: Update `es_model.mod` to incorporate MC improvements while keeping single-cell simplicity

**Steps**:
1. Compare `es_model.mod` (single) vs `ESMC_model_AMPL.mod` (MC)
2. Identify new constraints and equations for:
   - Renewable fuel production/balance
   - H2 infrastructure
   - Biomass conversion pathways
   - Expanded PV/solar definitions
3. Port relevant sections to single-cell model
4. Test with Finland data

**Pros**:
- ✅ Keep all MC technology improvements
- ✅ Finland data works as-is (no manipulation needed)
- ✅ Future-proof for adding more countries from MC
- ✅ Learn from MC's reference implementation
- ✅ Single-country focus (simpler than full MC)

**Cons**:
- ⏱️ Moderate effort (1-2 days code review and porting)
- 🧠 Need to understand MC model changes
- 🧪 Requires thorough testing

**Effort**: 1-2 days

**Risk**: LOW (MC model is validated reference)

---

### OPTION B: Use MC Model Directly

**Approach**: Use `EnergyScope_multi_cells` codebase but configure for single country (Finland only)

**Steps**:
1. Study MC model structure and workflow
2. Configure for single-cell mode (Finland only, no exchanges)
3. Use existing Finland data files from MC
4. Run MC model with single-country setup

**Pros**:
- ✅ Zero compatibility issues (MC data + MC model)
- ✅ Most modern, maintained codebase
- ✅ Guaranteed correct results
- ✅ Documentation and examples available

**Cons**:
- 📚 Steeper learning curve (multi-cell architecture)
- 🔧 May be overkill for single-country analysis
- 🔄 Different workflow from single-cell version

**Effort**: 2-3 days (learning MC structure)

**Risk**: VERY LOW (officially supported)

---

### OPTION C: Downgrade Finland Data

**Approach**: Remove MC-specific technologies/layers from Finland data to match Belgium format

**Steps**:
1. Remove 63 extra layer entries from Finland's `Layers_in_out.csv`
2. Verify all remaining technologies are in Belgium model
3. Manually fix any broken references
4. Test with Belgium model

**Pros**:
- ✅ No model code changes
- ✅ Familiar Belgium model workflow

**Cons**:
- ❌ Lose MC improvements (renewable fuels, H2, biomass pathways)
- ❌ Manual, error-prone data manipulation
- ❌ May break Finland data integrity (missing technologies)
- ❌ Not sustainable (can't easily add more MC countries)
- ⚠️ Risk losing critical Finland-specific technologies

**Effort**: 1-2 days (manual data cleaning + debugging)

**Risk**: HIGH (data corruption, missing technologies)

**NOT RECOMMENDED**

---

### OPTION D: Try Belgium Model First, Upgrade If Needed

**Approach**: Attempt to run Finland data with Belgium model, then upgrade based on actual errors

**Steps**:
1. Try running Belgium `es_model.mod` with Finland data
2. Document all errors and warnings
3. If fails, assess whether to:
   - Fix specific issues in model (quick patches)
   - Do full upgrade to MC (Option A)
   - Switch to MC model (Option B)

**Pros**:
- ✅ Quickest path to understand actual issues
- ✅ May reveal compatibility is better than expected
- ✅ Concrete error list to guide fixes

**Cons**:
- ⏱️ May waste time if model fundamentally incompatible
- 🐛 Risk of subtle bugs that pass but produce wrong results
- 🔄 May need to redo work if full upgrade needed anyway

**Effort**: 0.5 day test + 1-2 days fixes (if feasible)

**Risk**: MEDIUM (may produce incorrect results without obvious errors)

---

## Recommendation

### **Best Approach: Hybrid of A + D**

1. **Phase 1: Test Run** (2-3 hours)
   - Run Belgium model with Finland data
   - Document all errors
   - Assess severity and type of issues

2. **Phase 2: Decision Point**
   - If errors are minor (missing parameters, simple constraints) → **Quick fixes**
   - If errors involve new energy carriers/pathways → **Option A (Upgrade)**
   - If errors are fundamental/numerous → **Option B (Use MC model)**

3. **Phase 3: Implementation**
   - Based on Phase 2 decision
   - Likely outcome: Upgrade single-cell model with MC improvements

### Why This Approach?

- ⚡ Get concrete feedback quickly (test run)
- 🎯 Make informed decision based on actual issues
- 🔧 Avoid over-engineering if compatibility is good
- 📚 Have upgrade path ready if needed

---

## Next Steps (Immediate)

1. **Backup current work** ✅
   ```bash
   git commit -m "Finland data complete, pre-model-test"
   ```

2. **Attempt test run** (10-15 min)
   ```bash
   cd case_studies/ref_run
   # Update ESTD_main.run to point to Data/FI_2017
   # Run preprocessing
   python ../../scripts/run_energyscope.py --config config_fi_2017.yaml
   ```

3. **Document errors** (30 min)
   - Save all error messages
   - Categorize by type (missing tech, undefined layer, constraint violation)
   - Assess whether fixable or needs full upgrade

4. **Make decision** (1 hour)
   - Review error analysis
   - Estimate fix effort vs upgrade effort
   - Choose path forward

5. **Execute chosen path**
   - Option A: 1-2 days upgrade
   - Option B: 2-3 days MC adoption
   - Quick fixes: 0.5-1 day patches

---

## Technical Details for Upgrade (Option A)

**Files to compare**:
- Single: `energyscope/energy_model/es_model.mod` (380 lines)
- MC: `EnergyScope_multi_cells/esmc/energy_model/ESMC_model_AMPL.mod` (551 lines)

**Key differences to port** (preliminary assessment):
1. Renewable fuel balance equations
2. H2 production/storage/transport constraints
3. Biomass feedstock and conversion pathways
4. Split PV (rooftop vs utility scale)
5. Advanced solar (parabolic trough, solar tower)
6. Marine energy (tidal, wave)
7. Multi-modal cargo transport (ammonia, methanol, LFO)

**Testing strategy**:
- Use Belgium 2015 data first (validate no regression)
- Then test with Finland 2017 data
- Compare results with MC model if available

---

## Files for Reference

**Comparison outputs**:
- `Data/extra_finland/MC_vs_SingleCell_Technologies.txt` (detailed tech comparison)
- `Data/extra_finland/layers_extra_technologies.txt` (63 MC-only entries)

**Model files**:
- Single-cell: `energyscope/energy_model/es_model.mod`
- MC: `EnergyScope_multi_cells/esmc/energy_model/ESMC_model_AMPL.mod`
- Finland data: `Data/FI_2017/*.csv`
- Belgium data: `Data/2015/*.csv`

**Preprocessing**:
- Single-cell: `energyscope/preprocessing/es_pre/`
- MC: `EnergyScope_multi_cells/esmc/preprocessing/`

---

## Conclusion

**You are absolutely correct** to check this before running the model! The Finland data (from MC) has 63 additional layers and comes from a model with 45% more code. While technologies match, the Belgium single-cell model may not handle all MC energy carriers and pathways correctly.

**Recommended path**: Test run first (Option D Phase 1), then likely upgrade to MC technology set (Option A) based on errors.

**Timeline**: 
- Test + analysis: 0.5 day
- Upgrade (if needed): 1-2 days
- **Total**: 1.5-2.5 days to production-ready model

**Alternative**: Switch directly to MC model (Option B) - guaranteed compatibility, 2-3 day learning curve.
