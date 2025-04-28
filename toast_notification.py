import tkinter as tk
import webbrowser
from typing import Literal

Placement = Literal[
    "top-left",
    "top-center",
    "top-right",
    "bottom-left",
    "bottom-center",
    "bottom-right"
]

ToastType = Literal[
    "normal",
    "error",
    "warning",
    "info",
    "success"
]

TYPE_COLORS = {
    "normal": ("#333333", "white"),
    "error": ("#D32F2F", "white"),
    "warning": ("#FFA000", "black"),
    "info": ("#1976D2", "white"),
    "success": ("#388E3C", "white"),
}

class ToastNotification(tk.Tk):
    def __init__(
        self,
        title: str,
        message: str,
        duration: int = 3000,
        width: int = 300,
        height: int = 100,
        position: Placement = "bottom-right",
        margin: int = 20,
        toast_type: ToastType = "normal",
        slide_speed: int = 20,   # pixels per frame
        slide_interval: int = 10, # ms between moves
        url: str | None = None
    ):
        super().__init__()

        self.title_text = title
        self.message_text = message
        self.duration = duration
        self.width = width
        self.height = height
        self.position = position
        self.margin = margin
        self.toast_type = toast_type
        self.url = url

        self.slide_speed = slide_speed
        self.slide_interval = slide_interval

        self.setup_window()

        self.show_message()

        # Start slide animation from off-screen
        self.after(0, self.slide_in)
        self.bind("<Button-1>", self.on_click)

    def setup_window(self):
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        bg_color, _ = TYPE_COLORS.get(self.toast_type, ("#333333", "white"))
        self.configure(bg=bg_color)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Final target position
        self.target_x, self.target_y = self.calculate_position(screen_width, screen_height)

        # Starting position: off screen, depending on placement
        # We'll slide horizontally from off screen on X-axis (left or right side),
        # or from top or bottom depending on placement.

        # For simplicity, slide horizontally from left if on left side,
        # from right if on right side, else vertically from top or bottom.

        if "left" in self.position:
            self.current_x = -self.width  # fully off left screen
            self.current_y = self.target_y
            self.slide_axis = "x"
            self.slide_direction = 1  # slide rightward toward target_x
        elif "right" in self.position:
            self.current_x = screen_width
            self.current_y = self.target_y
            self.slide_axis = "x"
            self.slide_direction = -1  # slide leftward toward target_x
        elif "top" in self.position:
            self.current_x = self.target_x
            self.current_y = -self.height
            self.slide_axis = "y"
            self.slide_direction = 1  # slide downward toward target_y
        else:  # bottom center
            self.current_x = self.target_x
            self.current_y = screen_height
            self.slide_axis = "y"
            self.slide_direction = -1  # slide upward toward target_y

        self.geometry(f"{self.width}x{self.height}+{self.current_x}+{self.current_y}")

    def calculate_position(self, screen_width: int, screen_height: int):
        margin = self.margin
        match self.position:
            case "top-left":
                x = margin
                y = margin
            case "top-center":
                x = (screen_width - self.width) // 2
                y = margin
            case "top-right":
                x = screen_width - self.width - margin
                y = margin
            case "bottom-left":
                x = margin
                y = screen_height - self.height - margin
            case "bottom-center":
                x = (screen_width - self.width) // 2
                y = screen_height - self.height - margin
            case "bottom-right":
                x = screen_width - self.width - margin
                y = screen_height - self.height - margin
            case _:
                x = screen_width - self.width - margin
                y = screen_height - self.height - margin

        return x, y

    def show_message(self):
        bg_color, fg_color = TYPE_COLORS.get(self.toast_type, ("#333333", "white"))

        title_label = tk.Label(
            self,
            text=self.title_text,
            bg=bg_color,
            fg=fg_color,
            font=("Segoe UI", 14, "bold"),
            anchor="w"
        )
        title_label.pack(fill="x", padx=10, pady=(10, 0))

        message_label = tk.Label(
            self,
            text=self.message_text,
            bg=bg_color,
            fg=fg_color,
            font=("Segoe UI", 11),
            anchor="w",
            justify="left",
            wraplength=self.width - 20
        )
        message_label.pack(fill="both", expand=True, padx=10, pady=(5, 10))

    def slide_in(self):
        # Move incrementally toward target position
        if self.slide_axis == "x":
            if (self.slide_direction > 0 and self.current_x < self.target_x) or \
               (self.slide_direction < 0 and self.current_x > self.target_x):
                self.current_x += self.slide_speed * self.slide_direction
                # Clamp to target_x
                if (self.slide_direction > 0 and self.current_x > self.target_x) or \
                   (self.slide_direction < 0 and self.current_x < self.target_x):
                    self.current_x = self.target_x
                self.geometry(f"{self.width}x{self.height}+{self.current_x}+{self.current_y}")
                self.after(self.slide_interval, self.slide_in)
            else:
                # Reached target, hold duration then fade out
                self.after(self.duration, self.fade_out)
        else:
            if (self.slide_direction > 0 and self.current_y < self.target_y) or \
               (self.slide_direction < 0 and self.current_y > self.target_y):
                self.current_y += self.slide_speed * self.slide_direction
                # Clamp to target_y
                if (self.slide_direction > 0 and self.current_y > self.target_y) or \
                   (self.slide_direction < 0 and self.current_y < self.target_y):
                    self.current_y = self.target_y
                self.geometry(f"{self.width}x{self.height}+{self.current_x}+{self.current_y}")
                self.after(self.slide_interval, self.slide_in)
            else:
                # Reached target, hold duration then fade out
                self.after(self.duration, self.fade_out)

    def fade_out(self):
        # Use fade out like before
        opacity = self.attributes("-alpha") or 1.0
        step = 0.05
        new_opacity = opacity - step
        if new_opacity <= 0:
            self.destroy()
        else:
            self.attributes("-alpha", new_opacity)
            self.after(30, self.fade_out)

    def on_click(self, event):
        if self.url:
            try:
                # Attempt to open with Chrome first
                webbrowser.get(using='chrome').open(self.url)
            except:
                # Fallback to default browser
                webbrowser.open(self.url)

def show_toast(
    title: str,
    message: str,
    duration: int = 3000,
    width: int = 300,
    height: int = 100,
    position: Placement = "bottom-right",
    margin: int = 20,
    toast_type: ToastType = "normal",
    slide_speed: int = 20,
    slide_interval: int = 10,
    url: str | None = None
):
    toast = ToastNotification(
        title=title,
        message=message,
        duration=duration,
        width=width,
        height=height,
        position=position,
        margin=margin,
        toast_type=toast_type,
        slide_speed=slide_speed,
        slide_interval=slide_interval,
        url=url
    )
    toast.mainloop()
