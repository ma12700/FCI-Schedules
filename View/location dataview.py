# view.py
import tkinter as tk
from tkinter import messagebox, ttk


class ExamScheduleGUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Exam Schedule Management")
        self.root.configure(bg="#f4f4f9")
        self.root.geometry("900x600")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Manage Exam Schedule", bg="#4CAF50", fg="white", pady=10)
        self.label.pack(fill=tk.X)

        form_frame = tk.Frame(self.root, bg="#f4f4f9")
        form_frame.pack(fill=tk.X)

        self.create_form_row(form_frame, "Day", 0, "days")
        self.create_form_row(form_frame, "Time Slot", 1, "time_slots")
        self.create_form_row(form_frame, "Subject", 2)
        self.create_form_row(form_frame, "Duration (hours)", 3)

        button_frame = tk.Frame(self.root, bg="#f4f4f9")
        button_frame.pack(fill=tk.X)

        self.create_button(button_frame, "Book Exam", self.book_exam, 0)
        self.create_button(button_frame, "Cancel Exam", self.cancel_exam, 1)
        self.create_button(button_frame, "Refresh Grid", self.refresh_schedule, 2)

        self.grid_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.create_schedule_grid()

    def create_form_row(self, parent, label, row, combo_source=None):
        tk.Label(parent, text=label, bg="#f4f4f9").grid(row=row, column=0, sticky="w", padx=10, pady=5)
        if combo_source:
            # Validate attribute existence
            if not hasattr(self.controller, combo_source):
                raise AttributeError(f"{combo_source} is not a valid attribute in the controller.")
            
            values = getattr(self.controller, combo_source)
            combo = ttk.Combobox(parent, values=values)
            combo.grid(row=row, column=1, sticky="w", padx=10, pady=5)
            setattr(self, f"{label.lower().replace(' ', '_')}_combobox", combo)
        else:
            entry = tk.Entry(parent)
            entry.grid(row=row, column=1, sticky="w", padx=10, pady=5)
            setattr(self, f"{label.lower().replace(' ', '_')}_entry", entry)

    def create_button(self, parent, text, command, column):
        btn = tk.Button(parent, text=text, bg="#4CAF50", fg="white", command=command)
        btn.grid(row=0, column=column, padx=10, pady=5)

    def create_schedule_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        schedule = self.controller.get_schedule()

        tk.Label(self.grid_frame, text="Day/Time", bg="#d9e8f5").grid(row=0, column=0, padx=5, pady=5)
        for col, time_slot in enumerate(self.controller.time_slots, start=1):
            tk.Label(self.grid_frame, text=time_slot, bg="#d9e8f5").grid(row=0, column=col, padx=5, pady=5)

        for row, (day, slots) in enumerate(schedule.items(), start=1):
            tk.Label(self.grid_frame, text=day, bg="#d9e8f5").grid(row=row, column=0, padx=5, pady=5)
            for col, (time_slot, details) in enumerate(slots.items(), start=1):
                color = "green" if details["status"] == "Available" else "red"
                subject = details["subject"] if details["subject"] else "Available"
                tk.Button(
                    self.grid_frame,
                    text=subject,
                    bg=color,
                    fg="white",
                    relief=tk.RIDGE,
                    width=12,
                ).grid(row=row, column=col, padx=5, pady=5)

    def book_exam(self):
        day = self.day_combobox.get()
        time_slot = self.time_slot_combobox.get()
        subject = self.subject_entry.get()
        duration = self.duration_entry.get()

        if not duration.isdigit():
            messagebox.showerror("Invalid input", "Duration must be a number")
            return

        result = self.controller.book_exam(day, time_slot, subject, int(duration))
        messagebox.showinfo("Action Result", result)
        self.refresh_schedule()

    def cancel_exam(self):
        day = self.day_combobox.get()
        time_slot = self.time_slot_combobox.get()
        result = self.controller.cancel_exam(day, time_slot)
        messagebox.showinfo("Action Result", result)
        self.refresh_schedule()

    def refresh_schedule(self):
        self.create_schedule_grid()
