import os
import random
import time
import threading
from pynput import keyboard

event = threading.Event()

words = open('words.txt', 'r').read().splitlines()
word_count = len(words)
typing_buffer = ''
length = 100
height = 20
screen_buffer = []
offset_list = []
for _ in range(height):
    screen_buffer.append('')
    offset_list.append(0)
errors = 0
score = 0
refresh_rate = 0.2
wpm = int(input('Escolha a dificuldade (palavras por minuto): '))
difficulty = 60 / wpm
end_game = False

def clear():
    os.system('cls')

def listen():
    def on_press(key):
        global typing_buffer, errors, score, difficulty, end_game

        try:
            typing_buffer += key.char
        except AttributeError:
            if key == keyboard.Key.backspace:
                typing_buffer = typing_buffer[:len(typing_buffer) - 1]
            elif key == keyboard.Key.enter:
                if typing_buffer in screen_buffer:
                    index = len(screen_buffer) - 1 - screen_buffer[::-1].index(typing_buffer)
                    screen_buffer[index] = ''
                    typing_buffer = ''
                    score += 1
                    difficulty -= 0.1 if score > 0 and score % 5 == 0 else 0
                    os.system('color 7')
                    return
                os.system('color 4')
                difficulty -= 0.1
                errors += 1
                if errors == 6:
                    end_game = True

    def on_release(key):
        if key == keyboard.Key.esc:
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def draw():
    clear()
    for i in range(0, height):
        print(f'|{" " * offset_list[i] + screen_buffer[i]:<{length}}|')
    print(' ' * int(length / 2) + typing_buffer)
    print(f'Lives: {6 - errors}')
    print(f'Score: {score}')

def loop():
    global errors, difficulty, refresh_rate, end_game, time
    time_d = time.time()
    game_start = time.time()
    last_refresh = 0.0

    while True:
        if time.time() - time_d > 0.05:
            draw()
            
            if time.time() - last_refresh > difficulty:
                if screen_buffer[-1] != '':
                    errors += 1
                    if errors == 6 or end_game == True:
                        return False

                screen_buffer.insert(0, words[random.randint(1, word_count - 1)])
                screen_buffer.pop()
                offset_list.insert(0, random.randint(0, length - len(screen_buffer[0])))
                offset_list.pop()

                last_refresh = time.time()

                # if time.time() - game_start > 10:
                #     game_start = time.time()
                #     difficulty -= 0.1

            time_d = time.time()
        
t = threading.Thread(target=listen)
t.start()

def start():
    global typing_buffer
    loop()
    clear()
    draw()
    print('GAME OVER!')
    print('Deseja jogar novamente? (s/n) ')
    typing_buffer = ''
    if typing_buffer == 's':
        start()

start()