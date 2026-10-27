from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyBboxPatch

THU_MUC_HINH = Path(__file__).resolve().parent / "hinh"

KIEU_NUT = {
    "input": {"face": "#E3F2FD", "edge": "#1565C0"},
    "param": {"face": "#FCE4EC", "edge": "#AD1457"},
    "op": {"face": "#FFF3E0", "edge": "#E65100"},
    "output": {"face": "#E8F5E9", "edge": "#2E7D32"},
}

BAN_KINH = 0.42
MAU_TIEN = "#1565C0"
MAU_NGUOC = "#C62828"


def ve_nut(ax, nut):
    x, y = nut["pos"]
    kieu = KIEU_NUT[nut["kind"]]
    if nut["kind"] == "op":
        ax.add_patch(Circle((x, y), BAN_KINH, facecolor=kieu["face"], edgecolor=kieu["edge"], lw=2, zorder=3))
        ax.text(x, y + BAN_KINH + 0.12, nut["name"], ha="center", va="bottom", fontsize=12, color=kieu["edge"], zorder=4)
    else:
        ax.add_patch(
            FancyBboxPatch(
                (x - BAN_KINH * 1.15, y - BAN_KINH * 0.75),
                BAN_KINH * 2.3,
                BAN_KINH * 1.5,
                boxstyle="round,pad=0.06",
                facecolor=kieu["face"],
                edgecolor=kieu["edge"],
                lw=2,
                zorder=3,
            )
        )
    ax.text(x, y, nut["label"], ha="center", va="center", fontsize=13 if len(nut["label"]) < 12 else 10, zorder=4)
    if nut.get("value") is not None:
        ax.text(x, y - BAN_KINH - 0.1, nut["value"], ha="center", va="top", fontsize=9, color=MAU_TIEN, zorder=4)


def ve_canh(ax, p, q, nhan_gradient=None, lech_nhan=0.0):
    p = np.array(p, dtype=float)
    q = np.array(q, dtype=float)
    huong = (q - p) / np.linalg.norm(q - p)
    phap_tuyen = np.array([-huong[1], huong[0]])
    dau = p + huong * BAN_KINH * 1.25
    cuoi = q - huong * BAN_KINH * 1.25
    ax.annotate("", xy=cuoi, xytext=dau, arrowprops=dict(arrowstyle="-|>", color=MAU_TIEN, lw=1.8), zorder=2)
    if nhan_gradient is None:
        return
    dich = phap_tuyen * 0.16
    ax.annotate(
        "",
        xy=dau + dich,
        xytext=cuoi + dich,
        arrowprops=dict(arrowstyle="-|>", color=MAU_NGUOC, lw=1.4, linestyle="--"),
        zorder=2,
    )
    giua = (dau + cuoi) / 2 + phap_tuyen * (0.42 + lech_nhan)
    ax.text(
        giua[0],
        giua[1],
        nhan_gradient,
        ha="center",
        va="center",
        fontsize=9,
        color=MAU_NGUOC,
        bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85),
        zorder=5,
    )


def ve_do_thi(nut, canh, tieu_de, ten_file, kich_thuoc=(13, 6)):
    THU_MUC_HINH.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=kich_thuoc)
    for c in canh:
        ve_canh(ax, nut[c[0]]["pos"], nut[c[1]]["pos"], c[2] if len(c) > 2 else None, c[3] if len(c) > 3 else 0.0)
    for n in nut.values():
        ve_nut(ax, n)
    xs = [n["pos"][0] for n in nut.values()]
    ys = [n["pos"][1] for n in nut.values()]
    ax.set_xlim(min(xs) - 1.0, max(xs) + 1.0)
    ax.set_ylim(min(ys) - 1.6, max(ys) + 1.2)
    ax.set_aspect("equal")
    ax.axis("off")
    chu_giai = [
        Line2D([0], [0], color=MAU_TIEN, lw=2, label="Lan truyền tiến (Forward)"),
        Line2D([0], [0], color=MAU_NGUOC, lw=2, linestyle="--", label="Lan truyền ngược (Backward)"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor=KIEU_NUT["input"]["face"], markeredgecolor=KIEU_NUT["input"]["edge"], markersize=12, label="Nút đầu vào / dữ liệu"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor=KIEU_NUT["param"]["face"], markeredgecolor=KIEU_NUT["param"]["edge"], markersize=12, label="Nút tham số"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=KIEU_NUT["op"]["face"], markeredgecolor=KIEU_NUT["op"]["edge"], markersize=12, label="Nút phép toán"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor=KIEU_NUT["output"]["face"], markeredgecolor=KIEU_NUT["output"]["edge"], markersize=12, label="Nút đầu ra"),
    ]
    ax.legend(handles=chu_giai, loc="lower center", ncol=3, fontsize=9, frameon=False, bbox_to_anchor=(0.5, -0.12))
    ax.set_title(tieu_de, fontsize=13, fontweight="bold")
    duong_dan = THU_MUC_HINH / ten_file
    fig.savefig(duong_dan, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return duong_dan


def ve_do_thi_logistic(x, y, trong_so, bias, ky_hieu, tieu_de, ten_file):
    u = trong_so * x
    z = u + bias
    y_hat = 1.0 / (1.0 + np.exp(-z))
    loss = -(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat))
    dL_dyhat = -y / y_hat + (1 - y) / (1 - y_hat)
    dL_dz = y_hat - y
    w, b, xx = ky_hieu["w"], ky_hieu["b"], ky_hieu["x"]
    nut = {
        "w": {"pos": (0, 3.2), "kind": "param", "label": f"${w}$", "value": f"{trong_so:.4f}"},
        "x": {"pos": (0, 1.6), "kind": "input", "label": f"${xx}$", "value": f"{x:.4f}"},
        "mul": {"pos": (2.6, 2.4), "kind": "op", "name": "$u$", "label": r"$\times$", "value": f"u = {u:.4f}"},
        "b": {"pos": (2.6, 0.4), "kind": "param", "label": f"${b}$", "value": f"{bias:.4f}"},
        "add": {"pos": (5.2, 2.4), "kind": "op", "name": "$z$", "label": "$+$", "value": f"z = {z:.4f}"},
        "sig": {"pos": (7.8, 2.4), "kind": "op", "name": r"$\hat{y}$", "label": r"$\sigma$", "value": f"ŷ = {y_hat:.4f}"},
        "y": {"pos": (7.8, 0.4), "kind": "input", "label": "$y$", "value": f"{y:g}"},
        "bce": {"pos": (10.4, 2.4), "kind": "op", "name": "$L$", "label": "BCE", "value": f"L = {loss:.4f}"},
        "L": {"pos": (12.6, 2.4), "kind": "output", "label": "$L$", "value": None},
    }
    canh = [
        ("w", "mul", f"$\\partial L/\\partial {w}=(\\hat{{y}}-y){xx}$\n= {dL_dz * x:.4f}", 0.2),
        ("x", "mul"),
        ("mul", "add", f"$\\partial L/\\partial u$ = {dL_dz:.4f}"),
        ("b", "add", f"$\\partial L/\\partial {b}=\\hat{{y}}-y$\n= {dL_dz:.4f}", -0.95),
        ("add", "sig", f"$\\partial L/\\partial z=\\hat{{y}}-y$\n= {dL_dz:.4f}"),
        ("sig", "bce", f"$\\partial L/\\partial \\hat{{y}}$ = {dL_dyhat:.4f}"),
        ("y", "bce"),
        ("bce", "L", "$\\partial L/\\partial L$ = 1"),
    ]
    return ve_do_thi(nut, canh, tieu_de, ten_file, kich_thuoc=(14, 6))
