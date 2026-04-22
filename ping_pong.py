sa
from machine import Pin
from utime import sleep
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from machine import Pin, PWM
import time
import random



def main_pico_game():
    screen_height = 64
    screen_width = 128
    ball_size = int(4)
    paddle_width = int(16)
    paddle_height = int(4)

    paddle_y = 52

    # Left right up down buttons are all connected to the Pico
    up = Pin(2, Pin.IN, Pin.PULL_UP)
    down = Pin(3, Pin.IN, Pin.PULL_UP)
    left = Pin(4, Pin.IN, Pin.PULL_UP)
    right = Pin(5, Pin.IN, Pin.PULL_UP)

    buzzer = PWM(Pin(18))

    # Oled screen connected to GP14 (SDA) and GP15(SCL)
    i2c = I2C(1, sda = Pin(14), scl = Pin(15), freq = 400000)
    oled = SSD1306_I2C(screen_width, screen_height, i2c)

    # variables:
    ball_y = 0
    ball_x = int(screen_width/2)
    ball_vx = 2.0
    ball_vy = 2.0

    paddle_x = int(screen_width/2)
    paddle_vx = 4
    paddle_vy = 2

    soundFreq = 400 # sound when the ball hits something
    score = 0

    while True:
        # Move the paddle to the right
        if right.value() == 0:
            paddle_x += paddle_vx
            if paddle_x + paddle_width > screen_width:
                paddle_x = screen_width - paddle_width
        # Move the paddle to the left
        elif left.value() == 0:
            paddle_x -= paddle_vx
            if paddle_x < 0:
                paddle_x = 0
        elif up.value() == 0:
            paddle_y -= paddle_vy
            if paddle_y < 32:
                paddle_y = 32
        elif down.value() == 0:
            paddle_y += paddle_vy
            if paddle_y > 60:
                paddle_y = 60
     
        if abs(ball_vx) < 1:
            # if the ball moves too slow:
            ball_vx = 1

        ball_x = int(ball_x + ball_vx)
        ball_y = int(ball_y + ball_vy)

        collision = False

        if ball_x < 0:
            # collision with the left edge
            ball_x = 0
            ball_vx = -ball_vx
            collision = True
        if ball_y < 0:
            # collision with the top edge
            ball_y = 0
            ball_vy = - ball_vy
            collision = True
        if ball_x + ball_size > screen_width:
            # collision with the right edge
            ball_x = screen_width - ball_size
            ball_vx = - ball_vx
            collision = True
        if ball_y + ball_size > paddle_y and ball_x + ball_size > paddle_x and ball_x < paddle_x + paddle_width + ball_size:
            # increase the velocity a little bit
            ball_vy = - (ball_vy + 0.2)
            ball_y = paddle_y - ball_size

            ball_vx += (ball_x - (paddle_x + paddle_width / 2)) / 10

            collision = True
            score += 10
        if ball_y + ball_size > screen_height:
            # lose the gameeee
            oled.fill(0)
            oled.text("WHAT A CHICKEN", int(screen_width / 2) - int(len("WHAT A CHICKEN")/2 * 8), int(screen_height / 2) - 10)
            oled.text(str(score), screen_width - int(len(str(score)) * 8), 0)
            oled.show()

            # play a losing sound
            buzzer.freq(200)
            buzzer.duty_u16(2000)
            time.sleep(0.5)
            buzzer.duty_u16(0)

            while right.value() != 0 and left.value() != 0:
                time.sleep(0.001)
            break


        if collision:
            if soundFreq == 400:
                soundFreq = 800
            else:
                soundFreq = 400
            
            buzzer.freq(soundFreq)
            buzzer.duty_u16(2000)

        oled.fill(0)

        oled.fill_rect(paddle_x, paddle_y, paddle_width, paddle_height, 1)
        oled.fill_rect(ball_x, ball_y, ball_size, ball_size, 1)

        oled.text(str(score), screen_width - int(len(str(score) * 8)), 0)
        oled.show()

        time.sleep(0.01)
        buzzer.duty_u16(0)

if __name__ == "__main__":
    main_pico_game()
        
        

