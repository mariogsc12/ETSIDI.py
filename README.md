
# 🐍 ETSIDI.py Workshop – Python Project

This repository contains all the files developed during the **ETSIDI.py Python Workshop**, held at the **Escuela Técnica Superior de Ingeniería y Diseño Industrial (ETSIDI)**, part of the **Universidad Politécnica de Madrid**, in **September 2024**.

---

## 📁 Repository Structure

- `juego.py`  
  Contains the main game logic and user interface.  
  ▶️ Run it from the terminal using:  
  ```bash
  streamlit run juego.py
  ```

- `check_hsv_mouse.py`  
  Utility script to get the **HSV values** of a pixel under the mouse cursor.  
  Used to determine the color range for segmentation masks.

---

## 🧪 Project Demo

This project uses **computer vision** to detect a red pointer (e.g., a cap or marker) and interact with a mini-game developed in **Streamlit**.

### 🔴 Pointer Segmentation Example
Color segmentation in HSV to isolate the red cap:

![Pointer Segmentation](https://github.com/mariogsc12/TallerPython/blob/main/imagenes/segmentaci%C3%B3n_tap%C3%B3n_rojo2.jpg)

---

### 🌐 Streamlit Web App Interface
Interactive interface where the user controls elements using the detected red pointer:

![Streamlit Interface](https://github.com/mariogsc12/TallerPython/blob/main/imagenes/streamlit_webapp.jpg)

---

## 📦 Requirements

Make sure you have Python installed and then install the dependencies:

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, you can install manually:

```bash
pip install streamlit opencv-python
```

---

## 🚀 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/mariogsc12/TallerPython.git
   cd TallerPython
   ```

2. Run the game:
   ```bash
   streamlit run juego.py
   ```

3. (Optional) Use `check_hsv_mouse.py` to calibrate color detection.

---

## 👨‍🏫 Workshop Info

📍 **ETSIDI.py** – Python Workshop  
🏫 Universidad Politécnica de Madrid  
📅 September 2024

---

Feel free to ⭐️ this repository if you enjoyed the project!
