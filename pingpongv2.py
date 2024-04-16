import pyglet
import random
from pyglet.window import key
from pyglet.text import Label
from pyglet.graphics.shader import Shader, ShaderProgram

# Configurações da janela
window = pyglet.window.Window(width=800, height=600)
ball_speed_x = 200
ball_speed_y = 200
ball = pyglet.shapes.Circle(x=400, y=300, radius=10, color=(255, 255, 255))
paddle1 = pyglet.shapes.Rectangle(x=50, y=250, width=20, height=100, color=(255, 255, 255))
paddle2 = pyglet.shapes.Rectangle(x=730, y=250, width=20, height=100, color=(255, 255, 255))
paddle_speed = 300
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Variáveis de pontuação
score1 = 0
score2 = 0
score_display = Label(f"{score1}   {score2}", x=window.width // 2, y=window.height - 30, anchor_x='center', font_size=24)

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
        self.is_active = False  # Adicionar esta linha para gerenciar o estado de atividade da cena

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
        self.new_game_button = Button("New Game", window.width // 2 - 150, window.height // 2, 300, 50, self.start_new_game)
        self.options_button = Button("Options", window.width // 2 - 150, window.height // 2 - 60, 300, 50, self.show_options)

    def draw(self):
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
        self.paddle_speed = 350
        self.ball_speed_x = 100
        self.ball_speed_y = 100
        self.time_elapsed = 0
        self.score1 = 0
        self.score2 = 0
        self.score_display = Label(f"{self.score1}   {self.score2}", x=window.width // 2, y=window.height - 30, anchor_x='center', font_size=24)
        self.win_label = Label("", x=window.width // 2, y=window.height // 2 - 100, anchor_x='center', font_size=48, color=(255, 255, 0, 255))
        self.ball = pyglet.shapes.Circle(x=400, y=300, radius=10, color=(255, 255, 255))
        self.paddle1 = pyglet.shapes.Rectangle(x=50, y=250, width=20, height=100, color=(255, 255, 255))
        self.paddle2 = pyglet.shapes.Rectangle(x=730, y=250, width=20, height=100, color=(255, 255, 255))
        self.new_game_button = Button("New Game", window.width // 2 - 150, window.height // 2, 300, 50, self.restart_game)
        self.main_menu_button = Button("Main Menu", window.width // 2 - 150, window.height // 2 + 60, 300, 50, self.go_to_main_menu)
        self.game_over = False

    def update(self, dt):
        if self.game_over or not self.is_active:
            return
        self.time_elapsed += dt
        self.ball_speed_x += 1 * dt*10 * (1 if self.ball_speed_x > 0 else -1)  # Ajuste proporcional ao tempo
        self.ball_speed_y += 1 * dt * (1 if self.ball_speed_y > 0 else -1)  # Ajuste proporcional ao tempo
        self.ball.x += self.ball_speed_x * dt
        self.ball.y += self.ball_speed_y * dt

        # Movimento das barras
        if keys[key.W]:
            self.paddle1.y += self.paddle_speed * dt
        if keys[key.S]:
            self.paddle1.y -= self.paddle_speed * dt
        if keys[key.UP]:
            self.paddle2.y += self.paddle_speed * dt
        if keys[key.DOWN]:
            self.paddle2.y -= self.paddle_speed * dt

        # Impedir que as barras saiam da tela
        self.paddle1.y = max(0, min(self.paddle1.y, window.height - self.paddle1.height))
        self.paddle2.y = max(0, min(self.paddle2.y, window.height - self.paddle2.height))

        # Colisão com as paredes
        if self.ball.y <= 0 or self.ball.y >= window.height:
            self.ball_speed_y = -self.ball_speed_y

        # Colisão com as barras
        if (self.ball.x <= self.paddle1.x + self.paddle1.width and self.paddle1.y <= self.ball.y <= self.paddle1.y + self.paddle1.height) and self.ball_speed_x < 0:
            self.ball_speed_x *= -1
            self.ball.x = self.paddle1.x + self.paddle1.width  # Reposiciona a bola para evitar ficar presa
        elif (self.ball.x >= self.paddle2.x - self.paddle2.width and self.paddle2.y <= self.ball.y <= self.paddle2.y + self.paddle2.height) and self.ball_speed_x > 0:
            self.ball_speed_x *= -1
            self.ball.x = self.paddle2.x - self.paddle2.width  # Reposiciona a bola para evitar ficar presa

        # Atualizar a pontuação
        if self.ball.x < 0:
            self.score2 += 1
            self.reset_ball()
        elif self.ball.x > window.width:
            self.score1 += 1
            self.reset_ball()

        self.score_display.text = f"{self.score1}   {self.score2}"

        if self.score1 >= 5 or self.score2 >= 5:
            self.game_over = True
            winner = "P1" if self.score1 > self.score2 else "P2"
            global current_scene
            self.exit()
            current_scene = WinScene(winner)
            current_scene.enter()

    def draw(self):
        if self.is_active:
            self.ball.draw()
            self.paddle1.draw()
            self.paddle2.draw()
            self.score_display.draw()

    def reset_ball(self):
        self.ball.x = window.width // 2
        self.ball.y = window.height // 2
        self.ball_speed_x = -self.ball_speed_x  # Inverter a direção horizontal
        self.ball_speed_y *= -1  # Inverter a direção vertical para variar o jogo

    def restart_game(self):
        self.score1 = 0
        self.score2 = 0
        self.reset_ball()
        self.game_over = False
        self.score_display.text = f"{self.score1}   {self.score2}"

    def go_to_main_menu(self):
        global current_scene
        self.exit()
        current_scene = main_menu_scene
        current_scene.enter()

    def handle_mouse_press(self, x, y, button, modifiers):
        if self.game_over:
            self.new_game_button.check_click(x, y)
            self.main_menu_button.check_click(x, y)

class WinScene(Scene):
    def __init__(self, winner):
        super().__init__()
        self.win_label = Label(f"{winner} WINS!", x=window.width // 2, y=window.height // 2 + 100, anchor_x='center', font_size=48, color=(255, 255, 0, 255))
        self.new_game_button = Button("New Game", window.width // 2 - 150, window.height // 2, 300, 50, self.restart_game)
        self.main_menu_button = Button("Main Menu", window.width // 2 - 150, window.height // 2 - 60, 300, 50, self.go_to_main_menu)

    def draw(self):
        self.win_label.draw()
        self.new_game_button.draw()
        self.main_menu_button.draw()

    def handle_mouse_press(self, x, y, button, modifiers):
        self.new_game_button.check_click(x, y)
        self.main_menu_button.check_click(x, y)

    def restart_game(self):
        global current_scene
        current_scene.exit()
        game_scene.restart_game()
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

# Button class as previously described
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
        self.vertex_list = self.program.vertex_list(4, pyglet.gl.GL_QUADS,
            position=('f', [x, y, x + width, y, x + width, y + height, x, y + height]))

    def draw(self):
        with self.program:
            self.vertex_list.draw(pyglet.gl.GL_QUADS)
        self.label.draw()

    def check_click(self, x, y):
        if (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height):
            self.action()

# Instância das cenas
main_menu_scene = MainMenu()
game_scene = GameScene()
options_scene = OptionsScene()
current_scene = main_menu_scene
current_scene.enter()

# Eventos do Pyglet
@window.event
def on_draw():
    window.clear()
    current_scene.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    current_scene.handle_mouse_press(x, y, button, modifiers)

def update(dt):
    current_scene.update(dt)

pyglet.clock.schedule_interval(update, 1/60.0)  # 60 Hz

if __name__ == '__main__':
    pyglet.app.run()
