import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BULLET_RADIUS = 10

class CannonGame(Widget):
    def __init__(self, **kwargs):
        super(CannonGame, self).__init__(**kwargs)
        self.cannon = Cannon()
        self.target = Target()
        self.projectiles = []

    def update(self, dt):
        for projectile in self.projectiles:
            projectile.update(dt)
            if projectile.collide_widget(self.target):
                self.remove_widget(projectile)
                self.target.hit()

    def on_touch_down(self, touch):
        if touch.x < SCREEN_WIDTH / 2:
            self.cannon.rotate_towards(touch.pos)

    def fire_bullet(self, velocity):
        bullet = Bullet(pos=self.cannon.pos, velocity=velocity)
        self.projectiles.append(bullet)
        self.add_widget(bullet)


class Cannon(Widget):
    def rotate_towards(self, pos):
        # Calculate angle between cannon and touch position
        pass


class Target(Widget):
    def __init__(self, **kwargs):
        super(Target, self).__init__(**kwargs)
        self.hits = 0
        self.label = Label(text="Hits: 0", pos=(50, 50))
        self.add_widget(self.label)

    def hit(self):
        self.hits += 1
        self.label.text = f"Hits: {self.hits}"


class Bullet(Widget):
    def __init__(self, velocity=(100, 0), **kwargs):
        super(Bullet, self).__init__(**kwargs)
        self.velocity = velocity

    def update(self, dt):
        self.pos = (self.pos[0] + self.velocity[0] * dt, self.pos[1] + self.velocity[1] * dt)


class CannonGameApp(App):
    def build(self):
        game = CannonGame()
        Clock.schedule_interval(game.update, 1.0 / FPS)
        return game

if __name__ == '__main__':
    CannonGameApp().run()
