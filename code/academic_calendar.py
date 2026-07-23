"""
================================================================================
ACADEMIC_CALENDAR.PY — JNTUK R23 Academic Calendar & Timetable Engine
JNTUK R23 B.Tech AI & Data Science — Project 17 (V2)
================================================================================
[R23 Topic: Operational Analytics & Calendar Math]
Calculates total instructional working days and lab sessions factoring in:
  - Sem 1-1 Duration: Aug 4, 2025 to Jan 21, 2026
  - Sem 1-2 Duration: Jan 26, 2026 to Jul 9, 2026
  - 2nd Saturday Holidays rule
  - Official Public Holidays
================================================================================
"""

import datetime


class JNTUKAcademicCalendar:
    """
    [R23 Topic: Operational Analytics & Calendar Math]
    Calculates total instructional working days and lab sessions factoring in:
      - Sem 1-1 Duration: Aug 4, 2025 to Jan 21, 2026
      - Sem 1-2 Duration: Jan 26, 2026 to Jul 9, 2026
      - 2nd Saturday Holidays rule
      - Official Public Holidays
    """

    # ---- Semester Date Ranges ----
    SEM_1_1_START = datetime.date(2025, 8, 4)
    SEM_1_1_END = datetime.date(2026, 1, 21)

    SEM_1_2_START = datetime.date(2026, 1, 26)
    SEM_1_2_END = datetime.date(2026, 7, 9)

    # ---- Official Public Holidays ----
    PUBLIC_HOLIDAYS = {
        datetime.date(2025, 8, 15): "Independence Day",
        datetime.date(2025, 10, 2): "Gandhi Jayanti",
        datetime.date(2025, 10, 20): "Vijaya Dasami / Dussehra",
        datetime.date(2025, 11, 1): "Diwali",
        datetime.date(2026, 1, 14): "Sankranti / Bhogi",
        datetime.date(2026, 1, 15): "Makara Sankranti",
        datetime.date(2026, 1, 26): "Republic Day",
        datetime.date(2026, 3, 4): "Maha Shivaratri",
        datetime.date(2026, 3, 25): "Holi",
        datetime.date(2026, 4, 14): "Dr. B.R. Ambedkar Jayanti",
        datetime.date(2026, 5, 1): "May Day",
    }

    @classmethod
    def get_working_days(
        cls, start_date: datetime.date, end_date: datetime.date
    ) -> tuple[int, int]:
        """
        Counts instructional working days and lab slots between two dates.
        Excludes Sundays, 2nd Saturdays, and public holidays.
        Labs are scheduled on Monday, Wednesday, and Friday.

        Returns:
            tuple[int, int]: (working_days, lab_slots)
        """
        current = start_date
        working_days = 0
        lab_slots = 0

        while current <= end_date:
            weekday = current.weekday()  # Mon=0, Sun=6

            if weekday != 6:  # Sunday is always a holiday
                is_second_saturday = weekday == 5 and 8 <= current.day <= 14
                is_public_holiday = current in cls.PUBLIC_HOLIDAYS

                if not is_second_saturday and not is_public_holiday:
                    working_days += 1
                    if weekday in [0, 2, 4]:  # Labs on Mon, Wed, Fri
                        lab_slots += 1

            current += datetime.timedelta(days=1)

        return working_days, lab_slots

    @classmethod
    def get_semester_stats(cls) -> dict:
        """
        Returns a dictionary with working day and lab statistics for both semesters.
        """
        w_1_1, l_1_1 = cls.get_working_days(cls.SEM_1_1_START, cls.SEM_1_1_END)
        w_1_2, l_1_2 = cls.get_working_days(cls.SEM_1_2_START, cls.SEM_1_2_END)
        return {
            'sem1_1_working_days': w_1_1,
            'sem1_1_lab_slots': l_1_1,
            'sem1_2_working_days': w_1_2,
            'sem1_2_lab_slots': l_1_2,
            'total_working_days': w_1_1 + w_1_2,
            'total_lab_slots': l_1_1 + l_1_2,
        }
