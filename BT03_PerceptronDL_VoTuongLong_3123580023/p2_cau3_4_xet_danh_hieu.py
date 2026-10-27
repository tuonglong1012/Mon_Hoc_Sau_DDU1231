import matplotlib.pyplot as plt
import numpy as np

from ve_hinh import MAU_DUONG, luu_hinh, so, ve_perceptron

TRONG_SO = np.array([2.0, 1.0, 1.0])
NGUONG = 24.0
BIAS = -NGUONG
SINH_VIEN = [("SV1", 3.5, 9.0, 9.0), ("SV2", 3.0, 8.0, 9.0), ("SV3", 4.0, 10.0, 10.0)]
CAC_BIAS_MOI = [-22.0, -24.0, -26.0, -29.0]
DIEM_TOI_DA = np.array([4.0, 10.0, 10.0])


def step(v):
    return 1 if v >= 0 else 0


def diem_danh_hieu(x):
    return float(np.dot(TRONG_SO, x))


def phan_loai(bias=BIAS):
    kq = []
    for ten, *x in SINH_VIEN:
        d = diem_danh_hieu(x)
        v = d + bias
        y = step(v)
        kq.append({"ten": ten, "x": x, "D": d, "v": v, "y": y, "ket_qua": "Đạt" if y else "Không đạt"})
    return kq


def so_sanh_bias(cac_bias=CAC_BIAS_MOI):
    return [{"bias": b, "nguong": -b, "kq": phan_loai(b), "so_dat": sum(d["y"] for d in phan_loai(b))} for b in cac_bias]


def ve_mang():
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ve_perceptron(ax, ["1", "x₁ (Điểm TB)", "x₂ (Hạnh kiểm)", "x₃ (Rèn luyện)"], [BIAS, *TRONG_SO], "step")
    ax.set_title("Perceptron xét danh hiệu: y = step(2x₁ + x₂ + x₃ − 24)")
    return luu_hinh(fig, "p2_cau3_mang.png")


def ve_so_sanh_bias(cac_bias=CAC_BIAS_MOI):
    kq = phan_loai()
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ten = [d["ten"] for d in kq]
    diem = [d["D"] for d in kq]
    cot = ax.bar(ten, diem, color="#90CAF9", edgecolor="#1565C0", width=0.5)
    for c, d in zip(cot, diem):
        ax.text(c.get_x() + c.get_width() / 2, d + 0.3, f"D = {so(d)}", ha="center", fontsize=10)
    for k, b in enumerate(cac_bias):
        ax.axhline(-b, color=MAU_DUONG[k + 1], lw=1.8, ls="-" if b == BIAS else "--", label=f"b = {so(b)} → ngưỡng D ≥ {so(-b)}")
    ax.set_ylim(15, 31)
    ax.set_ylabel("Điểm danh hiệu D = 2x₁ + x₂ + x₃")
    ax.set_title("So sánh ngưỡng xét danh hiệu theo các giá trị bias")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    return luu_hinh(fig, "p2_cau4_so_sanh_bias.png")


if __name__ == "__main__":
    print("D toi da =", diem_danh_hieu(DIEM_TOI_DA))
    for d in phan_loai():
        print(f"{d['ten']}: x = {d['x']}, D = {d['D']:g}, v = {d['v']:g}, y = {d['y']}")
    for s in so_sanh_bias():
        print(f"b = {s['bias']:g} (D >= {s['nguong']:g}):", [(d["ten"], d["y"]) for d in s["kq"]])
    print("Da luu:", ve_mang().name, ve_so_sanh_bias().name)
