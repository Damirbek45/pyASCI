# pyASCI Project


======================================

English 

### Description

pyASCI is a Python application that converts images and videos into ASCII chars. It uses:

- **Tkinter** for the graphical user interface (GUI)
- **Pygame** for fullscreen rendering
- **OpenCV** for image and video processing
- **NumPy** for numerical operations (better optimization)
- **Moviepy** for extracting audio from video

The application allows to adjust the font size,select a CPU usage (High, Normal, or Low) for video processing, select render options(in realtime or pre-render it) switch between English/Russian languages and dark/light theme selection.


### Current Features 

- Converts images and videos to ASCII
- Renders output into fullscreen window
- Adjustable font size
- CPU usage mode selection for video processing (High, Normal or Low)
- Render options for video processing (Realtime or Pre-render)
- Saving rendered files for images
- Language support: English / Russian
- Theme support: Light / Dark

### Requirements


- Pygame (`pygame`)
- OpenCV-Python (`opencv-python`)
- NumPy (`numpy`)
- Darkdetect (`darkdetect`)
- Moviepy (`moviepy`)


### Installation

1. **Clone the repository** or download the code.
2. **Install the required Python packages:**

```
pip install pygame opencv-python numpy darkdetect moviepy
```
3. **Run the application**


### Usage

1. Click the **Select** button to choose a media file (image or video).
2. For video and image select a font chars size, resolution(original or fullscreen) and save file or not. For video, select a CPU Usage(renders faster but uses more CPU resources) and render options(real-time or pre-render)
3. ASCII version will be opened in full screen after rendering, video will loop infinitely
4. Press **ESC** to exit.


======================================

Русский 

### Описание

pyASCI это приложение на языке Python, преобразующее медиа файлы в ASCII. Оно использует:

- **Tkinter** для графического интерфейса (GUI)
- **Pygame** для полноэкранного рендеринга
- **OpenCV** для обработки изображений и видео
- **NumPy** для нумерационных операций (оптимизация)
- **Moviepy** для извлечения аудио из видео

Приложение позволяет выбрать размер шрифта и палитру символов, режим использований ЦП (высокий, обычный, низкий) для видео рендеринга, выбирать режим рендера(в реальном времени или предварительный) переключатся между русским/английским языками и выбрать тёмное/светлое оформление.


### Текущие функции

- Преобразование медиа файлов в ASCII
- Обрабатывает в полном экране
- Изменяемый размер шрифта
- Режимы использования ЦП (высокий, обычный или низкий)
- Режимы рендера (в реальном времени или предварительный)
- Поддерживаемые языки: Английский / Русский
- Поддерживаемые оформления: Светлое / Тёмное

### Библиотеки


- Pygame (`pygame`)
- OpenCV-Python (`opencv-python`)
- NumPy (`numpy`)
- Darkdetect (`darkdetect`)
- Moviepy (`moviepy`)

### Установка

1. **Клонируйте репозиторий** или скачайте код.
2. **Установите необходимые библиотеки:**

```
pip install pygame opencv-python numpy darkdetect moviepy
```
3. **Запустите приложение**


### Использование

1. Нажмите **Выбрать** для выбора медиа(видео или изображение).
2. Для видео и изображения выберите размер шрифта. Для изображения выберите режим отображения(оригинал или растянутый на весь экран) и сохранить ли файл или нет. Для видео выберите режим использования процессора (рендеринг будет быстрее, но использует больше ресурсов) и режим рендера(в реальном времени или предварительная загрузка).
3. ASCII-версия будет открыта в полном экране после рендеринга, видео будет постоянно запускаться заново.
4. Нажмите ESC для выхода.

