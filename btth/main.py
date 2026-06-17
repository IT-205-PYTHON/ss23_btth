"""
main.py
--------
Chứa menu điều hướng chính của Hệ Thống Chấm Công Linh Hoạt (Flex-Time Attendance).

Chạy chương trình bằng:  python main.py
(chạy từ thư mục gốc project, nơi chứa main.py và hrm_package/).

--------------------------------------------------------------------------
ADVANCED IMPORT (yêu cầu bắt buộc của đề bài):

    Sử dụng cú pháp "from ... import ... as ..." để đổi tên (alias) hàm,
    tránh xung đột tên và quản lý namespace gọn gàng:

        from hrm_package.time_calc import evaluate_flex_time as evaluate_shifts

    Nhờ đó, trong main.py ta gọi evaluate_shifts(...) thay vì evaluate_flex_time(...).
--------------------------------------------------------------------------
"""

from hrm_package import display_records, clock_in, clock_out
from hrm_package.time_calc import evaluate_flex_time as evaluate_shifts

# Dữ liệu khởi tạo mẫu (Mock Data) theo đúng đề bài.
attendance_book = [
    {"id": "NV01", "name": "Nguyễn Văn A", "times": ("08:30", "17:30")},
    {"id": "NV02", "name": "Trần Thị B", "times": ("09:30", None)},  # Đang làm việc.
    {"id": "NV03", "name": "Lê Văn C", "times": ("10:15", "19:15")}
]


def show_menu():
    """
    Hiển thị menu chức năng chính.

    Input: không có.
    Output: None, chỉ in menu ra màn hình.
    """
    print("\n=== HỆ THỐNG CHẤM CÔNG RIKKEI (FLEX-TIME) ===")
    print("1. Xem bảng chấm công ngày")
    print("2. Chấm công Vào (Clock-in)")
    print("3. Chấm công Ra (Clock-out)")
    print("4. Đánh giá vi phạm")
    print("5. Thoát chương trình")
    print("=================================================")


def main():
    """
    Hàm chính điều khiển toàn bộ luồng chương trình bằng vòng lặp while True.

    Input: không có.
    Output: None. Hàm chạy cho đến khi người dùng chọn chức năng 5 (thoát).

    Pseudocode:
        - Lặp vô hạn (while True):
            -> Hiển thị menu.
            -> Nhập lựa chọn của người dùng.
            -> Nếu lựa chọn == "1" -> gọi display_records(attendance_book).
            -> Nếu lựa chọn == "2" -> gọi clock_in(attendance_book).
            -> Nếu lựa chọn == "3" -> gọi clock_out(attendance_book).
            -> Nếu lựa chọn == "4" -> gọi evaluate_shifts(attendance_book).
            -> Nếu lựa chọn == "5" -> in lời chào kết thúc và break khỏi while.
            -> Nếu lựa chọn không hợp lệ -> in thông báo lỗi và lặp lại menu.
    """
    while True:
        show_menu()
        choice = input("Chọn chức năng (1-5): ").strip()

        if choice == "1":
            display_records(attendance_book)
        elif choice == "2":
            clock_in(attendance_book)
        elif choice == "3":
            clock_out(attendance_book)
        elif choice == "4":
            evaluate_shifts(attendance_book)
        elif choice == "5":
            print("Cảm ơn bạn đã sử dụng Hệ Thống Chấm Công Rikkei!")
            break
        else:
            print(">> Lựa chọn không hợp lệ! Vui lòng chọn từ 1 đến 5.")


if __name__ == "__main__":
    main()
