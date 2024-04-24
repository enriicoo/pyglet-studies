import pyglet
import random
from pyglet.window import key
from pyglet.text import Label
from pyglet.graphics.shader import Shader, ShaderProgram

# Window Settings
window = pyglet.window.Window(width=800, height=600)
ball_speed_x = 200
ball_speed_y = 200
ball = pyglet.shapes.Circle(x=400, y=300, radius=10, color=(255, 255, 255))
paddle1 = pyglet.shapes.Rectangle(x=50, y=250, width=20, height=100, color=(255, 255, 255))
paddle2 = pyglet.shapes.Rectangle(x=730, y=250, width=20, height=100, color=(255, 255, 255))
paddle_speed = 300
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Scoring variables
score1 = 0
score2 = 0
score_display = Label(f"{score1}   {score2}", x=window.width // 2, y=window.height - 30,
                      anchor_x='center', font_size=24)

# Shaders
vertex_shader = """
#version 330 core
layout(location = 0) in vec2 position;
uniform mat4 projection;
void main() {
    gl_Position = projection * vec4(position, 0.0, 1.0);
}
"""

fragment_shader = """
#version 330
uniform vec4 box_color;
out vec4 FragColor;
void main() {
    FragColor = box_color;
}
"""

class Scene:
    def __init__(self):
        self.is_active = False  # Add this line to manage scene activity state

    def enter(self):
        self.is_active = True

    def exit(self):
        self.is_active = False

    def update(self, dt):
        pass

    def draw(self):
        pass

    def handle_mouse_press(self, x, y, button, modifiers):
        pass

class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        self.title_label = Label(f"Ping-Pong!", x=window.width // 2, y=window.height // 2 + 100, anchor_x='center', font_size=48, color=(255, 255, 255, 255))
        self.new_game_button = Button("New Game", window.width // 2 - 150, window.height // 2, 300, 50, self.start_new_game)
        self.options_button = Button("Options", window.width // 2 - 150, window.height // 2 - 60, 300, 50, self.show_options)

    def draw(self):
        self.title_label.draw()
        self.new_game_button.draw()
        self.options_button.draw()

    def handle_mouse_press(self, x, y, button, modifiers):
        self.new_game_button.check_click(x, y)
        self.options_button.check_click(x, y)

    def start_new_game(self):
        global current_scene
        current_scene.exit()
        current_scene = game_scene
        current_scene.enter()

    def show_options(self):
        global current_scene
        current_scene.exit()
        current_scene = options_scene
        current_scene.enter()


class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.window_width = window_width
        self.window_height = window_height
        self.ball = Ball(x=400, y=300, radius=10, speed_x=200, speed_y=200)
        self.paddle1 = Paddle(x=50, y=250, width=20, height=100, speed=300, control_type='main')
        self.paddle2 = Paddle(x=730, y=250, width=20, height=100, speed=300, control_type='alternate')
        self.score1 = 0
        self.score2 = 0
        self.score_display = Label(f"{self.score1}   {self.score2}",
                                   x=window.width // 2, y=window.height - 30, anchor_x='center', font_size=24)

    def enter(self):
        self.is_active = True
        self.reset_game()

    def exit(self):
        self.is_active = False

    def update(self, dt):
        self.ball.update(dt, paddles=[self.paddle1, self.paddle2])
        self.paddle1.update(dt, keys)
        self.paddle2.update(dt, keys)
        self.check_score()

    def draw(self):
        self.ball.draw()
        self.paddle1.draw()
        self.paddle2.draw()
        self.score_display.draw()

    def handle_mouse_press(self, x, y, button, modifiers):
        pass  # Nothing at the moment

    def update_score_display(self):
        # This method updates the text of the score display whenever called
        self.score_display.text = f"{self.score1}   {self.score2}"

    def reset_game(self):
        self.ball.reset()
        self.paddle1.rectangle.y = 250
        self.paddle2.rectangle.y = 250
        self.score1 = 0
        self.score2 = 0
        self.update_score_display()

    def check_score(self):
        if self.ball.circle.x < 0:  # Ball goes out on the left side
            self.score2 += 1
            self.update_score_display()  # Update score display after modification
            self.ball.reset()
        elif self.ball.circle.x > self.window_width:  # Ball goes out on the right side
            self.score1 += 1
            self.update_score_display()  # Update score display after modification
            self.ball.reset()
        if self.score1 >= 5 or self.score2 >= 5:
            winner = "P1" if self.score1 > self.score2 else "P2"
            self.game_over_transition(winner)

    def game_over_transition(self, winner):
        self.exit()  # First deactivate this scene
        global current_scene
        current_scene = WinScene(winner)
        current_scene.enter()  # Activate the winning scene

class WinScene(Scene):
    def __init__(self, winner):
        super().__init__()
        self.win_label = Label(f"{winner} WINS!", x=window.width // 2, y=window.height // 2 + 100,
                               anchor_x='center', font_size=48, color=(255, 255, 0, 255))
        self.new_game_button = Button("New Game", window.width // 2 - 150, window.height // 2,
                                      300, 50, self.restart_game)
        self.main_menu_button = Button("Main Menu", window.width // 2 - 150, window.height // 2 - 60,
                                       300, 50, self.go_to_main_menu)

    def draw(self):
        self.win_label.draw()
        self.new_game_button.draw()
        self.main_menu_button.draw()

    def handle_mouse_press(self, x, y, button, modifiers):
        self.new_game_button.check_click(x, y)
        self.main_menu_button.check_click(x, y)

    def restart_game(self):
        global current_scene, game_scene
        current_scene.exit()
        game_scene.reset_game()
        current_scene = game_scene
        current_scene.enter()

    def go_to_main_menu(self):
        global current_scene
        self.exit()
        current_scene = main_menu_scene
        current_scene.enter()

class OptionsScene(Scene):
    def __init__(self):
        super().__init__()
        self.back_button = Button("Back", window.width // 2 - 150, window.height // 2, 300, 50, self.go_back)

    def draw(self):
        self.back_button.draw()

    def handle_mouse_press(self, x, y, button, modifiers):
        self.back_button.check_click(x, y)

    def go_back(self):
        global current_scene
        current_scene.exit()
        current_scene = main_menu_scene
        current_scene.enter()

class Button:
    def __init__(self, label, x, y, width, height, action):
        self.label = Label(label, x=x + width // 2, y=y + height // 2, anchor_x='center', anchor_y='center')
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.vert_shader = Shader(vertex_shader, 'vertex')
        self.frag_shader = Shader(fragment_shader, 'fragment')
        self.program = ShaderProgram(self.vert_shader, self.frag_shader)
        self.program['box_color'] = (0.3, 0.5, 1.0, 1.0)  # RGBA
        self.program['projection'] = pyglet.math.Mat4.orthogonal_projection(0, 800, 0, 600, -1, 1)
        self.vertex_list = self.program.vertex_list(
            4, pyglet.gl.GL_QUADS, position=('f', [x, y, x + width, y, x + width, y + height, x, y + height]))

    def draw(self):
        with self.program:
            self.vertex_list.draw(pyglet.gl.GL_QUADS)
        self.label.draw()

    def check_click(self, x, y):
        if (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height):
            self.action()

class Paddle:
    def __init__(self, x, y, width, height, speed, control_type='main', color=(255, 255, 255)):
        self.rectangle = pyglet.shapes.Rectangle(x, y, width, height, color=color)
        self.speed = speed
        self.control_type = control_type
        self.window_height = 600  # Window height; adjust according to your window configuration

    def update(self, dt, keys):
        if self.control_type == 'main':
            if keys[key.W]:
                self.move_up(dt)
            if keys[key.S]:
                self.move_down(dt)
        elif self.control_type == 'alternate':
            if keys[key.UP]:
                self.move_up(dt)
            if keys[key.DOWN]:
                self.move_down(dt)

    def move_up(self, dt):
        # Checks if the top of the paddle is below the top of the window before moving up
        if self.rectangle.y + self.rectangle.height < self.window_height:
            self.rectangle.y += self.speed * dt
        else:
            self.rectangle.y = self.window_height - self.rectangle.height

    def move_down(self, dt):
        # Checks if the base of the paddle is above the base of the window before moving down
        if self.rectangle.y > 0:
            self.rectangle.y -= self.speed * dt
        else:
            self.rectangle.y = 0  # Adjusts to be exactly on the edge if passing

    def draw(self):
        self.rectangle.draw()

class Ball:
    def __init__(self, x, y, radius, speed_x, speed_y, color=(255, 255, 255)):
        self.circle = pyglet.shapes.Circle(x, y, radius, color=color)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.window_width = 800
        self.window_height = 600
        self.shadows = []
        self.max_shadows = 5
        self.shadows_decrease = 1
        self.shadow_timer = 0

        self.shadow_interval = 0.2  # Time in seconds between shadow generations

    def update(self, dt, paddles):
        # Update ball position
        self.circle.x += self.speed_x * dt
        self.circle.y += self.speed_y * dt

        # Collision with top and bottom edges
        if self.circle.y <= 0 + self.circle.radius or self.circle.y >= self.window_height - self.circle.radius:
            self.speed_y = -self.speed_y

        # Check collision with all paddles
        for paddle in paddles:
            if self.collides_with_paddle(paddle):
                break

        # Refresh shadows
        self.shadow_timer += dt
        if len(self.shadows) < self.max_shadows:
            if self.shadow_timer >= self.shadow_interval:
                self.shadows.append([self.circle.x, self.circle.y, 1.0])  # Add new shadow
                self.shadow_timer = 0  # Reset timer
        # Reduce the opacity of existing shadows and remove shadows with zero opacity
        self.shadows = [[x, y, opacity - self.shadows_decrease*dt]
                        for x, y, opacity in self.shadows if opacity - dt > 0]

    def collides_with_paddle(self, paddle):
        # Paddle coordinates
        paddle_left = paddle.rectangle.x
        paddle_right = paddle.rectangle.x + paddle.rectangle.width
        paddle_top = paddle.rectangle.y + paddle.rectangle.height
        paddle_bottom = paddle.rectangle.y
        # Ball coordinates
        ball_left = self.circle.x - self.circle.radius
        ball_right = self.circle.x + self.circle.radius
        ball_top = self.circle.y + self.circle.radius
        ball_bottom = self.circle.y - self.circle.radius
        # Checking paddle collision
        if (ball_right > paddle_left and ball_left < paddle_right and
                ball_top > paddle_bottom and ball_bottom < paddle_top):
            # Refining collision with paddles
            if self.speed_x > 0:  # Ball moving to the right
                self.circle.x = paddle_left - self.circle.radius - 1
            elif self.speed_x < 0:  # Ball moving to the left
                self.circle.x = paddle_right + self.circle.radius + 1
            self.speed_x *= -1  # Inverting horizontal direction of the ball
            self.speed_x *= 1.1  # Speeding after each collision
            return True

        return False

    def reset(self):  # Resetting speed and position
        self.circle.x = self.window_width / 2
        self.circle.y = self.window_height / 2
        self.speed_x = -self.speed_x  # Changing horizontal direction when resetting
        self.speed_y *= -1  # Inverting vertical direction
        self.shadows.clear()

    def draw(self):
        self.circle.draw()
        for shadow in self.shadows:
            shadow_circle = pyglet.shapes.Circle(x=shadow[0], y=shadow[1], radius=10,
                                                 color=(255, 255, 255, int(255 * shadow[2])))
            shadow_circle.draw()

# Pyglet Events
@window.event
def on_draw():
    window.clear()
    current_scene.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    current_scene.handle_mouse_press(x, y, button, modifiers)

def update(dt):
    current_scene.update(dt)

keys = key.KeyStateHandler()
window.push_handlers(keys)

# Scenes Instances
window_width = 800
window_height = 600

main_menu_scene = MainMenu()
game_scene = GameScene()
options_scene = OptionsScene()
current_scene = main_menu_scene
current_scene.enter()

pyglet.clock.schedule_interval(update, 1/60.0)  # 60 Hz

if __name__ == '__main__':
    pyglet.app.run()
