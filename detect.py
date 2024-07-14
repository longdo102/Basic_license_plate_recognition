import cv2
def detect_plate(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 190, 200)  # Perform Edge detection

    cnts, new = cv2.findContours(edged.copy(), cv2.RETR_TREE,
                                 cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
    contour_plate = None
    license_plate = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            contour_plate = approx
            x, y, w, h = cv2.boundingRect(contour_plate)
            license_plate =gray[y:y + h, x:x + w]
            #license_plate = gray[y+2:y + h, x+2:x + w]
            #license_plate = cv2.threshold(license_plate, 128, 255, cv2.THRESH_BINARY)[1]
            break
        
    return license_plate

