import tkinter as tk
from tkinter import ttk, filedialog
import pygame
import cv2
import numpy as np
import time
import threading
import darkdetect

# Настройки
current_lang = 'en'
current_theme = 'system'

languages = {
    'en': {
        'main_title': "ASCII Transfer",
        'select_file_prompt': "Choose file: video/image (audio is optional when choosing video). ESC after selecting font to exit.",
        'select_button': "Select",
        'settings_button': "Settings",
        'char_dialog_title': "Character Selection",
        'char_preset_label': "Choose preset:",
        'char_custom_label': "Custom (min 2 chars, from dark to light):",
        'char_error_msg': "Please enter at least 2 characters",
        'font_dialog_title': "Font Settings",
        'font_size_label': "Font Size:",
        'processing_image': "Image selected. Rendering...",
        'processing_video': "Video selected. Rendering...",
        'theme_label': "Theme:",
        'language_label': "Language:",
        'light_theme': "Light",
        'dark_theme': "Dark",
        'system_theme': "System",
        'close_button': "Close",
        'default': "Default",
        'detailed': "Detailed",
        'simple': "Simple",
    },
    'ru': {
        'main_title': "ASCII трансфер",
        'select_file_prompt': "Выберите файл: видео/изображение (аудио опционально при выборе видео). ESC после выбора шрифта чтобы выйти.",
        'select_button': "Выбрать",
        'settings_button': "Настройки",
        'char_dialog_title': "Выбор символов",
        'char_preset_label': "Пресеты:",
        'char_custom_label': "Своя палитра (мин. 2, от тёмного к светлому):",
        'char_error_msg': "Введите не менее 2 символов",
        'font_dialog_title': "Настройки шрифта",
        'font_size_label': "Размер шрифта:",
        'processing_image': "Изображение выбрано. Обработка...",
        'processing_video': "Видео выбрано. Обработка...",
        'theme_label': "Тема:",
        'language_label': "Язык:",
        'light_theme': "Светлая",
        'dark_theme': "Тёмная",
        'system_theme': "Системная",
        'close_button': "Закрыть",
        'default': "Обычный",
        'detailed': "Расширенный",
        'simple': "Простой",
    }
}

themes = {
    'light': {
        'bg': 'white', 'fg': 'black',
        'button_bg': '#f0f0f0', 'button_fg': 'black',
        'entry_bg': 'white', 'entry_fg': 'black',
    },
    'dark': {
        'bg': '#2d2d2d', 'fg': 'white',
        'button_bg': '#404040', 'button_fg': 'white',
        'entry_bg': '#202020', 'entry_fg': 'white',
    }
}

# Функции виджетов
def set_language(lang):
    global current_lang
    current_lang = lang
    update_ui()

def set_theme(theme):
    global current_theme
    current_theme = theme
    apply_theme()

def get_actual_theme():
    if current_theme == 'system':
        return darkdetect.theme().lower() if darkdetect.theme() in ['Light', 'Dark'] else 'light'
    return current_theme.lower()

def apply_theme(widget=None):
    theme = get_actual_theme()
    colors = themes.get(theme, themes['light'])

    def _apply(w):
        if isinstance(w, tk.Tk) or isinstance(w, tk.Toplevel):
            w.configure(bg=colors['bg'])
        if isinstance(w, tk.Label):
            w.config(bg=colors['bg'], fg=colors['fg'])
        elif isinstance(w, tk.Button):
            w.config(
                bg=colors['button_bg'],
                fg=colors['button_fg'],
                activebackground=colors['button_bg'],
                activeforeground=colors['button_fg']
            )
        elif isinstance(w, tk.Entry):
            w.config(bg=colors['entry_bg'], fg=colors['entry_fg'], insertbackground=colors['fg'])
        elif isinstance(w, tk.Frame):
            w.config(bg=colors['bg'])
        elif isinstance(w, tk.Radiobutton):
            w.config(
                bg=colors['bg'],
                fg=colors['fg'],
                activebackground=colors['bg'],
                activeforeground=colors['fg'],
                selectcolor=colors['entry_bg']
            )
        for child in w.winfo_children():
            _apply(child)

    _apply(widget or root)

# Обновить интерфейс
def update_ui():
    root.title(languages[current_lang]['main_title'])
    info_label.config(text=languages[current_lang]['select_file_prompt'])
    start_button.config(text=languages[current_lang]['select_button'])
    settings_button.config(text=languages[current_lang]['settings_button'])
    apply_theme()

# Выбор файлов
def select_files():
    main_file = filedialog.askopenfilename(
        title=languages[current_lang]['select_file_prompt'],
        filetypes=[("Video/Image", "*.mp4 *.webm *.jpg *.jpeg *.png")]
    )
    if not main_file:
        return None, None
    audio = None
    if not main_file.lower().endswith(('.jpg', '.jpeg', '.png', '.webm')):
        audio = filedialog.askopenfilename(
            title=languages[current_lang]['select_file_prompt'],
            filetypes=[("Audio", "*.mp3")]
        )
    return main_file, audio

# Выбор символов
def get_ascii_chars():
    dialog = tk.Toplevel(root)
    dialog.title(languages[current_lang]['char_dialog_title'])
    apply_theme(dialog)
    default_chars = " .:-=+*#%@"
    detalized_chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    simple_chars = " #@"

    selected_chars = None

    # Выбор пресетов
    tk.Label(dialog, text=languages[current_lang]['char_preset_label'], bg=themes[get_actual_theme().lower()]['bg'], fg=themes[get_actual_theme().lower()]['fg']).pack(pady=10)
    btn_frame = tk.Frame(dialog, bg=themes[get_actual_theme().lower()]['bg'])
    btn_frame.pack()

    def select(chars):
        nonlocal selected_chars
        selected_chars = chars
        dialog.destroy()

    tk.Button(btn_frame, text=languages[current_lang]['default'], command=lambda: select(default_chars)).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text=languages[current_lang]['detailed'], command=lambda: select(detalized_chars)).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text=languages[current_lang]['simple'], command=lambda: select(simple_chars)).pack(side=tk.LEFT, padx=5)

    # Ввод пользователя
    tk.Label(dialog, text=languages[current_lang]['char_custom_label'], bg=themes[get_actual_theme().lower()]['bg'], fg=themes[get_actual_theme().lower()]['fg']).pack(pady=10)
    entry = tk.Entry(dialog)
    entry.pack()
    error_label = tk.Label(dialog, text="", fg="red", bg=themes[get_actual_theme().lower()]['bg'])
    error_label.pack()

    def confirm():
        nonlocal selected_chars
        chars = entry.get().strip()
        if len(chars) >= 2:
            selected_chars = chars
            dialog.destroy()
        else:
            error_label.config(text=languages[current_lang]['char_error_msg'])

    tk.Button(dialog, text="OK", command=confirm).pack(pady=10)
    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)
    return selected_chars

# Выбор шрифта
def get_font_settings():
    dialog = tk.Toplevel(root)
    dialog.title(languages[current_lang]['font_dialog_title'])
    apply_theme(dialog)
    colors = themes[get_actual_theme()]
    tk.Label(dialog, text=languages[current_lang]['font_size_label'], bg=colors['bg'], fg=colors['fg']).grid(row=0, column=0, padx=10, pady=5)
    sizes = [3, 5, 10, 15, 20, 25, 30]
    size_var = tk.IntVar(value=10)
    for i, size in enumerate(sizes):
        rb = tk.Radiobutton(
            dialog,
            text=str(size),
            variable=size_var,
            value=size,
            bg=colors['bg'],
            fg=colors['fg'],
            activebackground=colors['bg'],
            activeforeground=colors['fg'],
            selectcolor=colors['entry_bg'],
            highlightthickness=0
        )
        rb.grid(row=0, column=i + 1)
    tk.Button(dialog, text=languages[current_lang]['select_button'], command=dialog.destroy).grid(row=1, columnspan=len(sizes) + 1, pady=10)
    dialog.transient(root)
    dialog.grab_set()
    root.wait_window(dialog)
    return size_var.get()

# Функции рендеринга
def handle_image(image_path, chars):
    font_size = get_font_settings()
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("Изображение")
    font = pygame.font.SysFont("Courier", font_size)
    char_width, char_height = font.size("A")
    img = cv2.imread(image_path)
    if img is None:
        info_label.config(text="Ошибка загрузки изображения", fg="red")
        root.update()
        pygame.quit()
        return
    original_height, original_width = img.shape[:2]
    aspect_ratio = original_height / original_width
    cols = screen_width // char_width
    rows = screen_height // char_height
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (cols, rows), interpolation=cv2.INTER_NEAREST)
    lut = np.floor(np.linspace(0, len(chars) - 1, 256)).astype(np.uint8)
    ascii_indices = lut[resized]
    ascii_image = [''.join([chars[pixel] for pixel in row]) for row in ascii_indices]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        screen.fill((0, 0, 0))
        y_pos = (screen_height - rows * char_height) // 2
        for line in ascii_image:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, ((screen_width - cols * char_width) // 2, y_pos))
            y_pos += char_height
        pygame.display.flip()
    pygame.quit()

# Видео
def handle_video(video_path, audio_path, chars):
    pygame.init()
    pygame.font.init()
    font_size = get_font_settings()
    font = pygame.font.SysFont("Courier", font_size)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_width, screen_height = screen.get_size()
    char_width, char_height = font.size("A")
    output_size = (screen_width // char_width, screen_height // char_height)
    chars_array = np.array(list(chars))
    lut = np.floor(np.linspace(0, len(chars) - 1, 256)).astype(np.uint8)
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames, timestamps = [], []

    def render_frames():
        for i in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame_to_ascii(frame))
            timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
            if i % 150 == 0:  # обновляется каждые 150 кадров, можно изменить
                show_progress_bar(i + 1, frame_count)
        show_progress_bar(frame_count, frame_count)

    def frame_to_ascii(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, output_size, interpolation=cv2.INTER_NEAREST)
        indices = lut[resized]
        ascii_array = chars_array[indices]
        return [''.join(row.tolist()) for row in ascii_array]

    def show_progress_bar(progress, total):
        screen.fill((0, 0, 0))
        bar_width = screen_width * 0.7
        bar_height = 40
        x, y = (screen_width - bar_width) // 2, (screen_height - bar_height) // 2
        progress_percent = int((progress / total) * 100)
        progress_font = pygame.font.SysFont("Courier", 20)  # Fixed size
        text = progress_font.render(f"Загрузка:{progress_percent}%", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, y - 30))
        screen.blit(text, text_rect)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, int((progress / total) * bar_width), bar_height))
        pygame.display.flip()

    render_thread = threading.Thread(target=render_frames)
    render_thread.start()
    while render_thread.is_alive():
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
        time.sleep(0.1)
    render_thread.join()
    cap.release()

    def play_video():
        loop = True
        while loop:
            if audio_path:
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
            clock = pygame.time.Clock()
            start_time = time.time()
            for frame_index, ascii_frame in enumerate(frames):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        pygame.mixer.music.stop()
                        pygame.quit()
                        return False
                screen.fill((0, 0, 0))
                for y, line in enumerate(ascii_frame):
                    screen.blit(font.render(line, True, (255, 255, 255)), (0, y * char_height))
                pygame.display.flip()
                if frame_index < len(timestamps) - 1:  # проверка задержек
                    target_time = start_time + timestamps[frame_index + 1]
                    current_time = time.time()
                    delay = max(0, target_time - current_time)
                    if delay > 0.1:  # большие задержки
                        time.sleep(delay * 0.95)
                    else:
                        while time.time() < target_time:  # маленькие задержки
                            pass
                # Если достигнут конец видео, перезапуск
                if frame_index == len(frames) - 1:
                    break
            # Перезапуск видео и аудио
            pygame.mixer.music.stop()
        pygame.quit()

    play_video()

# проверка на выбор
def start_processing():
    file_path, audio_path = select_files()
    if not file_path:
        return
    chars = get_ascii_chars()
    if not chars:
        return
    if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.webm')):
        info_label.config(text=languages[current_lang]['processing_image'], fg='green')
        handle_image(file_path, chars)
    else:
        info_label.config(text=languages[current_lang]['processing_video'], fg='green')
        handle_video(file_path, audio_path, chars)

# Меню настроек
def open_settings():
    dialog = tk.Toplevel(root)
    dialog.title(languages[current_lang]['settings_button'])
    apply_theme(dialog)
    colors = themes[get_actual_theme()]

    # Языки
    lang_frame = tk.Frame(dialog, bg=colors['bg'])
    lang_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="w")
    tk.Label(lang_frame, text=languages[current_lang]['language_label'], bg=colors['bg'], fg=colors['fg']).pack(side=tk.LEFT)
    lang_var = tk.StringVar(value=current_lang)
    for i, (lang_code, lang_name) in enumerate([('en', 'English'), ('ru', 'Русский')]):
        rb = tk.Radiobutton(
            lang_frame,
            text=lang_name,
            variable=lang_var,
            value=lang_code,
            bg=colors['bg'],
            fg=colors['fg'],
            activebackground=colors['bg'],
            activeforeground=colors['fg'],
            selectcolor=colors['entry_bg'],
            highlightthickness=0,
            command=lambda: set_language(lang_var.get())
        )
        rb.pack(side=tk.LEFT, padx=5)

    # Настройки темы
    theme_frame = tk.Frame(dialog, bg=colors['bg'])
    theme_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")
    tk.Label(theme_frame, text=languages[current_lang]['theme_label'], bg=colors['bg'], fg=colors['fg']).pack(side=tk.LEFT)
    theme_var = tk.StringVar(value=current_theme)
    for i, theme in enumerate(['light', 'dark', 'system']):
        rb = tk.Radiobutton(
            theme_frame,
            text=languages[current_lang][f'{theme}_theme'],
            variable=theme_var,
            value=theme,
            bg=colors['bg'],
            fg=colors['fg'],
            activebackground=colors['bg'],
            activeforeground=colors['fg'],
            selectcolor=colors['entry_bg'],
            highlightthickness=0,
            command=lambda t=theme: set_theme(t)
        )
        rb.pack(side=tk.LEFT, padx=5)
    close_button = tk.Button(dialog, text=languages[current_lang]['close_button'], command=dialog.destroy)
    close_button.grid(row=2, column=0, columnspan=3, pady=10)

# Запуск
root = tk.Tk()
root.title(languages[current_lang]['main_title'])
info_label = tk.Label(root, text=languages[current_lang]['select_file_prompt'], font=('Arial', 12))
info_label.pack(pady=20)
start_button = tk.Button(root, text=languages[current_lang]['select_button'], font=('Arial', 14), command=start_processing)
start_button.pack(pady=10)
settings_button = tk.Button(root, text=languages[current_lang]['settings_button'], command=open_settings)
settings_button.pack(pady=10)
apply_theme()
root.mainloop()