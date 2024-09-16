import cv2 
import numpy as np 
import random
import streamlit as st
import os 
import keyboard
import time
import psutil

# --------------------- FUNCIONES ----------------------- 
def segmentation(hsv_frame):
    # Rangos de rojo en hsv
    lower_red1 = np.array([0, 140, 60])
    upper_red1 = np.array([10, 210, 160])

    lower_red2 = np.array([170, 140, 60])
    upper_red2 = np.array([180, 210, 160])

    # Creación de las máscaras 
    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    mask_red = mask1 + mask2 # combinación de ambas máscaras 
    red_bottle_cap = cv2.bitwise_and(hsv_frame, hsv_frame, mask=mask_red)  # operación AND al frame con la máscara

    # se convierte a escala de grises para facilitar la detección de contornos
    imgray = cv2.cvtColor(red_bottle_cap, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 140, 255, 0) # convierte escala de grises a binario

    return red_bottle_cap, thresh

def close_streamlit():
        time.sleep(5)
        # Close streamlit browser tab
        keyboard.press_and_release('ctrl+c')
        # Terminate streamlit python process
        pid = os.getpid()
        p = psutil.Process(pid)
        p.terminate()

# Configuración inicial Streamlit
st.title('Juego OpenCV')
st.write('Autor: Mario Gómez Sánchez-Celemín')

frame_placeholder=st.empty()

stop_button_pressed=st.button("Stop")
play_again_button_pressed=st.button("Play again")

# Variables globales
score=0
radius=10
collision_detected = True # evento asíncrono
game_over = False         # evento asíncrono


# ----------------- BUCLE INFINITO ------------------- 

# Capturar video desde la cámara web
video = cv2.VideoCapture(0)

# Bucle infinito para mostrar y procesar imagenes
while True:
    # Leer el frame actual del video
    ret, frame = video.read()
    
    frame=cv2.flip(frame,1) # girar la imagen para evitar el efecto espejo

    # Obtener el ancho y alto del frame capturado
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    x_min,x_max=20,frame_width-20
    y_min,y_max=50,frame_height-20

    if not game_over: # si se pierde no se ejecuta la lógica del juego
        # Cambiar target
        if collision_detected:
            target_x,target_y=random.randint(x_min+10, x_max-10),random.randint(y_min+10, y_max-10)
            collision_detected=False

        # Procesado de imagen
        # Convertir a formato hsv (recomendado para segmentación por colores)
        hsv_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        red_bottle_cap,thresh=segmentation(hsv_frame) # función definida para la segmentación (hsv y grises)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Se busca el mayor area entre los contornos detectados 
        if contours:
            max_area=10
            best_cnt=contours[0]
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > max_area:
                    max_area = area
                    best_cnt = cnt

            # cálculo de las coordenadas del circulo a traves del centroide
            M = cv2.moments(best_cnt)
            if M["m00"] != 0:  # Evitar división por cero
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Dibujar circulo en el frame original
                cv2.circle(frame, (cX, cY), radius, (0, 255, 0), -1)

                if(cX-x_min<radius or x_max-cX<radius or cY-y_min<radius or y_max-cY<radius):
                    game_over=True
                
                if abs(cX - target_x) < radius and abs(cY - target_y) < radius and not collision_detected:
                    score += 1
                    collision_detected=True

    # Dibujar elementos gráficos
    cv2.rectangle(frame,(x_min,y_min),(x_max,y_max),(0,0,0),4)
    cv2.putText(frame,f'Score: {score}',(10,25),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA)

    cv2.circle(frame, (target_x, target_y), radius, (255, 0, 0), -1)
    
    if game_over:
        cv2.putText(frame,'GAME OVER',(40,240),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,0),5,cv2.LINE_AA)
        cv2.putText(frame,'Press a button',(200,270),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA)

    # Mostrar los frames
    # cv2.imshow('mask', thresh)
    # cv2.imshow('hsv mask', red_bottle_cap)
    cv2.imshow('game', frame)

    frame_placeholder.image(frame, channels="RGB")


    if cv2.waitKey(1) & 0xFF == ord('r') or play_again_button_pressed:
        game_over=False
        score=0

    # Presionar 'q' para salir del bucle o botón de detener
    if cv2.waitKey(1) & 0xFF == ord('q') or stop_button_pressed:
        close_streamlit()
        break

# Liberar la cámara y cerrar todas las ventanas
video.release()
cv2.destroyAllWindows()