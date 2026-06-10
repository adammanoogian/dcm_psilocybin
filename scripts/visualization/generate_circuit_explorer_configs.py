#!/usr/bin/env python3
"""Generate DCM Circuit Explorer configs for the psilocybin study main results.

Reads the PEB ``.mat`` outputs in ``data/peb_outputs/`` and serialises them into
the ``dcm_circuit_explorer/v1`` JSON schema consumed by the generic explorer
template (``dcm_pytorch/src/pyro_dcm/utils/templates/dcm_circuit_explorer_template.html``).

Three configs are produced, matching the three requested "setups":

a) ``psilocybin_change.json``       -- only the per-condition change matrices
                                       (post - pre psilocybin, Hz).
b) ``psilocybin_behavioral.json``   -- only the per-condition behavioral-beta
                                       matrices (11D-ASC composite covariate).
c) ``psilocybin_both.json``         -- change and behavioral matrices together.

Each config carries the four poster "main results" as ``hypotheses`` cards. A
card highlights the matrix cells for the connections it discusses (and the
involved region nodes) and shows the result's narrative text.

The connectivity values are taken straight from the PEB ``.mat`` files using the
project's :class:`~plot_PEB_results.PEBDataLoader`, with the same Pp>=0.99
threshold and diagonal reversion the published heatmaps use, so the explorer
matches ``figures/peb_matrices/``.

Usage
-----
    python scripts/visualization/generate_circuit_explorer_configs.py

Outputs land in ``figures/circuit_explorer/`` alongside a copy of the explorer
HTML template (for self-contained viewing). Open the HTML in a browser and use
"Load JSON config" to pick one of the three configs.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "scripts" / "visualization"))

from plot_PEB_results import PEBDataLoader  # noqa: E402

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
PEB_DIR = PROJECT_ROOT / "data" / "peb_outputs"
OUT_DIR = PROJECT_ROOT / "figures" / "circuit_explorer"
TEMPLATE_SRC = (
    PROJECT_ROOT.parent
    / "dcm_pytorch"
    / "src"
    / "pyro_dcm"
    / "utils"
    / "templates"
    / "dcm_circuit_explorer_template.html"
)

# --------------------------------------------------------------------------- #
# Region model (10 ROIs, fixed order matching the PEB matrices)
# --------------------------------------------------------------------------- #
# Anatomical ROI name (as stored in the .mat) -> poster abbreviation.
ROI_ANATOMICAL = [
    "Frontal_Mid_L",
    "Frontal_Mid_R",
    "Hippocampus_L",
    "Hippocampus_R",
    "Occipital_Sup_L",
    "Occipital_Sup_R",
    "Temporal_Mid_L",
    "Temporal_Mid_R",
    "Thalamus_L",
    "Thalamus_R",
]
REGIONS = [
    "ldlPFC",
    "rdlPFC",
    "lHipp",
    "rHipp",
    "lSOG",
    "rSOG",
    "lMTG",
    "rMTG",
    "lThal",
    "rThal",
]
IDX = {name: i for i, name in enumerate(REGIONS)}

# Per-structure colours (L/R share a hue; hemisphere is conveyed by position).
_C_DLPFC, _C_HIPP, _C_SOG, _C_MTG, _C_THAL = (
    "#534AB7",  # dlPFC  - purple
    "#D85A30",  # Hipp   - orange
    "#1D9E75",  # SOG    - green
    "#185FA5",  # MTG    - blue
    "#9A7820",  # Thal   - gold
)
REGION_COLORS = [
    _C_DLPFC, _C_DLPFC,
    _C_HIPP, _C_HIPP,
    _C_SOG, _C_SOG,
    _C_MTG, _C_MTG,
    _C_THAL, _C_THAL,
]

# Bilateral layout: left column x=200, right column x=500; rows ordered
# fronto-occipital. Index order matches REGIONS / ROI order.
_LX, _RX, _R = 200, 500, 34
NODE_POSITIONS = [
    {"cx": _LX, "cy": 95, "r": _R, "role": "dlPFC"},   # 0 ldlPFC
    {"cx": _RX, "cy": 95, "r": _R, "role": "dlPFC"},   # 1 rdlPFC
    {"cx": _LX, "cy": 170, "r": _R, "role": "Hipp"},   # 2 lHipp
    {"cx": _RX, "cy": 170, "r": _R, "role": "Hipp"},   # 3 rHipp
    {"cx": _LX, "cy": 395, "r": _R, "role": "SOG"},    # 4 lSOG
    {"cx": _RX, "cy": 395, "r": _R, "role": "SOG"},    # 5 rSOG
    {"cx": _LX, "cy": 320, "r": _R, "role": "MTG"},    # 6 lMTG
    {"cx": _RX, "cy": 320, "r": _R, "role": "MTG"},    # 7 rMTG
    {"cx": _LX, "cy": 245, "r": _R, "role": "Thal"},   # 8 lThal
    {"cx": _RX, "cy": 245, "r": _R, "role": "Thal"},   # 9 rThal
]

# --------------------------------------------------------------------------- #
# PEB file map  (task -> filename)
# --------------------------------------------------------------------------- #
TASKS = ["rest", "movie", "music", "meditation"]
TASK_LABEL = {
    "rest": "Rest",
    "movie": "Movie",
    "music": "Music",
    "meditation": "Meditation",
}
CHANGE_FILES = {
    t: PEB_DIR / f"PEB_change_-ses-01-ses-02_-task-{t}_cov-_noFD.mat" for t in TASKS
}
_BEHAV_STEM = (
    "PEB_behav_associations_-ses-02_-task-{t}_"
    "cov-ASC11_COMPOSITE_SENSORY_AUDIOVISUAL_COMPLEX_ELEMENTARY_Aconstrained_noFD.mat"
)
BEHAV_FILES = {t: PEB_DIR / _BEHAV_STEM.format(t=t) for t in TASKS}

PP_THRESHOLD = 0.99

# --------------------------------------------------------------------------- #
# Matrix extraction (mirrors PEBPlotter.plot_heatmaps processing)
# --------------------------------------------------------------------------- #


def _reshape(model: dict, roi_n: int):
    """Reshape BMA posterior to (roi_n, roi_n, cov) Ep, Pp and estimated mask."""
    result = PEBDataLoader.reshape_posterior_simple(model, roi_n)
    if len(result) == 4:
        ep, pp, _, estimated = result
    else:
        ep, pp, _ = result
        estimated = None
    return ep, pp, estimated


def extract_change_matrix(path: Path) -> list[list[float]]:
    """Return the post-pre change matrix (Hz) as a (10, 10) list of lists.

    Rows are targets (To), columns are sources (From), matching ``Ep[i, j]`` =
    FROM j TO i. Cells with posterior probability below ``PP_THRESHOLD`` are
    zeroed; the diagonal is reverted exactly as the published heatmaps do.
    """
    loader = PEBDataLoader(str(path), PEBDataLoader.get_peb_plot_parameters())
    data = loader.get_data()
    ep, pp, _ = _reshape(data["model"], len(REGIONS))

    ep[pp < PP_THRESHOLD] = 0.0

    # change-type diagonal reversion (cov 0 = baseline, cov 1 = change).
    d1 = np.diag(ep[:, :, 0]).copy()
    d2 = np.diag(ep[:, :, 1]).copy()
    a2 = ep[:, :, 1].copy()
    np.fill_diagonal(a2, np.exp(d1) / 2 - np.exp(d1 + d2) / 2)
    ep[:, :, 1] = a2

    return _round(ep[:, :, 1])


def extract_behav_matrix(path: Path) -> list[list[float]]:
    """Return the behavioral-beta matrix as a (10, 10) list of lists.

    Covariate 1 is the 11D-ASC composite. Rows are targets, columns sources.
    """
    loader = PEBDataLoader(str(path), PEBDataLoader.get_peb_plot_parameters())
    data = loader.get_data()
    ep, pp, estimated = _reshape(data["model"], len(REGIONS))

    ep[pp < PP_THRESHOLD] = 0.0

    # behav-type diagonal reversion: only estimated, non-zero diagonal cells.
    for i_cov in range(ep.shape[2]):
        a = ep[:, :, i_cov].copy()
        diag = np.diag(a).copy()
        new_diag = diag.copy()
        if estimated is not None and len(estimated[0]) > 0:
            est_diag = {r for r, c in zip(estimated[0], estimated[1]) if r == c}
            for i in range(len(REGIONS)):
                if i in est_diag and diag[i] != 0:
                    new_diag[i] = -np.exp(diag[i]) / 2
        else:
            for i in range(len(REGIONS)):
                if diag[i] != 0:
                    new_diag[i] = -np.exp(diag[i]) / 2
        np.fill_diagonal(a, new_diag)
        ep[:, :, i_cov] = a

    return _round(ep[:, :, 1])


def _round(mat: np.ndarray) -> list[list[float]]:
    """Convert an array to a JSON-friendly rounded list of lists."""
    return [[round(float(v), 4) for v in row] for row in mat]


# --------------------------------------------------------------------------- #
# Poster main results -> hypotheses
# --------------------------------------------------------------------------- #
# Each connection is (source, target); the cell highlighted is [target, source].
RESULTS = [
    {
        "id": "R1",
        "label": "lHipp drives hallucinations",
        "short_desc": "Left hippocampus inhibits sensory cortices + thalamus; predicts symptoms",
        "color": _C_HIPP,
        "nodes": ["lHipp", "rSOG", "rMTG", "rThal", "lThal", "lSOG", "rHipp", "ldlPFC", "rdlPFC"],
        "conns": {
            "rest": [("lHipp", "rSOG"), ("lHipp", "rMTG"), ("lHipp", "rThal")],
            "movie": [
                ("lHipp", "lThal"), ("lHipp", "ldlPFC"),
                ("lHipp", "rdlPFC"), ("lHipp", "lSOG"),
            ],
            "music": [("lHipp", "rHipp")],
            "meditation": [],
        },
        "desc": (
            "Left hippocampal inhibition of sensory regions and thalamus consistently "
            "predicts symptoms, strongest during movie viewing (behavioral beta = 0.20 "
            "for lHipp->lThal). Supports the memory-driven hypothesis: the hippocampus "
            "imposes internally-generated content by suppressing sensory processing."
        ),
    },
    {
        "id": "R2",
        "label": "Inverse thalamic effect",
        "short_desc": "Sensory->thalamus inhibition is protective (challenges gating theory)",
        "color": _C_THAL,
        "nodes": ["lThal", "rThal", "lSOG", "rSOG", "lMTG", "ldlPFC", "rdlPFC", "lHipp"],
        "conns": {
            "rest": [("lSOG", "lThal"), ("lThal", "rdlPFC")],
            "movie": [("lSOG", "lThal"), ("lMTG", "lThal"), ("rThal", "ldlPFC")],
            "music": [("rSOG", "lThal"), ("lMTG", "rThal")],
            "meditation": [("rThal", "lHipp")],
        },
        "desc": (
            "Sensory-driven thalamic inhibition is protective during external "
            "stimulation - more bottom-up thalamic suppression means fewer symptoms "
            "(inverse betas around -0.08). The hippocampus overrides thalamic gating "
            "rather than thalamic dysfunction driving symptoms. Thalamic excitation of "
            "the hippocampus during meditation uniquely correlates with symptoms."
        ),
    },
    {
        "id": "R3",
        "label": "MTG <-> Hipp cross-talk",
        "short_desc": "Direction flips by condition (internal vs external processing)",
        "color": _C_MTG,
        "nodes": ["lHipp", "rHipp", "lMTG", "rMTG"],
        "conns": {
            "rest": [("lHipp", "rMTG"), ("rHipp", "lMTG")],
            "movie": [("rHipp", "rMTG")],
            "music": [("lMTG", "rHipp"), ("rMTG", "rHipp"), ("lHipp", "rMTG")],
            "meditation": [("lHipp", "lMTG"), ("rHipp", "rMTG")],
        },
        "desc": (
            "Bidirectional, condition-dependent coupling. During auditory input (music) "
            "MTG inhibits the hippocampus; at rest the direction reverses and the "
            "hippocampus drives MTG with a lateralized pattern (lHipp inhibits, rHipp "
            "excites). Hallucinations correlate with hippocampal dominance over this circuit."
        ),
    },
    {
        "id": "R4",
        "label": "dlPFC asymmetry",
        "short_desc": "L inhibits, R excites contralateral targets (rest/meditation)",
        "color": _C_DLPFC,
        "nodes": ["ldlPFC", "rdlPFC", "rHipp", "rSOG", "rMTG", "lThal", "lMTG", "rThal"],
        "conns": {
            "rest": [
                ("ldlPFC", "rHipp"), ("ldlPFC", "rSOG"), ("ldlPFC", "rMTG"),
                ("rdlPFC", "rHipp"), ("rdlPFC", "rSOG"), ("rdlPFC", "rMTG"),
                ("rdlPFC", "lThal"), ("rdlPFC", "ldlPFC"),
            ],
            "movie": [
                ("rdlPFC", "ldlPFC"), ("ldlPFC", "rdlPFC"),
                ("ldlPFC", "lMTG"), ("rdlPFC", "rMTG"), ("rdlPFC", "rThal"),
            ],
            "music": [("ldlPFC", "rHipp"), ("rdlPFC", "rHipp")],
            "meditation": [
                ("ldlPFC", "rHipp"), ("ldlPFC", "rSOG"), ("ldlPFC", "rMTG"),
                ("rdlPFC", "rSOG"), ("rdlPFC", "rMTG"), ("rdlPFC", "ldlPFC"),
            ],
        },
        "desc": (
            "During internally-directed states (rest/meditation) the dlPFC shows "
            "lateralized control - left dlPFC inhibits contralateral regions while right "
            "dlPFC excites them. The asymmetry reverses or disappears during external "
            "stimulation. Intact left prefrontal inhibition of the hippocampus "
            "(ldlPFC->rHipp, beta = -0.08) is protective."
        ),
    },
]


def _node_id(region: str) -> str:
    """Match the template's node id derivation: lowercase, alphanumerics only."""
    return "".join(ch for ch in region.lower() if ch.isalnum())


def _cells_for(conns: list[tuple[str, str]]) -> list[list[int]]:
    """Map (source, target) connections to [target_idx, source_idx] cell coords."""
    return [[IDX[tgt], IDX[src]] for src, tgt in conns]


# --------------------------------------------------------------------------- #
# Config assembly
# --------------------------------------------------------------------------- #


def _matrix_entry(label: str, color: str, vals: list[list[float]]) -> dict:
    return {
        "label": label,
        "color": color,
        "vals": vals,
        "note": "rows = target (To), cols = source (From).",
    }


def _base_config(subtitle: str) -> dict:
    return {
        "_schema": "dcm_circuit_explorer/v1",
        "_study": "DCM Psilocybin",
        "_status": "fitted",
        "meta": {
            "title": "Psilocybin DCM Circuit Explorer",
            "subtitle": subtitle,
            "tags": ["10-region", "PEB", "11D-ASC"],
        },
        "regions": REGIONS,
        "region_colors": REGION_COLORS,
        "node_positions": NODE_POSITIONS,
        "svg_edges": [],  # suppress the template's default HEART2ADAPT edges
        "phenotypes": [],
        "drugs": [],
        "fitted_params": None,
    }


def _hypotheses(matrix_keys_for_task: dict[str, list[str]]) -> list[dict]:
    """Build hypothesis cards.

    ``matrix_keys_for_task`` maps a task to the list of matrix keys whose cells
    should be highlighted for that task (e.g. ['Rest'] or ['Rest_chg','Rest_beh']).
    """
    hyps = []
    for res in RESULTS:
        hl_cells: dict[str, list[list[int]]] = {}
        for task, conns in res["conns"].items():
            if not conns:
                continue
            cells = _cells_for(conns)
            for key in matrix_keys_for_task.get(task, []):
                hl_cells.setdefault(key, []).extend(cells)
        hyps.append(
            {
                "id": res["id"],
                "label": res["label"],
                "short_desc": res["short_desc"],
                "color": res["color"],
                "hl_nodes": [_node_id(r) for r in res["nodes"]],
                "hl_edges": [],
                "b_overlays": [],
                "hl_cells": hl_cells,
                "desc": res["desc"],
            }
        )
    return hyps


def build_change_config(change_mats: dict[str, list[list[float]]]) -> dict:
    cfg = _base_config("Connectivity change (post - pre psilocybin, Hz)")
    matrices, mat_order, keys_for_task = {}, [], {}
    for t in TASKS:
        key = TASK_LABEL[t]
        matrices[key] = _matrix_entry(
            f"{key} - delta connectivity (post-pre, Hz)", _C_MTG, change_mats[t]
        )
        mat_order.append(key)
        keys_for_task[t] = [key]
    cfg["matrices"] = matrices
    cfg["mat_order"] = mat_order
    cfg["hypotheses"] = _hypotheses(keys_for_task)
    return cfg


def build_behav_config(behav_mats: dict[str, list[list[float]]]) -> dict:
    cfg = _base_config("Behavioral correlates (11D-ASC composite beta)")
    matrices, mat_order, keys_for_task = {}, [], {}
    for t in TASKS:
        key = TASK_LABEL[t]
        matrices[key] = _matrix_entry(
            f"{key} - behavioral beta (11D-ASC composite)", _C_THAL, behav_mats[t]
        )
        mat_order.append(key)
        keys_for_task[t] = [key]
    cfg["matrices"] = matrices
    cfg["mat_order"] = mat_order
    cfg["hypotheses"] = _hypotheses(keys_for_task)
    return cfg


def build_both_config(
    change_mats: dict[str, list[list[float]]],
    behav_mats: dict[str, list[list[float]]],
) -> dict:
    cfg = _base_config("Connectivity change + behavioral correlates")
    matrices, mat_order, keys_for_task = {}, [], {}
    for t in TASKS:
        ck, bk = f"{TASK_LABEL[t]}_chg", f"{TASK_LABEL[t]}_beh"
        matrices[ck] = _matrix_entry(
            f"{TASK_LABEL[t]} - delta connectivity (Hz)", _C_MTG, change_mats[t]
        )
        matrices[bk] = _matrix_entry(
            f"{TASK_LABEL[t]} - behavioral beta (11D-ASC)", _C_THAL, behav_mats[t]
        )
        mat_order.extend([ck, bk])
        keys_for_task[t] = [ck, bk]
    cfg["matrices"] = matrices
    cfg["mat_order"] = mat_order
    cfg["hypotheses"] = _hypotheses(keys_for_task)
    return cfg


# --------------------------------------------------------------------------- #
# PDF rendering (connectivity matrices only, styled like the explorer grid)
# --------------------------------------------------------------------------- #
_WHITE = np.array([1.0, 1.0, 1.0])


def _cell_rgb(v: float) -> np.ndarray:
    """Explorer ``cellBg`` colour, alpha-blended over white -> solid RGB."""
    if abs(v) < 0.001:
        return np.array([0.953, 0.957, 0.961])  # #F3F4F6
    norm = min(abs(v) / 0.5, 1.0)
    a = 0.15 + norm * 0.58
    base = np.array([29, 158, 117]) / 255 if v > 0 else np.array([216, 90, 48]) / 255
    return a * base + (1 - a) * _WHITE


def _cell_fg(v: float) -> str:
    """Explorer ``cellFg`` text colour."""
    if abs(v) < 0.001:
        return "#9CA3AF"
    if abs(v) / 0.5 > 0.55:
        return "#ffffff"
    return "#0B5E46" if v > 0 else "#8a3015"


def _result_cells(cfg: dict) -> dict[str, set[tuple[int, int]]]:
    """Union of poster-result highlighted cells per matrix key."""
    out: dict[str, set[tuple[int, int]]] = {}
    for hyp in cfg["hypotheses"]:
        for key, cells in hyp["hl_cells"].items():
            out.setdefault(key, set()).update((r, c) for r, c in cells)
    return out


def _draw_matrix(ax, key: str, entry: dict, outline: set[tuple[int, int]]) -> None:
    """Render one connectivity matrix onto ``ax`` in the explorer's style."""
    vals = entry["vals"]
    n = len(vals)
    rgb = np.ones((n, n, 3))
    for r in range(n):
        for c in range(n):
            rgb[r, c] = _cell_rgb(vals[r][c])
    ax.imshow(rgb, aspect="equal")

    for r in range(n):
        for c in range(n):
            v = vals[r][c]
            if abs(v) < 0.001:
                continue
            ax.text(
                c, r, f"{'+' if v > 0 else ''}{v:.2f}",
                ha="center", va="center", fontsize=6.5, color=_cell_fg(v),
            )

    for (r, c) in outline:
        ax.add_patch(
            Rectangle(
                (c - 0.5, r - 0.5), 1, 1, fill=False,
                edgecolor="black", linestyle=(0, (2, 1)), linewidth=1.3,
            )
        )

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(REGIONS, rotation=45, ha="right", fontsize=6)
    ax.set_yticklabels(REGIONS, fontsize=6)
    ax.set_xlabel("From (source)", fontsize=7)
    ax.set_ylabel("To (target)", fontsize=7)
    ax.set_title(entry["label"], fontsize=8, fontweight="bold")
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)


def _build_pages(cfg: dict) -> list:
    """Build one matplotlib figure per page (up to 4 connectivity matrices each)."""
    keys = cfg["mat_order"]
    outline = _result_cells(cfg)
    per_page = 4
    page_groups = [keys[i : i + per_page] for i in range(0, len(keys), per_page)]
    figs = []
    for page_keys in page_groups:
        fig, axes = plt.subplots(2, 2, figsize=(11, 11))
        axes = axes.ravel()
        for ax in axes:
            ax.axis("off")
        for ax, key in zip(axes, page_keys):
            ax.axis("on")
            _draw_matrix(ax, key, cfg["matrices"][key], outline.get(key, set()))
        fig.suptitle(
            cfg["meta"]["subtitle"]
            + "   ·   green = positive, orange = negative; "
            "dashed box = poster main-result connection",
            fontsize=9,
        )
        fig.tight_layout(rect=(0, 0, 1, 0.97))
        figs.append(fig)
    return figs


def render_pdf(cfg: dict, path: Path) -> None:
    """Render a config's connectivity matrices to a multi-page PDF."""
    figs = _build_pages(cfg)
    with PdfPages(path) as pdf:
        for fig in figs:
            pdf.savefig(fig)
    for fig in figs:
        plt.close(fig)


def render_png(cfg: dict, path: Path) -> list[Path]:
    """Render a config's connectivity matrices to PNG(s), one per page.

    Single-page configs write ``<stem>.png``; multi-page configs append the
    page-1 matrix-group name (``_change`` / ``_behavioral``).
    """
    figs = _build_pages(cfg)
    written = []
    if len(figs) == 1:
        figs[0].savefig(path, dpi=200, bbox_inches="tight")
        written.append(path)
    else:
        suffixes = ["_change", "_behavioral"]
        for i, fig in enumerate(figs):
            sfx = suffixes[i] if i < len(suffixes) else f"_p{i + 1}"
            out = path.with_name(path.stem + sfx + ".png")
            fig.savefig(out, dpi=200, bbox_inches="tight")
            written.append(out)
    for fig in figs:
        plt.close(fig)
    return written


# --------------------------------------------------------------------------- #
# Circuit-diagram rendering (nodes + directed edges, the explorer diagram)
# --------------------------------------------------------------------------- #
# Node layout in axis coords (0-1); left column x=0.22, right x=0.78,
# fronto-occipital top->bottom. Keyed by REGIONS index.
CIRCUIT_POS = {
    0: (0.22, 0.92), 1: (0.78, 0.92),   # ldlPFC / rdlPFC
    2: (0.22, 0.72), 3: (0.78, 0.72),   # lHipp / rHipp
    8: (0.22, 0.50), 9: (0.78, 0.50),   # lThal / rThal
    6: (0.22, 0.28), 7: (0.78, 0.28),   # lMTG / rMTG
    4: (0.22, 0.08), 5: (0.78, 0.08),   # lSOG / rSOG
}
_NODE_R = 0.052
_POS_GREEN = "#1D9E75"
_NEG_ORANGE = "#D85A30"


def _draw_circuit(ax, vals: list[list[float]], title: str) -> None:
    """Draw a directed circuit: arrows for every significant off-diagonal cell."""
    n = len(vals)
    # Edges first (under nodes). vals[tgt][src] = FROM src TO tgt.
    for tgt in range(n):
        for src in range(n):
            if tgt == src:
                continue
            v = vals[tgt][src]
            if abs(v) < 0.001:
                continue
            x0, y0 = CIRCUIT_POS[src]
            x1, y1 = CIRCUIT_POS[tgt]
            color = _POS_GREEN if v > 0 else _NEG_ORANGE
            lw = 0.8 + 3.4 * min(abs(v) / 0.3, 1.0)
            rad = 0.16 if x0 <= x1 else -0.16
            ax.add_patch(
                FancyArrowPatch(
                    (x0, y0), (x1, y1),
                    connectionstyle=f"arc3,rad={rad}",
                    arrowstyle="-|>", mutation_scale=11,
                    lw=lw, color=color, alpha=0.7,
                    shrinkA=15, shrinkB=15, zorder=1,
                )
            )
    # Nodes on top.
    for i in range(n):
        x, y = CIRCUIT_POS[i]
        col = REGION_COLORS[i]
        ax.add_patch(Circle((x, y), _NODE_R, facecolor="white",
                            edgecolor=col, lw=2.0, zorder=2))
        ax.text(x, y, REGIONS[i], ha="center", va="center",
                fontsize=7.5, fontweight="bold", color=col, zorder=3)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=10, fontweight="bold")


def render_circuit_png(
    mats: dict[str, list[list[float]]], subtitle: str, path: Path
) -> None:
    """Render the four per-condition circuit diagrams as one 2x2 PNG."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes = axes.ravel()
    for ax, t in zip(axes, TASKS):
        _draw_circuit(ax, mats[t], TASK_LABEL[t])
    fig.suptitle(
        subtitle + "    (arrow = FROM -> TO;  green = excitatory, "
        "orange = inhibitory;  width proportional to magnitude)",
        fontsize=11, y=0.98,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def _verify(name: str, cfg: dict) -> None:
    """Print a sanity report: how many highlighted cells are non-zero."""
    mats = cfg["matrices"]
    total = hit = 0
    for hyp in cfg["hypotheses"]:
        for key, cells in hyp["hl_cells"].items():
            vals = mats[key]["vals"]
            for r, c in cells:
                total += 1
                if abs(vals[r][c]) > 0.001:
                    hit += 1
    print(f"  [{name}] highlighted cells with non-zero value: {hit}/{total}")


def main() -> None:
    """Extract PEB matrices and write the three explorer configs."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Extracting change matrices...")
    change_mats = {t: extract_change_matrix(CHANGE_FILES[t]) for t in TASKS}
    print("Extracting behavioral matrices...")
    behav_mats = {t: extract_behav_matrix(BEHAV_FILES[t]) for t in TASKS}

    configs = {
        "psilocybin_change.json": build_change_config(change_mats),
        "psilocybin_behavioral.json": build_behav_config(behav_mats),
        "psilocybin_both.json": build_both_config(change_mats, behav_mats),
    }

    print("\nWriting configs + PDFs:")
    for fname, cfg in configs.items():
        path = OUT_DIR / fname
        path.write_text(json.dumps(cfg, indent=2))
        print(f"  {path}")
        _verify(fname, cfg)
        pdf_path = path.with_suffix(".pdf")
        render_pdf(cfg, pdf_path)
        print(f"  {pdf_path}")
        for png in render_png(cfg, path.with_suffix(".png")):
            print(f"  {png}")

    print("\nWriting circuit diagrams:")
    circuit_specs = [
        (change_mats, "Connectivity change (post - pre psilocybin, Hz)",
         OUT_DIR / "psilocybin_change_circuit.png"),
        (behav_mats, "Behavioral correlates (11D-ASC composite beta)",
         OUT_DIR / "psilocybin_behavioral_circuit.png"),
    ]
    for mats, subtitle, cpath in circuit_specs:
        render_circuit_png(mats, subtitle, cpath)
        print(f"  {cpath}")

    # Copy the explorer template alongside for self-contained viewing.
    if TEMPLATE_SRC.exists():
        dest = OUT_DIR / "dcm_circuit_explorer.html"
        shutil.copyfile(TEMPLATE_SRC, dest)
        print(f"\nTemplate copied to: {dest}")
    else:
        print(f"\nWARNING: template not found at {TEMPLATE_SRC}")

    print("\nDone. Open dcm_circuit_explorer.html and 'Load JSON config'.")


if __name__ == "__main__":
    main()
