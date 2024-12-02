import customtkinter as ctk
from tkinter import Canvas, Label
import time


class FTrackApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FTrack - Dynamic Sales Organizer")
        self.geometry("1920x1080")
        self.configure(fg_color="#161721")  # Dark background

        # Stopwatch variables
        self.start_time = None
        self.running = False
        self.elapsed_before_stop = 0

        self.counters = []
        self.total_profit = 0
        self.counter_spacing = 300  # Spacing between counters

        # Header
        self.total_label = ctk.CTkLabel(
            self,
            text="Total Profit: ￦0",
            font=("Arial", 20),
            text_color="white",
        )
        self.total_label.pack(pady=10)

        # Stopwatch Label
        self.stopwatch_label = Label(
            self, text="00:00:00", font=("Arial", 20), bg="#161721", fg="white"
        )
        self.stopwatch_label.place(x=890, y=10)
        self.update_stopwatch()

        # Stopwatch Control Buttons
        self.start_stop_button = ctk.CTkButton(
            self,
            text="Start/Stop",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="white",
            corner_radius=10,
            width = 10,
            command=self.toggle_stopwatch,
        )
        self.start_stop_button.place(x=1020, y=10)

        self.reset_button = ctk.CTkButton(
            self,
            text="Reset",
            fg_color="#ff0077",
            hover_color="#d6005e",
            text_color="white",
            corner_radius=10,
            width = 10,
            command=self.reset_stopwatch,
        )
        self.reset_button.place(x=1110, y=10)

        # Canvas Labels
        self.canvas_label = ctk.CTkLabel(
            self,
            text="FTrack, by the Computer Research Division",
            font=("Arial", 13),
            text_color="white"
        )
        self.canvas_label.place(x=20, y=10)
        self.canvas_label2 = ctk.CTkLabel(
            self,
            text="SpadesTech",
            font=("Arial", 13),
            text_color="white"
        )
        self.canvas_label2.place(x=20, y=30)

        # Canvas for draggable boxes
        self.counters_canvas = Canvas(
            self, bg="#252636", highlightthickness=0, width=900, height=550
        )  # Dark gray canvas
        self.counters_canvas.pack(pady=10, padx=20, fill="both", expand=True)

        # Add Counter Button
        self.add_counter_button = ctk.CTkButton(
            self,
            text="Add Counter",
            fg_color="#3b82f6",  # Blue button
            hover_color="#2563eb",
            text_color="white",
            corner_radius=10,
            width=1000,
            command=self.add_counter,
        )
        self.add_counter_button.pack(pady=10)

    def update_stopwatch(self):
        if self.running:
            elapsed_time = time.time() - self.start_time + self.elapsed_before_stop
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            milliseconds = int((elapsed_time - int(elapsed_time)) * 100)
            self.stopwatch_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}")
        self.after(10, self.update_stopwatch)

    def toggle_stopwatch(self):
        if self.running:
            self.stop_stopwatch()
        else:
            self.start_stopwatch()

    def start_stopwatch(self):
        if not self.running:
            self.start_time = time.time()
            self.running = True

    def stop_stopwatch(self):
        if self.running:
            self.running = False
            self.elapsed_before_stop += time.time() - self.start_time

    def reset_stopwatch(self):
        self.start_time = None
        self.running = False
        self.elapsed_before_stop = 0
        self.stopwatch_label.config(text="00:00:00")

    def get_elapsed_time(self):
        if self.start_time is None:
            return 0
        return time.time() - self.start_time if self.running else self.elapsed_before_stop

    def add_counter(self):
        # Determine position to place the new counter
        x, y = self.get_next_available_position()
        counter = Counter(self.counters_canvas, self.update_total_profit, self.remove_counter)
        self.counters.append(counter)
        counter_id = self.counters_canvas.create_window(x, y, window=counter, anchor="nw")
        counter.set_canvas_and_id(self.counters_canvas, counter_id)

    def get_next_available_position(self):
        #why does this work?
        if not self.counters:
            return 10, 10  # Start position for the first counter

        canvas_width = self.counters_canvas.winfo_width()
        num_counters = len(self.counters)

        # Calculate grid position
        col = num_counters % (canvas_width // self.counter_spacing)
        row = num_counters // (canvas_width // self.counter_spacing)

        x = col * self.counter_spacing + 10
        y = row * self.counter_spacing + 10
        return x, y

    def remove_counter(self, counter):
        if counter in self.counters:
            self.counters.remove(counter)
            counter.remove_from_canvas()
            self.update_total_profit()

    def update_total_profit(self):
        self.total_profit = sum(counter.get_profit() for counter in self.counters)
        self.total_label.configure(text=f"Total Profit: ￦{self.total_profit:.2f}")


class Counter(ctk.CTkFrame):
    def __init__(self, parent_canvas, update_total_callback, remove_callback):
        super().__init__(
            master=parent_canvas,
            width=250,
            height=120,
            border_width=4,
            border_color="#999999",
            fg_color="#42445c",  # Dark gray background for counters
            corner_radius=10,
        )

        self.parent_canvas = parent_canvas
        self.update_total_callback = update_total_callback
        self.remove_callback = remove_callback
        self.count = 0
        self.value = 0
        self.canvas_id = None

        # Enable dragging
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.perform_drag)

        # Counter Layout
        self.label_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter label",
            width=200,
            height=40,
            fg_color="#1e1e2e",  # Darker entry background
            text_color="#d1d1e0",  # Light text
        )
        self.label_entry.pack(padx=10, pady=10)

        self.value_entry = ctk.CTkEntry(
            self,
            placeholder_text="Value",
            width=200,
            height=40,
            fg_color="#1e1e2e",
            text_color="#d1d1e0",
        )
        self.value_entry.pack(padx=10)
        self.value_entry.bind("<KeyRelease>", self.update_value)

        # Button Row
        self.button_row = ctk.CTkFrame(self, fg_color="transparent")
        self.button_row.pack(pady=20, padx=20)

        self.decrement_button = ctk.CTkButton(
            self.button_row,
            text="-",
            width=40,
            height=40,
            font=("arial", 20),
            fg_color="#3b82f6",  # Blue button
            hover_color="#2563eb",
            corner_radius=20,
            command=self.decrement_count,
        )
        self.decrement_button.pack(side="left", padx=5)

        self.count_label = ctk.CTkLabel(
            self.button_row,
            text="Count: 0",
            text_color="#d1d1e0",  # Light gray text
            width=60,
        )
        self.count_label.pack(side="left", padx=5)

        self.increment_button = ctk.CTkButton(
            self.button_row,
            text="+",
            width=40,
            height=40,
            font=("arial", 20),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            corner_radius=20,  # Circular button
            command=self.increment_count,
        )
        self.increment_button.pack(side="left", padx=5)

        self.remove_button = ctk.CTkButton(
            self.button_row,
            text="X",
            width=40,
            height=40,
            fg_color="#ff0077",  # Pink button
            hover_color="#d6005e",
            corner_radius=20,  # Circular button
            command=self.show_confirmation,  # Show confirmation
        )
        self.remove_button.pack(side="left", padx=5)

    def set_canvas_and_id(self, canvas, canvas_id):
        self.parent_canvas = canvas
        self.canvas_id = canvas_id

    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def perform_drag(self, event):
        x = self.parent_canvas.coords(self.canvas_id)[0] + event.x - self.drag_start_x
        y = self.parent_canvas.coords(self.canvas_id)[1] + event.y - self.drag_start_y

        # Keep the counter within bounds
        canvas_width = self.parent_canvas.winfo_width()
        canvas_height = self.parent_canvas.winfo_height()
        width, height = self.winfo_width(), self.winfo_height()

        x = max(0, min(x, canvas_width - width))
        y = max(0, min(y, canvas_height - height))

        self.parent_canvas.coords(self.canvas_id, x, y)

    def update_value(self, event=None):
        try:
            self.value = float(self.value_entry.get())
        except ValueError:
            self.value = 0  # Default to 0 if input is invalid
        self.update_total_callback()

    def show_confirmation(self):
        # Clear the button row
        for widget in self.button_row.winfo_children():
            widget.destroy()

        # Add confirmation message
        confirm_label = ctk.CTkLabel(
            self.button_row,
            text="Delete this counter?",
            text_color="#ff7070",  # Red text for warning
        )
        confirm_label.pack(side="left", padx=5)

        # Add confirm button
        confirm_button = ctk.CTkButton(
            self.button_row,
            text="Confirm",
            width=80,
            fg_color="#ff0077",  # Pink button
            hover_color="#d6005e",
            corner_radius=10,
            command=self.remove_self,
        )
        confirm_button.pack(side="left", padx=5)

        # Add cancel button
        cancel_button = ctk.CTkButton(
            self.button_row,
            text="Cancel",
            width=80,
            fg_color="#3b82f6",  # Blue button
            hover_color="#2563eb",
            corner_radius=10,
            command=self.restore_buttons,
        )
        cancel_button.pack(side="left", padx=5)

    def restore_buttons(self):
        for widget in self.button_row.winfo_children():
            widget.destroy()

        self.decrement_button = ctk.CTkButton(
            self.button_row,
            text="-",
            width=40,
            height=40,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            corner_radius=20,
            command=self.decrement_count,
        )
        self.decrement_button.pack(side="left", padx=5)

        self.count_label = ctk.CTkLabel(
            self.button_row,
            text=f"Count: {self.count}",
            text_color="#d1d1e0",
            width=60,
        )
        self.count_label.pack(side="left", padx=5)

        self.increment_button = ctk.CTkButton(
            self.button_row,
            text="+",
            width=40,
            height=40,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            corner_radius=20,
            command=self.increment_count,
        )
        self.increment_button.pack(side="left", padx=5)

        self.remove_button = ctk.CTkButton(
            self.button_row,
            text="X",
            width=40,
            height=40,
            fg_color="#ff0077",
            hover_color="#d6005e",
            corner_radius=20,
            command=self.show_confirmation,
        )
        self.remove_button.pack(side="left", padx=5)

    def increment_count(self):
        self.count += 1
        self.update_display()

    def decrement_count(self):
        if self.count > 0:
            self.count -= 1
            self.update_display()

    def update_display(self):
        self.count_label.configure(text=f"Count: {self.count}")
        self.update_total_callback()

    def get_profit(self):
        return self.count * self.value

    def remove_self(self):
        self.remove_callback(self)

    def remove_from_canvas(self):
        if self.canvas_id is not None:
            self.parent_canvas.delete(self.canvas_id)
            self.destroy()


if __name__ == "__main__":
    app = FTrackApp()
    app.mainloop()
