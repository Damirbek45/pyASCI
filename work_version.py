import tkinter as tk
from tkinter import filedialog
import pygame
import cv2
import time # установить pygame+cv2

# Выбор файлов
def select_files():
    video = filedialog.askopenfilename(title="Выберите видео", filetypes=[("MP4 files", "*.mp4")])
    audio = filedialog.askopenfilename(title="Выберите аудио", filetypes=[("MP3 files", "*.mp3")])
    return video, audio

# Окно выбора
root = tk.Tk()
root.title("Выбор файлов")
info_label = tk.Label(root, text="Выберите файлы: 1 - видео, 2 - аудио(аудио необязательно)", font=("Arial", 12))
info_label.pack(pady=20)

# проверка на видео
def start_animation():
    video, audio = select_files()
    if not video:
        info_label.config(text="Выберите хотя бы видеофайл!", fg="red")
        return
    
    info_label.config(text="Видео выбрано. Запуск...", fg="green")
    root.update()

    pygame.init()
    pygame.font.init()
    chars = " .'^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$" # палитра
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("ASCII") # название
    pygame.mixer.init()

    font_sizes = [1, 3, 5, 10, 15, 20, 25, 30] # размеры
    menu_font = pygame.font.SysFont("Courier", 30)  

    # меню выбора
    def font_menu():
        selected_index = 0
        while True:
            screen.fill((0, 0, 0))
            menu_texts = [
                "Выберите размер шрифта (меньше - больше детализация, но дольше загрузка).",
                "Стрелки вверх/вниз - выбор, Enter - подтвердить, ESC после загрузки - выход.",
                "ПРИМЕЧАНИЕ: Из-за Alt+Tab скрипт не будет отвечать, но загрузка будет идти."
            ]
            for i, text in enumerate(menu_texts):
                render = menu_font.render(text, True, (255, 255, 255))
                screen.blit(render, (screen_width // 2 - render.get_width() // 2, 100 + i * 50))

            for i, size in enumerate(font_sizes):
                color = (255, 255, 0) if i == selected_index else (255, 255, 255)
                option_text = menu_font.render(f"{i + 1}. Размер - {size}", True, color)
                screen.blit(option_text, (screen_width // 2 - option_text.get_width() // 2, 300 + i * 50))

            pygame.display.flip()
            event = pygame.event.wait()

            # управление
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

    # Прогресс
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

    # Преобразование
    def frame_to_ascii(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, output_size)
        return [''.join(chars[int(pixel) * (len(chars) - 1) // 255] for pixel in row) for row in frame]

    # Считывание информации
    cap = cv2.VideoCapture(video)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames, timestamps = [], []

    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame_to_ascii(frame))
        timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0) # частота обновления
        if i % 10 == 0:  
            show_progress_bar(i + 1, frame_count) # обновление счетчика каждый 10 кадр

    cap.release()

    # Видео+аудио
    def audio_anim():
        if audio:
            pygame.mixer.music.load(audio)
            pygame.mixer.music.play()

        start_time = time.time()
        for frame_index, ascii_frame in enumerate(frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False

            screen.fill((0, 0, 0))
            for y, line in enumerate(ascii_frame):
                screen.blit(font.render(line, True, (255, 255, 255)), (0, y * char_height))
            pygame.display.flip()

            if frame_index < len(timestamps) - 1:
                time.sleep(max(0, timestamps[frame_index + 1] - (time.time() - start_time)))

        return True

    while audio_anim():
        pass

    pygame.mixer.music.stop()
    pygame.quit()


# Кнопка выбора+инит
start_button = tk.Button(root, text="Выбрать", font=("Arial", 14), command=start_animation)
start_button.pack(pady=10)
root.mainloop()
