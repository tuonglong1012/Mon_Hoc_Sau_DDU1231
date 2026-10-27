import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from do_thi_tinh_toan import THU_MUC_HINH, ve_do_thi_logistic

X = np.array([132, 141, 88, 154, 151, 102, 119, 106, 102, 143, 76, 168, 94, 186], dtype=float)
Y = np.array([1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1], dtype=float)
DANH_GIA = ["G" if y == 1 else "B" for y in Y]
TRUNG_TAM = 130.0
DO_RONG = 50.0
W0 = 0.0
B0 = 0.0
ALPHA = 0.2
SO_LAN_LAP = 1000
X_MOI = [125.0, 160.0]
NGUONG = 0.5


def chuan_hoa(x):
    return (np.asarray(x, dtype=float) - TRUNG_TAM) / DO_RONG


X_CHUAN = chuan_hoa(X)


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def lan_truyen_tien(w, b, x_chuan):
    z = w * x_chuan + b
    return z, sigmoid(z)


def bce_tung_mau(y, y_hat):
    return -(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat))


def ham_mat_mat(w, b):
    _, y_hat = lan_truyen_tien(w, b, X_CHUAN)
    return bce_tung_mau(Y, y_hat).mean()


def gradient(w, b):
    _, y_hat = lan_truyen_tien(w, b, X_CHUAN)
    sai_so = y_hat - Y
    return (sai_so * X_CHUAN).mean(), sai_so.mean()


def huan_luyen(so_lan_cap_nhat):
    lich_su = []
    w, b = W0, B0
    for t in range(so_lan_cap_nhat + 1):
        z, y_hat = lan_truyen_tien(w, b, X_CHUAN)
        loss = bce_tung_mau(Y, y_hat)
        gw, gb = gradient(w, b)
        lich_su.append(
            {
                "t": t,
                "w": w,
                "b": b,
                "z": z,
                "y_hat": y_hat,
                "sai_so": y_hat - Y,
                "sai_so_x": (y_hat - Y) * X_CHUAN,
                "loss": loss,
                "J": loss.mean(),
                "grad_w": gw,
                "grad_b": gb,
            }
        )
        w, b = w - ALPHA * gw, b - ALPHA * gb
    return lich_su


def huan_luyen_nhanh(so_lan_lap=SO_LAN_LAP):
    w, b = W0, B0
    ds_loss = [ham_mat_mat(w, b)]
    for _ in range(so_lan_lap):
        gw, gb = gradient(w, b)
        w, b = w - ALPHA * gw, b - ALPHA * gb
        ds_loss.append(ham_mat_mat(w, b))
    return w, b, np.array(ds_loss)


def huan_luyen_pytorch(so_lan_lap=SO_LAN_LAP):
    import torch

    x = torch.tensor(X_CHUAN, dtype=torch.float64)
    y = torch.tensor(Y, dtype=torch.float64)
    w = torch.tensor(W0, dtype=torch.float64, requires_grad=True)
    b = torch.tensor(B0, dtype=torch.float64, requires_grad=True)
    ds_loss = []
    for _ in range(so_lan_lap):
        y_hat = torch.sigmoid(w * x + b)
        loss = torch.nn.functional.binary_cross_entropy(y_hat, y)
        ds_loss.append(loss.item())
        loss.backward()
        with torch.no_grad():
            w -= ALPHA * w.grad
            b -= ALPHA * b.grad
        w.grad.zero_()
        b.grad.zero_()
    with torch.no_grad():
        ds_loss.append(torch.nn.functional.binary_cross_entropy(torch.sigmoid(w * x + b), y).item())
    return w.item(), b.item(), np.array(ds_loss)


def du_doan(w, b, danh_sach_x=X_MOI):
    ket_qua = []
    for x in danh_sach_x:
        xc = chuan_hoa(x)
        z, p = lan_truyen_tien(w, b, xc)
        ket_qua.append({"x": x, "x_chuan": float(xc), "z": float(z), "p": float(p), "nhan": int(p >= NGUONG)})
    return ket_qua


def danh_gia(w, b):
    _, p = lan_truyen_tien(w, b, X_CHUAN)
    y_du_doan = (p >= NGUONG).astype(int)
    y_that = Y.astype(int)
    tp = int(np.sum((y_du_doan == 1) & (y_that == 1)))
    tn = int(np.sum((y_du_doan == 0) & (y_that == 0)))
    fp = int(np.sum((y_du_doan == 1) & (y_that == 0)))
    fn = int(np.sum((y_du_doan == 0) & (y_that == 1)))
    accuracy = (tp + tn) / len(Y)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "p": p,
        "y_du_doan": y_du_doan,
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def ranh_gioi_quyet_dinh(w, b):
    x_chuan = -b / w
    return x_chuan, TRUNG_TAM + DO_RONG * x_chuan


def ve_du_lieu():
    THU_MUC_HINH.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.scatter(X[Y == 1], Y[Y == 1], s=70, c="#2E7D32", label="G - Tốt (y = 1)", zorder=3)
    ax.scatter(X[Y == 0], Y[Y == 0], s=70, c="#C62828", marker="s", label="B - Không tốt (y = 0)", zorder=3)
    for i in range(len(X)):
        ax.annotate(str(i + 1), (X[i], Y[i]), textcoords="offset points", xytext=(0, 9 if Y[i] else -15), ha="center", fontsize=8)
    ax.set_xlabel("Thời lượng phim x (phút)")
    ax.set_ylabel("Nhãn đánh giá y")
    ax.set_yticks([0, 1])
    ax.set_ylim(-0.3, 1.3)
    ax.set_title("Bài 2a - Phân bố 14 bộ phim theo thời lượng và nhãn đánh giá")
    ax.grid(alpha=0.3)
    ax.legend(loc="center right")
    duong_dan = THU_MUC_HINH / "bai2a_du_lieu.png"
    fig.savefig(duong_dan, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return duong_dan


def ve_sigmoid(cac_mo_hinh, ten_file, tieu_de):
    THU_MUC_HINH.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    x_ve = np.linspace(60, 200, 400)
    ax.scatter(X[Y == 1], Y[Y == 1], s=70, c="#2E7D32", label="G - Tốt (y = 1)", zorder=3)
    ax.scatter(X[Y == 0], Y[Y == 0], s=70, c="#C62828", marker="s", label="B - Không tốt (y = 0)", zorder=3)
    mau = ["#1565C0", "#6A1B9A", "#EF6C00"]
    for k, (ten, w, b) in enumerate(cac_mo_hinh):
        _, p = lan_truyen_tien(w, b, chuan_hoa(x_ve))
        ax.plot(x_ve, p, color=mau[k], lw=2, label=f"{ten}: w = {w:.4f}, b = {b:.4f}")
        _, x_rg = ranh_gioi_quyet_dinh(w, b)
        ax.axvline(x_rg, color=mau[k], ls="--", lw=1.3, label=f"Ranh giới ({ten}): x = {x_rg:.2f} phút")
    ax.axhline(NGUONG, color="gray", ls=":", lw=1.2, label="Ngưỡng 0.5")
    ax.set_xlabel("Thời lượng phim x (phút)")
    ax.set_ylabel("P(phim tốt) = ŷ")
    ax.set_ylim(-0.08, 1.08)
    ax.set_title(tieu_de)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8, loc="center left", bbox_to_anchor=(1.01, 0.5))
    duong_dan = THU_MUC_HINH / ten_file
    fig.savefig(duong_dan, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return duong_dan


def ve_loss(ds_loss_numpy, ds_loss_torch, lich_su_2_buoc):
    THU_MUC_HINH.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for ax, gioi_han in zip(axes, [len(ds_loss_numpy), 21]):
        ax.plot(np.arange(gioi_han), ds_loss_numpy[:gioi_han], color="#1565C0", lw=2, label="NumPy")
        ax.plot(np.arange(gioi_han), ds_loss_torch[:gioi_han], color="#EF6C00", lw=1.2, ls="--", label="PyTorch")
        ax.scatter([b["t"] for b in lich_su_2_buoc], [b["J"] for b in lich_su_2_buoc], color="#C62828", zorder=4, label="Câu (e): t = 0, 1, 2")
        ax.set_xlabel("Số lần lặp")
        ax.set_ylabel("J(w, b)")
        ax.grid(alpha=0.3)
        ax.legend()
    axes[0].set_title("Hàm mất mát qua 1000 lần lặp")
    axes[1].set_title("Phóng to 20 lần lặp đầu")
    duong_dan = THU_MUC_HINH / "bai2j_loss.png"
    fig.savefig(duong_dan, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return duong_dan


def ve_do_thi(lich_su):
    return ve_do_thi_logistic(
        X_CHUAN[0],
        Y[0],
        lich_su[0]["w"],
        lich_su[0]["b"],
        {"w": "w", "b": "b", "x": "x'"},
        "Bài 2 - Đồ thị tính toán Logistic Regression (mẫu 1: x = 132, x' = 0.04, y = 1, tham số khởi tạo)",
        "bai2_do_thi_tinh_toan.png",
    )


def in_bang(lich_su):
    for buoc in lich_su:
        print(f"\n===== t = {buoc['t']}: w = {buoc['w']:.6f}, b = {buoc['b']:.6f} =====")
        print(f"{'i':>2} {'x':>5} {'x_chuan':>8} {'y':>3} {'z':>10} {'y_hat':>10} {'loss':>10} {'y_hat-y':>10} {'(y_hat-y)x':>12}")
        for i in range(len(X)):
            print(
                f"{i + 1:>2} {X[i]:>5.0f} {X_CHUAN[i]:>8.2f} {int(Y[i]):>3} {buoc['z'][i]:>10.6f} {buoc['y_hat'][i]:>10.6f} "
                f"{buoc['loss'][i]:>10.6f} {buoc['sai_so'][i]:>10.6f} {buoc['sai_so_x'][i]:>12.6f}"
            )
        print(f"J = {buoc['J']:.6f}   dJ/dw = {buoc['grad_w']:.6f}   dJ/db = {buoc['grad_b']:.6f}")


def in_danh_gia(ten, kq):
    print(f"\n{ten}")
    print("  Nhãn dự đoán:", kq["y_du_doan"].tolist())
    print("  Nhãn thực tế:", Y.astype(int).tolist())
    print(f"  TP = {kq['TP']}, FP = {kq['FP']}, FN = {kq['FN']}, TN = {kq['TN']}")
    print(f"  Accuracy = {kq['accuracy']:.4f}, Precision = {kq['precision']:.4f}, Recall = {kq['recall']:.4f}, F1 = {kq['f1']:.4f}")


if __name__ == "__main__":
    lich_su = huan_luyen(2)
    in_bang(lich_su)
    w2, b2 = lich_su[-1]["w"], lich_su[-1]["b"]
    print(f"\nMô hình sau 2 lần cập nhật: y_hat = sigmoid({w2:.6f} * (x - 130)/50 + {b2:.6f})")
    for kq in du_doan(w2, b2):
        print(f"  x = {kq['x']:.0f} phút: x' = {kq['x_chuan']:.2f}, z = {kq['z']:.6f}, P(tốt) = {kq['p']:.6f}, nhãn = {kq['nhan']}")
    in_danh_gia("Đánh giá mô hình sau 2 lần cập nhật:", danh_gia(w2, b2))
    xc, xr = ranh_gioi_quyet_dinh(w2, b2)
    print(f"\nRanh giới quyết định: x' = {xc:.6f}  <=>  x = {xr:.4f} phút")
    w_np, b_np, loss_np = huan_luyen_nhanh()
    w_pt, b_pt, loss_pt = huan_luyen_pytorch()
    print(f"\nNumPy 1000 lần lặp:   w = {w_np:.6f}, b = {b_np:.6f}, J = {loss_np[-1]:.6f}")
    print(f"PyTorch 1000 lần lặp: w = {w_pt:.6f}, b = {b_pt:.6f}, J = {loss_pt[-1]:.6f}")
    print(f"Ranh giới sau 1000 lần lặp: x = {ranh_gioi_quyet_dinh(w_np, b_np)[1]:.4f} phút")
    for kq in du_doan(w_np, b_np):
        print(f"  x = {kq['x']:.0f} phút: P(tốt) = {kq['p']:.6f}, nhãn = {kq['nhan']}")
    in_danh_gia("Đánh giá mô hình sau 1000 lần lặp:", danh_gia(w_np, b_np))
    print("\nĐã lưu:")
    print(" ", ve_du_lieu())
    print(" ", ve_sigmoid([("Sau 2 lần cập nhật", w2, b2)], "bai2h_sigmoid.png", "Bài 2h - Đường Sigmoid và ranh giới quyết định sau 2 lần cập nhật"))
    print(" ", ve_sigmoid([("Sau 2 lần cập nhật", w2, b2), ("Sau 1000 lần lặp", w_np, b_np)], "bai2j_so_sanh_sigmoid.png", "Bài 2j - So sánh mô hình sau 2 lần cập nhật và sau 1000 lần lặp"))
    print(" ", ve_loss(loss_np, loss_pt, lich_su))
    print(" ", ve_do_thi(lich_su))
