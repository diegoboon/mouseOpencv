
import cv2
import numpy as np
import SeguimientoManos as sm  
import autopy  


anchocam, altocam = 1540, 1200 
cuadro = 100
anchopanta, altopanta = autopy.screen.size() 
sua = 5
pubix, pubiy = 0,0
cubix, cubiy = 0,0


#----------------------------------- Lectura de la camara----------------------------------------
cap = cv2.VideoCapture(0)
cap.set(3,anchocam)  
cap.set(4,altocam)


detector = sm.detectormanos(maxManos=1) 

while True:
    #----------------- Encontrar los puntos de la mano -----------------------------
    ret, frame = cap.read()
    frame = detector.encontrarmanos(frame) 
    lista, bbox = detector.encontrarposicion(frame) 

    #-----------------Obtener la punta del dedo indice y corazon----------------------------
    if len(lista) != 0:
        x1, y1 = lista[8][1:]                  
        x2, y2 = lista[12][1:]                 
        

        #----------------- Comprobar que dedos estan arriba --------------------------------
        dedos = detector.dedosarriba() 
        cv2.rectangle(frame, (cuadro, cuadro), (anchocam - cuadro, altocam - cuadro), (0, 0, 0), 2)  
        #-----------------Modo movimiento: solo dedo indice-------------------------------------
        if dedos[1]== 1 and dedos[2] == 0:  

            #-----------------> Modo movimiento conversion a las pixeles de mi pantalla-------------
            x3 = np.interp(x1, (cuadro,anchocam-cuadro), (0,anchopanta))
            y3 = np.interp(y1, (cuadro, altocam-cuadro), (0, altopanta))

            #------------------------------- Suavizado los valores ----------------------------------
            cubix = pubix + (x3 - pubix) / sua 
            cubiy = pubiy + (y3 - pubiy) / sua

            #-------------------------------- Mover el Mouse ---------------------------------------
            autopy.mouse.move(anchopanta - cubix,cubiy) 
            cv2.circle(frame, (x1,y1), 10, (0,0,0), cv2.FILLED)
            pubix, pubiy = cubix, cubiy

        #----------------------------- Comprobar si esta en modo click -------------------------
        if dedos[1] == 1 and dedos[2] == 1:  
            # --------------->Modo click: encontrar la distancia entre ellos-------------------------
            longitud, frame, linea = detector.distancia(8,12,frame) 
            print(longitud)
            if longitud < 30:
                cv2.circle(frame, (linea[4],linea[5]), 10, (0,255,0), cv2.FILLED)

                #-------------------- Hacemos click si la distancia es corta ---------------------------
                autopy.mouse.click()


    cv2.imshow("Mouse", frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()