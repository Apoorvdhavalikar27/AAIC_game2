import tkinter as tk
import random
from tkinter import messagebox

class Animal:
    def __init__(self, name, points, x, y, color):
        self.name = name
        self.points = points
        self.x = x
        self.y = y
        self.color = color
        self.id = None
        self.text_id = None
        self.move_speed = random.randint(20, 20)
        self.move_direction = random.choice(["up", "down", "left", "right"])

    def draw(self, canvas):
        self.id = canvas.create_oval(self.x-20, self.y-20, self.x+20, self.y+20, fill=self.color)
        self.text_id = canvas.create_text(self.x, self.y, text=self.name, fill="white")

    def move_randomly(self, canvas):
        if self.move_direction == "up":
            self.y -= self.move_speed
            if self.y < 20:
                self.y = 20
                self.move_direction = random.choice(["down", "left", "right"])
        elif self.move_direction == "down":
            self.y += self.move_speed
            if self.y > 380:
                self.y = 380
                self.move_direction = random.choice(["up", "left", "right"])
        elif self.move_direction == "left":
            self.x -= self.move_speed
            if self.x < 20:
                self.x = 20
                self.move_direction = random.choice(["up", "down", "right"])
        elif self.move_direction == "right":
            self.x += self.move_speed
            if self.x > 380:
                self.x = 380
                self.move_direction = random.choice(["up", "down", "left"])
        
        canvas.coords(self.id, self.x-20, self.y-20, self.x+20, self.y+20)
        canvas.coords(self.text_id, self.x, self.y)

class Gun:
    def __init__(self, name):
        self.name = name

    def shoot(self, x, y, animals):
        for animal in animals:
            if abs(animal.x - x) < 20 and abs(animal.y - y) < 20:
                return animal
        return None

class GameApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Animal Shooting Game")

        self.weapons = ["Pistol", "Rifle", "Shotgun", "Sniper"]

        # Set default weapon
        self.selected_weapon = tk.StringVar()
        self.selected_weapon.set(self.weapons[0])

        # Define animals
        self.animals = [
            Animal("Rabbit", 10, random.randint(50, 350), random.randint(50, 350), "brown"),
            Animal("Deer", 20, random.randint(50, 350), random.randint(50, 350), "tan"),
            Animal("Bear", 50, random.randint(50, 350), random.randint(50, 350), "darkgrey"),
            Animal("Fox", 15, random.randint(50, 350), random.randint(50, 350), "orange"),
            Animal("Wolf", 30, random.randint(50, 350), random.randint(50, 350), "grey")
        ]

        # Define gun
        self.gun = Gun("Pistol")

        # Create canvas to display animals
        self.canvas = tk.Canvas(master, width=550, height=550)
        self.canvas.pack()
        
        for animal in self.animals:
            animal.draw(self.canvas)
        
        self.weapon_menu = tk.OptionMenu(master, self.selected_weapon, *self.weapons)
        self.weapon_menu.pack(side="top", anchor="nw")

        # Create fire button
        self.fire_button = tk.Button(master, text="Fire", command=self.fire_bullet)
        self.fire_button.pack()
        self.fire_button.bind("<Motion>", self.move_fire_button)

        # Create quit button and place it on top
        self.quit_button = tk.Button(master, text="Quit", command=self.quit_game)
        self.quit_button.pack(side="left")

        self.total_points = 0
        self.score_text = self.canvas.create_text(50, 20, text=f"Points: {self.total_points}", anchor="nw", tags="score")

        # Move animals randomly
        self.move_animals()

    def move_animals(self):
        for animal in self.animals:
            animal.move_randomly(self.canvas)
        self.master.after(500, self.move_animals)

    def move_fire_button(self, event):
        new_left = event.x_root - self.master.winfo_rootx() - (self.fire_button.winfo_width() // 2)
        new_left = max(0, min(self.master.winfo_width() - self.fire_button.winfo_width(), new_left))
        self.fire_button.place(x=new_left, y=self.fire_button.winfo_y())

    def fire_bullet(self):
        bullet_x, bullet_y = self.fire_button.winfo_x() + self.fire_button.winfo_width() // 2, self.fire_button.winfo_y() + self.fire_button.winfo_height() // 2
        bullet_id = self.canvas.create_oval(bullet_x, bullet_y, bullet_x+5, bullet_y+5, fill="red")
        
        self.animate_bullet(bullet_id)

    def animate_bullet(self, bullet_id):
        bullet_coords = self.canvas.coords(bullet_id)
        bullet_x, bullet_y = bullet_coords[0], bullet_coords[1]

        if bullet_y > 0:
            self.canvas.move(bullet_id, 0, -10)
            self.master.after(50, self.animate_bullet, bullet_id)
        else:
            self.canvas.delete(bullet_id)

        selected_animal = self.gun.shoot(bullet_x, bullet_y, self.animals)
            
        if selected_animal:
            self.total_points += selected_animal.points
            self.update_score()
            self.canvas.delete(selected_animal.id)
            self.canvas.delete(selected_animal.text_id)
            self.animals.remove(selected_animal)

    def update_score(self):
        self.canvas.itemconfig(self.score_text, text=f"Points: {self.total_points}")

    def quit_game(self):
        messagebox.showinfo("Total Score", f"Your total score is: {self.total_points}")
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
