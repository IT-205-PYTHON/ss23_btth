"""
hrm_package/time_calc.py
----------------------------
Chứa logic tính toán thời gian và đánh giá vi phạm luật Flex-time.
- evaluate_flex_time(attendance_book): đánh giá vi phạm (chức năng 4).

Module chuẩn sử dụng: datetime (datetime.strptime để chuyển chuỗi "HH:MM"
thành đối tượng thời gian, phục vụ việc so sánh và tính khoảng cách giờ).

Luật Flex-time:
    - Khung giờ chuẩn: 08:30 - 17:30 (tổng 9 tiếng, đã tính cả nghỉ trưa).
    - Được phép đến muộn tối đa 90 phút (từ 08:31 đến 10:00), nhưng phải làm
      bù giờ: Giờ về = Giờ vào + 9 tiếng.
    - Nếu Giờ vào > 10:00 -> vi phạm "Đến muộn quá 90 phút" (không cần xét
      tiếp giờ ra).
    - Nếu Giờ vào hợp lệ (<= 10:00):
        + Tính (Giờ Ra - Giờ Vào).
        + Nếu tổng thời gian < 9 tiếng -> vi phạm "Về sớm, chưa hoàn thành
          đủ 9 tiếng bù giờ".
        + Nếu đủ (>=) 9 tiếng -> hợp lệ "Hoàn thành ca làm việc".
"""

from datetime import datetime, timedelta

# Mốc giờ vào muộn nhất được phép (08:31 - 10:00).
LATEST_VALID_CLOCK_IN = "10:00"

# Tổng số giờ làm việc chuẩn phải hoàn thành trong ngày (gồm cả nghỉ trưa).
REQUIRED_WORK_HOURS = 9


def evaluate_flex_time(attendance_book):
    """
    Đánh giá vi phạm luật Flex-time cho toàn bộ nhân viên trong attendance_book.

    Input:
        attendance_book (list[dict]): danh sách hồ sơ chấm công, mỗi hồ sơ gồm
            "id", "name", "times" (tuple Giờ Vào, Giờ Ra; Giờ Ra có thể None).
    Output:
        None: hàm chỉ in kết quả đánh giá ra màn hình, không trả về giá trị.

    Pseudocode:
        - Nếu attendance_book rỗng -> in "Chưa có dữ liệu chấm công." và return.
        - In tiêu đề "--- ĐÁNH GIÁ VI PHẠM FLEX-TIME ---".
        - Duyệt qua từng nhân viên trong attendance_book:
            -> Trích xuất giờ vào, giờ ra từ tuple "times".
            -> Nếu giờ ra là None (chưa chấm công ra)
                -> in "<mã> - Chưa hoàn tất: Chưa chấm công ra." và bỏ qua
                   (không đánh giá tiếp, vì đề bài chỉ yêu cầu xét khi đã đủ
                   cả Giờ Vào và Giờ Ra).
            -> Chuyển đổi chuỗi giờ vào, giờ ra, và mốc "10:00" thành đối
               tượng datetime bằng datetime.strptime(chuỗi, "%H:%M").
            -> Nếu giờ vào > mốc 10:00:
                -> in "<mã> - Vi phạm: Đến muộn quá 90 phút."
            -> Ngược lại (giờ vào <= 10:00):
                -> Tính khoảng thời gian làm việc = giờ_ra - giờ_vào (timedelta).
                -> Nếu khoảng thời gian < 9 tiếng (timedelta(hours=9)):
                    -> in "<mã> - Vi phạm: Về sớm, chưa hoàn thành đủ 9 tiếng
                       bù giờ."
                -> Ngược lại (đủ hoặc nhiều hơn 9 tiếng):
                    -> in "<mã> - Hợp lệ: Hoàn thành ca làm việc."
        - In dòng kết thúc.
    """
    if not attendance_book:
        print("Chưa có dữ liệu chấm công.")
        return

    print("--- ĐÁNH GIÁ VI PHẠM FLEX-TIME ---")

    latest_valid_time = datetime.strptime(LATEST_VALID_CLOCK_IN, "%H:%M")
    required_duration = timedelta(hours=REQUIRED_WORK_HOURS)

    for record in attendance_book:
        clock_in_str, clock_out_str = record["times"]

        if clock_out_str is None:
            print(f"{record['id']} - Chưa hoàn tất: Chưa chấm công ra.")
            continue

        clock_in_dt = datetime.strptime(clock_in_str, "%H:%M")
        clock_out_dt = datetime.strptime(clock_out_str, "%H:%M")

        if clock_in_dt > latest_valid_time:
            print(f"{record['id']} - Vi phạm: Đến muộn quá 90 phút.")
        else:
            worked_duration = clock_out_dt - clock_in_dt

            if worked_duration < required_duration:
                print(
                    f"{record['id']} - Vi phạm: Về sớm, chưa hoàn thành "
                    f"đủ 9 tiếng bù giờ."
                )
            else:
                print(f"{record['id']} - Hợp lệ: Hoàn thành ca làm việc.")

    print("------------------------------------------------")
