import cv2
import numpy as np

# Función para manejar el evento del mouse
def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:  # Detecta movimiento del ratón
        hsv_value = hsv_frame[y, x]   # Obtiene los valores HSV en la posición del ratón
        h_value = hsv_value[0]  # Canal H
        s_value = hsv_value[1]  # Canal S
        v_value = hsv_value[2]  # Canal V
        print(f'H: {h_value}, S: {s_value}, V: {v_value}')

# Cargar la imagen y convertir a HSV
frame = cv2.imread('ruta_de_tu_imagen.jpg')
hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Crear una ventana para mostrar la imagen
cv2.imshow('HSV Image', frame)

# Configurar la función del mouse
cv2.setMouseCallback('HSV Image', mouse_event)

# Mantener la ventana abierta hasta que se presione una tecla
cv2.waitKey(0)
cv2.destroyAllWindows()
