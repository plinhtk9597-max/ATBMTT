# cli.py
# Giao diện dòng lệnh cho chương trình A5/1 và TinyA5/1
#
# Chức năng:
#   1. Mã hóa văn bản (TinyA5/1) - in từng bước
#   2. Giải mã văn bản (TinyA5/1)
#   3. Mã hóa văn bản (A5/1)
#   4. Giải mã văn bản (A5/1)
#   5. Mã hóa tệp (A5/1)
#   6. Giải mã tệp (A5/1)
#   7. Chạy kiểm thử

import sys
import os
import time
import subprocess

# Thêm thư mục gốc vào sys.path để import được core/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.tiny_a5_1 import TinyA5_1
from core.a5_1 import A5_1
from core.utils import (text_to_bits, bits_to_text, file_to_bits,
                        bits_to_file, bits_to_string, string_to_bits)


# ============================================================
# HÀM NHẬP LIỆU
# ============================================================

def input_bits(prompt, length):
    """
    Nhập dãy bit từ bàn phím.
    Kiểm tra đúng độ dài và chỉ chứa ký tự 0/1.
    """
    while True:
        s = input(prompt).strip()
        if len(s) != length or not all(c in "01" for c in s):
            print(f"  ! Vui lòng nhập đúng {length} bit (chỉ 0 và 1)!")
            continue
        return [int(c) for c in s]


# ============================================================
# MENU CHÍNH
# ============================================================

def menu():
    print("\n" + "=" * 55)
    print("   CHƯƠNG TRÌNH MÃ HÓA A5/1 VÀ TINYA5/1")
    print("=" * 55)
    print("  1. Mã hóa văn bản (TinyA5/1) - in từng bước")
    print("  2. Giải mã văn bản (TinyA5/1)")
    print("  3. Mã hóa văn bản (A5/1)")
    print("  4. Giải mã văn bản (A5/1)")
    print("  5. Mã hóa tệp (A5/1)")
    print("  6. Giải mã tệp (A5/1)")
    print("  7. Chạy kiểm thử")
    print("  0. Thoát")
    print("=" * 55)
    return input("  Chọn chức năng: ").strip()


# ============================================================
# CHỨC NĂNG 1: MÃ HÓA TINYA5/1 (IN TỪNG BƯỚC)
# ============================================================

def chuc_nang_1():
    print("\n--- MÃ HÓA TINYA5/1 (CÓ IN TỪNG BƯỚC) ---")
    K = input_bits("Nhập khóa 23 bit: ", 23)
    text = input("Nhập văn bản: ")
    P = text_to_bits(text)
    print(f"\nBản rõ dạng bit ({len(P)} bit): {bits_to_string(P)[:80]}...")

    cipher = TinyA5_1(K)
    C = cipher.encrypt(P, verbose=True)

    # In các bước trung gian
    print("\n===== CÁC BƯỚC TRUNG GIAN =====")
    for line in cipher.get_log():
        print(line)

    print(f"\n>>> Bản mã: {bits_to_string(C)[:80]}...")


# ============================================================
# CHỨC NĂNG 2: GIẢI MÃ TINYA5/1
# ============================================================

def chuc_nang_2():
    print("\n--- GIẢI MÃ TINYA5/1 ---")
    K = input_bits("Nhập khóa 23 bit: ", 23)
    C_str = input("Nhập bản mã (dãy bit): ").strip()
    C = string_to_bits(C_str)

    decipher = TinyA5_1(K)
    P = decipher.decrypt(C)
    print(f">>> Bản rõ: {bits_to_text(P)}")


# ============================================================
# CHỨC NĂNG 3: MÃ HÓA A5/1
# ============================================================

def chuc_nang_3():
    print("\n--- MÃ HÓA A5/1 ---")
    K = input_bits("Nhập khóa 64 bit: ", 64)
    text = input("Nhập văn bản: ")
    P = text_to_bits(text)

    cipher = A5_1(K)
    start = time.time()
    C = cipher.encrypt(P)
    elapsed = time.time() - start

    print(f"\n>>> Bản mã ({len(C)} bit): {bits_to_string(C)[:80]}...")
    print(f">>> Thời gian mã hóa: {elapsed*1000:.3f} ms")


# ============================================================
# CHỨC NĂNG 4: GIẢI MÃ A5/1
# ============================================================

def chuc_nang_4():
    print("\n--- GIẢI MÃ A5/1 ---")
    K = input_bits("Nhập khóa 64 bit: ", 64)
    C_str = input("Nhập bản mã (dãy bit): ").strip()
    C = string_to_bits(C_str)

    decipher = A5_1(K)
    P = decipher.decrypt(C)
    print(f">>> Bản rõ: {bits_to_text(P)}")


# ============================================================
# CHỨC NĂNG 5: MÃ HÓA TỆP BẰNG A5/1
# ============================================================

def chuc_nang_5():
    print("\n--- MÃ HÓA TỆP BẰNG A5/1 ---")
    K = input_bits("Nhập khóa 64 bit: ", 64)
    infile = input("Nhập đường dẫn tệp gốc: ").strip()
    outfile = input("Nhập đường dẫn tệp mã: ").strip()

    try:
        P = file_to_bits(infile)
    except OSError as e:
        print(f"  ! Không đọc được tệp: {e}")
        return

    print(f"Đã đọc {len(P)} bit từ tệp.")

    cipher = A5_1(K)
    start = time.time()
    C = cipher.encrypt(P)
    elapsed = time.time() - start

    bits_to_file(C, outfile)
    print(f">>> Đã mã hóa trong {elapsed:.3f} giây.")
    print(f">>> Tệp mã lưu tại: {outfile}")


# ============================================================
# CHỨC NĂNG 6: GIẢI MÃ TỆP BẰNG A5/1
# ============================================================

def chuc_nang_6():
    print("\n--- GIẢI MÃ TỆP BẰNG A5/1 ---")
    K = input_bits("Nhập khóa 64 bit: ", 64)
    infile = input("Nhập đường dẫn tệp mã: ").strip()
    outfile = input("Nhập đường dẫn tệp giải mã: ").strip()

    try:
        C = file_to_bits(infile)
    except OSError as e:
        print(f"  ! Không đọc được tệp: {e}")
        return

    print(f"Đã đọc {len(C)} bit từ tệp mã.")

    decipher = A5_1(K)
    start = time.time()
    P = decipher.decrypt(C)
    elapsed = time.time() - start

    bits_to_file(P, outfile)
    print(f">>> Đã giải mã trong {elapsed:.3f} giây.")
    print(f">>> Tệp giải mã lưu tại: {outfile}")


# ============================================================
# CHỨC NĂNG 7: CHẠY BỘ KIỂM THỬ
# ============================================================

def chuc_nang_7():
    print("\n--- CHẠY BỘ KIỂM THỬ ---")
    test_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "tests", "test_all.py"
    )
    subprocess.run([sys.executable, test_path])


# ============================================================
# HÀM MAIN
# ============================================================

def main():
    while True:
        choice = menu()

        if choice == "1":
            chuc_nang_1()
        elif choice == "2":
            chuc_nang_2()
        elif choice == "3":
            chuc_nang_3()
        elif choice == "4":
            chuc_nang_4()
        elif choice == "5":
            chuc_nang_5()
        elif choice == "6":
            chuc_nang_6()
        elif choice == "7":
            chuc_nang_7()
        elif choice == "0":
            print("\nTạm biệt!")
            break
        else:
            print("  ! Chức năng không hợp lệ!")


if __name__ == "__main__":
    main()


