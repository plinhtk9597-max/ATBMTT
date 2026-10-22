# Bài tập lớn: Hệ mã A5/1 và TinyA5/1

## Giới thiệu

Bài tập lớn môn *An toàn và Bảo mật Thông tin*. Nhóm cài đặt hệ mã dòng *A5/1* (dùng trong mạng 2G GSM) và phiên bản thu nhỏ *TinyA5/1* (dùng cho mục đích giảng dạy).

## Cấu trúc thư mục

```
ATBMTT/
├── core/
│   ├── __init__.py
│   ├── tiny_a5_1.py      # Thuật toán TinyA5/1
│   ├── a5_1.py           # Thuật toán A5/1 tổng quát
│   └── utils.py          # Hàm chuyển đổi text/file <-> bit
├── tests/
│   ├── __init__.py
│   └── test_all.py       # Bộ kiểm thử
├── cli.py                # Giao diện dòng lệnh
├── main.py               # Điểm khởi chạy
├── README.md             # File này
└── .gitignore

```
## Phân công nhóm

| Thành viên | Công việc |
|---|---|
| Kiều Phương Linh - Leader | TinyA5/1 + phân tích độ an toàn |
| Trần Thu Trang | Bối cảnh + utils.py |
| Trịnh Minh Châu | Mô tả thuật toán + sơ đồ khối + CLI |
| Lê Hoàng Mai | Ví dụ tính tay + bộ kiểm thử |
| Đào Quang Trung | So sánh với RC4 + A5/1 |

## Tài liệu tham khảo

1. Biryukov, A., Shamir, A., & Wagner, D. (2000). *Real Time Cryptanalysis of A5/1 on a PC*. FSE 2000.
2. Golic, J. (1997). *Cryptanalysis of the Alleged A5 Stream Cipher*. EUROCRYPT 1997.
3. Gendrullis, T., Novotny, M., & Rupp, A. (2008). *A Real-World Attack Breaking A5/1 within Hours*. ePrint 2008/147.
4. Gundaram, P. K., Tentu, A. N., & Allu, S. N. (2022). *State Transition Analysis of GSM Encryption Algorithm A5/1*. Journal of Communications Software and Systems.
