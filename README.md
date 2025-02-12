# pyASCI Project


======================================

English 

### Description

pyASCI is a Python application that converts images and videos into ASCII chars. It uses:

- **Tkinter** for the graphical user interface (GUI)
- **Pygame** for fullscreen rendering
- **OpenCV** for image and video processing
- **NumPy** for numerical operations (better optimization)

The application allows to adjust the font size,select a CPU usage (High, Normal, or Low) for video processing, switch between English/Russian languages and dark/light theme selection.


### Current Features 

- Converts images and videos to ASCII
- Renders output into fullscreen window
- Adjustable font size
- CPU usage mode selection for video processing (High, Normal, Low)
- Language support: English / Russian
- Theme support: Light / Dark

### Requirements


- Pygame
- OpenCV-Python (`opencv-pythong`)
- NumPy (`numpy`)
- Darkdetect (`darkdetect`)


### Installation

1. **Clone the repository** or download the code.
2. **Install the required Python packages:*

```
pis install pygame opencv-python numpy darkdetect
```
3. **Run the application*


### Usage

1. Click the **Select** button to choose a media file (image or video).
   - For video files, you can also select an audio file.
2. For video and image select a font appear size. For video, select a CPU Usage(renders faster but uses more resources)
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

Приложение позволяет выбрать размер шрифта и палитру символов, режим использований ЦП (высокий, обычный, низкий) для видео рендеринга, переключатся между русским/английским языками и выбрать тёмное/светлое оформление.


### Текущие функции

- Преобразование медиа файлов в ASCII
- Обрабатывает в полном экране
- Изменяемый размер шрифта
- Режимы использования ЦП (высокий, обычный и низкий)
- Поддерживаемые языки: Английский / Русский
- Поддерживаемые оформления: Светлое / Тёмное

### Библиотеки


- Pygame
- OpenCV-Python (`opencv-pythong`)
- NumPy (`numpy`)
- Darkdetect (`darkdetect`)


### Установка

1. **Клонируйте репозиторий** или скачайте код.
2. **Установите необходимые библиотеки:*

```
pis install pygame opencv-python numpy darkdetect
```
3. **Запустите приложение*


### Использование

1. Нажмите **Выбрать** для выбора медиа(видео или изображение).
   - Для видео так же можно выбрать аудио.
2. Для видео и изображения выберите размер шрифта. Для видео выберите использование процессора (рендеринг будет быстрее, но использует больше ресурсов).
3. ASCII-версия будет открыта в полном экране после рендеринга, видео будет постоянно запускаться заново.
4. Нажмите ESC для выхода.

