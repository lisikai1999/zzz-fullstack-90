from typing import List, Tuple


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def gcd_with_steps(a: int, b: int) -> Tuple[int, List[dict]]:
    steps = []
    original_a, original_b = a, b
    while b:
        q = a // b
        r = a % b
        steps.append({
            "expression": f"{a} = {q} × {b} + {r}",
            "quotient": q,
            "remainder": r,
        })
        a, b = b, r
    steps.append({
        "expression": f"GCD({original_a}, {original_b}) = {a}",
        "quotient": None,
        "remainder": None,
    })
    return a, steps


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def mod_inverse(e: int, phi: int) -> int:
    g, x, _ = extended_gcd(e % phi, phi)
    if g != 1:
        raise ValueError(f"No modular inverse: gcd({e}, {phi}) = {g}")
    return x % phi


def mod_inverse_with_steps(e: int, phi: int) -> Tuple[int, List[dict]]:
    steps = []

    def ext_gcd_steps(a, b):
        if a == 0:
            return b, 0, 1, []
        g, x1, y1, sub_steps = ext_gcd_steps(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        sub_steps.append({
            "expression": f"Back-substitute: x = {y1} - ({b}//{a}) × {x1} = {x}, y = {x1}",
        })
        return g, x, y, sub_steps

    g, x, y, back_steps = ext_gcd_steps(e % phi, phi)
    if g != 1:
        raise ValueError(f"No modular inverse: gcd({e}, {phi}) = {g}")

    d = x % phi
    steps.extend(back_steps)
    steps.append({
        "expression": f"d = {x} mod {phi} = {d}",
    })
    steps.append({
        "expression": f"Verify: {e} × {d} mod {phi} = {(e * d) % phi}",
    })
    return d, steps


def mod_exp_steps(base: int, exponent: int, modulus: int) -> Tuple[int, List[dict]]:
    steps = []
    binary = bin(exponent)[2:]

    steps.append({
        "step_number": 1,
        "title": "将指数转为二进制",
        "expression": f"{exponent} 的二进制 = {binary}",
        "explanation": "使用从高位到低位的逐位平方-乘法",
        "intermediate_value": None,
        "bit": None,
        "operation": "init",
    })

    result = 1
    step_num = 2
    for i, bit in enumerate(binary):
        old_result = result
        squared = (result * result) % modulus
        if bit == '1':
            result = (squared * base) % modulus
            operation = "square_and_multiply"
            expr = f"{old_result}² mod {modulus} = {squared}; × {base} mod {modulus} = {result}"
        else:
            result = squared
            operation = "square"
            expr = f"{old_result}² mod {modulus} = {result}"

        steps.append({
            "step_number": step_num,
            "title": f"第 {i+1} 位 (bit={bit})",
            "expression": expr,
            "explanation": f"{'平方后乘以底数' if bit == '1' else '仅平方'}",
            "intermediate_value": result,
            "bit": int(bit),
            "operation": operation,
        })
        step_num += 1

    return result, steps


def find_coprime(phi: int) -> int:
    candidates = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 65537]
    for e in candidates:
        if e < phi and gcd(e, phi) == 1:
            return e
    for e in range(3, phi, 2):
        if gcd(e, phi) == 1:
            return e
    raise ValueError("Cannot find coprime")


def small_primes(limit: int = 1000) -> List[int]:
    return [n for n in range(2, limit) if is_prime(n)]
