import matplotlib.pyplot as plt
import numpy as np

from ve_hinh import ke_truc, luu_hinh, so, to_hai_phia, ve_duong_thang, ve_perceptron

HE_SO_GOC = -1.5
TUNG_DO_GOC = 3.0
W = np.array([3.0, 2.0])
B = -6.0
DIEM_THU = np.array([[0.0, 3.0], [2.0, 0.0], [0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [-1.0, 4.0], [3.0, -1.0]])
GIOI_HAN_X = (-2.0, 4.0)
GIOI_HAN_Y = (-2.0, 6.0)


def tau(s):
    return np.where(s >= 0, 1, -1)


def perceptron(x):
    s = x @ W + B
    return s, tau(s)


def nam_tren_duong(x1):
    x1 = np.asarray(x1, dtype=float)
    x2 = HE_SO_GOC * x1 + TUNG_DO_GOC
    return np.allclose(W[0] * x1 + W[1] * x2 + B, 0.0)


def bang_kiem_tra():
    s, y = perceptron(DIEM_THU)
    return [{"x": tuple(float(v) for v in x), "s": si, "y": int(yi)} for x, si, yi in zip(DIEM_THU, s, y)]


def ve_hinh():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1, 1.1]})
    ve_perceptron(ax1, ["1", "x₁", "x₂"], [B, W[0], W[1]], "τ")
    ax1.set_title("Perceptron: y = τ(3x₁ + 2x₂ − 6)")
    ke_truc(ax2, GIOI_HAN_X, GIOI_HAN_Y)
    to_hai_phia(ax2, W[0], W[1], B, GIOI_HAN_X, GIOI_HAN_Y)
    ve_duong_thang(ax2, W[0], W[1], B, GIOI_HAN_X, color="#1565C0", lw=2.2, label="x₂ = −1.5x₁ + 3")
    s, y = perceptron(DIEM_THU)
    for (x1, x2), yi in zip(DIEM_THU, y):
        ax2.scatter(x1, x2, s=45, c="black", zorder=4)
        ax2.annotate(f"({so(x1)}, {so(x2)}): {'+1' if yi > 0 else '−1'}", (x1, x2), textcoords="offset points", xytext=(6, 5), fontsize=8)
    ax2.legend(loc="upper right", fontsize=8)
    ax2.set_title("Ranh giới quyết định và hai miền phân lớp")
    return luu_hinh(fig, "p1_cau1_ranh_gioi.png")


if __name__ == "__main__":
    print("Perceptron: s = 3*x1 + 2*x2 - 6, y = tau(s)")
    print("Trung duong x2 = -1.5*x1 + 3:", nam_tren_duong(np.linspace(-2, 4, 13)))
    for dong in bang_kiem_tra():
        print(f"  x = {dong['x']}: s = {dong['s']:g}, y = {dong['y']:+d}")
    print("Da luu:", ve_hinh().name)
