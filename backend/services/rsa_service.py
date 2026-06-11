from typing import Tuple, List
from utils.math_helpers import (
    is_prime, gcd, gcd_with_steps, mod_inverse_with_steps,
    mod_exp_steps, find_coprime,
)


def generate_keys_with_steps(p: int, q: int, e_candidate: int = None) -> dict:
    if not is_prime(p):
        raise ValueError(f"{p} 不是素数")
    if not is_prime(q):
        raise ValueError(f"{q} 不是素数")
    if p == q:
        raise ValueError("p 和 q 不能相同")

    steps = []

    n = p * q
    steps.append({
        "step_number": 1,
        "title": "计算 n = p × q",
        "expression": f"n = {p} × {q} = {n}",
        "explanation": "n 是公钥和私钥共用的模数",
    })

    phi_n = (p - 1) * (q - 1)
    steps.append({
        "step_number": 2,
        "title": "计算欧拉函数 φ(n) = (p-1)(q-1)",
        "expression": f"φ({n}) = ({p}-1)({q}-1) = {p-1} × {q-1} = {phi_n}",
        "explanation": "φ(n) 表示小于 n 且与 n 互素的正整数个数",
    })

    if e_candidate is None:
        e = find_coprime(phi_n)
    else:
        e = e_candidate

    gcd_val, gcd_steps = gcd_with_steps(e, phi_n)
    if gcd_val != 1:
        raise ValueError(f"e={e} 与 φ(n)={phi_n} 不互素，gcd={gcd_val}")

    steps.append({
        "step_number": 3,
        "title": "选择公钥指数 e (需与 φ(n) 互素)",
        "expression": f"验证 gcd({e}, {phi_n}) = 1",
        "explanation": f"e 必须与 φ(n) 互素，确保加密是可逆的",
        "sub_steps": gcd_steps,
    })

    d, inv_steps = mod_inverse_with_steps(e, phi_n)
    steps.append({
        "step_number": 4,
        "title": "计算私钥指数 d = e⁻¹ mod φ(n)",
        "expression": f"d = {e}⁻¹ mod {phi_n} = {d}",
        "explanation": "使用扩展欧几里得算法求模逆元，使得 e×d ≡ 1 (mod φ(n))",
        "sub_steps": inv_steps,
    })

    return {
        "steps": steps,
        "public_key": {"e": e, "n": n},
        "private_key": {"d": d, "n": n},
        "parameters": {"p": p, "q": q, "phi_n": phi_n, "n": n, "e": e, "d": d},
    }


def encrypt_with_steps(message: int, e: int, n: int) -> dict:
    if message >= n:
        raise ValueError(f"消息 m={message} 必须小于 n={n}")
    if message < 0:
        raise ValueError("消息不能为负数")

    ciphertext, steps = mod_exp_steps(message, e, n)

    return {
        "result": ciphertext,
        "steps": steps,
        "summary": {
            "original_message": message,
            "exponent": e,
            "modulus": n,
            "exponent_binary": bin(e)[2:],
            "ciphertext": ciphertext,
        },
    }


def decrypt_with_steps(ciphertext: int, d: int, n: int) -> dict:
    if ciphertext >= n:
        raise ValueError(f"密文 c={ciphertext} 必须小于 n={n}")

    message, steps = mod_exp_steps(ciphertext, d, n)

    return {
        "result": message,
        "steps": steps,
        "summary": {
            "ciphertext": ciphertext,
            "exponent": d,
            "modulus": n,
            "exponent_binary": bin(d)[2:],
            "decrypted_message": message,
        },
    }
