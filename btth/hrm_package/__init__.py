"""
hrm_package/__init__.py
-------------------------
Biến thư mục hrm_package/ thành một package Python.

Re-export các hàm quan trọng từ các module con (ui_display, attendance_logic,
time_calc) ngay tại cấp package, giúp main.py có thể import gọn gàng:

    from hrm_package import display_records, clock_in, clock_out
    from hrm_package.time_calc import evaluate_flex_time as evaluate_shifts

(Riêng evaluate_flex_time vẫn được import trực tiếp từ module con tại main.py
 để minh họa cú pháp "Advanced Import" với alias "as" theo yêu cầu đề bài.)
"""

from hrm_package.ui_display import display_records
from hrm_package.attendance_logic import clock_in, clock_out

__all__ = [
    "display_records",
    "clock_in",
    "clock_out",
]
