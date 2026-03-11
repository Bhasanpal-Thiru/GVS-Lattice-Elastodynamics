import os
import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# 1. Fundamental Constants & SPARC Parameters
# ==============================================================================
G_grav_kpc = 4.30091e-6    # Newton's G in (kpc * (km/s)^2) / M_sun
G_standard = 6.67430e-11   # Standard G in m^3 kg^-1 s^-2
M_sun = 1.989e30           # Solar Mass in kg
a_0 = 1.2e-10              # GVS Vacuum Stress Limit in m/s^2

# Standard SPARC Mass-to-Light Ratios (at 3.6 microns)
Upsilon_disk = 0.5
Upsilon_bulge = 0.7

# ==============================================================================
# 2. Parse the SPARC Database
# ==============================================================================
sparc_folder = 'SPARC_Data' # Update this if your folder name is different
sparc_masses = []
sparc_velocities = []

for filename in os.listdir(sparc_folder):
    if filename.endswith(".dat"):
        filepath = os.path.join(sparc_folder, filename)

        try:
            # SPARC .dat columns: Rad, Vobs, errV, Vgas, Vdisk, Vbul
            data = np.loadtxt(filepath)
            if len(data) == 0: continue

            # Use the outermost data point to represent the flat rotation velocity (V_f)
            R_out = data[-1, 0]    # Radius in kpc
            V_obs = data[-1, 1]    # Observed Velocity in km/s

            V_gas = data[-1, 3]
            V_disk = data[-1, 4]
            V_bulge = data[-1, 5]

            # Calculate Baryonic Mass (M_b)
            # Newtonian Velocity formula: V^2 = GM/R --> M = (V^2 * R) / G
            # Note: V_gas can sometimes be negative in raw data to represent
            # net outward forces, so we use V_gas * abs(V_gas)
            M_gas = (V_gas * abs(V_gas) * R_out) / G_grav_kpc
            M_disk = Upsilon_disk * (V_disk**2 * R_out) / G_grav_kpc
            M_bulge = Upsilon_bulge * (V_bulge**2 * R_out) / G_grav_kpc

            M_baryon_total = M_gas + M_disk + M_bulge

            # Filter out bad data flags (e.g., negative total mass or zero velocity)
            if M_baryon_total > 0 and V_obs > 0:
                sparc_masses.append(M_baryon_total)
                sparc_velocities.append(V_obs)

        except Exception as e:
            # Skip files with formatting issues
            pass

# ==============================================================================
# 3. GVS Theoretical Prediction
# ==============================================================================
# Theoretical Derivation: V_f = (G * M_b * a_0)^(1/4)
mass_array = np.logspace(7, 12, 100)
v_theoretical = ((G_standard * (mass_array * M_sun) * a_0)**0.25) / 1000 # Convert to km/s

# ==============================================================================
# 4. PRD-Standard Visualization
# ==============================================================================
plt.figure(figsize=(10, 6))

# Plot the exact GVS mathematical derivation
plt.plot(mass_array, v_theoretical, color='red', linewidth=3, zorder=5,
         label=r'GVS Prediction: $V_f = \sqrt[4]{G M_b a_0}$')

# Plot the extracted SPARC experimental data
plt.scatter(sparc_masses, sparc_velocities, color='steelblue', edgecolor='black',
            s=45, alpha=0.7, zorder=3, label=f'SPARC Data (n={len(sparc_masses)} Galaxies)')

# Formatting
plt.xscale('log')
plt.yscale('log')
plt.title('Macro-Scale Validation: GVS vs. SPARC Dataset', fontsize=15, fontweight='bold')
plt.xlabel(r'Visible Baryonic Mass $M_b$ ($M_\odot$)', fontsize=13)
plt.ylabel(r'Flat Rotation Velocity $V_f$ (km/s)', fontsize=13)

# Add grid and legend
plt.grid(True, which="major", ls="-", alpha=0.4)
plt.grid(True, which="minor", ls="--", alpha=0.1)
plt.legend(fontsize=12, loc='upper left')
plt.tight_layout()

# Export for the LaTeX manuscript
plt.savefig('GVS_SPARC_Validation.png', dpi=300)
print(f"Successfully processed {len(sparc_masses)} galaxies and saved the plot.")
plt.show()
