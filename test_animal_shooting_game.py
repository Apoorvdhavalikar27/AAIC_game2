import unittest
from unittest.mock import patch
import tkinter as tk
from animal_shooting_game import Animal, Gun, GameApp

class TestAnimal(unittest.TestCase):
    def setUp(self):
        self.canvas = tk.Canvas(tk.Tk())
        self.animal = Animal("TestAnimal", 10, 100, 100, "red")

    def test_initialization(self):
        self.assertEqual(self.animal.name, "TestAnimal")
        self.assertEqual(self.animal.points, 10)
        self.assertEqual(self.animal.x, 100)
        self.assertEqual(self.animal.y, 100)
        self.assertEqual(self.animal.color, "red")
        self.assertIsNone(self.animal.id)
        self.assertIsNone(self.animal.text_id)
        self.assertIn(self.animal.move_direction, ["up", "down", "left", "right"])
        self.assertGreaterEqual(self.animal.move_speed, 5)
        self.assertLessEqual(self.animal.move_speed, 20)

    def test_draw(self):
        self.animal.draw(self.canvas)
        self.assertIsNotNone(self.animal.id)
        self.assertIsNotNone(self.animal.text_id)


class TestGun(unittest.TestCase):
    def setUp(self):
        self.gun = Gun("TestGun")

    def test_initialization(self):
        self.assertEqual(self.gun.name, "TestGun")

    def test_shoot_no_hit(self):
        animals = [Animal("Rabbit", 10, 100, 100, "brown")]
        result = self.gun.shoot(0, 0, animals)
        self.assertIsNone(result)

    def test_shoot_hit(self):
        animals = [Animal("Rabbit", 10, 100, 100, "brown")]
        result = self.gun.shoot(100, 100, animals)
        self.assertEqual(result, animals[0])

class TestGameApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = GameApp(self.root)
        self.app.canvas.pack()

    def tearDown(self):
        self.root.destroy()

    def test_initialization(self):
        self.assertEqual(self.app.weapons, ["Pistol", "Rifle", "Shotgun", "Sniper"])
        self.assertEqual(self.app.selected_weapon.get(), "Pistol")
        self.assertEqual(len(self.app.animals), 5)
        self.assertIsInstance(self.app.canvas, tk.Canvas)
        self.assertIsNotNone(self.app.gun.name)
        self.assertEqual(self.app.total_points, 0)

    @patch('tkinter.messagebox.showinfo')
    def test_quit_game(self, mock_showinfo):
        self.app.quit_game()
        mock_showinfo.assert_called_once_with("Total Score", "Your total score is: 0")

if __name__ == "__main__":
    unittest.main()
