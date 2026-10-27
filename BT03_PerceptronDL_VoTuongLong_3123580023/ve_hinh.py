from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

THU_MUC_HINH = Path(__file__).resolve().parent / "hinh"

MAU_DUONG = ["#1565C0", "#E65100", "#2E7D32", "#6A1B9A", "#C62828", "#00838F"]
MAU_DUONG_TINH = "#A5D6A7"
MAU_AM = "#EF9A9A"


def luu_hinh(fig, ten_file):
    THU_MUC_HINH.mkdir(exist_ok=True)
    duong_dan = THU_MUC_HINH / ten_file
    fig.savefig(duong_dan, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return duong_dan


def so(x):
    return f"{x:g}".replace("-", "−")


def bieu_thuc_tuyen_tinh(he_so, ten_bien):
    phan = []
    for a, ten in zip(he_so, ten_bien):
        if abs(a) < 1e-12:
            continue
        gia_tri = abs(a)
        than = ten if ten and gia_tri == 1 else f"{gia_tri:g}{ten}"
        if not phan:
            phan.append(("−" if a < 0 else "") + than)
        else:
            phan.append(("− " if a < 0 else "+ ") + than)
    return " ".join(phan) if phan else "0"


def ke_truc(ax, gioi_han_x, gioi_han_y, ten_x="x₁", ten_y="x₂"):
    ax.axhline(0, color="black", lw=0.8)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlim(*gioi_han_x)
    ax.set_ylim(*gioi_han_y)
    ax.set_xlabel(ten_x)
    ax.set_ylabel(ten_y)
    ax.grid(alpha=0.3)
    ax.set_aspect("equal")


def ve_duong_thang(ax, w1, w2, b, gioi_han_x, **kieu):
    if abs(w2) > 1e-12:
        x = np.linspace(*gioi_han_x, 200)
        ax.plot(x, -(w1 * x + b) / w2, **kieu)
    else:
        ax.axvline(-b / w1, **kieu)


def to_mien(ax, ham, gioi_han_x, gioi_han_y, mau, nhan=None, do_dam=0.35):
    xx, yy = np.meshgrid(np.linspace(*gioi_han_x, 600), np.linspace(*gioi_han_y, 600))
    ax.contourf(xx, yy, ham(xx, yy).astype(float), levels=[0.5, 1.5], colors=[mau], alpha=do_dam)
    if nhan:
        ax.plot([], [], "s", color=mau, alpha=0.6, ms=11, label=nhan)


def to_hai_phia(ax, w1, w2, b, gioi_han_x, gioi_han_y, nhan_duong="y = +1", nhan_am="y = −1"):
    to_mien(ax, lambda u, v: w1 * u + w2 * v + b >= 0, gioi_han_x, gioi_han_y, MAU_DUONG_TINH, nhan_duong)
    to_mien(ax, lambda u, v: w1 * u + w2 * v + b < 0, gioi_han_x, gioi_han_y, MAU_AM, nhan_am)


def ve_perceptron(ax, nhan_dau_vao, trong_so, ten_ham, ten_ra="y"):
    n = len(nhan_dau_vao)
    cac_y = np.linspace((n - 1) * 1.2, 0, n)
    y_giua = cac_y.mean()
    x_nut = 3.2
    for nhan, w, y in zip(nhan_dau_vao, trong_so, cac_y):
        ax.add_patch(Circle((0, y), 0.18, fc="#E3F2FD", ec="#1565C0", lw=1.5))
        ax.text(-0.3, y, nhan, ha="right", va="center", fontsize=11)
        dich = np.array([x_nut - 0.6, y_giua + (y - y_giua) * 0.25])
        ax.annotate("", xy=dich, xytext=(0.2, y), arrowprops=dict(arrowstyle="-|>", color="#455A64", lw=1.3))
        t = 0.45
        ax.text(0.2 + t * (dich[0] - 0.2), y + t * (dich[1] - y) + 0.13, so(w), ha="center", va="bottom", fontsize=11, color="#AD1457", fontweight="bold")
    ax.add_patch(Circle((x_nut, y_giua), 0.58, fc="#FFF3E0", ec="#E65100", lw=1.8))
    ax.text(x_nut, y_giua, f"Σ | {ten_ham}", ha="center", va="center", fontsize=11)
    ax.annotate("", xy=(x_nut + 1.5, y_giua), xytext=(x_nut + 0.6, y_giua), arrowprops=dict(arrowstyle="-|>", color="#455A64", lw=1.5))
    ax.text(x_nut + 1.62, y_giua, ten_ra, ha="left", va="center", fontsize=12)
    do_dai_nhan = max(len(nhan) for nhan in nhan_dau_vao)
    ax.set_xlim(-0.5 - 0.17 * do_dai_nhan, x_nut + 2.2)
    ax.set_ylim(-0.6, cac_y[0] + 0.6)
    ax.set_aspect("equal")
    ax.axis("off")


def ve_diem(ax, toa_do, nhan, ten=None, co=90):
    for (x1, x2), t, i in zip(toa_do, nhan, range(len(nhan))):
        duong = t > 0
        ax.scatter(x1, x2, s=co, c="#1565C0" if duong else "white", edgecolors="#1565C0" if duong else "#C62828", marker="o" if duong else "s", linewidths=1.8, zorder=4)
        if ten:
            ax.annotate(ten[i], (x1, x2), textcoords="offset points", xytext=(7, 6), fontsize=10, fontweight="bold")
