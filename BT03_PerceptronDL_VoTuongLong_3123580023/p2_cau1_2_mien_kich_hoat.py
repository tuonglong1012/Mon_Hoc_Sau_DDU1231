from itertools import product

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

from ve_hinh import MAU_DUONG, bieu_thuc_tuyen_tinh, ke_truc, luu_hinh, so, to_mien, ve_duong_thang

W_AN = np.array([[2.0, 0.0, 1.0], [1.0, 2.0, 1.0], [1.0, 3.0, 0.0]])
W_RA = np.array([2.0, 3.0, 1.0, 1.0])
BIAS_CU = 1.0
BIAS_MOI = -1.0
GIOI_HAN_X = (-5.0, 4.0)
GIOI_HAN_Y = (-3.0, 4.0)


def doi_bias(w_an=W_AN, cu=BIAS_CU, moi=BIAS_MOI):
    w = w_an.copy()
    w[w[:, 2] == cu, 2] = moi
    return w


W_AN_MOI = doi_bias()


def phi(v):
    return (np.asarray(v) >= 0).astype(int)


def lan_truyen(x1, x2, w_an=W_AN, w_ra=W_RA):
    x1, x2 = np.asarray(x1, dtype=float), np.asarray(x2, dtype=float)
    v_an = [w[0] * x1 + w[1] * x2 + w[2] for w in w_an]
    o = [phi(v) for v in v_an]
    v_ra = w_ra[0] * o[0] + w_ra[1] * o[1] + w_ra[2] * o[2] + w_ra[3]
    return v_an, o, v_ra, phi(v_ra)


def bieu_thuc_an(w_an=W_AN):
    return [bieu_thuc_tuyen_tinh(w, ["x₁", "x₂", ""]) for w in w_an]


def bieu_thuc_ra(w_ra=W_RA):
    return bieu_thuc_tuyen_tinh(w_ra, ["o₁", "o₂", "o₃", ""])


def dieu_kien_an(w_an=W_AN):
    kq = []
    for w in w_an:
        if abs(w[1]) < 1e-12:
            kq.append(f"x₁ ≥ {so(-w[2] / w[0])}" if w[0] > 0 else f"x₁ ≤ {so(-w[2] / w[0])}")
        else:
            dau = "≥" if w[1] > 0 else "≤"
            kq.append(f"x₂ {dau} {bieu_thuc_tuyen_tinh([-w[0] / w[1], -w[2] / w[1]], ['x₁', ''])}")
    return kq


def bang_to_hop(w_ra=W_RA):
    cac_dong = []
    for o in product([0, 1], repeat=3):
        v = float(np.dot(w_ra[:3], o) + w_ra[3])
        cac_dong.append({"o": o, "v": v, "y": int(v >= 0)})
    return cac_dong


def khao_sat_luoi(w_an=W_AN, w_ra=W_RA, so_diem=601):
    xx, yy = np.meshgrid(np.linspace(*GIOI_HAN_X, so_diem), np.linspace(*GIOI_HAN_Y, so_diem))
    _, o, _, y = lan_truyen(xx, yy, w_an, w_ra)
    mau = {tuple(int(v) for v in t) for t in zip(o[0].ravel(), o[1].ravel(), o[2].ravel())}
    return {"ty_le_kich_hoat": float(y.mean()), "cac_mau_o": sorted(mau)}


def khoang_cach_goc(w_an=W_AN):
    return [abs(w[2]) / np.hypot(w[0], w[1]) for w in w_an]


def giao_diem(w_an=W_AN):
    kq = []
    for i in range(3):
        for j in range(i + 1, 3):
            a = np.array([w_an[i][:2], w_an[j][:2]])
            c = -np.array([w_an[i][2], w_an[j][2]])
            kq.append((i + 1, j + 1, np.linalg.solve(a, c)))
    return kq


def ve_mien(ax, w_an, w_ra, tieu_de):
    ke_truc(ax, GIOI_HAN_X, GIOI_HAN_Y)
    to_mien(ax, lambda u, v: lan_truyen(u, v, w_an, w_ra)[3] == 1, GIOI_HAN_X, GIOI_HAN_Y, "#A5D6A7", "Miền y = 1", 0.45)
    for k, w in enumerate(w_an):
        mau = MAU_DUONG[k]
        ve_duong_thang(ax, w[0], w[1], w[2], GIOI_HAN_X, color=mau, lw=2, label=f"Nơ-ron {k + 1}: {bieu_thuc_tuyen_tinh(w, ['x₁', 'x₂', ''])} = 0")
        if abs(w[1]) < 1e-12:
            goc = np.array([-w[2] / w[0], GIOI_HAN_Y[0] + 0.6 + k * 0.4])
        else:
            x0 = GIOI_HAN_X[1] - 1.3 - 1.2 * k
            goc = np.array([x0, -(w[0] * x0 + w[2]) / w[1]])
        huong = w[:2] / np.hypot(w[0], w[1]) * 0.7
        ax.annotate("", xy=goc + huong, xytext=goc, arrowprops=dict(arrowstyle="-|>", color=mau, lw=1.8))
        ax.text(*(goc + huong * 1.25), f"o{chr(0x2081 + k)} = 1", color=mau, fontsize=8, ha="center", va="center")
    ax.legend(loc="lower left", fontsize=7.5, framealpha=0.95)
    ax.set_title(tieu_de, fontsize=10)


def ve_mot_mien(w_an, w_ra, tieu_de, ten_file):
    fig, ax = plt.subplots(figsize=(7.5, 6))
    ve_mien(ax, w_an, w_ra, tieu_de)
    return luu_hinh(fig, ten_file)


def ve_so_sanh():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.6))
    ve_mien(ax1, W_AN, W_RA, "Trước khi đổi bias (Câu 1)")
    ve_mien(ax2, W_AN_MOI, W_RA, "Sau khi đổi bias 1 → −1 (Câu 2)")
    for w_cu, w_moi in zip(W_AN, W_AN_MOI):
        if w_cu[2] != w_moi[2]:
            ve_duong_thang(ax2, w_cu[0], w_cu[1], w_cu[2], GIOI_HAN_X, color="gray", lw=1.2, ls=":")
    return luu_hinh(fig, "p2_cau2_so_sanh_bias.png")


def ve_mang(w_an, w_ra, ten_file):
    fig, ax = plt.subplots(figsize=(8, 5.2))
    vao = {"x₁": (0, 3.0), "x₂": (0, 1.8), "1": (0, 0.6)}
    an = [(3.2, 3.4), (3.2, 2.0), (3.2, 0.6)]
    ra = (6.4, 2.0)
    bias_ra = (3.2, -0.8)
    for (ten, p) in vao.items():
        ax.add_patch(Circle(p, 0.22, fc="#E3F2FD", ec="#1565C0", lw=1.5))
        ax.text(p[0] - 0.4, p[1], ten, ha="right", va="center", fontsize=12)
    for k, p in enumerate(an):
        ax.add_patch(Circle(p, 0.32, fc="#FFF3E0", ec="#E65100", lw=1.6))
        ax.text(*p, str(k + 1), ha="center", va="center", fontsize=12, fontweight="bold")
        for j, q in enumerate(vao.values()):
            d = np.array(p) - np.array(q)
            dau = np.array(q) + d / np.linalg.norm(d) * 0.22
            cuoi = np.array(p) - d / np.linalg.norm(d) * 0.32
            ax.annotate("", xy=cuoi, xytext=dau, arrowprops=dict(arrowstyle="-|>", color=MAU_DUONG[k], lw=1.1, alpha=0.85))
        ax.text(p[0], p[1] + 0.42, f"w{chr(0x2081 + k)} = [{', '.join(so(v) for v in w_an[k])}]", fontsize=9, color=MAU_DUONG[k], ha="center", va="bottom", fontweight="bold", bbox=dict(fc="white", ec="none", pad=0.5))
    ax.add_patch(Circle(bias_ra, 0.22, fc="#E3F2FD", ec="#1565C0", lw=1.5))
    ax.text(bias_ra[0] - 0.4, bias_ra[1], "1", ha="right", va="center", fontsize=12)
    ax.add_patch(Circle(ra, 0.36, fc="#E8F5E9", ec="#2E7D32", lw=1.8))
    ax.text(*ra, "4", ha="center", va="center", fontsize=12, fontweight="bold")
    for k, q in enumerate(an + [bias_ra]):
        d = np.array(ra) - np.array(q)
        dau = np.array(q) + d / np.linalg.norm(d) * (0.32 if k < 3 else 0.22)
        cuoi = np.array(ra) - d / np.linalg.norm(d) * 0.36
        ax.annotate("", xy=cuoi, xytext=dau, arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=1.2))
        nhan = dau + (cuoi - dau) * 0.45
        ten = f"o{chr(0x2081 + k)} · {so(w_ra[k])}" if k < 3 else so(w_ra[k])
        ax.text(*nhan, ten, fontsize=9, color="#2E7D32", ha="center", va="center", fontweight="bold", bbox=dict(fc="white", ec="none", pad=0.5))
    ax.annotate("", xy=(ra[0] + 1.3, ra[1]), xytext=(ra[0] + 0.36, ra[1]), arrowprops=dict(arrowstyle="-|>", color="#455A64", lw=1.5))
    ax.text(ra[0] + 1.42, ra[1], "y", ha="left", va="center", fontsize=12)
    ax.text(ra[0], ra[1] + 0.48, f"w₄ = [{', '.join(so(v) for v in w_ra)}]", fontsize=9, color="#2E7D32", ha="center", va="bottom", fontweight="bold")
    ax.text(0.2, -1.15, "Thứ tự trọng số: [x₁, x₂, bias] ở tầng ẩn; [o₁, o₂, o₃, bias] ở tầng ra", fontsize=8.5, color="#455A64", ha="left")
    ax.set_xlim(-1.2, 8.3)
    ax.set_ylim(-1.3, 4.3)
    ax.set_aspect("equal")
    ax.axis("off")
    return luu_hinh(fig, ten_file)


if __name__ == "__main__":
    for ten, w_an in (("Cau 1", W_AN), ("Cau 2", W_AN_MOI)):
        print(ten, "- trong so tang an:", w_an.tolist(), "- tang ra:", W_RA.tolist())
        print("  Giao diem:", [(i, j, p.round(4).tolist()) for i, j, p in giao_diem(w_an)])
        print("  Khoang cach tu goc toi duong:", np.round(khoang_cach_goc(w_an), 4).tolist())
        print("  Khao sat luoi:", khao_sat_luoi(w_an))
    print("Bang to hop o -> v4:", [(d["o"], d["v"], d["y"]) for d in bang_to_hop()])
    print("Da luu:", ve_mang(W_AN, W_RA, "p2_cau1_mang.png").name, ve_mang(W_AN_MOI, W_RA, "p2_cau2_mang.png").name)
    print("Da luu:", ve_mot_mien(W_AN, W_RA, "Miền kích hoạt của mạng (Câu 1)", "p2_cau1_mien_kich_hoat.png").name)
    print("Da luu:", ve_mot_mien(W_AN_MOI, W_RA, "Miền kích hoạt sau khi đổi bias (Câu 2)", "p2_cau2_mien_kich_hoat.png").name, ve_so_sanh().name)
