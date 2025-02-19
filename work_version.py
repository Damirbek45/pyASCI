import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import time
import threading
import locale
import os
import tempfile
import concurrent.futures

# requirements
import pygame
import cv2
import numpy as np
import darkdetect
import moviepy as mp

# Глобальные переменные
DEFAULT = " .:-=+*#%@"
DETAILED = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MINIMUM = " .oO@"
FRAME_UPDATE = 150  # каждые 150 кадров, можно изменить
FONT_SIZES = [3, 5, 10, 15, 20, 25, 30]  # размеры шрифта

# Локализация (языки)
LANGUAGES = {
    "en": {
        "main_title": "ASCII Transfer",
        "select_file_prompt": "Choose file: video/image",
        "select_button": "Select",
        "settings_button": "Settings",
        "char_dialog_title": "Character Selection",
        "char_preset_label": "Choose preset:",
        "char_custom_label": "Custom (min 2 chars, from dark to light):",
        "char_error_msg": "Please enter at least 2 characters",
        "font_dialog_title": "Font Settings",
        "font_size_label": "Font Size:",
        "processing_image": "Image selected. Choose an options.",
        "processing_video": "Video selected. Choose an options.",
        "theme_label": "Theme:",
        "language_label": "Language:",
        "light_theme": "Light",
        "dark_theme": "Dark",
        "system_theme": "System",
        "system_lang": "System",
        "close_button": "Close",
        "default": "Default",
        "detailed": "Detailed",
        "minimum": "Minimum",
        "high_cpu_mode": "High CPU Usage Mode",
        "low_cpu_mode": "Low CPU Usage Mode",
        "normal_cpu_mode": "Balanced",
        "cpu_mode_label": "CPU Mode:",
        "image_mode_label": "Image Display Mode:",
        "video_render_mode_label": "Video Render Mode:",
        "keep_resolution": "Keep Resolution",
        "stretch_full": "Stretch to Full Screen",
        "real_time": "Real Time Render",
        "pre_render": "Pre-render",
        "info_button": "Info",
        "save_image": "Save image after exiting",
        "play_audio": "Play audio with video",
        "loading_text": "Loading",
        "error": "Error",
        "failed_load_image": "Failed to load image.",
        "failed_open_video": "Failed to open video.",
        "audio_error": "Audio Error",
        "audio_extraction_error": "Audio extraction error: {error}",
        "audio_error_msg": "Audio error: {error}",
        "no_frames_error": "No frames were pre-rendered. Please check the video file.",
        "error_occurred": "An error occurred: {error}"
    },
    "ru": {
        "main_title": "ASCII трансфер",
        "select_file_prompt": "Выберите файл: видео/изображение",
        "select_button": "Выбрать",
        "settings_button": "Настройки",
        "char_dialog_title": "Выбор символов",
        "char_preset_label": "Пресеты:",
        "char_custom_label": "Своя палитра (мин. 2, от тёмного к светлому):",
        "char_error_msg": "Введите не менее 2 символов",
        "font_dialog_title": "Настройки шрифта",
        "font_size_label": "Размер шрифта:",
        "processing_image": "Изображение выбрано. Выберите настройки рендера.",
        "processing_video": "Видео выбрано. Выберите настройки рендера.",
        "theme_label": "Тема:",
        "language_label": "Язык:",
        "light_theme": "Светлая",
        "dark_theme": "Тёмная",
        "system_theme": "Системная",
        "system_lang": "Системный",
        "close_button": "Закрыть",
        "default": "Обычный",
        "detailed": "Расширенный",
        "minimum": "Минимальный",
        "high_cpu_mode": "Максимальная нагрузка ЦП",
        "low_cpu_mode": "Экономия ресурсов ЦП",
        "normal_cpu_mode": "Баланс",
        "cpu_mode_label": "Режим ЦП:",
        "image_mode_label": "Режим отображения изображения:",
        "video_render_mode_label": "Режим рендеринга видео:",
        "keep_resolution": "Оригинальный размер",
        "stretch_full": "Растянуть на весь экран",
        "real_time": "Рендер в реальном времени",
        "pre_render": "Предварительный рендер",
        "info_button": "Инфо",
        "save_image": "Сохранить изображение после выхода",
        "play_audio": "Воспроизводить аудио вместе с видео",
        "loading_text": "Загрузка",
        "error": "Ошибка",
        "failed_load_image": "Не удалось загрузить изображение.",
        "failed_open_video": "Не удалось открыть видео.",
        "audio_error": "Ошибка аудио",
        "audio_extraction_error": "Ошибка извлечения аудио: {error}",
        "audio_error_msg": "Ошибка аудио: {error}",
        "no_frames_error": "Не было пред-рендеренных кадров. Проверьте видеофайл.",
        "error_occurred": "Произошла ошибка: {error}"
    }
}

# Оформления (темы)
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

# Текст в Info
INFO_MESSAGES = {
    "video": {
        "en": (
            "Font Size: Sets the size of the characters (the less – the better details, but loads longer).\n\n"
            "CPU Mode:\n"
            " - High: Minimal loading, high CPU usage. Recommended for modern PC.\n"
            " - Balanced: Balanced performance and CPU usage.\n"
            " - Low: More loading, lower CPU usage. Recommended for old PC.\n\n"
            "Video Render Mode:\n"
            " - Real Time Render: Starts a video immediately and renders it on the fly. Works better for modern PC.\n"
            " - Pre-render: Processes all frames before start.\n\n"
            "Press ESC to exit while loading/after rendering."
        ),
        "ru": (
            "Размер шрифта: устанавливает размер символов (меньше – более детализированно, но медленная загрузка).\n\n"
            "Режим ЦП:\n"
            " - Максимальная нагрузка: минимальная загрузка, высокая нагрузка ЦП. Рекомендуется для современных ПК.\n"
            " - Баланс: сбалансированное соотношение загрузки и нагрузки ЦП.\n"
            " - Экономия ресурсов: долгая загрузка, низкая нагрузка ЦП. Рекомендуется для старых ПК.\n\n"
            "Режим рендеринга видео:\n"
            " - Рендер в реальном времени: запускает видео сразу и обрабатывает кадры на лету. Работает лучше для современных компьютеров.\n"
            " - Предварительный рендер: обрабатывает все кадры перед запуском.\n\n"
            "Нажмите ESC для выхода во время рендеринга/после него."
        )
    },
    "image": {
        "en": (
            "Font Size: Sets the size of the characters (the less – the better details).\n\n"
            "Image Display mode:\n"
            " - Keep Resolution: Uses the original image resolution.\n"
            " - Stretch to Full Screen: Scales image to full screen.\n\n"
            "Press ESC to exit while loading/after rendering."
        ),
        "ru": (
            "Размер шрифта: устанавливает размер символов (меньше – более детализированно).\n\n"
            "Режим показа изображения:\n"
            " - Оригинальный размер: использует оригинальное разрешение изображения.\n"
            " - Растянуть на весь экран: масштабирует изображение на весь экран.\n\n"
            "Нажмите ESC для выхода после рендеринга."
        )
    }
}

# Основной класс приложения
class ASCIIApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = "system"      # язык по умолчанию 
        self.current_theme = "system"     # оформление по умолчанию
        self.languages = LANGUAGES
        self.themes = THEMES
        self._build_ui()
        self.apply_theme()

    # определение языка системы
    def detect_system_language(self):
        try:
            locale.setlocale(locale.LC_ALL, '')
        except locale.Error:
            pass
        lang_tuple = locale.getlocale()
        lang = lang_tuple[0]
        if not lang or lang == "C":
            lang_env = os.environ.get("LANG", "en")
            lang = lang_env.split('.')[0]
        if lang.lower().startswith("ru"):
            return "ru"
        return "en"
    
    def get_effective_lang(self):
        return self.detect_system_language() if self.current_lang == "system" else self.current_lang

    # Инициализация основного окна приложения
    def _build_ui(self):
        effective_lang = self.get_effective_lang()
        self.root.title(self.languages[effective_lang]["main_title"])
        self.info_label = tk.Label(self.root, text=self.languages[effective_lang]["select_file_prompt"], font=("Arial", 12))
        self.info_label.pack(pady=20)
        self.start_button = tk.Button(self.root, text=self.languages[effective_lang]["select_button"],
                                      font=("Arial", 14), command=self.start_processing)
        self.start_button.pack(pady=10)
        self.settings_button = tk.Button(self.root, text=self.languages[effective_lang]["settings_button"],
                                         command=self.open_settings)
        self.settings_button.pack(pady=10)

    # Обновление текста интерфейса
    def update_ui(self):
        effective_lang = self.get_effective_lang()
        self.root.title(self.languages[effective_lang]["main_title"])
        self.info_label.config(text=self.languages[effective_lang]["select_file_prompt"])
        self.start_button.config(text=self.languages[effective_lang]["select_button"])
        self.settings_button.config(text=self.languages[effective_lang]["settings_button"])
        self.apply_theme()

    # Применение темы 
    def get_actual_theme(self):
        if self.current_theme == "system":
            detected = darkdetect.theme()
            if detected in ["Light", "Dark"]:
                return detected.lower()
            return "light"
        return self.current_theme.lower()

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
            elif isinstance(w, tk.Checkbutton):
                w.config(bg=colors["bg"], fg=colors["fg"],
                         activebackground=colors["bg"], activeforeground=colors["fg"],
                         selectcolor=colors["entry_bg"])
            for child in w.winfo_children():
                _apply(child)
        _apply(widget if widget else self.root)

    # Окно настроек (выбор языка и оформления)
    def open_settings(self):
        effective_lang = self.get_effective_lang()
        dialog = tk.Toplevel(self.root)
        dialog.title(self.languages[effective_lang]["settings_button"])
        self.apply_theme(dialog)
        colors = self.themes[self.get_actual_theme()]

        # Выбор языка
        lang_frame = tk.Frame(dialog, bg=colors["bg"])
        lang_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        tk.Label(lang_frame, text=self.languages[effective_lang]["language_label"],
                 bg=colors["bg"], fg=colors["fg"]).pack(side=tk.LEFT)
        lang_var = tk.StringVar(value=self.current_lang)
        for code, default_name in [("en", "English"), ("ru", "Русский"), ("system", None)]:
            if code == "system":
                if self.current_lang == "system":
                    effective_display = "English" if self.get_effective_lang() == "en" else "Русский"
                    label = f"{self.languages[effective_lang]['system_lang']} ({effective_display})"
                else:
                    label = self.languages[effective_lang]["system_lang"]
            else:
                label = default_name
            rb = tk.Radiobutton(lang_frame, text=label, variable=lang_var, value=code,
                                bg=colors["bg"], fg=colors["fg"],
                                activebackground=colors["bg"], activeforeground=colors["fg"],
                                selectcolor=colors["entry_bg"],
                                command=lambda: self.set_language(lang_var.get()))
            rb.pack(side=tk.LEFT, padx=5)

        # Выбор оформления
        theme_frame = tk.Frame(dialog, bg=colors["bg"])
        theme_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="w")
        tk.Label(theme_frame, text=self.languages[effective_lang]["theme_label"],
                 bg=colors["bg"], fg=colors["fg"]).pack(side=tk.LEFT)
        theme_var = tk.StringVar(value=self.current_theme)
        for theme in ["light", "dark", "system"]:
            if theme == "system":
                if self.current_theme == "system":
                    effective_system = self.get_actual_theme()  
                    label_text = f"{self.languages[effective_lang]['system_theme']} ({self.languages[effective_lang][f'{effective_system}_theme']})"
                else:
                    label_text = self.languages[effective_lang]["system_theme"]
            else:
                label_text = self.languages[effective_lang][f"{theme}_theme"]
            rb = tk.Radiobutton(theme_frame, text=label_text,
                                variable=theme_var, value=theme,
                                bg=colors["bg"], fg=colors["fg"],
                                activebackground=colors["bg"], activeforeground=colors["fg"],
                                selectcolor=colors["entry_bg"],
                                command=lambda: self.set_theme(theme_var.get()))
            rb.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(dialog, text=self.languages[effective_lang]["close_button"],
                                 command=dialog.destroy)
        close_button.grid(row=2, column=0, columnspan=3, pady=10)

    def set_language(self, lang):
        self.current_lang = lang
        self.update_ui()

    def set_theme(self, theme):
        self.current_theme = theme
        self.apply_theme()

    # Выбор файла
    def select_files(self):
        effective_lang = self.get_effective_lang()
        file_path = filedialog.askopenfilename(
            title=self.languages[effective_lang]["select_file_prompt"],
            filetypes=[ # Расширения файлов
                ("Video", "*.mp4 *.webm *.avi *.mkv *.mov"),
                ("Image", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All Files", "*.*")
            ]
        )
        if not file_path:
            return None, None
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            return file_path, None
        else:
            return file_path, None

    # Выбор символов
    def get_ascii_chars(self):
        effective_lang = self.get_effective_lang()
        dialog = tk.Toplevel(self.root)
        dialog.title(self.languages[effective_lang]["char_dialog_title"])
        colors = self.themes[self.get_actual_theme()]
        dialog.configure(bg=colors["bg"])
        tk.Label(dialog, text=self.languages[effective_lang]["char_preset_label"],
                 bg=colors["bg"], fg=colors["fg"]).pack(pady=10)
        btn_frame = tk.Frame(dialog, bg=colors["bg"])
        btn_frame.pack()
        selected_chars = None
        def select(chars):
            nonlocal selected_chars
            selected_chars = chars
            dialog.destroy()
        tk.Button(btn_frame, text=self.languages[effective_lang]["default"],
                  command=lambda: select(DEFAULT), bg=colors["button_bg"], fg=colors["button_fg"]).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.languages[effective_lang]["detailed"],
                  command=lambda: select(DETAILED), bg=colors["button_bg"], fg=colors["button_fg"]).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text=self.languages[effective_lang]["minimum"],
                  command=lambda: select(MINIMUM), bg=colors["button_bg"], fg=colors["button_fg"]).pack(side=tk.LEFT, padx=5)
        tk.Label(dialog, text=self.languages[effective_lang]["char_custom_label"],
                 bg=colors["bg"], fg=colors["fg"]).pack(pady=10)
        entry = tk.Entry(dialog, bg=colors["entry_bg"], fg=colors["entry_fg"])
        entry.pack()
        error_label = tk.Label(dialog, text="", fg="red", bg=colors["bg"])
        error_label.pack()
        def confirm():
            nonlocal selected_chars
            chars = entry.get().strip()
            if len(chars) >= 2:
                selected_chars = chars
                dialog.destroy()
            else:
                error_label.config(text=self.languages[effective_lang]["char_error_msg"])
        tk.Button(dialog, text="OK", command=confirm,
                  bg=colors["button_bg"], fg=colors["button_fg"]).pack(pady=10)
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        return selected_chars

    # Настройки шрифта и режима отображения/рендеринга
    def get_font_settings(self, include_cpu_options=True):
        effective_lang = self.get_effective_lang()
        result = None
        dialog = tk.Toplevel(self.root)
        dialog.title(self.languages[effective_lang]["font_dialog_title"])
        colors = self.themes[self.get_actual_theme()]
        self.apply_theme(dialog)
        sizes = FONT_SIZES if include_cpu_options else [1] + FONT_SIZES
        tk.Label(dialog, text=self.languages[effective_lang]["font_size_label"],
                 bg=colors["bg"], fg=colors["fg"]).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        size_var = tk.IntVar(value=10)
        for i, size in enumerate(sizes):
            rb = tk.Radiobutton(dialog, text=str(size), variable=size_var, value=size,
                                bg=colors["bg"], fg=colors["fg"], activebackground=colors["bg"],
                                activeforeground=colors["fg"], selectcolor=colors["entry_bg"], highlightthickness=0)
            rb.grid(row=0, column=i+1, padx=5, pady=5)
        for col in range(1, len(sizes)+1):
            dialog.grid_columnconfigure(col, weight=1)
        current_row = 1

        # Опции для видео
        if include_cpu_options:
            tk.Label(dialog, text=self.languages[effective_lang]["cpu_mode_label"],
                     bg=colors["bg"], fg=colors["fg"]).grid(row=current_row, column=0, padx=10, pady=5, sticky="w")
            cpu_mode_var = tk.StringVar(value="balanced")
            rb_high = tk.Radiobutton(dialog, text=self.languages[effective_lang]["high_cpu_mode"],
                                     variable=cpu_mode_var, value="high",
                                     bg=colors["bg"], fg=colors["fg"], activebackground=colors["bg"],
                                     activeforeground=colors["fg"], selectcolor=colors["entry_bg"])
            rb_high.grid(row=current_row, column=1, padx=5, pady=5)
            rb_balanced = tk.Radiobutton(dialog, text=self.languages[effective_lang]["normal_cpu_mode"],
                                         variable=cpu_mode_var, value="balanced",
                                         bg=colors["bg"], fg=colors["fg"], activebackground=colors["bg"],
                                         activeforeground=colors["fg"], selectcolor=colors["entry_bg"])
            rb_balanced.grid(row=current_row, column=2, padx=5, pady=5)
            rb_low = tk.Radiobutton(dialog, text=self.languages[effective_lang]["low_cpu_mode"],
                                    variable=cpu_mode_var, value="low",
                                    bg=colors["bg"], fg=colors["fg"], activebackground=colors["bg"],
                                    activeforeground=colors["fg"], selectcolor=colors["entry_bg"])
            rb_low.grid(row=current_row, column=3, padx=5, pady=5)
            current_row += 1
            tk.Label(dialog, text=self.languages[effective_lang]["video_render_mode_label"],
                     bg=colors["bg"], fg=colors["fg"]).grid(row=current_row, column=0, padx=10, pady=5, sticky="w")
            video_render_var = tk.StringVar(value="pre_render")
            rb_rt = tk.Radiobutton(dialog, text=self.languages[effective_lang]["real_time"],
                                   variable=video_render_var, value="real_time",
                                   bg=colors["bg"], fg=colors["fg"], activebackground=colors["bg"],
                                   activeforeground=colors["fg"], selectcolor=colors["entry_bg"])
            rb_rt.grid(row=current_row, column=1, padx=5, pady=5)
            rb_pr = tk.Radiobutton(dialog, text=self.languages[effective_lang]["pre_render"],
                                   variable=video_render_var, value="pre_render",
                                   bg=colors["bg"], fg=colors["fg"], activebackground=colors["bg"],
                                   activeforeground=colors["fg"], selectcolor=colors["entry_bg"])
            rb_pr.grid(row=current_row, column=2, padx=5, pady=5)
            current_row += 1
            play_audio_var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(dialog, text=self.languages[effective_lang]["play_audio"],
                                variable=play_audio_var, bg=colors["bg"], fg=colors["fg"],
                                selectcolor=colors["entry_bg"])
            cb.grid(row=current_row, column=0, columnspan=3, padx=10, pady=5, sticky="w")
            current_row += 1
            result = (size_var.get(), cpu_mode_var.get(), video_render_var.get(), play_audio_var.get())
        else:
            # Опции для изображения
            tk.Label(dialog, text=self.languages[effective_lang]["image_mode_label"],
                     bg=colors["bg"], fg=colors["fg"]).grid(row=current_row, column=0, padx=10, pady=5, sticky="w")
            image_mode_var = tk.StringVar(value="stretch")
            rb_keep = tk.Radiobutton(dialog, text=self.languages[effective_lang]["keep_resolution"],
                                     variable=image_mode_var, value="keep",
                                     bg=colors["bg"], fg=colors["fg"], activebackground=colors["bg"],
                                     activeforeground=colors["fg"], selectcolor=colors["entry_bg"])
            rb_keep.grid(row=current_row, column=1, padx=5, pady=5)
            rb_stretch = tk.Radiobutton(dialog, text=self.languages[effective_lang]["stretch_full"],
                                        variable=image_mode_var, value="stretch",
                                        bg=colors["bg"], fg=colors["fg"], activebackground=colors["bg"],
                                        activeforeground=colors["fg"], selectcolor=colors["entry_bg"])
            rb_stretch.grid(row=current_row, column=2, padx=5, pady=5)
            current_row += 1
            save_frame = tk.Frame(dialog, bg=colors["bg"])
            save_frame.grid(row=current_row, column=0, columnspan=3, padx=10, pady=5, sticky="w")
            save_image_var = tk.BooleanVar(value=False)
            tk.Checkbutton(save_frame, text=self.languages[effective_lang]["save_image"],
                           variable=save_image_var, bg=colors["bg"], fg=colors["fg"],
                           selectcolor=colors["entry_bg"]).pack(side=tk.LEFT)
            current_row += 1
            result = (size_var.get(), image_mode_var.get(), save_image_var.get())

        def show_custom_message(title, message):
            msg_win = tk.Toplevel(dialog)
            msg_win.title(title)
            self.apply_theme(msg_win)
            tk.Label(msg_win, text=message, bg=colors["bg"], fg=colors["fg"], wraplength=400).pack(padx=20, pady=20)
            tk.Button(msg_win, text="OK", command=msg_win.destroy,
                      bg=colors["button_bg"], fg=colors["button_fg"]).pack(pady=(0,20))
            msg_win.grab_set()
            dialog.wait_window(msg_win)
        def show_info():
            key = "video" if include_cpu_options else "image"
            info_text = INFO_MESSAGES[key][effective_lang]
            show_custom_message(self.languages[effective_lang]["info_button"], info_text)
        bottom_frame = tk.Frame(dialog, bg=colors["bg"])
        bottom_frame.grid(row=current_row, column=0, columnspan=len(sizes)+1, sticky="ew", pady=10)
        def on_select():
            nonlocal result
            if include_cpu_options:
                result = (size_var.get(), cpu_mode_var.get(), video_render_var.get(), play_audio_var.get())
            else:
                result = (size_var.get(), image_mode_var.get(), save_image_var.get())
            dialog.destroy()
        select_button = tk.Button(bottom_frame, text=self.languages[effective_lang]["select_button"],
                                  command=on_select, bg=colors["button_bg"], fg=colors["button_fg"])
        select_button.pack(side=tk.LEFT, padx=10)
        info_button = tk.Button(bottom_frame, text=self.languages[effective_lang]["info_button"],
                                command=show_info, bg=colors["button_bg"], fg=colors["button_fg"])
        info_button.pack(side=tk.RIGHT, padx=10)
        def on_close():
            nonlocal result
            result = None
            dialog.destroy()
        dialog.protocol("WM_DELETE_WINDOW", on_close)
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        return result

    # Обработка изображения
    def handle_image(self, image_path, ascii_chars):
        effective_lang = self.get_effective_lang()
        settings = self.get_font_settings(include_cpu_options=False)
        if settings is None:
            return
        font_size, image_mode, save_image = settings
        try:
            pygame.init()
            img = cv2.imread(image_path)
            if img is None:
                messagebox.showerror(self.languages[effective_lang]["error"], self.languages[effective_lang]["failed_load_image"])
                pygame.quit()
                return
            # Запуск
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            screen_width, screen_height = screen.get_size()
            pygame.display.set_caption("Image")
            font = pygame.font.SysFont("Courier", font_size)
            char_width, char_height = font.size("A")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Оригинальное разрешение
            if image_mode == "keep":
                img_height, img_width = gray.shape
                cols = img_width // char_width
                rows = img_height // char_height
            # Полный экран
            else:
                cols = screen_width // char_width
                rows = screen_height // char_height
            resized = cv2.resize(gray, (cols, rows), interpolation=cv2.INTER_NEAREST)
            # Рендер символов
            lut = np.floor(np.linspace(0, len(ascii_chars) - 1, 256)).astype(np.uint8)
            ascii_indices = lut[resized]
            ascii_array = list(ascii_chars)
            ascii_image = [''.join(ascii_array[pixel] for pixel in row) for row in ascii_indices]
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        if save_image:
                            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                                     filetypes=[("PNG Image", "*.png")])
                            if save_path:
                                pygame.image.save(screen, save_path)
                        running = False
                screen.fill((0, 0, 0))
                render_width = cols * char_width
                render_height = rows * char_height
                x_offset = (screen_width - render_width) // 2
                y_offset = (screen_height - render_height) // 2
                y_pos = y_offset
                for line in ascii_image:
                    text_surface = font.render(line, True, (255, 255, 255))
                    screen.blit(text_surface, (x_offset, y_pos))
                    y_pos += char_height
                pygame.display.flip()
            pygame.quit()
        except Exception as e:
            messagebox.showerror(self.languages[effective_lang]["error"],
                                 self.languages[effective_lang]["error_occurred"].format(error=e))
            pygame.quit()

    # Обработка видео
    def handle_video(self, video_path, audio_path, ascii_chars):
        effective_lang = self.get_effective_lang()
        try:
            pygame.init()
            pygame.font.init()
            settings = self.get_font_settings(include_cpu_options=True)
            if settings is None:
                return
            font_size, cpu_mode, video_render_mode, play_audio = settings
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                messagebox.showerror(self.languages[effective_lang]["error"],
                                     self.languages[effective_lang]["failed_open_video"])
                pygame.quit()
                return
            # Запуск 
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            screen_width, screen_height = screen.get_size()
            pygame.display.set_caption("Video")
            font = pygame.font.SysFont("Courier", font_size)
            char_width, char_height = font.size("A")
            output_size = (screen_width // char_width, screen_height // char_height)
            # Извлечение аудио из видео
            temp_audio_file = None
            if play_audio:
                if audio_path is None:
                    try:
                        temp_audio_file = tempfile.mktemp(suffix=".mp3")
                        clip = mp.VideoFileClip(video_path)
                        clip.audio.write_audiofile(temp_audio_file, logger=None)
                        audio_path = temp_audio_file
                    except Exception as e:
                        messagebox.showerror(self.languages[effective_lang]["audio_error"],
                                             self.languages[effective_lang]["audio_extraction_error"].format(error=e))
            # LUT для конвертации
            lut = np.floor(np.linspace(0, len(ascii_chars) - 1, 256)).astype(np.uint8)
            ascii_list = list(ascii_chars)
            # Преобразование в ASCII
            def frame_to_ascii(frame):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                resized = cv2.resize(gray, output_size, interpolation=cv2.INTER_NEAREST)
                indices = lut[resized]
                return [''.join(ascii_list[pixel] for pixel in row) for row in indices]
            # Пре-рендер
            if video_render_mode == "pre_render":
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                if fps <= 0:
                    fps = 30 # фпс по умолчанию
                frames, timestamps = [], []
                # ивент если нажать ESC во время загрузки(предотвращает ошибку)
                cancel_pre_render = threading.Event()
                def show_progress_bar(progress, total):
                    screen.fill((0, 0, 0))
                    bar_width = screen_width * 0.7
                    bar_height = 40
                    x = (screen_width - bar_width) // 2
                    y = (screen_height - bar_height) // 2
                    progress_percent = int((progress / total) * 100)
                    loading_text = f"{self.languages[effective_lang]['loading_text']}: {progress_percent}%"
                    progress_font = pygame.font.SysFont("Courier", 20)
                    text = progress_font.render(loading_text, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(screen_width // 2, y - 30))
                    screen.blit(text, text_rect)
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, int((progress / total) * bar_width), bar_height))
                    pygame.display.flip()

                # Обработка кадров
                def render_frames():
                    delay = 0 if cpu_mode == "high" else (0.01 if cpu_mode == "balanced" else 0.05)
                    futures = []
                    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                        for i in range(frame_count):
                            if cancel_pre_render.is_set():
                                break
                            ret, frame = cap.read()
                            if not ret:
                                break
                            # Параллельное преобразование(thread)
                            futures.append(executor.submit(frame_to_ascii, frame))
                            timestamps.append(i / fps)
                            if i % FRAME_UPDATE == 0:
                                show_progress_bar(i + 1, frame_count)
                            time.sleep(delay)
                        for future in futures:
                            frames.append(future.result())
                    show_progress_bar(frame_count, frame_count)
                render_thread = threading.Thread(target=render_frames)
                render_thread.start()
                while render_thread.is_alive():
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            cancel_pre_render.set()
                    time.sleep(0.2)
                render_thread.join()
                # закрытие во время пре-рендера
                if cancel_pre_render.is_set():
                    cap.release()
                    pygame.quit()
                    return
                cap.release()
                # Проверка обработки
                if not frames:
                    messagebox.showerror(self.languages[effective_lang]["error"],
                                         self.languages[effective_lang]["no_frames_error"])
                    pygame.quit()
                    return
                if play_audio and audio_path:
                    try:
                        pygame.mixer.music.load(audio_path)
                        pygame.mixer.music.play()
                    except Exception as e:
                        messagebox.showerror(self.languages[effective_lang]["audio_error"],
                                             self.languages[effective_lang]["audio_error_msg"].format(error=e))
                start_time = time.time()
                clock = pygame.time.Clock()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            running = False
                            if play_audio:
                                pygame.mixer.music.stop()
                            break
                    screen.fill((0, 0, 0))
                    elapsed = time.time() - start_time
                    # Индекс кадра по времени и fps для синхрониации
                    current_frame_index = int(elapsed * fps)
                    if current_frame_index >= len(frames):
                        start_time = time.time()
                        current_frame_index = 0
                    ascii_frame = frames[current_frame_index]
                    for y, line in enumerate(ascii_frame):
                        screen.blit(font.render(line, True, (255, 255, 255)), (0, y * char_height))
                    pygame.display.flip()
                    clock.tick(60)
            else:
                if play_audio and audio_path:
                    try:
                        pygame.mixer.music.load(audio_path)
                        pygame.mixer.music.play()
                    except Exception as e:
                        messagebox.showerror(self.languages[effective_lang]["audio_error"],
                                             self.languages[effective_lang]["audio_error_msg"].format(error=e))
                start_time = time.time()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                            running = False
                            if play_audio:
                                pygame.mixer.music.stop()
                            break
                    ret, frame = cap.read()
                    if not ret:
                        cap.release()
                        running = False
                        break
                    frame_timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                    elapsed_time = time.time() - start_time
                    wait_time = frame_timestamp - elapsed_time
                    if wait_time > 0:
                        time.sleep(wait_time)
                    ascii_frame = frame_to_ascii(frame)
                    screen.fill((0, 0, 0))
                    for y, line in enumerate(ascii_frame):
                        screen.blit(font.render(line, True, (255, 255, 255)), (0, y * char_height))
                    pygame.display.flip()
                    pygame.time.Clock().tick(120) # 120 фпс лок
                cap.release()
            pygame.quit()
            # Удалить аудио после воспроизведения
            if temp_audio_file and os.path.exists(temp_audio_file):
                os.remove(temp_audio_file)
        except Exception as e:
            messagebox.showerror(self.languages[effective_lang]["error"],
                                 self.languages[effective_lang]["error_occurred"].format(error=e))
            pygame.quit()

    # Старт обработки
    def start_processing(self):
        file_path, audio_path = self.select_files()
        if not file_path:
            return
        ascii_chars = self.get_ascii_chars()
        if not ascii_chars:
            return
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            self.info_label.config(text=self.languages[self.get_effective_lang()]["processing_image"])
            self.root.update()
            self.handle_image(file_path, ascii_chars)
        else:
            self.info_label.config(text=self.languages[self.get_effective_lang()]["processing_video"])
            self.root.update()
            self.handle_video(file_path, audio_path, ascii_chars)

# Старт приложения
def main():
    root = tk.Tk()
    app = ASCIIApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
