import tkinter as tk
from tkinter import filedialog
import pygame
import cv2
import numpy as np
import time #установить opencv-python, numpy, pygame

#Выбор файлов
def select_files():
    video = filedialog.askopenfilename(title="Выберите видео", filetypes=[("MP4 files", "*.mp4")])
    audio = filedialog.askopenfilename(title="Выберите аудио", filetypes=[("MP3 files", "*.mp3")])
    return video, audio

root = tk.Tk()
root.title("Выбор файлов")
info_label = tk.Label(root, text="Выберите файлы: 1 - видео, 2 - аудио(аудио необязательно)", font=("Arial", 12))
info_label.pack(pady=20)

#Запуск видео
def start_animation():
    video, audio = select_files()
    if not video:
        info_label.config(text="Выберите хотя бы видеофайл!", fg="red")
        return
    
    info_label.config(text="Видео выбрано. Запуск...", fg="green")
    root.update()

    pygame.init()
    pygame.font.init()
    chars = " .:-=+*#%@" #палитра
    chars_array = np.array(list(chars)) #нампи для оптимизации
    len_chars_minus_1 = len(chars) - 1

    # инициализация
    lut = np.array([(i * len_chars_minus_1) // 255 for i in range(256)], dtype=np.uint8)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("ASCII")
    pygame.mixer.init()

    #Шрифт
    font_sizes = [3, 5, 10, 15, 20, 25, 30]
    menu_font = pygame.font.SysFont("Courier", 30)

    #Меню выбора
    def font_menu():
        selected_index = 0
        while True:
            screen.fill((0, 0, 0))
            menu_texts = [
                "Выберите размер шрифта (меньше - больше детализация, но дольше загрузка).",
                "Стрелки вверх/вниз - выбор, Enter - подтвердить, ESC после загрузки - выход.",
                "ПРИМЕЧАНИЕ: При Alt+Tab скрипт не будет отвечать, но загрузка будет идти."
            ]
            for i, text in enumerate(menu_texts):
                render = menu_font.render(text, True, (255, 255, 255))
                screen.blit(render, (screen_width // 2 - render.get_width() // 2, 100 + i * 50))

            #Размеры
            for i, size in enumerate(font_sizes):
                color = (255, 255, 0) if i == selected_index else (255, 255, 255)
                option_text = menu_font.render(f"{i + 1}. Размер - {size}", True, color)
                screen.blit(option_text, (screen_width // 2 - option_text.get_width() // 2, 300 + i * 50))

            pygame.display.flip()
            event = pygame.event.wait()

            #Управление
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(font_sizes)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(font_sizes)
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    selected_index = event.key - pygame.K_1
                elif event.key == pygame.K_RETURN:
                    return font_sizes[selected_index]

    #Прогресс бар
    def show_progress_bar(progress, total):
        screen.fill((0, 0, 0))
        bar_width = screen_width * 0.6
        bar_height = 50
        x, y = (screen_width - bar_width) // 2, (screen_height - bar_height) // 2
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, int((progress / total) * bar_width), bar_height))
        progress_text = menu_font.render(f"Загрузка... {int((progress / total) * 100)}%", True, (255, 255, 255))
        screen.blit(progress_text, (screen_width // 2 - progress_text.get_width() // 2, y + bar_height + 10))
        pygame.display.flip()

    font_size = font_menu()
    font = pygame.font.SysFont("Courier", font_size)
    char_width, char_height = font.size("A")
    output_size = (screen_width // char_width, screen_height // char_height)

    #Трансфер в аскии
    def frame_to_ascii(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, output_size, interpolation=cv2.INTER_NEAREST)
        indices = lut[resized]
        ascii_array = chars_array[indices]
        ascii_frame = [''.join(row.tolist()) for row in ascii_array]
        return ascii_frame

    #кадры + таймкоды для синхронизации
    cap = cv2.VideoCapture(video)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames, timestamps = [], []

    # обновление прогресс бара
    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame_to_ascii(frame))
        timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
        if i % 100 == 0: #каждые 100 кадров
            show_progress_bar(i + 1, frame_count)

    cap.release()

    #аудио
    def audio_anim():
        if audio:
            pygame.mixer.music.load(audio)
            pygame.mixer.music.play()

        clock = pygame.time.Clock()
        start_time = time.time()
        video_duration = timestamps[-1] if timestamps else 0

        #ESC чтобы выйти
        for frame_index, ascii_frame in enumerate(frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return False

            screen.fill((0, 0, 0))
            for y, line in enumerate(ascii_frame):
                screen.blit(font.render(line, True, (255, 255, 255)), (0, y * char_height))
            pygame.display.flip()

            # синхронизация
            if frame_index < len(timestamps) - 1:
                target_time = start_time + timestamps[frame_index + 1]
                current_time = time.time()
                delay = max(0, target_time - current_time)

                # проверка задержки
                if delay > 0.1:  # большие задержки
                    time.sleep(delay * 0.95)
                else:  # маленькие задержки
                    while time.time() < target_time:
                        pass

            # проверка синхрона
            if audio and time.time() - start_time > video_duration:
                break

        return True

    while audio_anim():
        pass

    pygame.mixer.music.stop()
    pygame.quit()

#Запуск
start_button = tk.Button(root, text="Выбрать", font=("Arial", 14), command=start_animation)
start_button.pack(pady=10)
root.mainloop()