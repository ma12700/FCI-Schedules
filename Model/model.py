# model.py

class ExamSchedule:
    def __init__(self, name, days, time_slots):
        self.name = name
        self.schedule = {
            day: {slot: {"status": "Available", "subject": None, "duration": None} for slot in time_slots}
            for day in days
        }
    
    def book_exam(self, day, time_slot, subject, duration):
        if day in self.schedule and time_slot in self.schedule[day]:
            if self.schedule[day][time_slot]["status"] == "Available":
                self.schedule[day][time_slot] = {"status": "Reserved", "subject": subject, "duration": duration}
                return f"Exam for {subject} booked at {time_slot} on {day} for {duration} hour(s)."
            else:
                return f"Time slot {time_slot} on {day} is already reserved."
        else:
            return "Invalid day or time slot."
    
    def cancel_exam(self, day, time_slot):
        if day in self.schedule and time_slot in self.schedule[day]:
            if self.schedule[day][time_slot]["status"] == "Reserved":
                self.schedule[day][time_slot] = {"status": "Available", "subject": None, "duration": None}
                return f"Booking canceled at {time_slot} on {day}."
            else:
                return f"No exam booked at {time_slot} on {day}."
        else:
            return "Invalid day or time slot."
    
    def get_schedule(self):
        return self.schedule
