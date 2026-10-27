import matplotlib.pyplot as plt
import numpy as np

from ve_hinh import bieu_thuc_tuyen_tinh, ke_truc, luu_hinh, so, to_hai_phia, ve_diem, ve_duong_thang

X = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
T = np.array([-1, 1, 1, 1])
TEN_MAU = ["a", "b", "c", "d"]
W0 = np.array([0.0, 1.0])
B0 = -0.5
RHO = 0.4
SO_BUOC_TOI_DA = 100


def sign(s):
    return np.where(s >= 0, 1, -1)


def phan_loai(w, b):
    s = X @ w + b
    y = sign(s)
    return s, y, y != T


def ham_mat_mat(w, b):
    s, _, sai = phan_loai(w, b)
    return float(np.sum(-T[sai] * s[sai]))


def gradient(w, b):
    _, _, sai = phan_loai(w, b)
    return -(T[sai, None] * X[sai]).sum(axis=0) + 0.0, -float(T[sai].sum()) + 0.0


def huan_luyen(w0=W0, b0=B0, rho=RHO):
    lich_su = []
    w, b = np.array(w0, dtype=float), float(b0)
    for k in range(SO_BUOC_TOI_DA):
        s, y, sai = phan_loai(w, b)
        gw, gb = gradient(w, b)
        buoc = {"k": k, "w": w.copy(), "b": b, "s": s, "y": y, "sai": sai, "J": ham_mat_mat(w, b), "gw": gw, "gb": gb}
        lich_su.append(buoc)
        if not sai.any():
            break
        w = w - rho * gw
        b = b - rho * gb
        buoc["w_moi"], buoc["b_moi"] = w.copy(), b
    return lich_su


def ve_cac_buoc(lich_su):
    n = len(lich_su)
    fig, cac_ax = plt.subplots(1, n, figsize=(5.2 * n, 5))
    cac_ax = np.atleast_1d(cac_ax)
    gx, gy = (-0.6, 1.8), (-0.6, 1.8)
    for ax, buoc in zip(cac_ax, lich_su):
        w, b = buoc["w"], buoc["b"]
        ke_truc(ax, gx, gy)
        to_hai_phia(ax, w[0], w[1], b, gx, gy)
        ve_duong_thang(ax, w[0], w[1], b, gx, color="#1565C0", lw=2.2, label=f"{bieu_thuc_tuyen_tinh([w[0], w[1], round(b, 6)], ['x₁', 'x₂', ''])} = 0")
        ve_diem(ax, X, T, TEN_MAU)
        for i in np.where(buoc["sai"])[0]:
            ax.scatter(*X[i], s=420, facecolors="none", edgecolors="#C62828", linewidths=2, zorder=5)
        so_sai = int(buoc["sai"].sum())
        ax.set_title(f"Bước {buoc['k']}: w = ({so(w[0])}, {so(w[1])}), b = {so(round(b, 6))}\n{so_sai} mẫu phân loại sai, J = {so(round(buoc['J'], 6))}", fontsize=10)
        ax.legend(loc="upper right", fontsize=8)
    return luu_hinh(fig, "p1_cau3_cac_buoc.png")


if __name__ == "__main__":
    for buoc in huan_luyen():
        print(f"Buoc {buoc['k']}: w = {buoc['w']}, b = {buoc['b']:g}, J = {buoc['J']:g}, sai = {[TEN_MAU[i] for i in np.where(buoc['sai'])[0]]}")
        print(f"  s = {buoc['s']}, y = {buoc['y']}, dJ/dw = {buoc['gw']}, dJ/db = {buoc['gb']:g}")
    print("Da luu:", ve_cac_buoc(huan_luyen()).name)
