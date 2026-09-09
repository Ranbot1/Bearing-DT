# Generated-artifact retention policy

Reproduction claims must be auditable from repository artifacts, not only from Markdown summaries.

For every accepted physics / signal-processing milestone, the **generation script** must produce:

- exact config snapshot and runtime overrides;
- full generated twin arrays (NPZ);
- a compact, text-inspectable signal export;
- spectra / feature tables used to obtain reported numbers;
- signal-processing figures in SVG and PNG;
- per-class metrics;
- provenance manifest and SHA-256 values.

For the **fixed Git snapshot**, retain enough text/visual evidence for direct inspection while keeping repository history manageable. Full binary NPZ files may stay reproducible rather than versioned in every commit, but their generation-side hashes must be recorded.

Current fixed snapshot:
- [20260909_6203_r1r2](audit_snapshots/20260909_6203_r1r2/README.md)

The builder is:
- [scripts/06_build_audit_snapshot.py](../scripts/06_build_audit_snapshot.py)
