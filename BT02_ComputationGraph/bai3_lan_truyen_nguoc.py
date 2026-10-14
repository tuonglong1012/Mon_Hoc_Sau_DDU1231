from do_thi_tinh_toan import ve_do_thi

GIA_TRI_DAU = {"a": 2.0, "b": 3.0, "c": 4.0, "d": 5.0}
ALPHA = 0.01


def ham_J(a, b, c, d):
    return 3 * a + 2 * (4 * b + 5 * c * d)


def lan_truyen_tien(a, b, c, d):
    u1 = 3 * a
    u2 = 4 * b
    u3 = c * d
    u4 = 5 * u3
    u5 = u2 + u4
    u6 = 2 * u5
    J = u1 + u6
    return {"a": a, "b": b, "c": c, "d": d, "u1": u1, "u2": u2, "u3": u3, "u4": u4, "u5": u5, "u6": u6, "J": J}


def dao_ham_cuc_bo(v):
    return {
        ("u1", "a"): 3.0,
        ("u2", "b"): 4.0,
        ("u3", "c"): v["d"],
        ("u3", "d"): v["c"],
        ("u4", "u3"): 5.0,
        ("u5", "u2"): 1.0,
        ("u5", "u4"): 1.0,
        ("u6", "u5"): 2.0,
        ("J", "u1"): 1.0,
        ("J", "u6"): 1.0,
    }


def lan_truyen_nguoc(v):
    cb = dao_ham_cuc_bo(v)
    g = {"J": 1.0}
    g["u1"] = g["J"] * cb[("J", "u1")]
    g["u6"] = g["J"] * cb[("J", "u6")]
    g["u5"] = g["u6"] * cb[("u6", "u5")]
    g["u2"] = g["u5"] * cb[("u5", "u2")]
    g["u4"] = g["u5"] * cb[("u5", "u4")]
    g["u3"] = g["u4"] * cb[("u4", "u3")]
    g["a"] = g["u1"] * cb[("u1", "a")]
    g["b"] = g["u2"] * cb[("u2", "b")]
    g["c"] = g["u3"] * cb[("u3", "c")]
    g["d"] = g["u3"] * cb[("u3", "d")]
    return g


def dao_ham_khai_trien(a, b, c, d):
    return {"a": 3.0, "b": 8.0, "c": 10.0 * d, "d": 10.0 * c}


def cap_nhat_gradient_descent(tham_so, grad, alpha=ALPHA):
    return {k: tham_so[k] - alpha * grad[k] for k in ("a", "b", "c", "d")}


def tinh_bang_pytorch(tham_so):
    import torch

    t = {k: torch.tensor(v, dtype=torch.float64, requires_grad=True) for k, v in tham_so.items()}
    u1 = 3 * t["a"]
    u2 = 4 * t["b"]
    u3 = t["c"] * t["d"]
    u4 = 5 * u3
    u5 = u2 + u4
    u6 = 2 * u5
    J = u1 + u6
    J.backward()
    return J.item(), {k: t[k].grad.item() for k in ("a", "b", "c", "d")}


def ve_do_thi_bai3(v, g):
    nut = {
        "a": {"pos": (0, 4.2), "kind": "input", "label": "$a$", "value": f"{v['a']:g}"},
        "b": {"pos": (0, 2.6), "kind": "input", "label": "$b$", "value": f"{v['b']:g}"},
        "c": {"pos": (0, 1.0), "kind": "input", "label": "$c$", "value": f"{v['c']:g}"},
        "d": {"pos": (0, -0.6), "kind": "input", "label": "$d$", "value": f"{v['d']:g}"},
        "u1": {"pos": (3.0, 4.2), "kind": "op", "name": "$u_1=3a$", "label": r"$\times 3$", "value": f"u1 = {v['u1']:g}"},
        "u2": {"pos": (3.0, 2.6), "kind": "op", "name": "$u_2=4b$", "label": r"$\times 4$", "value": f"u2 = {v['u2']:g}"},
        "u3": {"pos": (3.0, 0.2), "kind": "op", "name": "$u_3=cd$", "label": r"$\times$", "value": f"u3 = {v['u3']:g}"},
        "u4": {"pos": (5.6, 0.2), "kind": "op", "name": "$u_4=5u_3$", "label": r"$\times 5$", "value": f"u4 = {v['u4']:g}"},
        "u5": {"pos": (8.0, 1.6), "kind": "op", "name": "$u_5=u_2+u_4$", "label": "$+$", "value": f"u5 = {v['u5']:g}"},
        "u6": {"pos": (10.4, 1.6), "kind": "op", "name": "$u_6=2u_5$", "label": r"$\times 2$", "value": f"u6 = {v['u6']:g}"},
        "Jop": {"pos": (12.8, 3.0), "kind": "op", "name": "$J=u_1+u_6$", "label": "$+$", "value": f"J = {v['J']:g}"},
        "J": {"pos": (15.0, 3.0), "kind": "output", "label": "$J$", "value": None},
    }
    canh = [
        ("a", "u1", f"$\\partial J/\\partial a$ = {g['a']:g}"),
        ("b", "u2", f"$\\partial J/\\partial b$ = {g['b']:g}"),
        ("c", "u3", f"$\\partial J/\\partial c$ = {g['c']:g}"),
        ("d", "u3", f"$\\partial J/\\partial d$ = {g['d']:g}", -0.95),
        ("u3", "u4", f"$\\partial J/\\partial u_3$ = {g['u3']:g}", -0.95),
        ("u2", "u5", f"$\\partial J/\\partial u_2$ = {g['u2']:g}"),
        ("u4", "u5", f"$\\partial J/\\partial u_4$ = {g['u4']:g}", -1.0),
        ("u5", "u6", f"$\\partial J/\\partial u_5$ = {g['u5']:g}", -0.95),
        ("u1", "Jop", f"$\\partial J/\\partial u_1$ = {g['u1']:g}"),
        ("u6", "Jop", f"$\\partial J/\\partial u_6$ = {g['u6']:g}", -1.0),
        ("Jop", "J", "$\\partial J/\\partial J$ = 1"),
    ]
    return ve_do_thi(nut, canh, "Bài 3 - Đồ thị tính toán J = 3a + 2(4b + 5cd) tại a = 2, b = 3, c = 4, d = 5", "bai3_do_thi_tinh_toan.png", kich_thuoc=(15, 7))


if __name__ == "__main__":
    v = lan_truyen_tien(**GIA_TRI_DAU)
    print("Lan truyền tiến:")
    for k in ("u1", "u2", "u3", "u4", "u5", "u6", "J"):
        print(f"  {k} = {v[k]:g}")
    print("\nĐạo hàm cục bộ:")
    for (ra, vao), gt in dao_ham_cuc_bo(v).items():
        print(f"  d{ra}/d{vao} = {gt:g}")
    g = lan_truyen_nguoc(v)
    print("\nLan truyền ngược:")
    for k in ("J", "u1", "u6", "u5", "u2", "u4", "u3", "a", "b", "c", "d"):
        print(f"  dJ/d{k} = {g[k]:g}")
    kt = dao_ham_khai_trien(**GIA_TRI_DAU)
    print("\nKiểm chứng bằng khai triển J = 3a + 8b + 10cd:")
    for k in ("a", "b", "c", "d"):
        print(f"  dJ/d{k} = {kt[k]:g}  (đồ thị: {g[k]:g}, khớp: {abs(kt[k] - g[k]) < 1e-12})")
    moi = cap_nhat_gradient_descent(GIA_TRI_DAU, g)
    J_moi = ham_J(**moi)
    print("\nGradient Descent (alpha = 0.01):")
    for k in ("a", "b", "c", "d"):
        print(f"  {k}' = {GIA_TRI_DAU[k]:g} - {ALPHA} * {g[k]:g} = {moi[k]:.4f}")
    print(f"  J' = {J_moi:.4f}, J = {v['J']:g}, giảm {v['J'] - J_moi:.4f}")
    J_pt, g_pt = tinh_bang_pytorch(GIA_TRI_DAU)
    print(f"\nPyTorch Autograd: J = {J_pt:g}")
    for k in ("a", "b", "c", "d"):
        print(f"  {k}.grad = {g_pt[k]:g}  (thủ công: {g[k]:g}, khớp: {abs(g_pt[k] - g[k]) < 1e-12})")
    print("\nĐã lưu:", ve_do_thi_bai3(v, g))
