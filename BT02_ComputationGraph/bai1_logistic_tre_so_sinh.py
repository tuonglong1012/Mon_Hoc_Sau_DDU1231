import numpy as np

from do_thi_tinh_toan import ve_do_thi_logistic

X = np.array([2.4, 3.3, 3.2, 2.5])
Y = np.array([0.0, 1.0, 1.0, 0.0])
GIOI_TINH = ["Nữ", "Nam", "Nam", "Nữ"]
THETA0_0 = 0.5
THETA1_0 = 0.5
ALPHA = 0.2
X_MOI = [2.8, 3.5]
NGUONG = 0.5


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def lan_truyen_tien(theta0, theta1, x):
    z = theta0 + theta1 * x
    return z, sigmoid(z)


def bce_tung_mau(y, y_hat):
    return -(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat))


def gradient(theta0, theta1):
    _, y_hat = lan_truyen_tien(theta0, theta1, X)
    sai_so = y_hat - Y
    return sai_so.mean(), (sai_so * X).mean()


def huan_luyen(so_lan_cap_nhat=2):
    lich_su = []
    theta0, theta1 = THETA0_0, THETA1_0
    for t in range(so_lan_cap_nhat + 1):
        z, y_hat = lan_truyen_tien(theta0, theta1, X)
        loss = bce_tung_mau(Y, y_hat)
        g0, g1 = gradient(theta0, theta1)
        lich_su.append(
            {
                "t": t,
                "theta0": theta0,
                "theta1": theta1,
                "z": z,
                "y_hat": y_hat,
                "sai_so": y_hat - Y,
                "sai_so_x": (y_hat - Y) * X,
                "loss": loss,
                "J": loss.mean(),
                "grad0": g0,
                "grad1": g1,
            }
        )
        theta0, theta1 = theta0 - ALPHA * g0, theta1 - ALPHA * g1
    return lich_su


def du_doan(theta0, theta1, danh_sach_x=X_MOI):
    ket_qua = []
    for x in danh_sach_x:
        z, p = lan_truyen_tien(theta0, theta1, x)
        nhan = int(p >= NGUONG)
        ket_qua.append({"x": x, "z": z, "p": p, "nhan": nhan, "gioi_tinh": "Nam" if nhan else "Nữ"})
    return ket_qua


def ve_do_thi(lich_su):
    return ve_do_thi_logistic(
        X[0],
        Y[0],
        lich_su[0]["theta1"],
        lich_su[0]["theta0"],
        {"w": r"\theta_1", "b": r"\theta_0", "x": "x"},
        "Bài 1 - Đồ thị tính toán Logistic Regression (mẫu 1: x = 2.4, y = 0, tham số khởi tạo)",
        "bai1_do_thi_tinh_toan.png",
    )


def in_bang(lich_su):
    for buoc in lich_su:
        print(f"\n===== t = {buoc['t']}: theta0 = {buoc['theta0']:.6f}, theta1 = {buoc['theta1']:.6f} =====")
        print(f"{'i':>2} {'x':>5} {'y':>3} {'z':>10} {'y_hat':>10} {'loss':>10} {'y_hat-y':>10} {'(y_hat-y)x':>12}")
        for i in range(len(X)):
            print(
                f"{i + 1:>2} {X[i]:>5} {int(Y[i]):>3} {buoc['z'][i]:>10.6f} {buoc['y_hat'][i]:>10.6f} "
                f"{buoc['loss'][i]:>10.6f} {buoc['sai_so'][i]:>10.6f} {buoc['sai_so_x'][i]:>12.6f}"
            )
        print(f"J = {buoc['J']:.6f}   dJ/dtheta0 = {buoc['grad0']:.6f}   dJ/dtheta1 = {buoc['grad1']:.6f}")


if __name__ == "__main__":
    lich_su = huan_luyen(2)
    in_bang(lich_su)
    print("\nLoss trung bình qua các thời điểm:")
    for buoc in lich_su:
        print(f"  J(theta^({buoc['t']})) = {buoc['J']:.6f}")
    cuoi = lich_su[-1]
    print("\nDự đoán với mô hình sau 2 lần cập nhật:")
    for kq in du_doan(cuoi["theta0"], cuoi["theta1"]):
        print(f"  x = {kq['x']} kg: z = {kq['z']:.6f}, P(Nam) = {kq['p']:.6f} -> {kq['gioi_tinh']}")
    print("\nĐã lưu:", ve_do_thi(lich_su))
