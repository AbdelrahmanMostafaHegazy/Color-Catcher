import tkinter as tk
from tkinter import ttk
import random
import time

class ColorCatcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Catcher")

        self.score = 0
        self.time_left = 30
        self.level = 1
        self.balls = []
        self.is_paused = False

        self.style = ttk.Style()
        self.style.theme_use('clam')  # Choose a modern theme

        self.canvas = tk.Canvas(root, width=600, height=600, bg="lightblue")
        self.canvas.pack()

        self.basket = self.canvas.create_rectangle(250, 550, 350, 580, fill="blue")
        self.root.bind("<Motion>", self.move_basket)

        self.score_label = ttk.Label(root, text=f"Score: {self.score}")
        self.score_label.pack(pady=5)

        self.time_label = ttk.Label(root, text=f"Time left: {self.time_left} seconds")
        self.time_label.pack(pady=5)

        self.level_label = ttk.Label(root, text=f"Level: {self.level}")
        self.level_label.pack(pady=5)

        self.pause_button = ttk.Button(root, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.restart_button = ttk.Button(root, text="Restart", command=self.restart_game)
        self.restart_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.root.after(1000, self.update_timer)
        self.root.after(1000, self.drop_ball)
        
        # Load sounds
        self.catch_sound = None  # Placeholder for catch sound
        self.special_sound = None  # Placeholder for special sound
        self.end_sound = None  # Placeholder for end sound

    def move_basket(self, event):
        if not self.is_paused:
            x = event.x
            self.canvas.coords(self.basket, x-50, 550, x+50, 580)

    def drop_ball(self):
        if not self.is_paused and self.time_left > 0:
            ball_type = random.choice(["normal", "fast", "special", "powerup"])
            color = random.choice(["red", "green", "yellow", "purple", "orange"])
            x = random.randint(50, 550)
            ball = self.canvas.create_oval(x-15, 0, x+15, 30, fill=color, outline=color, tags=ball_type)
            self.balls.append(ball)
            self.move_ball(ball, ball_type)
            drop_interval = max(1000 - self.level * 100, 200)
            self.root.after(drop_interval, self.drop_ball)

    def move_ball(self, ball, ball_type):
        if not self.is_paused:
            speed = 5 + self.level if ball_type != "fast" else 10 + self.level
            self.canvas.move(ball, 0, speed)
            ball_coords = self.canvas.coords(ball)
            basket_coords = self.canvas.coords(self.basket)

            if ball_coords[3] >= basket_coords[1] and ball_coords[2] >= basket_coords[0] and ball_coords[0] <= basket_coords[2]:
                if ball_type == "normal":
                    self.score += 1
                elif ball_type == "fast":
                    self.score += 2
                elif ball_type == "special":
                    self.score += 5
                    self.play_sound(self.special_sound)
                elif ball_type == "powerup":
                    self.time_left += 5
                    self.score += 1
                    self.play_sound(self.catch_sound)
                    self.canvas.create_text(ball_coords[0], ball_coords[1], text="+5s", fill="gold", font=("Arial", 10))
                self.score_label.config(text=f"Score: {self.score}")
                self.canvas.delete(ball)
                self.balls.remove(ball)
                self.check_level_up()
            elif ball_coords[3] < 600:
                self.root.after(50, self.move_ball, ball, ball_type)
            else:
                self.canvas.delete(ball)
                self.balls.remove(ball)

    def update_timer(self):
        if not self.is_paused and self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=f"Time left: {self.time_left} seconds")
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.end_game()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Resume" if self.is_paused else "Pause")

    def restart_game(self):
        self.score = 0
        self.time_left = 30
        self.level = 1
        self.is_paused = False
        self.score_label.config(text=f"Score: {self.score}")
        self.time_label.config(text=f"Time left: {self.time_left} seconds")
        self.level_label.config(text=f"Level: {self.level}")
        self.canvas.delete("all")
        self.basket = self.canvas.create_rectangle(250, 550, 350, 580, fill="blue")
        for ball in self.balls:
            self.canvas.delete(ball)
        self.balls.clear()
        self.root.after(1000, self.update_timer)
        self.root.after(1000, self.drop_ball)

    def check_level_up(self):
        if self.score >= 10 * self.level:
            self.level += 1
            self.level_label.config(text=f"Level: {self.level}")

    def end_game(self):
        self.play_sound(self.end_sound)
        self.canvas.create_text(300, 300, text="Game Over!", font=("Arial", 24), fill="red")
        self.canvas.create_text(300, 340, text=f"Your Score: {self.score}", font=("Arial", 18), fill="black")
        play_again_button = ttk.Button(self.canvas, text="Play Again", command=self.restart_game)
        self.canvas.create_window(300, 380, window=play_again_button)
        for ball in self.balls:
            self.canvas.delete(ball)
        self.balls.clear()

    def play_sound(self, sound):
        try:
            # Uncomment and replace 'sound' with actual sound file path to play sound
            # winsound.PlaySound(sound, winsound.SND_ASYNC)
            pass
        except Exception as e:
            print(f"Error playing sound: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    game = ColorCatcher(root)
    root.mainloop()
