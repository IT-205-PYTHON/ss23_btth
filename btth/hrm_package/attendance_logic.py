"""
hrm_package/attendance_logic.py
----------------------------------
Chứa logic chấm công Vào / Ra:
- clock_in(attendance_book): chấm công vào (chức năng 2).
- clock_out(attendance_book): chấm công ra (chức năng 3) - trọng tâm xử lý
  việc GHI ĐÈ (thay thế) Tuple, vì tuple là cấu trúc bất biến (immutable).
"""


def _find_record_index(attendance_book, employee_id):
    """
    Hàm phụ trợ (private, không export ra ngoài package): tìm vị trí (index)
    của hồ sơ nhân viên trong attendance_book dựa trên mã nhân viên.

    Input:
        attendance_book (list[dict]): danh sách hồ sơ chấm công.
        employee_id (str): mã nhân viên cần tìm.
    Output:
        int: index của hồ sơ nếu tìm thấy, -1 nếu không tìm thấy.

    Pseudocode:
        - Chuẩn hóa employee_id (strip + upper) để so khớp không phân biệt
          khoảng trắng/hoa thường.
        - Duyệt qua attendance_book bằng enumerate().
        - So sánh mã đã chuẩn hóa với "id" của từng hồ sơ (cũng chuẩn hóa).
        - Nếu khớp -> trả về index.
        - Nếu duyệt hết không thấy -> trả về -1.
    """
    normalized_id = employee_id.strip().upper()

    for index, record in enumerate(attendance_book):
        if record["id"].strip().upper() == normalized_id:
            return index

    return -1


def clock_in(attendance_book):
    """
    Tạo mới một hồ sơ chấm công Vào cho nhân viên và thêm vào attendance_book.

    Input:
        attendance_book (list[dict]): danh sách hồ sơ chấm công, sẽ được thêm
                                       một dict mới (in-place) nếu thành công.
    Output:
        None: hàm chỉ in kết quả ra màn hình và cập nhật attendance_book.

    Pseudocode (Chức năng 2 - Chấm công Vào):
        - Nhập mã nhân viên, tên nhân viên, giờ vào (HH:MM).
        - Chuẩn hóa mã nhân viên (strip + upper).
        - Kiểm tra mã nhân viên đã tồn tại trong attendance_book chưa
          (dùng _find_record_index()).
            -> Nếu đã tồn tại -> in "Mã nhân viên đã tồn tại!" và return
               (không cho phép trùng mã NV).
        - Tạo dictionary mới:
            {"id": mã đã chuẩn hóa, "name": tên, "times": (giờ vào, None)}
          Lưu ý: times là tuple 2 phần tử, phần Giờ Ra để None vì nhân viên
          vừa chấm công vào, chưa có giờ ra.
        - Thêm dictionary mới vào cuối attendance_book bằng append().
        - In thông báo "Thành công: Đã ghi nhận <mã> chấm công vào lúc <giờ>!"
    """
    employee_id = input("Nhập mã nhân viên: ").strip().upper()
    employee_name = input("Nhập tên nhân viên: ").strip()
    clock_in_time = input("Nhập giờ vào (HH:MM): ").strip()

    if _find_record_index(attendance_book, employee_id) != -1:
        print("Mã nhân viên đã tồn tại!")
        return

    new_record = {
        "id": employee_id,
        "name": employee_name,
        "times": (clock_in_time, None)
    }
    attendance_book.append(new_record)

    print(f"Thành công: Đã ghi nhận {employee_id} chấm công vào lúc {clock_in_time}!")


def clock_out(attendance_book):
    """
    Cập nhật giờ ra cho một nhân viên đã chấm công vào trước đó.

    *** Xử lý Tuple cốt lõi ***
    Vì tuple là cấu trúc dữ liệu BẤT BIẾN (immutable) - không thể sửa trực
    tiếp một phần tử trong tuple (ví dụ KHÔNG thể làm record["times"][1] = "18:00")
    nên giải pháp là:
        1. Trích xuất (unpack) Giờ Vào cũ từ tuple hiện tại.
        2. Tạo một TUPLE HOÀN TOÀN MỚI kết hợp (Giờ Vào cũ, Giờ Ra mới).
        3. Ghi đè (gán lại) tuple mới này vào key "times" của dictionary.

    Input:
        attendance_book (list[dict]): danh sách hồ sơ chấm công, sẽ bị thay
                                       đổi trực tiếp (in-place) nếu thành công.
    Output:
        None: hàm chỉ in kết quả ra màn hình và cập nhật attendance_book.

    Pseudocode (Chức năng 3 - Chấm công Ra):
        - Nhập mã nhân viên.
        - Tìm index hồ sơ bằng _find_record_index().
        - Nếu index == -1 -> in "Không tìm thấy nhân viên!" và return.
        - Trích xuất tuple times hiện tại: old_clock_in, old_clock_out = record["times"].
        - Nếu old_clock_out đã có giá trị (khác None)
            -> in "Nhân viên đã chấm công ra trước đó!" và return
               (tránh ghi đè giờ ra hai lần).
        - Nhập giờ ra mới (HH:MM).
        - Tạo TUPLE MỚI: new_times = (old_clock_in, giờ_ra_mới).
        - Ghi đè: record["times"] = new_times.
        - In thông báo chấm công ra thành công.
    """
    employee_id = input("Nhập mã nhân viên: ").strip().upper()
    index = _find_record_index(attendance_book, employee_id)

    if index == -1:
        print("Không tìm thấy nhân viên!")
        return

    record = attendance_book[index]
    old_clock_in, old_clock_out = record["times"]  # Trích xuất tuple cũ.

    if old_clock_out is not None:
        print("Nhân viên đã chấm công ra trước đó!")
        return

    clock_out_time = input("Nhập giờ ra (HH:MM): ").strip()

    # Tạo tuple HOÀN TOÀN MỚI (Giờ Vào cũ, Giờ Ra mới) rồi ghi đè lại vào "times".
    new_times = (old_clock_in, clock_out_time)
    record["times"] = new_times

    print(f"Thành công: Đã ghi nhận {employee_id} chấm công ra lúc {clock_out_time}!")
