import cv2

# Inizializza il tracker
tracker = cv2.TrackerMOSSE_create()

# Carica il video di input
video = cv2.VideoCapture('nome_del_tuo_video.mp4')

# Leggi il primo frame del video
ret, frame = video.read()

# Seleziona una regione di interesse (ROI) da tracciare
bbox = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)

# Inizializza il tracker con la ROI selezionata
tracker.init(frame, bbox)

# Ciclo principale per leggere il video frame per frame
while True:
    # Leggi il frame successivo
    ret, frame = video.read()

    # Esci dal ciclo se il video è terminato
    if not ret:
        break

    # Aggiorna il tracker per ottenere la nuova posizione dell'oggetto
    success, bbox = tracker.update(frame)

    # Disegna il rettangolo intorno all'oggetto tracciato
    if success:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Mostra il frame con il rettangolo del tracciamento
    cv2.imshow("Frame", frame)

    # Interrompi l'esecuzione se viene premuto il tasto 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia le risorse
video.release()
cv2.destroyAllWindows()
