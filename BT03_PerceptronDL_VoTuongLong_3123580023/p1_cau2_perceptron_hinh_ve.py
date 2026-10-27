import matplotlib.pyplot as plt
import numpy as np

from ve_hinh import bieu_thuc_tuyen_tinh, ke_truc, luu_hinh, so, to_hai_phia, ve_diem, ve_duong_thang, ve_perceptron

W_A = np.array([2.0, 1.0])
B_A = -3.0
X_THU = np.array([[-1.0, 0.0], [2.0, 0.0]])
GIAO_TRUC_X1 = np.array([2.0, 0.0])
GIAO_TRUC_X2 = np.array([0.0, -1.0])
X_LOGIC = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
TEN_MAU = ["a", "b", "c", "d"]
T_AND = np.array([-1, -1, -1, 1])
T_OR = np.array([-1, 1, 1, 1])
W_AND = np.array([1.0, 1.0])
B_AND = -1.5
W_OR = np.array([1.0, 1.0])
B_OR = -0.5


def f_g(s):
    return np.where(s >= 0, 1, -1)


def dau_ra(w, b, x):
    s = np.asarray(x) @ w + b
    return s, f_g(s)


def duong_thang_qua_hai_diem(p, q):
    w1 = q[1] - p[1]
    w2 = -(q[0] - p[0])
    b = -(w1 * p[0] + w2 * p[1])
    if w1 < 0:
        w1, w2, b = -w1, -w2, -b
    return np.array([w1, w2]), b


def ranh_gioi_cau_a():
    return -W_A[0] / W_A[1], -B_A / W_A[1]


def perceptron_cau_c():
    return duong_thang_qua_hai_diem(GIAO_TRUC_X1, GIAO_TRUC_X2)


def bang_logic(w, b, t):
    s, y = dau_ra(w, b, X_LOGIC)
    return [{"ten": n, "x": tuple(int(v) for v in x), "s": si, "y": int(yi), "t": int(ti)} for n, x, si, yi, ti in zip(TEN_MAU, X_LOGIC, s, y, t)]


def ve_cau_a():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1, 1.1]})
    ve_perceptron(ax1, ["1", "x₁", "x₂"], [B_A, W_A[0], W_A[1]], "f_g")
    ax1.set_title("Perceptron đề cho: y = f_g(2x₁ + x₂ − 3)")
    gx, gy = (-2.0, 3.5), (-2.0, 5.0)
    ke_truc(ax2, gx, gy)
    to_hai_phia(ax2, W_A[0], W_A[1], B_A, gx, gy)
    ve_duong_thang(ax2, W_A[0], W_A[1], B_A, gx, color="#1565C0", lw=2.2, label="x₂ = −2x₁ + 3")
    s, y = dau_ra(W_A, B_A, X_THU)
    for k, ((x1, x2), si, yi) in enumerate(zip(X_THU, s, y)):
        ax2.scatter(x1, x2, s=70, c="black", zorder=4)
        ax2.annotate(f"x⁽{k + 1}⁾ = ({x1:g}, {x2:g})\ns = {so(si)}, y = {'+1' if yi > 0 else '−1'}", (x1, x2), textcoords="offset points", xytext=(-10, -32), fontsize=8)
    ax2.legend(loc="upper right", fontsize=8)
    ax2.set_title("Câu 2a–b: ranh giới 2x₁ + x₂ − 3 = 0")
    return luu_hinh(fig, "p1_cau2ab_ranh_gioi.png")


def ve_cau_c():
    w, b = perceptron_cau_c()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={"width_ratios": [1, 1.1]})
    ve_perceptron(ax1, ["1", "x₁", "x₂"], [b, w[0], w[1]], "f_g")
    ax1.set_title(f"Perceptron tìm được: y = f_g({bieu_thuc_tuyen_tinh([w[0], w[1], b], ['x₁', 'x₂', ''])})")
    gx, gy = (-2.0, 5.0), (-3.0, 2.5)
    ke_truc(ax2, gx, gy)
    to_hai_phia(ax2, w[0], w[1], b, gx, gy)
    ve_duong_thang(ax2, w[0], w[1], b, gx, color="#1565C0", lw=2.2, label="x₂ = 0.5x₁ − 1")
    for p in (GIAO_TRUC_X1, GIAO_TRUC_X2):
        ax2.scatter(*p, s=60, c="black", zorder=4)
        ax2.annotate(f"({so(p[0])}, {so(p[1])})", p, textcoords="offset points", xytext=(6, 6), fontsize=9)
    ax2.legend(loc="upper left", fontsize=8)
    ax2.set_title("Câu 2c: đường thẳng qua (2, 0) và (0, −1)")
    return luu_hinh(fig, "p1_cau2c_ranh_gioi.png")


def ve_cau_d():
    fig, cac_ax = plt.subplots(1, 2, figsize=(11, 4.8))
    gx, gy = (-0.6, 1.8), (-0.6, 1.8)
    for ax, ten, w, b, t in ((cac_ax[0], "AND", W_AND, B_AND, T_AND), (cac_ax[1], "OR", W_OR, B_OR, T_OR)):
        ke_truc(ax, gx, gy)
        to_hai_phia(ax, w[0], w[1], b, gx, gy)
        ve_duong_thang(ax, w[0], w[1], b, gx, color="#1565C0", lw=2.2, label=f"x₁ + x₂ − {abs(b):g} = 0")
        ve_diem(ax, X_LOGIC, t, TEN_MAU)
        ax.legend(loc="upper right", fontsize=8)
        ax.set_title(f"Hàm {ten}: y = f_g(x₁ + x₂ − {abs(b):g})")
    return luu_hinh(fig, "p1_cau2d_and_or.png")


if __name__ == "__main__":
    a, c = ranh_gioi_cau_a()
    print(f"Cau 2a: 2*x1 + x2 - 3 = 0  <=>  x2 = {a:g}*x1 + {c:g}")
    for k, (si, yi) in enumerate(zip(*dau_ra(W_A, B_A, X_THU))):
        print(f"Cau 2b: x({k + 1}) = {X_THU[k].tolist()}: s = {si:g}, y = {yi:+d}")
    w, b = perceptron_cau_c()
    print(f"Cau 2c: w = {w}, b = {b:g}")
    for ten, ww, bb, t in (("AND", W_AND, B_AND, T_AND), ("OR", W_OR, B_OR, T_OR)):
        print(f"Cau 2d {ten}:", [(d["ten"], d["s"], d["y"], d["t"]) for d in bang_logic(ww, bb, t)])
    print("Da luu:", ve_cau_a().name, ve_cau_c().name, ve_cau_d().name)
