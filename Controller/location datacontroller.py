# controller.py
from model import ExamSchedule


class ExamScheduleController:
    def __init__(self):
        self.exam_schedule = ExamSchedule(
            "Semester Exam Schedule",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            ["9 AM", "12 PM", "3 PM"],
        )
        self.days = list(self.exam_schedule.schedule.keys())
        self.time_slots = list(next(iter(self.exam_schedule.schedule.values())).keys())

    def book_exam(self, day, time_slot, subject, duration):
        return self.exam_schedule.book_exam(day, time_slot, subject, duration)

    def cancel_exam(self, day, time_slot):
        return self.exam_schedule.cancel_exam(day, time_slot)

    def get_schedule(self):
        return self.exam_schedule.get_schedule()
