# PyGLCube 🧊

A simple 3D cube simulation developed using **Python** with **PyOpenGL** for rendering and **Pygame** for window and event handling.

This project serves as a foundational exercise in 3D computer graphics, demonstrating object transformation, camera control, and interactive user input in a Python environment.

---

## Features

* **3D Rendering:** A cube is rendered in a 3D space using OpenGL.
* **Real-time Rotation:** The cube can be rotated in real-time along the X, Y, and Z axes.
* **Interactive Controls:** Users can control the cube's rotation using keyboard or mouse inputs.
* **Simple Camera:** A basic perspective view to observe the cube.

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Python 3.8+**
* **pip** (Python package installer)
* **Git**

---

## Installation & Setup

To run this project on your local machine, follow these steps:

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/mdzpaulina/Cubo.git](https://github.com/mdzpaulina/Cubo.git)
    cd Cubo
    ```

2.  **Create and activate a virtual environment:**
    * On **macOS/Linux**:
        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```
    * On **Windows**:
        ```sh
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the required packages:**
    With the virtual environment activated, install all dependencies from the `requirements.txt` file.
    ```sh
    pip install -r requirements.txt
    ```

---

## Usage

Once the installation is complete, you can run the application with the following command:

```sh
python main.py
```

* **Zoom:** Use the mouse scroll wheel to zoom in and out.

---

## Technologies Used

* **Python:** The core programming language.
* **PyOpenGL:** A Python binding for the OpenGL graphics API, used for all 3D rendering.
* **Pygame:** Used for creating the window, the main application loop, and handling user input.
* **NumPy:** Used for efficient matrix operations and calculations required for 3D transformations.
* **Pillow (PIL Fork):** Can be used for texture mapping on the cube's faces.
