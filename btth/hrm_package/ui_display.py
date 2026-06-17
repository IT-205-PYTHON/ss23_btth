"""
hrm_package/ui_display.py
----------------------------
Chứa logic hiển thị giao diện (UI) cho người dùng terminal.

- display_records(attendance_book): in bảng chấm công ngày (chức năng 1).

Third-party module sử dụng: tabulate (làm đẹp bảng dữ liệu trên console).
Cài đặt bằng: pip install tabulate
"""

from tabulate import tabulate


def display_records(attendance_book):
    """
    Hiển thị bảng chấm công của toàn bộ nhân viên trong attendance_book.

    Input:
        attendance_book (list[dict]): danh sách hồ sơ chấm công, mỗi hồ sơ gồm
            "id", "name", "times" (tuple gồm Giờ Vào và Giờ Ra, Giờ Ra có thể None).
    Output:
        None: hàm chỉ in bảng ra màn hình, không trả về giá trị.

    Pseudocode:
        - Nếu attendance_book rỗng -> in "Chưa có dữ liệu chấm công." và return.
        - Khởi tạo danh sách rows rỗng.
        - Duyệt qua từng nhân viên trong attendance_book:
            -> Trích xuất giờ vào, giờ ra từ tuple "times".
            -> Nếu giờ ra là None -> hiển thị "[Đang làm việc]".
            -> Thêm dòng [mã, tên, giờ vào, giờ ra/hiển thị] vào rows.
        - Dùng tabulate(rows, headers, tablefmt) để format thành bảng.
        - In tiêu đề "--- BẢNG CHẤM CÔNG ---", bảng, và dòng kết thúc.
    """
    if not attendance_book:
        print("Chưa có dữ liệu chấm công.")
        return

    headers = ["Mã NV", "Tên Nhân Viên", "Giờ Vào", "Giờ Ra"]
    rows = []

    for record in attendance_book:
        clock_in_time, clock_out_time = record["times"]
        display_clock_out = "[Đang làm việc]" if clock_out_time is None else clock_out_time

        rows.append([
            record["id"],
            record["name"],
            clock_in_time,
            display_clock_out,
        ])

    print("--- BẢNG CHẤM CÔNG ---")
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    print("------------------------------------------------")
