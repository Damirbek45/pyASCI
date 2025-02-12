# pyASCI Project


======================================

#* English */

### Description

pyASCI is a Python application that converts images and videos into ASCII characters. It uses:

- **Tkinter** for the graphical user interface (GUI)
- **Pygame** for fullscreen rendering
- **OpenCV** for image and video processing
- **NumPy** for numerical operations (better optimization)

The application allows you to adjust the font size, select a CPUSage mode (High, Normal, or Low) for video processing, switch between English and Russian languages, and choose between a light or dark theme.


### Current Features 

- Converts images and videos to ASCII
- Renders output in a fullscreen window
- Adjustable font size with evenly spaced options
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
3. **Run the application:*

```
python your_script.py
```

### Usage

1. Click the **Select** button to choose a media file (image or video).
   - For video files, you can also select an audio file.
2. For video files, select a font size and CS usage mode (High, Normal, or Low).    For images, only the font size is requested.
3. The ASCII version will render in a fullscreen window.
4. Press **ESC** to exit.