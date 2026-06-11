from utils.math_helpers import mod_exp_steps, is_prime


def compute_exchange_steps(p: int, g: int, a_private: int, b_private: int) -> dict:
    steps = []

    steps.append({
        "step_number": 1,
        "actor": "public",
        "title": "协商公开参数",
        "expression": f"素数 p = {p}, 生成元 g = {g}",
        "explanation": "双方在不安全信道上协商公开参数",
        "result": None,
    })

    A, a_sub_steps = mod_exp_steps(g, a_private, p)
    steps.append({
        "step_number": 2,
        "actor": "alice",
        "title": "Alice 计算公开值 A = g^a mod p",
        "expression": f"A = {g}^{a_private} mod {p} = {A}",
        "explanation": "Alice 用私钥 a 计算公开值并发送给 Bob",
        "result": A,
        "sub_steps": [s for s in a_sub_steps if s.get("intermediate_value") is not None],
    })

    B, b_sub_steps = mod_exp_steps(g, b_private, p)
    steps.append({
        "step_number": 3,
        "actor": "bob",
        "title": "Bob 计算公开值 B = g^b mod p",
        "expression": f"B = {g}^{b_private} mod {p} = {B}",
        "explanation": "Bob 用私钥 b 计算公开值并发送给 Alice",
        "result": B,
        "sub_steps": [s for s in b_sub_steps if s.get("intermediate_value") is not None],
    })

    steps.append({
        "step_number": 4,
        "actor": "exchange",
        "title": "交换公开值",
        "expression": f"Alice 发送 A={A} 给 Bob；Bob 发送 B={B} 给 Alice",
        "explanation": "窃听者可以看到 A 和 B，但无法推导出共享密钥",
        "result": None,
    })

    s_alice, s_alice_steps = mod_exp_steps(B, a_private, p)
    steps.append({
        "step_number": 5,
        "actor": "alice",
        "title": "Alice 计算共享密钥 s = B^a mod p",
        "expression": f"s = {B}^{a_private} mod {p} = {s_alice}",
        "explanation": "Alice 用收到的 B 和自己的私钥 a 计算共享密钥",
        "result": s_alice,
        "sub_steps": [s for s in s_alice_steps if s.get("intermediate_value") is not None],
    })

    s_bob, s_bob_steps = mod_exp_steps(A, b_private, p)
    steps.append({
        "step_number": 6,
        "actor": "bob",
        "title": "Bob 计算共享密钥 s = A^b mod p",
        "expression": f"s = {A}^{b_private} mod {p} = {s_bob}",
        "explanation": "Bob 用收到的 A 和自己的私钥 b 计算共享密钥",
        "result": s_bob,
        "sub_steps": [s for s in s_bob_steps if s.get("intermediate_value") is not None],
    })

    return {
        "steps": steps,
        "shared_secret": s_alice,
        "security_note": (
            f"窃听者看到 p={p}, g={g}, A={A}, B={B}，"
            f"但必须解决离散对数问题才能求出 a 或 b"
        ),
    }


def compute_mitm_steps(p: int, g: int, a_private: int, b_private: int, m_private: int) -> dict:
    steps = []

    steps.append({
        "step_number": 1,
        "actor": "public",
        "title": "公开参数",
        "expression": f"p = {p}, g = {g}",
        "explanation": "公开协商的参数",
        "result": None,
    })

    A, _ = mod_exp_steps(g, a_private, p)
    steps.append({
        "step_number": 2,
        "actor": "alice",
        "title": "Alice 计算 A = g^a mod p",
        "expression": f"A = {g}^{a_private} mod {p} = {A}",
        "explanation": "Alice 的公开值",
        "result": A,
    })

    M, _ = mod_exp_steps(g, m_private, p)
    steps.append({
        "step_number": 3,
        "actor": "mallory",
        "title": "Mallory 截获 A，发送自己的 M 给 Bob",
        "expression": f"M = {g}^{m_private} mod {p} = {M}",
        "explanation": "Mallory 用自己的私钥生成公开值，冒充 Alice 发给 Bob",
        "result": M,
    })

    B, _ = mod_exp_steps(g, b_private, p)
    steps.append({
        "step_number": 4,
        "actor": "bob",
        "title": "Bob 计算 B = g^b mod p",
        "expression": f"B = {g}^{b_private} mod {p} = {B}",
        "explanation": "Bob 的公开值",
        "result": B,
    })

    steps.append({
        "step_number": 5,
        "actor": "mallory",
        "title": "Mallory 截获 B，发送 M 给 Alice",
        "expression": f"Mallory 发送 M={M} 给 Alice (冒充 Bob)",
        "explanation": "Alice 以为收到的是 Bob 的公开值",
        "result": None,
    })

    s_am, _ = mod_exp_steps(A, m_private, p)
    s_ma, _ = mod_exp_steps(M, a_private, p)
    steps.append({
        "step_number": 6,
        "actor": "mallory",
        "title": "Mallory 与 Alice 的共享密钥",
        "expression": f"s_MA = A^m mod p = {A}^{m_private} mod {p} = {s_am}",
        "explanation": f"Alice 计算的是 M^a = {s_ma}，两者相等: {s_am == s_ma}",
        "result": s_am,
    })

    s_bm, _ = mod_exp_steps(B, m_private, p)
    s_mb, _ = mod_exp_steps(M, b_private, p)
    steps.append({
        "step_number": 7,
        "actor": "mallory",
        "title": "Mallory 与 Bob 的共享密钥",
        "expression": f"s_MB = B^m mod p = {B}^{m_private} mod {p} = {s_bm}",
        "explanation": f"Bob 计算的是 M^b = {s_mb}，两者相等: {s_bm == s_mb}",
        "result": s_bm,
    })

    steps.append({
        "step_number": 8,
        "actor": "summary",
        "title": "攻击结果",
        "expression": f"Alice-Mallory 密钥: {s_am}, Mallory-Bob 密钥: {s_bm}",
        "explanation": "Mallory 可以解密双方的消息，修改后重新加密转发，双方毫无察觉",
        "result": None,
    })

    return {
        "steps": steps,
        "alice_mallory_secret": s_am,
        "mallory_bob_secret": s_bm,
        "explanation": "中间人攻击成功：Mallory 分别与 Alice 和 Bob 建立了不同的共享密钥",
    }


def compute_color_mixing(alice_color: str, bob_color: str, common_color: str) -> dict:
    import colorsys

    def hex_to_rgb(h: str):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(r, g, b):
        return f"#{int(r):02x}{int(g):02x}{int(b):02x}"

    def rgb_to_hsl(r, g, b):
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        return h * 360, s * 100, l * 100

    def hsl_to_rgb(h, s, l):
        r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
        return round(r * 255), round(g * 255), round(b * 255)

    def mix(c1: str, c2: str) -> str:
        r1, g1, b1 = hex_to_rgb(c1)
        r2, g2, b2 = hex_to_rgb(c2)
        h1, s1, l1 = rgb_to_hsl(r1, g1, b1)
        h2, s2, l2 = rgb_to_hsl(r2, g2, b2)
        h = (h1 + h2) % 360
        s = max(40, (s1 + s2) / 2)
        l = 30 + ((l1 + l2) % 40)
        r, g, b = hsl_to_rgb(h, s, l)
        return rgb_to_hex(r, g, b)

    alice_mixed = mix(common_color, alice_color)
    bob_mixed = mix(common_color, bob_color)
    alice_final = mix(bob_mixed, alice_color)
    bob_final = mix(alice_mixed, bob_color)

    return {
        "common_color": common_color,
        "alice": {
            "private_color": alice_color,
            "mixed_public": alice_mixed,
            "final_shared": alice_final,
        },
        "bob": {
            "private_color": bob_color,
            "mixed_public": bob_mixed,
            "final_shared": bob_final,
        },
        "explanation": (
            "颜色混合类比：双方各自将私有颜色混入公共颜色，交换混合结果后，"
            "再各自混入自己的私有颜色，最终得到相同的颜色。"
            "窃听者只能看到混合后的颜色，无法分离出私有颜色。"
        ),
        "animation_keyframes": [
            {"time": 0, "phase": "show_common", "description": "展示公共颜色"},
            {"time": 1, "phase": "mix_private", "description": "各自混入私有颜色"},
            {"time": 2, "phase": "exchange", "description": "交换混合后的颜色"},
            {"time": 3, "phase": "final_mix", "description": "再次混入自己的私有颜色"},
            {"time": 4, "phase": "reveal", "description": "双方得到相同的最终颜色"},
        ],
    }
