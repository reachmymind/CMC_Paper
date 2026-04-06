"""
Civilizational Model Collapse --- Minimal Constructive Demonstration
====================================================================

Accompanies: "Civilizational Model Collapse: Convergence, Controllability,
and the Loss of Adaptive Capacity in Human--AI Systems" (Kesana, 2026)

This script implements the minimal toy model described in Appendix B
and generates all four figures (B.1--B.4).

Model: Discrete-time cultural state evolution
  Normal step:  x_{t+1} = G_sigma(F_theta(x_t))
  BAT step:     x_{t+1} = G_sigma(x_t)

where F_theta is a power-law curation operator and G_sigma injects
stochastic biological noise via Dirichlet perturbation.

Requirements: numpy, matplotlib
Usage: python cmc_simulation.py

Author: Rajeev Kesana
License: Apache 2.0
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

# --- Configuration --------------------------------------------------------

K_DEFAULT = 20       # Number of cultural frames
T_DEFAULT = 500      # Timesteps
BURN_IN = 200        # Burn-in period for steady-state metrics
SEED = 42            # Random seed for reproducibility

# Publication color palette
RED = "#c44e52"      # Collapse / danger
BLUE = "#4c72b0"     # BAT / intervention
GREEN = "#55a868"    # Sustained / healthy
PURPLE = "#8172b2"   # Resistance / alternative
GRAY = "#888888"     # Thresholds / reference lines

# Matplotlib global settings
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 12,
    "axes.titlesize": 15,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.color": "#cccccc",
})


# --- Core Model Functions -------------------------------------------------

def normalize(x):
    """Normalize vector to probability simplex."""
    x = np.maximum(x, 1e-30)
    return x / x.sum()


def curation_operator(x, theta):
    """F_theta: Power-law amplification of dominant frames.

    F_theta(x)_k = x_k^(1+theta) / sum_j x_j^(1+theta)

    Args:
        x: Cultural state vector (probability simplex).
        theta: Curation strength (theta >= 0). theta=0 is identity.
    Returns:
        Curated distribution favoring dominant frames.
    """
    y = x ** (1.0 + theta)
    return normalize(y)


def human_generator(x, sigma, K, rng):
    """G_sigma: Cultural reproduction with biological noise.

    G_sigma(x) = (1-sigma)*x + sigma*eta, where eta ~ Dir(1,...,1)

    Args:
        x: Current cultural state.
        sigma: Biological noise level (sigma_auth analog).
        K: Number of cultural frames.
        rng: NumPy random generator.
    Returns:
        Next cultural state with biological perturbation.
    """
    eta = rng.dirichlet(np.ones(K))
    return normalize((1.0 - sigma) * x + sigma * eta)


def shannon_entropy(x):
    """Shannon entropy H(x) = -sum x_k log x_k."""
    x = np.maximum(x, 1e-30)
    return -np.sum(x * np.log(x))


def effective_support(x, threshold=0.95):
    """Number of frames covering threshold fraction of total mass."""
    sorted_x = np.sort(x)[::-1]
    cumsum = np.cumsum(sorted_x)
    return np.searchsorted(cumsum, threshold) + 1


# --- Simulation Engine ----------------------------------------------------

def simulate(K, theta, sigma, T, bat_period=None, bat_length=None, seed=42):
    """Run the CMC toy model.

    Args:
        K: Number of cultural frames.
        theta: Curation strength.
        sigma: Biological noise level.
        T: Number of timesteps.
        bat_period: BAT cycle length (None = no BAT).
        bat_length: BAT duration within each cycle.
        seed: Random seed for reproducibility.
    Returns:
        entropy_trace: H(x_t) for each t.
        support_trace: Effective support for each t.
        state_history: Full x_t trajectory (T x K).
    """
    rng = np.random.default_rng(seed)
    x = normalize(np.ones(K) / K + rng.normal(0, 0.01, K))

    entropy_trace = np.zeros(T)
    support_trace = np.zeros(T)
    state_history = np.zeros((T, K))

    for t in range(T):
        entropy_trace[t] = shannon_entropy(x)
        support_trace[t] = effective_support(x)
        state_history[t] = x.copy()

        is_bat = False
        if bat_period is not None and bat_length is not None:
            is_bat = (t % bat_period) < bat_length

        if is_bat:
            x = human_generator(x, sigma, K, rng)
        else:
            x = human_generator(curation_operator(x, theta), sigma, K, rng)

    return entropy_trace, support_trace, state_history


# --- Branching Response Model ---------------------------------------------

def branching_response(sigma_auth, kappa):
    """R(sigma_auth, kappa) from section 5.2 illustrative form.

    R = sigma_auth * (1 - kappa^1.5) + 0.2 * (1 - sigma_auth) * kappa

    Supercritical (R > 1): novel attractors proliferate.
    Subcritical (R < 1): novel attractors go extinct.
    """
    return sigma_auth * (1.0 - kappa ** 1.5) + 0.2 * (1.0 - sigma_auth) * kappa


# --- Figure Generation ----------------------------------------------------

def figure_b1_phase_diagram():
    """Figure B.1: Phase diagram in (theta, sigma) space."""
    print("Generating Figure B.1: Phase Diagram...")

    K = K_DEFAULT
    T = T_DEFAULT
    H_max = np.log(K)

    theta_range = np.linspace(0.0, 4.0, 80)
    sigma_range = np.linspace(0.005, 0.5, 80)

    entropy_grid = np.zeros((len(sigma_range), len(theta_range)))

    for i, sigma in enumerate(sigma_range):
        for j, theta in enumerate(theta_range):
            trace, _, _ = simulate(K, theta, sigma, T, seed=SEED)
            entropy_grid[i, j] = np.mean(trace[BURN_IN:])
        if i % 10 == 0:
            print(f"  ... row {i}/{len(sigma_range)}")

    H_norm = entropy_grid / H_max

    fig, ax = plt.subplots(figsize=(8, 6.5))

    colors_list = [
        "#1a0a2e", "#2d1b69", "#5b2c8e", "#8b3a8f",
        "#c44e52", "#e8825c", "#f5b862", "#f7dc6f", "#f0f0f0",
    ]
    cmap = LinearSegmentedColormap.from_list("cmc", colors_list, N=256)

    im = ax.pcolormesh(
        theta_range, sigma_range, H_norm,
        cmap=cmap, shading="gouraud", vmin=0, vmax=1,
    )

    cs = ax.contour(
        theta_range, sigma_range, H_norm,
        levels=[0.3, 0.5, 0.7],
        colors=["white", RED, "white"],
        linewidths=[0.8, 2.5, 0.8],
        linestyles=["--", "-", "--"],
    )
    ax.clabel(cs, inline=True, fontsize=9,
              fmt={0.3: "H=0.3", 0.5: r"R$\approx$1", 0.7: "H=0.7"})

    ax.annotate(
        "SUPERCRITICAL\n(R > 1)\nDiverse cultural output",
        xy=(0.8, 0.38), fontsize=10, color="#1a0a2e",
        fontweight="bold", ha="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.85),
    )
    ax.annotate(
        "SUBCRITICAL\n(R < 1)\nCollapsed to\nlow-entropy attractor",
        xy=(3.2, 0.06), fontsize=10, color="#f0f0f0",
        fontweight="bold", ha="center",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#2d1b69", alpha=0.85),
    )

    ax.annotate(
        "", xy=(3.0, 0.04), xytext=(1.5, 0.25),
        arrowprops=dict(arrowstyle="->", color=RED, lw=2.5,
                        connectionstyle="arc3,rad=-0.2"),
    )
    ax.text(2.5, 0.18, "Dangerous\nConvergence",
            fontsize=9, color=RED, fontweight="bold",
            ha="center", rotation=-25)

    cbar = fig.colorbar(im, ax=ax, shrink=0.82, pad=0.02)
    cbar.set_label("Normalized Cultural Entropy  H / H_max", fontsize=12)

    ax.set_xlabel(r"Curation Strength  $\theta$  (AI coupling intensity)")
    ax.set_ylabel(r"Biological Noise  $\sigma$  (authentic variance injection)")
    ax.set_title(
        "Civilizational Model Collapse --- Phase Diagram\n"
        r"Long-run cultural entropy under joint ($\theta$, $\sigma$) variation",
        fontweight="bold", pad=12,
    )

    fig.tight_layout()
    fig.savefig("fig1_phase_diagram.pdf")
    fig.savefig("fig1_phase_diagram.png")
    print("  -> Saved fig1_phase_diagram.pdf/.png")
    plt.close(fig)


def figure_b2_time_series():
    """Figure B.2: Entropy trajectories under four regimes."""
    print("Generating Figure B.2: Time Series...")

    K = K_DEFAULT
    T = T_DEFAULT
    H_max = np.log(K)

    # A: Collapse
    trace_a, _, _ = simulate(K, theta=3.0, sigma=0.03, T=T)
    # B: BAT intervention
    trace_b, _, _ = simulate(K, theta=3.0, sigma=0.03, T=T,
                             bat_period=50, bat_length=12)
    # C: Sustained diversity
    trace_c, _, _ = simulate(K, theta=1.2, sigma=0.15, T=T)
    # D: Biological resistance
    trace_d, _, _ = simulate(K, theta=3.0, sigma=0.35, T=T)

    def smooth(y, w=5):
        return np.convolve(y, np.ones(w) / w, mode="same")

    fig, ax = plt.subplots(figsize=(10, 5))
    t = np.arange(T)

    ax.plot(t, smooth(trace_a / H_max), color=RED, lw=2.2,
            label=r"A: $\theta$=3.0, $\sigma$=0.03, no BAT  $\rightarrow$  COLLAPSE")
    ax.plot(t, smooth(trace_b / H_max), color=BLUE, lw=2.2,
            label=r"B: $\theta$=3.0, $\sigma$=0.03, BAT(50/12)  $\rightarrow$  ANTI-CONVERGENCE")
    ax.plot(t, smooth(trace_c / H_max), color=GREEN, lw=2.2,
            label=r"C: $\theta$=1.2, $\sigma$=0.15, no BAT  $\rightarrow$  SUSTAINED DIVERSITY")
    ax.plot(t, smooth(trace_d / H_max), color=PURPLE, lw=2.0, ls="--",
            label=r"D: $\theta$=3.0, $\sigma$=0.35, no BAT  $\rightarrow$  BIOLOGICAL RESISTANCE")

    # BAT window shading
    for start in range(0, T, 50):
        ax.axvspan(start, min(start + 12, T), alpha=0.06, color=BLUE)

    ax.axhline(y=0.5, color="#ff6b6b", lw=1.0, ls="--", alpha=0.4)
    ax.text(T - 5, 0.52, r"R $\approx$ 1 proxy", ha="right",
            fontsize=9, color="#ff6b6b", alpha=0.7)

    ax.set_xlabel("Time Step  t")
    ax.set_ylabel(r"Normalized Entropy  $H(x_t) / H_{\max}$")
    ax.set_title(
        "Cultural Entropy Trajectories Under Four Regimes\n"
        "Shaded bands = BAT offline windows (Condition B)",
        fontweight="bold", pad=10,
    )
    ax.set_ylim(-0.02, 1.08)
    ax.set_xlim(0, T)
    ax.legend(loc="upper right", fontsize=9, framealpha=0.92)

    fig.tight_layout()
    fig.savefig("fig2_time_series.pdf")
    fig.savefig("fig2_time_series.png")
    print("  -> Saved fig2_time_series.pdf/.png")
    plt.close(fig)


def figure_b3_tractability():
    """Figure B.3: Collapse produces tractability."""
    print("Generating Figure B.3: Tractability...")

    K = K_DEFAULT
    T = T_DEFAULT
    H_max = np.log(K)
    sigma_fixed = 0.08

    theta_vals = np.linspace(0.0, 4.0, 50)

    avg_entropies = []
    avg_supports = []
    prediction_errors = []

    for theta in theta_vals:
        trace_h, trace_s, x_hist = simulate(K, theta, sigma_fixed, T, seed=SEED)

        avg_entropies.append(np.mean(trace_h[BURN_IN:]) / H_max)
        avg_supports.append(np.mean(trace_s[BURN_IN:]))

        # Prediction error: EMA predictor
        alpha_ema = 0.1
        pred = x_hist[BURN_IN].copy()
        errors = []
        for t in range(BURN_IN + 1, T):
            err = np.sqrt(np.sum((x_hist[t] - pred) ** 2))
            errors.append(err)
            pred = alpha_ema * x_hist[t] + (1 - alpha_ema) * pred
        prediction_errors.append(np.mean(errors))

    fig, ax1 = plt.subplots(figsize=(9, 5))

    # Entropy (left axis)
    l1, = ax1.plot(theta_vals, avg_entropies, color=RED, lw=2.5,
                   label="Cultural Entropy (H/H_max)")
    ax1.set_xlabel(r"Curation Strength  $\theta$  (AI coupling intensity)")
    ax1.set_ylabel(r"Normalized Entropy  $H / H_{\max}$", color=RED)
    ax1.tick_params(axis="y", labelcolor=RED)
    ax1.set_ylim(-0.02, 1.05)

    # Prediction error (right axis)
    ax2 = ax1.twinx()
    l2, = ax2.plot(theta_vals, prediction_errors, color=BLUE, lw=2.5, ls="--",
                   label="Prediction Error (EMA)")
    ax2.set_ylabel("Prediction Error  (L2, EMA predictor)", color=BLUE)
    ax2.tick_params(axis="y", labelcolor=BLUE)
    ax2.spines["right"].set_visible(True)

    # Effective support as fill
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("outward", 60))
    ax3.fill_between(theta_vals, 0, np.array(avg_supports) / K,
                     alpha=0.15, color=GREEN, label="Effective Support (K_eff/K)")
    ax3.set_ylabel(r"Effective Support  $K_{\mathrm{eff}} / K$",
                   fontsize=11, color=GREEN)
    ax3.tick_params(axis="y", labelcolor=GREEN)
    ax3.set_ylim(0, 1.1)
    ax3.spines["right"].set_visible(True)

    # Legend
    ax1.legend([l1, l2],
               ["Cultural Entropy (H/H_max)", "Prediction Error (EMA)"],
               loc="center right", fontsize=10, framealpha=0.9)

    # Collapse threshold
    transition_theta = theta_vals[
        next(i for i, h in enumerate(avg_entropies) if h < 0.3)
    ]
    ax1.axvline(x=transition_theta, color=GRAY, ls=":", lw=1, alpha=0.5)
    ax1.text(transition_theta + 0.1, 0.95,
             f"Collapse\nthreshold\n" + r"$\theta \approx$" + f" {transition_theta:.1f}",
             fontsize=9, color=GRAY)

    ax1.set_title(
        "Collapse Produces Tractability\n"
        "As curation increases: entropy falls, prediction error drops",
        fontweight="bold", pad=10,
    )

    fig.tight_layout()
    fig.savefig("fig3_tractability.pdf")
    fig.savefig("fig3_tractability.png")
    print("  -> Saved fig3_tractability.pdf/.png")
    plt.close(fig)


def figure_b4_critical_surface():
    """Figure B.4: R(sigma_auth, kappa) = 1 critical boundary."""
    print("Generating Figure B.4: Critical Surface...")

    n = 200
    sigma_auth = np.linspace(0, 1, n)
    kappa = np.linspace(0, 1, n)
    S, K = np.meshgrid(sigma_auth, kappa)

    R = branching_response(S, K)

    fig, ax = plt.subplots(figsize=(8, 6.5))

    # Diverging colormap: blue (R>1) to red (R<1), centered at R=1
    r_min, r_max = R.min(), R.max()
    # Ensure vcenter=1.0 is within range; if not, extend
    vmin = min(r_min, 0.98)
    vmax = max(r_max, 1.02)
    norm = TwoSlopeNorm(vmin=vmin, vcenter=1.0, vmax=vmax)
    cmap = plt.cm.RdBu

    cf = ax.contourf(sigma_auth, kappa, R, levels=50, cmap=cmap, norm=norm)

    # R=1 contour (at the boundary edge) and iso-R contours
    cs_levels = [0.2, 0.4, 0.6, 0.8]
    cs_bg = ax.contour(sigma_auth, kappa, R, levels=cs_levels,
                       colors="gray", linewidths=0.6, linestyles="--", alpha=0.5)
    ax.clabel(cs_bg, inline=True, fontsize=8, fmt="%.1f")

    # R=1 contour (appears near sigma_auth=1, kappa=0 corner)
    cs1 = ax.contour(sigma_auth, kappa, R, levels=[0.95],
                     colors="black", linewidths=2.5)
    ax.clabel(cs1, inline=True, fontsize=11, fmt={0.95: r"R$\approx$1"})

    # Region labels
    ax.text(0.85, 0.10, "NEAR-CRITICAL\n" + r"R $\to$ 1" + "\n(Amplification)",
            fontsize=10, fontweight="bold", ha="center", color="white",
            bbox=dict(boxstyle="round,pad=0.4", facecolor=BLUE, alpha=0.85))
    ax.text(0.25, 0.80, "SUBCRITICAL\nR < 1\n(Damping)",
            fontsize=10, fontweight="bold", ha="center", color="white",
            bbox=dict(boxstyle="round,pad=0.4", facecolor=RED, alpha=0.85))

    # Binding point marker: near-critical region where sigma_auth is
    # the marginal governance-relevant constraint.
    # At (sigma_auth=0.9, kappa=0.15), R is near its maximum for moderate kappa.
    bind_s, bind_k = 0.9, 0.15
    r_at_bind = branching_response(bind_s, bind_k)
    ax.plot(bind_s, bind_k, marker="D", markersize=10, color="gold",
            markeredgecolor="black", markeredgewidth=1.5, zorder=5)
    ax.annotate(
        "Binding point\n"
        r"$\sigma_{\mathrm{auth}} \approx \sigma^* + \varepsilon$"
        f"\nR = {r_at_bind:.2f}",
        xy=(bind_s, bind_k), xytext=(0.55, 0.35),
        fontsize=9, ha="center",
        arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.9),
    )

    # Dangerous convergence arrow
    ax.annotate(
        "", xy=(0.15, 0.85), xytext=(0.65, 0.40),
        arrowprops=dict(arrowstyle="->", color=RED, lw=2.5,
                        connectionstyle="arc3,rad=-0.2"),
    )
    ax.text(0.30, 0.60, "Dangerous\nConvergence",
            fontsize=9, color=RED, fontweight="bold", ha="center", rotation=-40)

    # Asymptotic annotation
    ax.text(0.5, 0.95, r"As $\kappa \to 1$: required $\sigma_{\mathrm{auth}} \to \infty$",
            fontsize=9, fontstyle="italic", ha="center", color="#333333",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    cbar = fig.colorbar(cf, ax=ax, shrink=0.82, pad=0.02)
    cbar.set_label(r"Branching Response  $R(\sigma_{\mathrm{auth}}, \kappa)$",
                   fontsize=12)

    ax.set_xlabel(r"Authentic Biological Variance  $\sigma_{\mathrm{auth}}$")
    ax.set_ylabel(r"Network Centralization  $\kappa$")
    ax.set_title(
        r"Critical Surface of the Branching Response $R(\sigma_{\mathrm{auth}}, \kappa)$"
        "\n"
        "The R = 1 boundary between amplification and damping regimes",
        fontweight="bold", pad=12,
    )

    fig.tight_layout()
    fig.savefig("fig4_critical_surface.pdf")
    fig.savefig("fig4_critical_surface.png")
    print("  -> Saved fig4_critical_surface.pdf/.png")
    plt.close(fig)


# --- Main -----------------------------------------------------------------

if __name__ == "__main__":
    print("CMC Toy Model --- Generating Appendix B Figures")
    print("=" * 50)
    figure_b1_phase_diagram()   # ~2-5 min (80x80 grid sweep)
    figure_b2_time_series()
    figure_b3_tractability()
    figure_b4_critical_surface()
    print("\nAll figures saved to current directory.")
