"""Bo kiem thu Tiny A5/1 va A5/1"""
from pathlib import Path
from tempfile import TemporaryDirectory

from tiny_a5_1 import TinyA5_1
from a5_1 import A5_1


def bits(s):
    return [int(ch) for ch in s]


def bitstr(values):
    return "".join(map(str, values))


TINY_KEY_CLASS = "10010101001110100110000"
TINY_KEY_GROUP = "10110100101101101001011"
FULL_KEY = "1010010010111000101010111001001010011010011010101110100100101011"

def reference_a51(key_str, n):
    x = int(key_str[:19], 2)
    y = int(key_str[19:41], 2)
    z = int(key_str[41:], 2)
    mx, my, mz = (1 << 19) - 1, (1 << 22) - 1, (1 << 23) - 1

    def at(reg, length, index):
        return (reg >> (length - index - 1)) & 1

    out = []
    for _ in range(n):
        a, b, c = at(x, 19, 8), at(y, 22, 10), at(z, 23, 10)
        majority = 1 if a + b + c >= 2 else 0
        if a == majority:
            feedback = at(x, 19, 13) ^ at(x, 19, 16) ^ at(x, 19, 17) ^ at(x, 19, 18)
            x = (feedback << 18) | (x >> 1)
            x &= mx
        if b == majority:
            feedback = at(y, 22, 20) ^ at(y, 22, 21)
            y = (feedback << 21) | (y >> 1)
            y &= my
        if c == majority:
            feedback = at(z, 23, 7) ^ at(z, 23, 20) ^ at(z, 23, 21) ^ at(z, 23, 22)
            z = (feedback << 22) | (z >> 1)
            z &= mz
        out.append(at(x, 19, 18) ^ at(y, 22, 21) ^ at(z, 23, 22))
    return out


def test_tiny_teacher():
    key = bits(TINY_KEY_CLASS)
    cipher = TinyA5_1(key)
    actual_stream = [cipher.generate_bit() for _ in range(3)]
    assert actual_stream == bits("100"), f"Expected S=100; Actual S={bitstr(actual_stream)}"
    encrypted = TinyA5_1(key).encrypt(bits("111"))
    assert encrypted == bits("011"), f"Expected C=011; Actual C={bitstr(encrypted)}"
    recovered = TinyA5_1(key).decrypt(encrypted)
    assert recovered == bits("111"), f"Expected P=111; Actual P={bitstr(recovered)}"
    return "S: 100 == 100; C: 011 == 011; P': 111 == 111"


def test_tiny_group():
    key = bits(TINY_KEY_GROUP)
    cipher = TinyA5_1(key)
    states = []
    stream = []
    for _ in range(3):
        stream.append(cipher.generate_bit())
        states.append((bitstr(cipher.X), bitstr(cipher.Y), bitstr(cipher.Z)))
    expected_states = [
        ("010110", "10010110", "110100101"),
        ("101011", "11001011", "111010010"),
        ("110101", "01100101", "011101001"),
    ]
    assert states == expected_states, f"Expected states={expected_states}; Actual={states}"
    assert stream == bits("101"), f"Expected S=101; Actual S={bitstr(stream)}"
    encrypted = TinyA5_1(key).encrypt(bits("101"))
    assert encrypted == bits("000"), f"Expected C=000; Actual C={bitstr(encrypted)}"
    assert TinyA5_1(key).decrypt(encrypted) == bits("101")
    return "S: 101 == 101; C: 000 == 000; 3 states == expected"


def test_tiny_roundtrip():
    for plaintext in ["0", "111000111", "1010011010100110", "0" * 128]:
        key = bits(TINY_KEY_CLASS)
        cipher = TinyA5_1(key)
        encrypted = cipher.encrypt(bits(plaintext))
        recovered = cipher.decrypt(encrypted)
        assert recovered == bits(plaintext), f"Roundtrip failed for P={plaintext}"
    return "4 ban ro / 4 lan giai ma chinh xac"

def test_tiny_bad_key():
    for n in [0, 22, 24]:
        try:
            TinyA5_1([0] * n)
        except ValueError:
            continue
        raise AssertionError(f"Key length={n}: expected ValueError but none raised")
    return "0, 22, 24 bits -> ValueError"


def test_full_roundtrip():
    for plaintext in ["101", "1011001011100001", "01" * 128]:
        cipher = A5_1(bits(FULL_KEY))
        encrypted = cipher.encrypt(bits(plaintext))
        recovered = cipher.decrypt(encrypted)
        assert recovered == bits(plaintext), "Full A5/1 roundtrip mismatch"
    return "3 ban ro / 3 lan giai ma chinh xac"


def test_full_independent_reference():
    key = bits(FULL_KEY)
    expected = reference_a51(FULL_KEY, 64)
    cipher = A5_1(key)
    actual = [cipher.generate_bit() for _ in range(64)]
    assert actual == expected, f"Expected S={bitstr(expected)}; Actual S={bitstr(actual)}"
    return f"Expected S={bitstr(expected)}; Actual S={bitstr(actual)}"


def test_full_bad_key():
    for n in [0, 63, 65]:
        try:
            A5_1([0] * n)
        except ValueError:
            continue
        raise AssertionError(f"Key length={n}: expected ValueError but none raised")
    return "0, 63, 65 bits -> ValueError"


def test_real_file():
    original = ("Demo file van ban A5/1 - Noi dung du dai.\n" * 15).encode("utf-8")
    with TemporaryDirectory() as folder:
        folder = Path(folder)
        src, enc, out = folder / "input.bin", folder / "encrypted.bin", folder / "decrypted.bin"
        src.write_bytes(original)
        plain_bits = [int(b) for v in src.read_bytes() for b in f"{v:08b}"]
        c = A5_1(bits(FULL_KEY))
        encrypted_bits = c.encrypt(plain_bits)
        enc.write_bytes(bytes(int(bitstr(encrypted_bits[i:i+8]), 2)
                              for i in range(0, len(encrypted_bits), 8)))
        loaded = [int(b) for v in enc.read_bytes() for b in f"{v:08b}"]
        decrypted_bits = A5_1(bits(FULL_KEY)).decrypt(loaded)
        out.write_bytes(bytes(int(bitstr(decrypted_bits[i:i+8]), 2)
                              for i in range(0, len(decrypted_bits), 8)))
        assert out.read_bytes() == src.read_bytes(), "Recovered file differs from original"
        assert enc.read_bytes() != src.read_bytes(), "Encrypted file equals original"
    return f"Original == Decrypted ({len(original)} bytes)"


def test_utils():
    import utils
    for text in ["A", "Hello A5/1"]:
        recovered = utils.bits_to_text(utils.text_to_bits(text))
        assert recovered == text, f"Expected {text!r}; Actual {recovered!r}"
    with TemporaryDirectory() as folder:
        src = Path(folder) / "source.bin"
        dst = Path(folder) / "restored.bin"
        src.write_bytes(bytes(range(256)))
        utils.bits_to_file(utils.file_to_bits(src), dst)
        assert dst.read_bytes() == src.read_bytes(), "utils file -> bits -> file failed"
    return "ASCII text and binary file conversion == expected"


def main():
    cases = [
        ("TC01", "Tiny - vi du tren lop (known answer)", test_tiny_teacher),
        ("TC02", "Tiny - vi du tinh tay nhom + trang thai", test_tiny_group),
        ("TC03", "Tiny - ma hoa / giai ma", test_tiny_roundtrip),
        ("TC04", "Tiny - tu choi khoa sai", test_tiny_bad_key),
        ("TC05", "A5/1 - ma hoa / giai ma", test_full_roundtrip),
        ("TC06", "A5/1 - doi chieu trien khai doc lap", test_full_independent_reference),
        ("TC07", "A5/1 - tu choi khoa sai", test_full_bad_key),
        ("TC08", "A5/1 - ma hoa / giai ma tep that", test_real_file),
        ("TC09", "Utils - chuyen doi text/bit va file/bit", test_utils),
    ]
    passed, failed = 0, 0
    print("=" * 75)
    print("TEST SUITE: Tiny A5/1 + A5/1 | PASS/FAIL theo ket qua THUC TE")
    print("=" * 75)
    for code, name, test in cases:
        try:
            info = test()
        except Exception as exc:
            failed += 1
            print(f"[FAIL] {code} - {name}")
            print(f"       {type(exc).__name__}: {exc}")
        else:
            passed += 1
            print(f"[PASS] {code} - {name}")
            print(f"       {info}")
print("-" * 75)
print("TEST SUMMARY")
print(f"Total Tests : {len(cases)}")
print(f"Passed      : {passed}")
print(f"Failed      : {failed}")
print("-" * 75)

return 0 if failed == 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
