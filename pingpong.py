import pyglet
from pyglet.window import key
from pyglet.text import Label

# Settings
window = pyglet.window.Window(width=800, height=600)
ball_speed_x = 200
ball_speed_y = 200
ball = pyglet.shapes.Circle(x=400, y=300, radius=10, color=(255, 255, 255))
paddle1 = pyglet.shapes.Rectangle(x=50, y=250, width=20, height=100, color=(255, 255, 255))
paddle2 = pyglet.shapes.Rectangle(x=730, y=250, width=20, height=100, color=(255, 255, 255))
paddle_speed = 300
keys = key.KeyStateHandler()
window.push_handlers(keys)

# Score variables
score1 = 0
score2 = 0
score_display = Label(f"{score1}   {score2}", x=window.width // 2, y=window.height - 30, anchor_x='center',
                      font_size=24)


def update(dt):
    global ball_speed_x, ball_speed_y, score1, score2

    ball.x += ball_speed_x * dt
    ball.y += ball_speed_y * dt

    # Paddle movements
    if keys[key.W] and paddle1.y + paddle1.height < 600:
        paddle1.y += paddle_speed * dt
    if keys[key.S] and paddle1.y > 0:
        paddle1.y -= paddle_speed * dt
    if keys[key.UP] and paddle2.y + paddle2.height < 600:
        paddle2.y += paddle_speed * dt
    if keys[key.DOWN] and paddle2.y > 0:
        paddle2.y -= paddle_speed * dt

    # Wall collision
    if ball.y <= 0 or ball.y >= 600:
        ball_speed_y *= -1

    # Paddle collision
    if (ball.x <= paddle1.x + paddle1.width and paddle1.y <= ball.y <= paddle1.y + paddle1.height) or \
            (ball.x >= paddle2.x - paddle2.width and paddle2.y <= ball.y <= paddle2.y + paddle2.height):
        ball_speed_x *= -1

    # Setting score
    if ball.x < 0:
        score2 += 1
        ball.x, ball.y = window.width // 2, window.height // 2
    elif ball.x > window.width:
        score1 += 1
        ball.x, ball.y = window.width // 2, window.height // 2

    # Display score
    score_display.text = f"{score1}   {score2}"


@window.event
def on_draw():
    window.clear()
    ball.draw()
    paddle1.draw()
    paddle2.draw()
    score_display.draw()


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1 / 60.0)
    pyglet.app.run()
