import numpy as np
import matplotlib.pyplot as plt

# 1. Experimental Data (CREMA Collaboration & CODATA)
m_electron = 0.511
r_proton_electron = 0.8751  # Historic CODATA value (uncompressed)

m_muon = 105.66
r_proton_muon = 0.8414      # CREMA muonic hydrogen value (compressed)

# 2. GVS Topological Compression Derivation
delta_r = r_proton_electron - r_proton_muon
delta_m = m_muon - m_electron
kappa = delta_r / delta_m  # GVS Elastic Coupling Constant

lepton_masses = np.linspace(0, 150, 200)

sm_prediction = np.full_like(lepton_masses, r_proton_electron)
gvs_prediction = r_proton_electron - (kappa * lepton_masses)

# 3. PRD-Standard Visualization
plt.figure(figsize=(9, 6))

plt.plot(lepton_masses, sm_prediction, 'k--', linewidth=2, label='Standard Model QED (Invariant Radius)')
plt.plot(lepton_masses, gvs_prediction, 'r-', linewidth=3, label='GVS Prediction (Geometric Compression)')

plt.scatter([m_electron], [r_proton_electron], color='blue', s=100, edgecolor='black', zorder=5,
            label=f'Electron Probe Data ($r_p$ = {r_proton_electron} fm)')
plt.scatter([m_muon], [r_proton_muon], color='purple', s=100, edgecolor='black', zorder=5,
            label=f'Muon Probe Data (CREMA, $r_p$ = {r_proton_muon} fm)')

# Annotations (Adjusted coordinates for cleaner arrows)
plt.annotate(r'Vacuum Stress $\sigma_{vac}$ minimal', xy=(m_electron, r_proton_electron),
             xytext=(m_electron + 5, r_proton_electron + 0.005), fontsize=11,
             arrowprops=dict(facecolor='black', arrowstyle='->', alpha=0.5))

# MOVED TEXT: Shifted slightly up and right to give the arrow breathing room
plt.annotate(r'Vacuum Stress $\sigma_{vac}$ intensely polarizes $l_0^2$ pixels', xy=(m_muon, r_proton_muon),
             xytext=(m_muon - 60, r_proton_muon - 0.008), fontsize=11,
             arrowprops=dict(facecolor='black', arrowstyle='->', alpha=0.5))

# Formatting
plt.title('Micro-Scale Validation: GVS vs. Proton Radius Anomaly', fontsize=14, fontweight='bold')
plt.xlabel(r'Probing Lepton Mass ($MeV/c^2$)', fontsize=12)
plt.ylabel(r'Measured Topological Proton Radius $r_p$ (fm)', fontsize=12)
plt.xlim(-5, 120)
plt.ylim(0.825, 0.890)

plt.grid(True, alpha=0.3, ls='--')

# MOVED LEGEND: Anchored to the empty upper right corner
plt.legend(fontsize=11, loc='upper right', framealpha=0.95)

plt.tight_layout()

# Export for the LaTeX manuscript
plt.savefig('GVS_Micro_Validation.png', dpi=300)
plt.show()
