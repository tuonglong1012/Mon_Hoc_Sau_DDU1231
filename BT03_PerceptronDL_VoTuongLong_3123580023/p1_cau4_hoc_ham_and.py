import matplotlib.pyplot as plt
import numpy as np

from ve_hinh import MAU_DUONG, ke_truc, luu_hinh, so, ve_diem, ve_duong_thang, to_hai_phia

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
Y_D = np.array([0, 0, 0, 1])
W0 = np.array([0.3, -0.2])
THETA = 0.4
ALPHA = 0.2
SO_EPOCH_TOI_DA = 50


def step(z):
    return 1 if z >= 0 else 0


def huan_luyen(w0=W0, theta=THETA, alpha=ALPHA):
    w = np.array(w0, dtype=float)
    cac_dong = []
    w_cuoi_epoch = [w.copy()]
    for epoch in range(1, SO_EPOCH_TOI_DA + 1):
        so_loi = 0
        for x, y_d in zip(X, Y_D):
            z = float(np.round(x @ w - theta, 10))
            y = step(z)
            e = y_d - y
            w = np.round(w + alpha * e * x, 10)
            so_loi += e != 0
            cac_dong.append({"epoch": epoch, "x1": int(x[0]), "x2": int(x[1]), "y_d": int(y_d), "z": z, "y": y, "e": int(e), "w1": w[0], "w2": w[1], "cap_nhat": e != 0})
        w_cuoi_epoch.append(w.copy())
        if so_loi == 0:
            break
    return cac_dong, w_cuoi_epoch


def ve_cac_epoch(w_cuoi_epoch):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8))
    gx, gy = (-0.6, 1.8), (-0.6, 2.4)
    t = np.where(Y_D == 1, 1, -1)
    ke_truc(ax1, gx, gy)
    for k, w in enumerate(w_cuoi_epoch):
        nhan = "Khởi tạo" if k == 0 else f"Sau epoch {k}"
        ve_duong_thang(ax1, w[0], w[1], -THETA, gx, color=MAU_DUONG[k % len(MAU_DUONG)], lw=1.8, ls="--" if k < len(w_cuoi_epoch) - 1 else "-", label=f"{nhan}: w = ({so(w[0])}, {so(w[1])})")
    ve_diem(ax1, X, t, None)
    ax1.legend(loc="upper right", fontsize=7)
    ax1.set_title("Đường x₁w₁ + x₂w₂ = θ qua các epoch")
    w = w_cuoi_epoch[-1]
    ke_truc(ax2, gx, gy)
    to_hai_phia(ax2, w[0], w[1], -THETA, gx, gy, "Y = 1", "Y = 0")
    ve_duong_thang(ax2, w[0], w[1], -THETA, gx, color="#1565C0", lw=2.2, label=f"{so(w[0])}x₁ + {so(w[1])}x₂ = {so(THETA)}")
    ve_diem(ax2, X, t, None)
    ax2.legend(loc="upper right", fontsize=8)
    ax2.set_title("Perceptron AND sau huấn luyện")
    return luu_hinh(fig, "p1_cau4_cac_epoch.png")


if __name__ == "__main__":
    cac_dong, w_cuoi_epoch = huan_luyen()
    print("epoch x1 x2 Yd  z      Y  e   w1    w2   cap_nhat")
    for d in cac_dong:
        print(f"{d['epoch']:5d} {d['x1']:2d} {d['x2']:2d} {d['y_d']:2d} {d['z']:6.2f} {d['y']:2d} {d['e']:2d} {d['w1']:5.2f} {d['w2']:5.2f}  {d['cap_nhat']}")
    print("Trong so cuoi:", w_cuoi_epoch[-1], "theta =", THETA)
    print("Da luu:", ve_cac_epoch(w_cuoi_epoch).name)
