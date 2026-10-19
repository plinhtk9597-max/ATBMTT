"""
Cài đặt thuật toán mã dòng A5/1 (phiên bản tổng quát)
và chương trình thực hành kiểm chứng hai chiều mã hóa - giải mã.

Cấu trúc:
  - Thanh ghi X: 19 bit (0..18)
  - Thanh ghi Y: 22 bit (0..21)
  - Thanh ghi Z: 23 bit (0..22)
  - Khóa K: 64 bit

Bit clock: x8, y10, z10
Bit xuất dòng khóa: s_i = x18 XOR y21 XOR z22
"""

# =====================================================================
# PHẦN 1: ĐỊNH NGHĨA LỚP THUẬT TOÁN A5/1 (BỘ KIỂM THỬ SẼ GỌI VÀO ĐÂY)
# =====================================================================

class A5_1:
    """
    Lớp cài đặt thuật toán A5/1 tổng quát.
    
    Sử dụng:
        cipher = A5_1(key_bits)
        C = cipher.encrypt(P)
        P = cipher.decrypt(C)
    """

    def __init__(self, key_bits):
        """
        Khởi tạo với khóa K 64 bit.
        Phân bổ: X (19 bit đầu), Y (22 bit tiếp theo), Z (23 bit cuối).
        """
        if len(key_bits) != 64:
            raise ValueError(f"Khóa phải có đúng 64 bit, nhận được {len(key_bits)}")
        self.key_bits = key_bits[:]   # Lưu lại khóa gốc để reset
        self.X = key_bits[0:19]       # 19 bit đầu (x0..x18)
        self.Y = key_bits[19:41]      # 22 bit tiếp theo (y0..y21)
        self.Z = key_bits[41:64]      # 23 bit cuối (z0..z22)
        self.step = 0                 # Đếm số bước sinh số
        self.log = []                 # Lưu log các bước

    def reset(self):
        """Reset trạng thái 3 thanh ghi về ban đầu (dùng trước khi giải mã)."""
        self.X = self.key_bits[0:19]
        self.Y = self.key_bits[19:41]
        self.Z = self.key_bits[41:64]
        self.step = 0
        self.log = []

    @staticmethod
    def majority(a, b, c):
        """Hàm chiếm đa số: trả về 1 nếu có >= 2 bit 1, ngược lại trả về 0."""
        return 1 if (a + b + c) >= 2 else 0

    def clock_X(self):
        """Quay thanh ghi X (19 bit). Đa thức: t = x13 ^ x16 ^ x17 ^ x18."""
        t = self.X[13] ^ self.X[16] ^ self.X[17] ^ self.X[18]
        self.X = [t] + self.X[:-1]

    def clock_Y(self):
        """Quay thanh ghi Y (22 bit). Đa thức: t = y20 ^ y21."""
        t = self.Y[20] ^ self.Y[21]
        self.Y = [t] + self.Y[:-1]

    def clock_Z(self):
        """Quay thanh ghi Z (23 bit). Đa thức: t = z7 ^ z20 ^ z21 ^ z22."""
        t = self.Z[7] ^ self.Z[20] ^ self.Z[21] ^ self.Z[22]
        self.Z = [t] + self.Z[:-1]

    def generate_bit(self, verbose=False):
        """Sinh 1 bit dòng khóa s_i theo luật đa số Majority."""
        self.step += 1

        # 1. Lấy bit điều khiển xung nhịp
        x8, y10, z10 = self.X[8], self.Y[10], self.Z[10]

        # 2. Tính m = maj(x8, y10, z10)
        m = self.majority(x8, y10, z10)

        if verbose:
            self.log.append(f"\n--- Bước {self.step} ---")
            self.log.append(f"  Trước : X={self.X}")
            self.log.append(f"          Y={self.Y}")
            self.log.append(f"          Z={self.Z}")
            self.log.append(f"  Clock : x8={x8}, y10={y10}, z10={z10} -> m={m}")

        # 3. Thanh ghi nào có bit clock bằng m thì mới quay
        if x8 == m:
            self.clock_X()
            if verbose: self.log.append("  Quay X")
        if y10 == m:
            self.clock_Y()
            if verbose: self.log.append("  Quay Y")
        if z10 == m:
            self.clock_Z()
            if verbose: self.log.append("  Quay Z")

        # 4. Xuất bit dòng khóa tại các bit ngoài cùng bên phải
        s = self.X[18] ^ self.Y[21] ^ self.Z[22]

        if verbose:
            self.log.append(f"  Sau   : X={self.X}")
            self.log.append(f"          Y={self.Y}")
            self.log.append(f"          Z={self.Z}")
            self.log.append(f"  s{self.step-1} = {self.X[18]} XOR {self.Y[21]} XOR {self.Z[22]} = {s}")

        return s

    def encrypt(self, plaintext_bits, verbose=False):
        """Mã hóa danh sách bit bản rõ: C_i = P_i XOR s_i."""
        ciphertext_bits = []
        for i, p in enumerate(plaintext_bits):
            s = self.generate_bit(verbose=verbose)
            c = p ^ s
            ciphertext_bits.append(c)
            if verbose:
                self.log.append(f"  -> C{i} = P{i} XOR s = {p} XOR {s} = {c}")
        return ciphertext_bits

    def decrypt(self, ciphertext_bits, verbose=False):
        """Giải mã: reset trạng thái thanh ghi rồi mã hóa lại trên bản mã (C XOR S)."""
        self.reset()
        return self.encrypt(ciphertext_bits, verbose=verbose)

    def get_log(self):
        """Trả về log các bước dịch chuyển để phục vụ in kết quả."""
        return self.log


# =====================================================================
# PHẦN 2: CÁC HÀM TIỆN ÍCH CHUYỂN ĐỔI DỮ LIỆU
# =====================================================================

def text_to_bits(text: str) -> list:
    """Chuyển đổi chuỗi văn bản UTF-8 thành danh sách bit 0/1."""
    byte_arr = text.encode("utf-8")
    bits = []
    for b in byte_arr:
        bits.extend([int(bit) for bit in format(b, "08b")])
    return bits


def bits_to_text(bits: list) -> str:
    """Chuyển đổi danh sách bit 0/1 thành chuỗi ký tự UTF-8."""
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte_chunk = bits[i:i+8]
        if len(byte_chunk) == 8:
            byte_val = int("".join(map(str, byte_chunk)), 2)
            bytes_list.append(byte_val)
    return bytes(bytes_list).decode("utf-8", errors="replace")


def bits_to_hex(bits: list) -> str:
    """Chuyển danh sách bit sang chuỗi Hexadecimal để xem kết quả mã hóa."""
    bit_str = "".join(map(str, bits))
    if not bit_str:
        return ""
    num_bytes = (len(bit_str) + 7) // 8
    val = int(bit_str, 2)
    return hex(val)[2:].upper().zfill(num_bytes * 2)


# =====================================================================
# PHẦN 3: CÁC HÀM THỰC HÀNH & KIỂM THỬ HAI CHIỀU MÃ HÓA / GIẢI MÃ
# =====================================================================

def demo_bit_encryption(key_bits: list):
    """Kiểm thử mã hóa và giải mã trên danh sách bit."""
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
    """Kiểm thử mã hóa và giải mã trên chuỗi văn bản tự nhiên."""
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
