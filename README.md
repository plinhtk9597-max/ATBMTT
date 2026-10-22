# Bài tập lớn: Hệ mã A5/1 và TinyA5/1

## Giới thiệu

Bài tập lớn môn *An toàn và Bảo mật Thông tin*. Nhóm cài đặt hệ mã dòng *A5/1* (dùng trong mạng 2G GSM) và phiên bản thu nhỏ *TinyA5/1* (dùng cho mục đích giảng dạy).

## Cấu trúc thư mục

```text
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

