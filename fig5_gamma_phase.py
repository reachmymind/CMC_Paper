"""
Collapse Trichotomy Phase Diagram
gamma = sigma_auth / (1 - L) vs R(sigma_auth, kappa)

Schematic diagram showing three civilizational regimes:
  Sanctuary (high gamma, R > 1)
  Collapse (low gamma, R < 1, C4 holds)
  Capture (very low gamma, R << 1, not C4)

For: "Civilizational Model Collapse" (Kesana, 2026), Figure 5
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 13,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

fig, ax = plt.subplots(figsize=(9, 7))

# --- Background gradient for the three regimes ---
nx, ny = 300, 300
gamma_range = np.linspace(0, 3.0, nx)
R_range = np.linspace(0, 1.8, ny)
G, R = np.meshgrid(gamma_range, R_range)

gamma_crit = 0.8
gamma_capture = 0.3
R_capture = 0.4

regime = np.zeros((ny, nx, 4))

for i in range(ny):
    for j in range(nx):
        g = gamma_range[j]
        r = R_range[i]

        if r > 1.0:
            intensity = min(1.0, (r - 1.0) / 0.8)
            alpha = 0.15 + 0.25 * intensity
            regime[i, j] = [0.20, 0.38, 0.65, alpha]
        elif g < gamma_capture and r < R_capture:
            intensity = (1 - g / gamma_capture) * (1 - r / R_capture)
            alpha = 0.15 + 0.35 * min(1.0, intensity)
            regime[i, j] = [0.60, 0.15, 0.15, alpha]
        else:
            g_factor = max(0, 1 - g / 2.0)
            r_factor = max(0, 1 - r / 1.0)
            intensity = g_factor * r_factor
            alpha = 0.08 + 0.25 * intensity
            regime[i, j] = [0.85, 0.55, 0.15, alpha]

ax.imshow(regime, extent=[0, 3.0, 0, 1.8], origin='lower', aspect='auto', zorder=0)

# --- Critical boundaries ---
ax.axhline(y=1.0, color='#2d5ba0', lw=2.5, ls='-', alpha=0.9, zorder=3)
ax.text(2.85, 1.04, 'R = 1', fontsize=11, color='#2d5ba0',
        fontweight='bold', ha='right', va='bottom')

ax.axvline(x=gamma_crit, color='#c44e52', lw=1.5, ls='--', alpha=0.5, zorder=2)
ax.text(gamma_crit + 0.03, 1.72, r'$\gamma_{\mathrm{crit}}$', fontsize=12,
        color='#c44e52', fontweight='bold', va='top')

# C4 failure boundary
c4_gamma = np.linspace(0.01, 0.8, 100)
c4_R = R_capture * np.exp(-2.0 * (c4_gamma - gamma_capture))
c4_R = np.clip(c4_R, 0, 0.9)
mask = c4_R < 0.85
ax.plot(c4_gamma[mask], c4_R[mask], color='#8b1a1a', lw=2.0, ls=':', alpha=0.7, zorder=3)
ax.text(0.55, 0.62, 'C4 boundary', fontsize=9, color='#8b1a1a',
        fontstyle='italic', rotation=-35, alpha=0.8)

# --- Regime labels ---
ax.text(2.0, 1.40, 'SANCTUARY', fontsize=16, fontweight='bold',
        color='#1a3a6e', ha='center', va='center', zorder=5,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9,
                  edgecolor='#2d5ba0', linewidth=1.5))
ax.text(2.0, 1.24, r'High $\gamma$, R > 1' + '\nGenerative Sovereignty',
        fontsize=9, color='#1a3a6e', ha='center', va='top', zorder=5)

ax.text(1.8, 0.55, 'COLLAPSE', fontsize=16, fontweight='bold',
        color='#7a4a00', ha='center', va='center', zorder=5,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.9,
                  edgecolor='#c48800', linewidth=1.5))
ax.text(1.8, 0.39, r'Low $\gamma$, C4 holds' + '\nSteerable Circuit',
        fontsize=9, color='#7a4a00', ha='center', va='top', zorder=5)

ax.text(0.22, 0.16, 'CAPTURE', fontsize=14, fontweight='bold',
        color='#f0e0e0', ha='center', va='center', zorder=5,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#4a1010', alpha=0.9,
                  edgecolor='#8b1a1a', linewidth=1.5))
ax.text(0.22, 0.04, r'$\gamma \to 0$, $\neg$C4' + '\nFixed-Point Stagnation',
        fontsize=8, color='#8b1a1a', ha='center', va='bottom',
        fontstyle='italic', zorder=5)

# --- Dynamic arrows ---
# Optimization pressure: Sanctuary -> Collapse
ax.annotate('', xy=(0.6, 0.7), xytext=(2.2, 1.35),
            arrowprops=dict(arrowstyle='->', color='#c44e52', lw=2.5,
                           connectionstyle='arc3,rad=-0.15'),
            zorder=4)
ax.text(1.15, 1.18, 'Optimization\npressure', fontsize=9, color='#c44e52',
        fontweight='bold', ha='center', rotation=-30, zorder=5,
        fontstyle='italic')

# Self-reinforcing feedback: Collapse -> Capture
ax.annotate('', xy=(0.35, 0.35), xytext=(0.7, 0.65),
            arrowprops=dict(arrowstyle='->', color='#8b1a1a', lw=2.0,
                           connectionstyle='arc3,rad=-0.3'),
            zorder=4)
ax.text(0.30, 0.55, r'$L \uparrow \Rightarrow \gamma \downarrow$' + '\n(self-reinforcing)',
        fontsize=8, color='#8b1a1a', ha='center', zorder=5,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

# BAT intervention: Collapse -> Sanctuary
ax.annotate('', xy=(1.3, 1.05), xytext=(0.8, 0.55),
            arrowprops=dict(arrowstyle='->', color='#2d8b6e', lw=2.5,
                           connectionstyle='arc3,rad=0.2'),
            zorder=4)
ax.text(0.75, 0.85, 'BAT\nintervention', fontsize=9, color='#2d8b6e',
        fontweight='bold', ha='center', zorder=5,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85))

# --- Axes ---
ax.set_xlabel(r'Safety Parameter  $\gamma = \sigma_{\mathrm{auth}} \,/\, (1 - L)$',
              fontsize=13, fontweight='bold')
ax.set_ylabel(r'Branching Response  $R(\sigma_{\mathrm{auth}}, \kappa)$',
              fontsize=13, fontweight='bold')
ax.set_title(
    r'Phase Diagram of the Collapse Trichotomy' + '\n'
    r'Civilizational regimes governed by $\gamma$ and $R$',
    fontsize=14, fontweight='bold', pad=15)
ax.set_xlim(0, 3.0)
ax.set_ylim(0, 1.8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.tight_layout()
fig.savefig('fig5_gamma_phase_diagram.pdf', dpi=300)
fig.savefig('fig5_gamma_phase_diagram.png', dpi=300)
print("Saved fig5_gamma_phase_diagram.pdf/.png")
plt.close(fig)
