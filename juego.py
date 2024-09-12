import cv2 
import numpy as np 

# Rangos de rojo en hsv
lower_red1 = np.array([0, 160, 60])
upper_red1 = np.array([10, 210, 120])

lower_red2 = np.array([170, 160, 60])
upper_red2 = np.array([180, 210, 120])

# Capturar video desde la cámara web
video = cv2.VideoCapture(0)

while True:
    # Leer el frame actual del video
    ret, frame = video.read()
    
    # Convertir a formato hsv (recomendado para segmentación por colores)
    hsv_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # Creación de las máscaras 
    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    mask_red = mask1 + mask2 # combinación de ambas máscaras 
    red_bottle_cap = cv2.bitwise_and(hsv_frame, hsv_frame, mask=mask_red)  # operación AND al frame con la máscara

    # se convierte a escala de grises para facilitar la detección de contornos
    imgray = cv2.cvtColor(red_bottle_cap, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 140, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Se busca el mayor area entre los contornos detectados 
    if contours:
        max_area=50
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
            cv2.circle(frame, (cX, cY), 10, (0, 255, 0), -1)

    # Mostrar los frames
    cv2.imshow('gary mask', thresh)
    cv2.imshow('hsv mask', red_bottle_cap)
    cv2.imshow('Detected Circles', frame)
    
    # Presionar 'q' para salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar todas las ventanas
video.release()
cv2.destroyAllWindows()