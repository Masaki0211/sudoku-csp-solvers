"""Turn experiments/results/*.csv into the tables and figures used in the slides.

Owner: Masaki Kajikuri

Usage (from the repository root):
    python experiments/analyze.py

Writes to experiments/results/:
    summary_by_band.csv   median nodes / backtracks / seconds and completion per solver and band
    summary_overall.csv   the same over all 500 puzzles
    spearman.csv          RQ2: Spearman rho of clue count and dataset rating vs nodes
    fig_nodes_by_band.png, fig_time_by_band.png, fig_rq2_scatter.png
Solvers that have no results file yet are left out automatically.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "experiments" / "results"

# fixed order and color per solver (color follows the solver, never its rank)
ORDER = ["bt", "bt_mrv", "bt_mrv_fc", "bt_mrv_mac", "minigrid"]
LABEL = {"bt": "BT", "bt_mrv": "BT+MRV", "bt_mrv_fc": "BT+MRV+FC",
         "bt_mrv_mac": "BT+MRV+MAC", "minigrid": "Minigrid [1]"}
COLOR = {"bt": "#2a78d6", "bt_mrv": "#eb6834", "bt_mrv_fc": "#1baf7a",
         "bt_mrv_mac": "#eda100", "minigrid": "#e87ba4"}
CELL_BASED = ["bt", "bt_mrv", "bt_mrv_fc", "bt_mrv_mac"]   # node = one cell assignment

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 15, "axes.titlesize": 17,
    "axes.labelsize": 16, "xtick.labelsize": 14, "ytick.labelsize": 14,
    "legend.fontsize": 14, "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#52514e", "axes.labelcolor": "#0b0b0b",
    "xtick.color": "#52514e", "ytick.color": "#52514e",
    "grid.color": "#e4e3df", "grid.linewidth": 0.8,
})


def load() -> pd.DataFrame:
    frames = [pd.read_csv(RES / f"{s}.csv") for s in ORDER if (RES / f"{s}.csv").exists()]
    df = pd.concat(frames, ignore_index=True)
    for col in ("solved", "timed_out", "correct", "matches_dataset"):
        df[col] = df[col].astype(str).str.lower() == "true"
    return df


def summarize(df: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    g = df.groupby(keys)
    out = pd.DataFrame({
        "puzzles": g.size(),
        "solved_pct": g["solved"].mean() * 100,
        "timeouts": g["timed_out"].sum(),
        "wrong": g.apply(lambda x: (x["solved"] & ~x["correct"]).sum(), include_groups=False),
        "median_nodes": g["nodes"].median(),
        "mean_nodes": g["nodes"].mean(),
        "max_nodes": g["nodes"].max(),
        "median_backtracks": g["backtracks"].median(),
        "median_seconds": g["seconds"].median(),
        "mean_seconds": g["seconds"].mean(),
        "max_seconds": g["seconds"].max(),
    }).reset_index()
    return out


def grouped_bars(ax, table, solvers, value, ylabel, title):
    bands = sorted(table["band"].unique())
    width = 0.8 / len(solvers)
    for k, s in enumerate(solvers):
        sub = table[table["solver"] == s].set_index("band").reindex(bands)
        xs = [b + (k - (len(solvers) - 1) / 2) * width for b in bands]
        ax.bar(xs, sub[value], width=width * 0.92, color=COLOR[s], label=LABEL[s], zorder=3)
    ax.set_yscale("log")
    ax.set_xticks(bands, [f"Band {b}" for b in bands])
    ax.set_xlabel("Difficulty band (dataset rating, 100 puzzles each)")
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc="left")
    ax.grid(axis="y", which="major", zorder=0)
    ax.legend(frameon=False, ncol=len(solvers), loc="upper left", bbox_to_anchor=(0, 1.0))


def main():
    df = load()
    solvers = [s for s in ORDER if s in set(df["solver"])]
    by_band = summarize(df, ["solver", "band"])
    overall = summarize(df, ["solver"])
    by_band.round(4).to_csv(RES / "summary_by_band.csv", index=False)
    overall.round(4).to_csv(RES / "summary_overall.csv", index=False)

    rows = []
    for s in solvers:
        d = df[(df["solver"] == s) & df["solved"]]
        for x in ("clues", "difficulty"):
            rho, p = spearmanr(d[x], d["nodes"])
            rows.append({"solver": s, "predictor": x, "n": len(d), "rho": rho, "p": p})
    rho = pd.DataFrame(rows)
    rho.round(4).to_csv(RES / "spearman.csv", index=False)

    cell = [s for s in solvers if s in CELL_BASED]
    fig, ax = plt.subplots(figsize=(11, 5.6))
    grouped_bars(ax, by_band, cell, "median_nodes", "Median nodes per puzzle (log scale)",
                 "Fig. 3  Search nodes by difficulty band")
    ax.set_ylim(top=ax.get_ylim()[1] * 8)
    fig.tight_layout()
    fig.savefig(RES / "fig_nodes_by_band.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5.6))
    grouped_bars(ax, by_band, solvers, "median_seconds", "Median seconds per puzzle (log scale)",
                 "Fig. 4  Solve time by difficulty band")
    ax.set_ylim(top=ax.get_ylim()[1] * 8)
    fig.tight_layout()
    fig.savefig(RES / "fig_time_by_band.png", dpi=200)
    plt.close(fig)

    focus = "bt_mrv" if "bt_mrv" in solvers else solvers[0]
    d = df[(df["solver"] == focus) & df["solved"]]
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.0), sharey=True)
    for ax, x, xl in ((axes[0], "clues", "Clue count"),
                      (axes[1], "difficulty", "Dataset rating (difficulty)")):
        r = rho[(rho.solver == focus) & (rho.predictor == x)].iloc[0]
        ax.scatter(d[x], d["nodes"].clip(lower=1), s=40, alpha=0.55, color=COLOR[focus],
                   edgecolors="white", linewidths=0.8, zorder=3)
        ax.set_yscale("log")
        ax.set_xlabel(xl)
        ax.set_title(f"Spearman ρ = {r.rho:.2f}", loc="left")
        ax.grid(axis="y", zorder=0)
    axes[0].set_ylabel(f"{LABEL[focus]} nodes (log scale)")
    fig.suptitle(f"Fig. 5  RQ2: what predicts effort? ({LABEL[focus]}, {len(d)} puzzles)",
                 x=0.01, ha="left", fontsize=17)
    fig.tight_layout()
    fig.savefig(RES / "fig_rq2_scatter.png", dpi=200)
    plt.close(fig)

    pd.set_option("display.width", 200)
    print(overall.round(3).to_string(index=False))
    print(by_band.round(3).to_string(index=False))
    print(rho.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
