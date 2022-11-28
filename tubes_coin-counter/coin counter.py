import imutils
import cv2
import numpy as np

cap = cv2.VideoCapture('http://192.168.103.59:8080/video')  # alamat ip dari ipcam di android
cap.set(3, 720)
cap.set(4, 1020)
while True:
    _, frame = cap.read() # mengambil tiap frame dari hasil input video
    frame_img = frame.copy()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # mengubah frame menjadi format grayscale
    img = cv2.bilateralFilter(img, 11, 17, 17)  # filter untuk smoothing
    _, thres = cv2.threshold(img, 155, 255, cv2.THRESH_BINARY) # mengubah image menjadi biner dengan threshold
    thres = cv2.bitwise_not(thres)#mengubah citra biner menjadi terbalik
    thres = cv2.medianBlur(thres, 5) # menambahkan median blur pada citra
    edged = cv2.Canny(thres, 5, 100) #mencari tepian dengan metode canny
    cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] #menemukan menemukan garis lengkung yang terhubung
    cnt_len = 0 #fungsi perhitungan
    for each in range(len(cnts)):
        if cv2.contourArea(cnts[each]) > 1000:#area sambungan lebih dari 1000 piksel maka dihitung sebagai koin
            frame_img = cv2.drawContours(frame_img, cnts, each, (0, 255, 0), 5)
            cnt_len += 1
    frame_txt = frame_img.copy()
    frame_txt = cv2.putText(frame_img, "Jumlah Koin " + str(cnt_len), \
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0)) #penambahan teks keterangan jumlah koin

    cv2.imshow('Penghitung Koin', imutils.resize(frame_txt, width=700)) # penampil windows dan cara exit
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
