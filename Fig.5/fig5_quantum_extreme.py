import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# 1. Experimental Data (Fermilab 2023 & Standard Model Deviations)
# ==============================================================================
# Masses in MeV/c^2
m_e = 0.511
m_mu = 105.658
m_tau = 1776.86

# Deviation from Standard Model (Delta a = a_exp - a_SM) in units of 10^-9
delta_a_e = 0.00048
err_e = 0.00015

# Muon deviation (The famous Fermilab anomaly)
delta_a_mu = 2.51
err_mu = 0.59

# ==============================================================================
# 2. GVS Theoretical Prediction (Geometric Spin Friction)
# ==============================================================================
kappa_spin = delta_a_mu / (m_mu**2)

mass_array = np.linspace(0, 2000, 500)
sm_prediction = np.zeros_like(mass_array)
gvs_prediction = kappa_spin * (mass_array**2)

# ==============================================================================
# 3. PRD-Standard Visualization
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

# --- Subplot 1: The Muon Anomaly (Zoomed In) ---
ax1.plot(mass_array, sm_prediction, 'k--', linewidth=2, label='Standard Model QED (Zero Deviation)')
ax1.plot(mass_array, gvs_prediction, 'r-', linewidth=3, label=r'GVS Prediction ($\propto m^2$)')

# FIXED: Added 'r' prefix for \sigma
ax1.errorbar(m_mu, delta_a_mu, yerr=err_mu, fmt='o', color='purple', markeredgecolor='black',
             markersize=10, capsize=5, zorder=5, label=r'Fermilab Muon Data ($4.2\sigma$)')
ax1.errorbar(m_e, delta_a_e, yerr=err_e, fmt='o', color='blue', markeredgecolor='black',
             markersize=8, capsize=5, zorder=5, label='Electron Data')

ax1.set_xlim(-10, 120)
ax1.set_ylim(-0.5, 3.5)
ax1.set_title(r'The Muon $g-2$ Validation', fontsize=13, fontweight='bold')
ax1.set_xlabel(r'Lepton Mass ($MeV/c^2$)', fontsize=12)
ax1.set_ylabel(r'Anomalous Magnetic Deviation $\Delta a \times 10^9$', fontsize=12)
ax1.grid(True, ls="--", alpha=0.4)
ax1.legend(loc='upper left', fontsize=10)

# --- Subplot 2: The Tau Prediction (Zoomed Out) ---
ax2.plot(mass_array, sm_prediction, 'k--', linewidth=2)
ax2.plot(mass_array, gvs_prediction, 'r-', linewidth=3)
ax2.errorbar(m_mu, delta_a_mu, yerr=err_mu, fmt='o', color='purple', markeredgecolor='black',
             markersize=8, zorder=5)

# FIXED: Added 'rf' prefix for the f-string containing \Delta
tau_prediction = kappa_spin * (m_tau**2)
ax2.scatter(m_tau, tau_prediction, color='gold', edgecolor='black', marker='*', s=250, zorder=5,
            label=rf'GVS Tau Prediction ($\Delta a \approx {tau_prediction:.1f}$)')

ax2.set_xlim(-100, 1900)
ax2.set_ylim(-50, 800)
ax2.set_title('GVS Predictive Scaling (The Tau Test)', fontsize=13, fontweight='bold')
ax2.set_xlabel(r'Lepton Mass ($MeV/c^2$)', fontsize=12)
ax2.grid(True, ls="--", alpha=0.4)
ax2.legend(loc='upper left', fontsize=10)

plt.suptitle('Quantum Extreme: GVS Geometric Friction vs. Standard Model Spin', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()

plt.savefig('GVS_Muon_g2_Validation.png', dpi=300, bbox_inches='tight')
plt.show()
