#Bản rút gọn 1. 
# core/utils.py
# Các hàm tiện ích chuyển đổi dữ liệu

def text_to_bits(text):
    """Chuyển chuỗi văn bản thành list bit."""
    bits = []
    for char in text:
        code = ord(char)
        for i in range(7, -1, -1):
            bits.append((code >> i) & 1)
    return bits

def bits_to_text(bits):
    """Chuyển list bit thành chuỗi văn bản."""
    if len(bits) % 8 != 0:
        raise ValueError("Số bit phải chia hết cho 8!")
    text = ""
    for i in range(0, len(bits), 8):
        code = 0
        for j in range(8):
            code = (code << 1) | bits[i + j]
        text += chr(code)
    return text

def file_to_bits(filepath):
    """Đọc file và chuyển thành list bit."""
    with open(filepath, "rb") as f:
        data = f.read()
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def bits_to_file(bits, filepath):
    """Ghi list bit ra file."""
    if len(bits) % 8 != 0:
        raise ValueError("Số bit phải chia hết cho 8!")
    data = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        data.append(byte)
    with open(filepath, "wb") as f:
        f.write(data)

def bits_to_string(bits):
    """Chuyển list bit thành chuỗi '0101...'."""
    return "".join(str(b) for b in bits)

def string_to_bits(s):
    """Chuyển chuỗi '0101...' thành list bit."""
    return [int(c) for c in s if c in "01"]
    

#Bản đầy đủ
# core/utils.py
# Các hàm tiện ích chuyển đổi dữ liệu cho A5/1 và TinyA5/1
#
# File này cung cấp các hàm chuyển đổi qua lại giữa:
#   - Văn bản (text) <-> Dãy bit (bit list)
#   - Tệp tin (file) <-> Dãy bit (bit list)
#   - Dãy bit <-> Chuỗi "0101..." để hiển thị
#
# Lưu ý: A5/1 làm việc trên đơn vị bit, còn người dùng nhập văn bản
# hoặc tệp tin. Do đó cần các hàm chuyển đổi này.


# ============================================================
# 1. CHUYỂN ĐỔI VĂN BẢN <-> BIT
# ============================================================

def text_to_bits(text):
    """
    Chuyển chuỗi văn bản thành danh sách bit.

    Mỗi ký tự được biểu diễn bằng 8 bit (mã ASCII/Unicode).
    Bit cao nhất (MSB) được đặt trước.

    Tham số:
        text (str): Chuỗi văn bản cần chuyển đổi.

    Trả về:
        list[int]: Danh sách các bit 0/1.

    Ví dụ:
        >>> text_to_bits("A")
        [0, 1, 0, 0, 0, 0, 0, 1]   # 'A' = 65 = 01000001
        >>> text_to_bits("Hi")
        [0,1,0,0,1,0,0,0, 0,1,1,0,1,0,0,1]   # 'H'=72, 'i'=105
    """
    bits = []
    for char in text:
        code = ord(char)              # Lấy mã Unicode của ký tự
        for i in range(7, -1, -1):    # Lấy từ bit cao xuống bit thấp
            bits.append((code >> i) & 1)
    return bits


def bits_to_text(bits):
    """
    Chuyển danh sách bit thành chuỗi văn bản.

    Yêu cầu: số bit phải chia hết cho 8.
    Mỗi nhóm 8 bit tương ứng với 1 ký tự.

    Tham số:
        bits (list[int]): Danh sách các bit 0/1.

    Trả về:
        str: Chuỗi văn bản đã khôi phục.

    Lỗi:
        ValueError: Nếu số bit không chia hết cho 8.

    Ví dụ:
        >>> bits_to_text([0,1,0,0,0,0,0,1])
        'A'
    """
    if len(bits) % 8 != 0:
        raise ValueError(f"Số bit phải chia hết cho 8, nhận được {len(bits)} bit!")
    text = ""
    for i in range(0, len(bits), 8):
        code = 0
        for j in range(8):
            code = (code << 1) | bits[i + j]
        text += chr(code)
    return text


# ============================================================
# 2. CHUYỂN ĐỔI TỆP TIN <-> BIT
# ============================================================

def file_to_bits(filepath):
    """
    Đọc tệp tin nhị phân và chuyển thành danh sách bit.

    Dùng cho demo mã hóa tệp văn bản hoặc ảnh nhỏ.

    Tham số:
        filepath (str): Đường dẫn tệp tin cần đọc.

    Trả về:
        list[int]: Danh sách các bit 0/1.

    Ví dụ:
        >>> bits = file_to_bits("input.txt")
        >>> len(bits)
        800   # nếu file có 100 byte
    """
    with open(filepath, "rb") as f:
        data = f.read()
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def bits_to_file(bits, filepath):
    """
    Ghi danh sách bit ra tệp tin nhị phân.

    Yêu cầu: số bit phải chia hết cho 8.

    Tham số:
        bits (list[int]): Danh sách các bit 0/1.
        filepath (str): Đường dẫn tệp tin đích.

    Lỗi:
        ValueError: Nếu số bit không chia hết cho 8.

    Ví dụ:
        >>> bits_to_file([0,1,0,0,0,0,0,1], "output.bin")
    """
    if len(bits) % 8 != 0:
        raise ValueError(f"Số bit phải chia hết cho 8, nhận được {len(bits)} bit!")
    data = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        data.append(byte)
    with open(filepath, "wb") as f:
        f.write(data)


# ============================================================
# 3. HIỂN THỊ DÃY BIT
# ============================================================

def bits_to_string(bits):
    """
    Chuyển danh sách bit thành chuỗi "0101..." để hiển thị.

    Tham số:
        bits (list[int]): Danh sách các bit 0/1.

    Trả về:
        str: Chuỗi gồm các ký tự '0' và '1'.

    Ví dụ:
        >>> bits_to_string([1, 0, 1, 1])
        '1011'
    """
    return "".join(str(b) for b in bits)


def string_to_bits(s):
    """
    Chuyển chuỗi "0101..." thành danh sách bit.

    Bỏ qua mọi ký tự không phải '0' hoặc '1'.

    Tham số:
        s (str): Chuỗi gồm các ký tự '0' và '1' (có thể lẫn ký tự khác).

    Trả về:
        list[int]: Danh sách các bit 0/1.

    Ví dụ:
        >>> string_to_bits("1011")
        [1, 0, 1, 1]
        >>> string_to_bits("1 0 1 1")
        [1, 0, 1, 1]   # bỏ qua dấu cách
    """
    return [int(c) for c in s if c in "01"]


# ============================================================
# 4. HÀM HỖ TRỢ DEBUG VÀ DEMO
# ============================================================


def format_bits(bits, group_size=8):
    """
    Định dạng dãy bit thành các nhóm để dễ đọc.

    Tham số:
        bits (list[int]): Danh sách các bit 0/1.
        group_size (int): Số bit mỗi nhóm.

    Trả về:
        str: Chuỗi đã được định dạng.

    Ví dụ:
        >>> format_bits([1,0,1,1,0,0,1,0, 1,1,0,0,1,1,0,0])
        '10110010 11001100'
    """
    s = bits_to_string(bits)
    groups = []
    for i in range(0, len(s), group_size):
        groups.append(s[i:i+group_size])
    return " ".join(groups)


def count_bits(bits):
    """
    Đếm số bit 0 và số bit 1 trong dãy.

    Tham số:
        bits (list[int]): Danh sách các bit 0/1.

    Trả về:
        tuple: (số_bit_0, số_bit_1)

    Ví dụ:
        >>> count_bits([1,0,1,1,0,0])
        (3, 3)
    """
    count_0 = bits.count(0)
    count_1 = bits.count(1)
    return (count_0, count_1)

    

