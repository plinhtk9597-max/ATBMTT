"""
Chương trình thực hành: Hệ mã dòng A5/1
Nhiệm vụ: Cài đặt và kiểm chứng đủ 2 chiều MÃ HÓA và GIẢI MÃ
Sử dụng module: core/a5_1.py
"""

from core.a5_1 import A5_1


def text_to_bits(text: str) -> list:
    """Chuyển đổi chuỗi ký tự UTF-8 thành danh sách bit 0/1."""
    byte_arr = text.encode("utf-8")
    bits = []
    for b in byte_arr:
        bits.extend([int(bit) for bit in format(b, "08b")])
    return bits


def bits_to_text(bits: list) -> str:
    """Chuyển đổi danh sách bit 0/1 trở lại thành chuỗi ký tự UTF-8."""
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte_chunk = bits[i:i+8]
        if len(byte_chunk) == 8:
            byte_val = int("".join(map(str, byte_chunk)), 2)
            bytes_list.append(byte_val)
    return bytes(bytes_list).decode("utf-8", errors="replace")


def bits_to_hex(bits: list) -> str:
    """Chuyển danh sách bit sang chuỗi Hexadecimal để quan sát bản mã."""
    bit_str = "".join(map(str, bits))
    if not bit_str:
        return ""
    num_bytes = (len(bit_str) + 7) // 8
    val = int(bit_str, 2)
    return hex(val)[2:].upper().zfill(num_bytes * 2)


def demo_bit_encryption(key_bits: list):
    print("\n" + "=" * 65)
    print("THỬ NGHIỆM 1: MÃ HÓA VÀ GIẢI MÃ TRÊN DÃY BIT (BINARY)")
    print("=" * 65)

    cipher = A5_1(key_bits)
    plaintext_bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1]
    print(f"[+] Bản rõ ban đầu (P)       : {plaintext_bits}")

    # Chiều 1: Mã hóa
    ciphertext_bits = cipher.encrypt(plaintext_bits, verbose=True)
    print(f"[->] Bản mã sinh ra (C = P⊕S): {ciphertext_bits}")

    # Chiều 2: Giải mã
    decrypted_bits = cipher.decrypt(ciphertext_bits, verbose=False)
    print(f"[<-] Bản rõ giải mã (P' = C⊕S): {decrypted_bits}")

    assert plaintext_bits == decrypted_bits, "LỖI: Bản rõ giải mã không trùng khớp!"
    print("[✓] KẾT QUẢ: Đã kiểm chứng chính xác 100% hai chiều trên chuỗi bit!")


def demo_text_encryption(key_bits: list):
    print("\n" + "=" * 65)
    print("THỬ NGHIỆM 2: MÃ HÓA VÀ GIẢI MÃ TRÊN VĂN BẢN (TEXT/STRING)")
    print("=" * 65)

    cipher = A5_1(key_bits)
    original_message = "An toan va bao mat thong tin - Nhom 7"
    print(f"[+] Thông điệp ban đầu (P) : \"{original_message}\"")

    message_bits = text_to_bits(original_message)
    print(f"[+] Độ dài dữ liệu bit     : {len(message_bits)} bits")

    # Chiều 1: Mã hóa văn bản
    cipher.reset()
    encrypted_bits = cipher.encrypt(message_bits, verbose=False)
    print(f"[->] Bản mã Hexadecimal (C): {bits_to_hex(encrypted_bits)}")

    # Chiều 2: Giải mã văn bản
    recovered_bits = cipher.decrypt(encrypted_bits, verbose=False)
    recovered_message = bits_to_text(recovered_bits)
    print(f"[<-] Văn bản giải mã (P')  : \"{recovered_message}\"")

    assert original_message == recovered_message, "LỖI: Văn bản giải mã không khớp!"
    print("[✓] KẾT QUẢ: Giải mã khôi phục nguyên vẹn văn bản gốc!")
    print("=" * 65)


if __name__ == "__main__":
    raw_key = "1010010010111000101010111001001010011010011010101110100100101011"
    key_bits = [int(b) for b in raw_key]

    print("KHÓA K (64 bit):", raw_key)
    demo_bit_encryption(key_bits)
    demo_text_encryption(key_bits)
