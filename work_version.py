import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import cv2
import numpy as np
import time
import threading
import darkdetect

# Пресеты 
default  = " .:-=+*#%@"
detailed = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
minimum     = " .oO@"

FRAME_UPDATE_INTERVAL = 150  # каждые 150 кадров,можно изменить
DEFAULT_FONT_SIZES = [3, 5, 10, 15, 20, 25, 30] # размеры шрифта

# Языки
LANGUAGES = {
    "en": {
        "main_title": "ASCII Transfer",
        "select_file_prompt": "Choose file: video/image (audio is optional when choosing video). ESC after selecting font to exit.",
        "select_button": "Select",
        "settings_button": "Settings",
        "char_dialog_title": "Character Selection",
        "char_preset_label": "Choose preset:",
        "char_custom_label": "Custom (min 2 chars, from dark to light):",
        "char_error_msg": "Please enter at least 2 characters",
        "font_dialog_title": "Font Settings",
        "font_size_label": "Font Size:",
        "processing_image": "Image selected. Rendering...",
        "processing_video": "Video selected. Rendering...",
        "theme_label": "Theme:",
        "language_label": "Language:",
        "light_theme": "Light",
        "dark_theme": "Dark",
        "system_theme": "System",
        "close_button": "Close",
        "default": "Default",
        "detailed": "Detailed",
        "minimum": "Minimum",
    },
    "ru": {
        "main_title": "ASCII трансфер",
        "select_file_prompt": "Выберите файл: видео/изображение (аудио опционально при выборе видео). ESC после выбора шрифта чтобы выйти.",
        "select_button": "Выбрать",
        "settings_button": "Настройки",
        "char_dialog_title": "Выбор символов",
        "char_preset_label": "Пресеты:",
        "char_custom_label": "Своя палитра (мин. 2, от тёмного к светлому):",
        "char_error_msg": "Введите не менее 2 символов",
        "font_dialog_title": "Настройки шрифта",
        "font_size_label": "Размер шрифта:",
        "processing_image": "Изображение выбрано. Обработка...",
        "processing_video": "Видео выбрано. Обработка...",
        "theme_label": "Тема:",
        "language_label": "Язык:",
        "light_theme": "Светлая",
        "dark_theme": "Тёмная",
        "system_theme": "Системная",
        "close_button": "Закрыть",
        "default": "Обычный",
        "detailed": "Расширенный",
        "minimum": "Минимальный",
    }
}

# Темы
THEMES = {
    "light": {
        "bg": "white",
        "fg": "black",
        "button_bg": "#f0f0f0",
        "button_fg": "black",
        "entry_bg": "white",
        "entry_fg": "black",
    },
    "dark": {
        "bg": "#2d2d2d",
        "fg": "white",
        "button_bg": "#404040",
        "button_fg": "white",
        "entry_bg": "#202020",
        "entry_fg": "white",
    },
}


# Класс 
class ASCIIApp:
    
    def __init__(self, root):
        self.root = root
        self.current_lang = "en"        # язык по умолчанию
        self.current_theme = "system"     # тема по умолчанию
        self.languages = LANGUAGES
        self.themes = THEMES
        self._build_ui()                
        self.apply_theme()             

    # Интерфейс
    def _build_ui(self):
        self.root.title(self.languages[self.current_lang]["main_title"])
        self.info_label = tk.Label(self.root,text=self.languages[self.current_lang]["select_file_prompt"],font=("Arial", 12))

        self.info_label.pack(pady=20)
        self.start_button = tk.Button(self.root,
        text=self.languages[self.current_lang]["select_button"],font=("Arial", 14),command=self.start_processing)

        self.start_button.pack(pady=10)
        self.settings_button = tk.Button(self.root,text=self.languages[self.current_lang]["settings_button"],command=self.open_settings)
        self.settings_button.pack(pady=10)

    # Обновление интерфейса 
    def update_ui(self):
        self.root.title(self.languages[self.current_lang]["main_title"])
        self.info_label.config(text=self.languages[self.current_lang]["select_file_prompt"])
        self.start_button.config(text=self.languages[self.current_lang]["select_button"])
        self.settings_button.config(text=self.languages[self.current_lang]["settings_button"])
        self.apply_theme()

    # Текущая тема
    def get_actual_theme(self):
        if self.current_theme == "system":
            detected = darkdetect.theme()
            if detected in ["Light", "Dark"]:
                return detected.lower()
            return "light"
        return self.current_theme.lower()

    # Смена темы
    def apply_theme(self, widget=None):
        theme_name = self.get_actual_theme()
        colors = self.themes.get(theme_name, self.themes["light"])
        def _apply(w):
            if isinstance(w, (tk.Tk, tk.Toplevel)):
                w.configure(bg=colors["bg"])
            elif isinstance(w, tk.Label):
                w.config(bg=colors["bg"], fg=colors["fg"])
            elif isinstance(w, tk.Button):
                w.config(bg=colors["button_bg"], fg=colors["button_fg"],
                         activebackground=colors["button_bg"], activeforeground=colors["button_fg"])
            elif isinstance(w, tk.Entry):
                w.config(bg=colors["entry_bg"], fg=colors["entry_fg"], insertbackground=colors["fg"])
            elif isinstance(w, tk.Frame):
                w.config(bg=colors["bg"])
            elif isinstance(w, tk.Radiobutton):
                w.config(bg=colors["bg"], fg=colors["fg"],
                         activebackground=colors["bg"], activeforeground=colors["fg"],
                         selectcolor=colors["entry_bg"])
            for child in w.winfo_children():
                _apply(child)
        _apply(widget if widget else self.root)

    # Настройки
    def open_settings(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.languages[self.current_lang]["settings_button"])
        self.apply_theme(dialog)
        colors = self.themes[self.get_actual_theme()]
        # Выбор языка
        lang_frame = tk.Frame(dialog, bg=colors["bg"])
        lang_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        tk.Label(lang_frame, text=self.languages[self.current_lang]["language_label"],bg=colors["bg"], fg=colors["fg"]).pack(side=tk.LEFT)
        lang_var = tk.StringVar(value=self.current_lang)
        for code, name in [("en", "English"), ("ru", "Русский")]:
            rb = tk.Radiobutton(lang_frame, text=name, variable=lang_var, value=code,bg=colors["bg"], fg=colors["fg"],activebackground=colors["bg"], activeforeground=colors["fg"],selectcolor=colors["entry_bg"],command=lambda: self.set_language(lang_var.get()))
            rb.pack(side=tk.LEFT, padx=5)
        # Выбор темы
        theme_frame = tk.Frame(dialog, bg=colors["bg"])
        theme_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        tk.Label(theme_frame, text=self.languages[self.current_lang]["theme_label"],bg=colors["bg"], fg=colors["fg"]).pack(side=tk.LEFT)
        theme_var = tk.StringVar(value=self.current_theme)
        for theme in ["light", "dark", "system"]:
            rb = tk.Radiobutton(theme_frame, text=self.languages[self.current_lang][f"{theme}_theme"],variable=theme_var, value=theme,bg=colors["bg"], fg=colors["fg"],activebackground=colors["bg"], activeforeground=colors["fg"],selectcolor=colors["entry_bg"],command=lambda t=theme: self.set_theme(t))
            rb.pack(side=tk.LEFT, padx=5)
        close_button = tk.Button(dialog, text=self.languages[self.current_lang]["close_button"],
                                 command=dialog.destroy)
        close_button.grid(row=2, column=0, columnspan=3, pady=10)

    # Смена языка
    def set_language(self, lang):
        self.current_lang = lang
        self.update_ui()

    # Смена темы
    def set_theme(self, theme):
        self.current_theme = theme
        self.apply_theme()

    # Выбор файлов
    def select_files(self):
        file_path = filedialog.askopenfilename(
            title=self.languages[self.current_lang]["select_file_prompt"],
            filetypes=[("Video/Image", "*.mp4 *.webm *.jpg *.jpeg *.png")]
        )
        if not file_path:
            return None, None
        audio_path = None
        # Выбор аудио
        if not file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.webm')):
            audio_path = filedialog.askopenfilename(
                title=self.languages[self.current_lang]["select_file_prompt"],
                filetypes=[("Audio", "*.mp3")]
            )
        return file_path, audio_path

    # Выбор палитры
    def get_ascii_chars(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.languages[self.current_lang]["char_dialog_title"])
        colors = self.themes[self.get_actual_theme()]
        dialog.configure(bg=colors["bg"])
        # Пресеты 
        tk.Label(dialog, text=self.languages[self.current_lang]["char_preset_label"],bg=colors["bg"], fg=colors["fg"]).pack(pady=10)
        btn_frame = tk.Frame(dialog, bg=colors["bg"])
        btn_frame.pack()
        selected_chars = None
        def select(chars):
            nonlocal selected_chars
            selected_chars = chars
            dialog.destroy()
        # Кнопки пресетов
        tk.Button(btn_frame, text=self.languages[self.current_lang]["default"],command=lambda: select(default),bg=colors["button_bg"], fg=colors["button_fg"]).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.languages[self.current_lang]["detailed"],command=lambda: select(detailed),bg=colors["button_bg"], fg=colors["button_fg"]).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.languages[self.current_lang]["text"],command=lambda: select(minimum),bg=colors["button_bg"], fg=colors["button_fg"]).pack(side=tk.LEFT, padx=5)
        # Кастомная палитра
        tk.Label(dialog, text=self.languages[self.current_lang]["char_custom_label"],bg=colors["bg"], fg=colors["fg"]).pack(pady=10)

        entry = tk.Entry(dialog, bg=colors["entry_bg"], fg=colors["entry_fg"])
        entry.pack()
        error_label = tk.Label(dialog, text="", fg="red", bg=colors["bg"])
        error_label.pack()
        def confirm():
            nonlocal selected_chars
            chars = entry.get().strip()
            if len(chars) >= 2: # Проверка длины
                selected_chars = chars
                dialog.destroy()
            else:
                error_label.config(text=self.languages[self.current_lang]["char_error_msg"])
        tk.Button(dialog, text="OK", command=confirm,
                  bg=colors["button_bg"], fg=colors["button_fg"]).pack(pady=10)
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        return selected_chars

    # Размер шрифта
    def get_font_settings(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.languages[self.current_lang]["font_dialog_title"])
        colors = self.themes[self.get_actual_theme()]
        self.apply_theme(dialog)
        tk.Label(dialog, text=self.languages[self.current_lang]["font_size_label"],
                 bg=colors["bg"], fg=colors["fg"]).grid(row=0, column=0, padx=10, pady=5)
        size_var = tk.IntVar(value=10)
        for i, size in enumerate(DEFAULT_FONT_SIZES):
            rb = tk.Radiobutton(dialog, text=str(size), variable=size_var, value=size,bg=colors["bg"], fg=colors["fg"],activebackground=colors["bg"], activeforeground=colors["fg"],selectcolor=colors["entry_bg"], highlightthickness=0)
            rb.grid(row=0, column=i + 1)
        tk.Button(dialog, text=self.languages[self.current_lang]["select_button"],command=dialog.destroy,bg=colors["button_bg"], fg=colors["button_fg"]).grid(row=1, column=0,columnspan=len(DEFAULT_FONT_SIZES) + 1, pady=10)
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        return size_var.get()

    # Обработка
    def start_processing(self):
        file_path, audio_path = self.select_files()
        if not file_path:
            return
        ascii_chars = self.get_ascii_chars()
        if not ascii_chars:
            return
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.webm')):
            self.info_label.config(text=self.languages[self.current_lang]["processing_image"])
            self.root.update()
            self.handle_image(file_path, ascii_chars)
        else:
            self.info_label.config(text=self.languages[self.current_lang]["processing_video"])
            self.root.update()
            self.handle_video(file_path, audio_path, ascii_chars)

    # Изображение
    def handle_image(self, image_path, ascii_chars):
        font_size = self.get_font_settings()
        try:
            pygame.init()
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            screen_width, screen_height = screen.get_size()
            pygame.display.set_caption("Image")
            font = pygame.font.SysFont("Courier", font_size)
            char_width, char_height = font.size("A")
            img = cv2.imread(image_path)
            if img is None:
                messagebox.showerror("Error", "Failed to load image.")
                pygame.quit()
                return
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cols = screen_width // char_width
            rows = screen_height // char_height
            resized = cv2.resize(gray, (cols, rows), interpolation=cv2.INTER_NEAREST)
            # Преобразование в ASCII
            lut = np.floor(np.linspace(0, len(ascii_chars) - 1, 256)).astype(np.uint8)
            ascii_indices = lut[resized]
            ascii_array = np.array(list(ascii_chars))
            ascii_image = [''.join(ascii_array[pixel] for pixel in row) for row in ascii_indices]
            running = True
            while running: # ESC чтобы выйти
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
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            pygame.quit()

    # Видео
    def handle_video(self, video_path, audio_path, ascii_chars):
        try:
            pygame.init()
            pygame.font.init()
            font_size = self.get_font_settings()
            font = pygame.font.SysFont("Courier", font_size)
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            screen_width, screen_height = screen.get_size()
            char_width, char_height = font.size("A")
            output_size = (screen_width // char_width, screen_height // char_height)
            chars_array = np.array(list(ascii_chars))
            lut = np.floor(np.linspace(0, len(ascii_chars) - 1, 256)).astype(np.uint8)
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                messagebox.showerror("Error", "Failed to open video.")
                pygame.quit()
                return
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frames, timestamps = [], []

            # Преобразование в ASCII
            def frame_to_ascii(frame):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                resized = cv2.resize(gray, output_size, interpolation=cv2.INTER_NEAREST)
                indices = lut[resized]
                ascii_array_local = chars_array[indices]
                return [''.join(row.tolist()) for row in ascii_array_local]

            # Прогресс бар
            def show_progress_bar(progress, total):
                screen.fill((0, 0, 0))
                bar_width = screen_width * 0.7
                bar_height = 40
                x, y = (screen_width - bar_width) // 2, (screen_height - bar_height) // 2
                progress_percent = int((progress / total) * 100)
                progress_font = pygame.font.SysFont("Courier", 20) 
                text = progress_font.render(f"Loading:{progress_percent}%", True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen_width // 2, y - 30))
                screen.blit(text, text_rect)
                pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
                pygame.draw.rect(screen, (255, 255, 255), (x, y, int((progress / total) * bar_width), bar_height))
                pygame.display.flip()

            def render_frames():
                for i in range(frame_count):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frames.append(frame_to_ascii(frame))
                    timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
                    if i % FRAME_UPDATE_INTERVAL == 0:
                        show_progress_bar(i + 1, frame_count)
                    time.sleep(0.001) # задержка для снижения траты ресурсов
                show_progress_bar(frame_count, frame_count)

            render_thread = threading.Thread(target=render_frames)
            render_thread.start()
            while render_thread.is_alive(): #ESC чтобы выйти
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        exit()
                time.sleep(0.2)
            render_thread.join()
            cap.release()

            # Аудио(если выбрано)
            if audio_path:
                try:
                    pygame.mixer.music.load(audio_path)
                    pygame.mixer.music.play()
                except Exception as e:
                    messagebox.showerror("Audio Error", f"Audio error: {e}")
            clock = pygame.time.Clock()
            start_time = time.time()
            playing = True
            while playing:
                for event in pygame.event.get(): # ESC чтобы выйти
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        playing = False
                        pygame.mixer.music.stop()
                        break
                screen.fill((0, 0, 0))
                current_time = time.time() - start_time
                frame_index = 0
                for idx, t in enumerate(timestamps):
                    if t > current_time:
                        break
                    frame_index = idx
                if frame_index >= len(frames):
                    start_time = time.time()
                    continue
                ascii_frame = frames[frame_index]
                for y, line in enumerate(ascii_frame):
                    screen.blit(font.render(line, True, (255, 255, 255)), (0, y * char_height))
                pygame.display.flip()
                clock.tick(60)  # FPS Lock, можно изменить
            pygame.quit()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            pygame.quit()

# ДЕНИС _MAIN_
def main():
    root = tk.Tk()
    app = ASCIIApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
