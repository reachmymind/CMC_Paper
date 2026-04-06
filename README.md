# Civilizational Model Collapse

**Convergence, Controllability, and the Loss of Adaptive Capacity in Human--AI Systems**

Rajeev Kesana (Independent Researcher, Hyderabad, India)
with direct AI collaboration from Claude (Anthropic) and Grok (xAI)
Adversarial peer review by ChatGPT (OpenAI), Gemini (Google DeepMind), and Claude (Anthropic)

April 2026

## Abstract

Current AI risk is often framed as an external prediction or control problem. We argue that a more immediate threat is Civilizational Model Collapse (CMC) --- the recursive convergence of a coupled human--AI system toward a low-entropy attractor in which human outputs are progressively filtered to match prior AI expectations, eliminating out-of-distribution novelty.

## Repository Contents

- `main.tex` --- Full paper source (LaTeX)
- `references.bib` --- Bibliography (16 entries)
- `cmc_simulation.py` --- Minimal constructive model (Appendix A simulations, figs 1--4)
- `fig5_gamma_phase.py` --- Phase diagram generator (Fig 5)
- `fig[1-5]*.pdf` --- Pre-rendered figures

## Build

```bash
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## License

CC BY 4.0
