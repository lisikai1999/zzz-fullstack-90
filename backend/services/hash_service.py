from typing import List, Tuple

K_CONSTANTS = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
]

INIT_HASH = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
]


def right_rotate(val: int, n: int, bits: int = 32) -> int:
    return ((val >> n) | (val << (bits - n))) & ((1 << bits) - 1)


def mask32(val: int) -> int:
    return val & 0xFFFFFFFF


def pad_message(message_bytes: bytes) -> bytes:
    msg_len = len(message_bytes)
    bit_len = msg_len * 8
    message_bytes += b'\x80'
    while (len(message_bytes) % 64) != 56:
        message_bytes += b'\x00'
    message_bytes += bit_len.to_bytes(8, 'big')
    return message_bytes


def simplified_sha(message: str, hash_bits: int = 16, num_rounds: int = 16) -> dict:
    message_bytes = message.encode('utf-8')
    message_hex = message_bytes.hex()
    padded = pad_message(message_bytes)

    padding_explanation = (
        f"原始消息 {len(message_bytes)} 字节 → 添加 0x80 + 零填充 → "
        f"附加 64 位长度 → 总计 {len(padded)} 字节 ({len(padded)//64} 个 512 位块)"
    )

    h = list(INIT_HASH)
    blocks_result = []

    for block_idx in range(len(padded) // 64):
        block = padded[block_idx * 64:(block_idx + 1) * 64]
        block_hex = block.hex()

        W = []
        for i in range(16):
            W.append(int.from_bytes(block[i*4:(i+1)*4], 'big'))

        a, b, c, d, e, f, g, hh = h

        rounds = []
        for i in range(min(num_rounds, 16)):
            state_before = {
                "a": f"{a:08x}", "b": f"{b:08x}", "c": f"{c:08x}", "d": f"{d:08x}",
                "e": f"{e:08x}", "f": f"{f:08x}", "g": f"{g:08x}", "h": f"{hh:08x}",
            }

            sigma1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ ((~e & 0xFFFFFFFF) & g)
            temp1 = mask32(hh + sigma1 + ch + K_CONSTANTS[i] + W[i])

            sigma0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = mask32(sigma0 + maj)

            hh = g
            g = f
            f = e
            e = mask32(d + temp1)
            d = c
            c = b
            b = a
            a = mask32(temp1 + temp2)

            state_after = {
                "a": f"{a:08x}", "b": f"{b:08x}", "c": f"{c:08x}", "d": f"{d:08x}",
                "e": f"{e:08x}", "f": f"{f:08x}", "g": f"{g:08x}", "h": f"{hh:08x}",
            }

            operations = {
                "Σ1(e)": f"{sigma1:08x}",
                "Ch(e,f,g)": f"{ch:08x}",
                "temp1": f"{temp1:08x}",
                "Σ0(a)": f"{sigma0:08x}",
                "Maj(a,b,c)": f"{maj:08x}",
                "temp2": f"{temp2:08x}",
            }

            rounds.append({
                "round_number": i,
                "W_i": f"{W[i]:08x}",
                "K_i": f"{K_CONSTANTS[i]:08x}",
                "state_before": state_before,
                "state_after": state_after,
                "operations": operations,
            })

        h[0] = mask32(h[0] + a)
        h[1] = mask32(h[1] + b)
        h[2] = mask32(h[2] + c)
        h[3] = mask32(h[3] + d)
        h[4] = mask32(h[4] + e)
        h[5] = mask32(h[5] + f)
        h[6] = mask32(h[6] + g)
        h[7] = mask32(h[7] + hh)

        chain_value = ''.join(f"{x:08x}" for x in h)

        blocks_result.append({
            "block_index": block_idx,
            "block_data_hex": block_hex,
            "rounds": rounds,
            "chain_value_after": chain_value,
        })

    full_hash = ''.join(f"{x:08x}" for x in h)
    truncated_bits = hash_bits
    truncated_hex_len = (truncated_bits + 3) // 4
    final_hash = full_hash[:truncated_hex_len]

    return {
        "final_hash": final_hash,
        "hash_bits": hash_bits,
        "message_hex": message_hex,
        "padding_explanation": padding_explanation,
        "blocks": blocks_result,
    }


def quick_hash(data: bytes, hash_bits: int = 16) -> str:
    padded = pad_message(data)
    h = list(INIT_HASH)

    for block_idx in range(len(padded) // 64):
        block = padded[block_idx * 64:(block_idx + 1) * 64]
        W = [int.from_bytes(block[i*4:(i+1)*4], 'big') for i in range(16)]

        a, b, c, d, e, f, g, hh = h
        for i in range(16):
            sigma1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ ((~e & 0xFFFFFFFF) & g)
            temp1 = mask32(hh + sigma1 + ch + K_CONSTANTS[i] + W[i])
            sigma0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = mask32(sigma0 + maj)
            hh, g, f, e = g, f, e, mask32(d + temp1)
            d, c, b, a = c, b, a, mask32(temp1 + temp2)

        h[0] = mask32(h[0] + a)
        h[1] = mask32(h[1] + b)
        h[2] = mask32(h[2] + c)
        h[3] = mask32(h[3] + d)
        h[4] = mask32(h[4] + e)
        h[5] = mask32(h[5] + f)
        h[6] = mask32(h[6] + g)
        h[7] = mask32(h[7] + hh)

    full_hash = ''.join(f"{x:08x}" for x in h)
    truncated_hex_len = (hash_bits + 3) // 4
    return full_hash[:truncated_hex_len]
