"""
Critical Investigation: MC vs Single-Cell Model Compatibility

Question: Can the Belgium single-cell AMPL model handle Finland data from MC version?
Approach: Compare technology and layer sets between versions.
"""

import pandas as pd
from pathlib import Path

def compare_model_versions():
    """Compare Belgium single-cell vs Finland (MC) technology and layer sets."""
    
    print("="*80)
    print("CRITICAL COMPATIBILITY CHECK: MC vs SINGLE-CELL MODEL")
    print("="*80)
    print("\nContext:")
    print("  - Finland data extracted from MULTI-CELL (MC) version")
    print("  - Belgium model is SINGLE-CELL version")
    print("  - MC likely has newer/more technologies")
    print("  - Must verify compatibility before model run!")
    
    # 1. Compare Technologies.csv
    print("\n" + "="*80)
    print("1. TECHNOLOGIES COMPARISON")
    print("="*80)
    
    # Belgium single-cell
    be_tech = pd.read_csv("Data/2015/Technologies.csv", sep=';', skiprows=2)
    be_tech_names = set(be_tech.iloc[:, 3].dropna().str.strip())
    print(f"\nBelgium single-cell (2015): {len(be_tech_names)} technologies")
    
    # Finland from MC
    fi_tech = pd.read_csv("Data/FI_2017/Technologies.csv", sep=';', skiprows=2)
    fi_tech_names = set(fi_tech.iloc[:, 3].dropna().str.strip())
    print(f"Finland from MC (2017):     {len(fi_tech_names)} technologies")
    
    # Differences
    common_tech = be_tech_names & fi_tech_names
    fi_only = fi_tech_names - be_tech_names
    be_only = be_tech_names - fi_tech_names
    
    print(f"\nCommon technologies:        {len(common_tech)}")
    print(f"Finland-only (MC additions): {len(fi_only)}")
    print(f"Belgium-only (deprecated):   {len(be_only)}")
    
    if fi_only:
        print(f"\n{'='*80}")
        print(f"FINLAND-ONLY TECHNOLOGIES (from MC, not in Belgium model):")
        print(f"{'='*80}")
        for i, tech in enumerate(sorted(fi_only), 1):
            print(f"{i:3d}. {tech}")
    
    if be_only:
        print(f"\n{'='*80}")
        print(f"BELGIUM-ONLY TECHNOLOGIES (may be deprecated in MC):")
        print(f"{'='*80}")
        for i, tech in enumerate(sorted(be_only), 1):
            print(f"{i:3d}. {tech}")
    
    # 2. Compare Layers_in_out.csv
    print("\n" + "="*80)
    print("2. LAYERS_IN_OUT COMPARISON")
    print("="*80)
    
    # Belgium
    be_layers = pd.read_csv("Data/2015/Layers_in_out.csv", sep=';')
    be_layers_names = set(be_layers.iloc[:, 0].dropna().str.strip())
    print(f"\nBelgium single-cell (2015): {len(be_layers_names)} entries")
    
    # Finland
    fi_layers = pd.read_csv("Data/FI_2017/Layers_in_out.csv", sep=';')
    fi_layers_names = set(fi_layers.iloc[:, 0].dropna().str.strip())
    print(f"Finland from MC (2017):     {len(fi_layers_names)} entries")
    
    # Differences
    common_layers = be_layers_names & fi_layers_names
    fi_layers_only = fi_layers_names - be_layers_names
    be_layers_only = be_layers_names - fi_layers_names
    
    print(f"\nCommon entries:             {len(common_layers)}")
    print(f"Finland-only (MC):          {len(fi_layers_only)}")
    print(f"Belgium-only:               {len(be_layers_only)}")
    
    if fi_layers_only:
        print(f"\n{'='*80}")
        print(f"FINLAND-ONLY LAYERS (from MC, not in Belgium):")
        print(f"{'='*80}")
        # Categorize by type
        resources = [l for l in fi_layers_only if any(x in l for x in ['COAL', 'GAS', 'OIL', 'URANIUM', 'WOOD', 'WASTE', 'BIOMASS'])]
        layers = [l for l in fi_layers_only if any(x in l for x in ['ELECTRICITY', 'H2', 'HEAT', 'AMMONIA', 'METHANOL', 'DIESEL', 'GASOLINE', 'JET_FUEL', 'LFO'])]
        techs = [l for l in fi_layers_only if l not in resources and l not in layers]
        
        if resources:
            print(f"\nResources ({len(resources)}):")
            for r in sorted(resources):
                print(f"  - {r}")
        if layers:
            print(f"\nEnergy carriers/Layers ({len(layers)}):")
            for l in sorted(layers):
                print(f"  - {l}")
        if techs:
            print(f"\nTechnologies ({len(techs)}):")
            for t in sorted(techs)[:20]:  # First 20 only
                print(f"  - {t}")
            if len(techs) > 20:
                print(f"  ... and {len(techs)-20} more")
    
    # 3. Risk Assessment
    print("\n" + "="*80)
    print("3. COMPATIBILITY RISK ASSESSMENT")
    print("="*80)
    
    risk_level = "LOW"
    if len(fi_only) > 10:
        risk_level = "HIGH"
    elif len(fi_only) > 5:
        risk_level = "MEDIUM"
    
    print(f"\nRisk Level: {risk_level}")
    print(f"\nReasons:")
    print(f"  - {len(fi_only)} technologies in Finland data not in Belgium model")
    print(f"  - {len(fi_layers_only)} layer entries in Finland data not in Belgium")
    
    if risk_level == "HIGH":
        print(f"\n  ⚠️ HIGH RISK: Model will likely fail with 'undefined technology' errors")
        print(f"  ⚠️ Belgium AMPL model code needs updating to handle MC technologies")
    
    # 4. Recommendations
    print("\n" + "="*80)
    print("4. RECOMMENDATIONS")
    print("="*80)
    
    print(f"\n{'OPTION A: Upgrade Single-Cell Model (RECOMMENDED)'}")
    print("  Pros:")
    print("    + Keep Finland data as-is (more technologies = more flexibility)")
    print("    + MC version is newer, likely better technology definitions")
    print("    + Future-proof: easier to add more countries from MC")
    print("  Cons:")
    print("    - Need to adapt AMPL model code (es_model.mod)")
    print("    - More complex model with more technologies")
    print("  Effort: Medium (adapt model structure)")
    
    print(f"\n{'OPTION B: Downgrade Finland Data'}")
    print("  Pros:")
    print("    + No model code changes needed")
    print("    + Simpler, proven Belgium model")
    print("  Cons:")
    print("    - Lose MC technology improvements")
    print("    - Manual data manipulation (error-prone)")
    print("    - May miss important Finland-specific technologies")
    print("  Effort: Medium-High (manual data cleaning)")
    
    print(f"\n{'OPTION C: Use MC Model Directly'}")
    print("  Pros:")
    print("    + Guaranteed compatibility (MC model + MC data)")
    print("    + Most modern codebase")
    print("  Cons:")
    print("    - Multi-cell complexity (may be overkill for single country)")
    print("    - Different model structure to learn")
    print("  Effort: Low (just use MC version)")
    
    print("\n" + "="*80)
    print("RECOMMENDATION:")
    print("="*80)
    print("\nBest approach: OPTION A - Upgrade single-cell model to MC technology set")
    print("\nRationale:")
    print("  1. Keep benefits of single-cell model (simpler than full MC)")
    print("  2. Leverage MC's improved technology definitions")
    print("  3. MC model code can guide the upgrade (reference implementation)")
    print("  4. More maintainable long-term")
    
    print("\nNext steps:")
    print("  1. Review MC model structure (esmc/ folder)")
    print("  2. Identify key differences in AMPL code")
    print("  3. Update es_model.mod to handle MC technology set")
    print("  4. Test with Finland data")
    
    # Export detailed lists
    print("\n" + "="*80)
    print("EXPORTING DETAILED COMPARISON")
    print("="*80)
    
    output_dir = Path("Data/extra_finland")
    
    with open(output_dir / "MC_vs_SingleCell_Technologies.txt", 'w') as f:
        f.write("MC vs SINGLE-CELL TECHNOLOGY COMPARISON\n")
        f.write("="*80 + "\n\n")
        f.write(f"Belgium single-cell: {len(be_tech_names)} technologies\n")
        f.write(f"Finland from MC:     {len(fi_tech_names)} technologies\n")
        f.write(f"Common:              {len(common_tech)}\n")
        f.write(f"Finland-only (MC):   {len(fi_only)}\n")
        f.write(f"Belgium-only:        {len(be_only)}\n\n")
        
        f.write("FINLAND-ONLY (MC additions):\n")
        f.write("-"*80 + "\n")
        for tech in sorted(fi_only):
            f.write(f"{tech}\n")
        
        f.write("\n" + "="*80 + "\n\n")
        f.write("BELGIUM-ONLY (potentially deprecated in MC):\n")
        f.write("-"*80 + "\n")
        for tech in sorted(be_only):
            f.write(f"{tech}\n")
    
    print(f"  ✓ MC_vs_SingleCell_Technologies.txt")
    print(f"\n  Files saved to: {output_dir}/")
    
    return {
        'tech_fi_only': fi_only,
        'tech_be_only': be_only,
        'layers_fi_only': fi_layers_only,
        'layers_be_only': be_layers_only,
        'risk_level': risk_level
    }

if __name__ == "__main__":
    results = compare_model_versions()
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\nCompatibility Risk: {results['risk_level']}")
    print(f"MC-only technologies: {len(results['tech_fi_only'])}")
    print(f"MC-only layer entries: {len(results['layers_fi_only'])}")
    
    if results['risk_level'] in ['HIGH', 'MEDIUM']:
        print("\n⚠️  ACTION REQUIRED: Cannot run Belgium model with Finland data as-is")
        print("    Recommend upgrading single-cell model to MC technology set")
