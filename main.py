import os
import cv2
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import RAISED, filedialog
from PIL import Image, ImageTk
import numpy as np
from tkinter import messagebox
import pytesseract
import detect   # file tự định nghĩa
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# khi mà bấm chọn hoặc lưu ảnh, thì nó hiên ngay mở folder đó luôn
project_folder = os.path.dirname(os.path.abspath(__file__))
initial_dir = os.path.join(project_folder)
window = tk.Tk()
window.resizable(False, False)
window.title("Nhận diện biển số xe")
window.geometry("1250x700+150+50")  # 1250*700 là chiều dài và chiều rộng, +150+50 để căn giữa, căn bên trái và bên phải cách 150px

# đường dẫn file ảnh
script_dir = os.path.dirname(os.path.abspath(__file__))
path_img = os.path.join(script_dir, 'input', '7.jpg')
tk.Label(window, text="NHẬN DIỆN BIỂN SỐ XE", width=10,
         height=2, anchor="center", bg="gray", fg="black", font='tahoma 12 bold').pack(side='top', fill='both')

# frame chứa ảnh gốc
left_frame = tk.LabelFrame(window, text="Ảnh gốc", font='tahoma 12 italic',
                           bg='#fff', fg='#000', width=720, padx=10).pack(side='left', fill="y")
img = Image.open(path_img)
img_resize = img.resize((670, 600))
img_original = ImageTk.PhotoImage(img_resize)
label_original_image = tk.Label(left_frame, image=img_original, anchor="e")
label_original_image.place(x=2, y=80)


# frame bên phải, chứa ảnh kết quả và các button chức năng
right_frame = tk.LabelFrame(window, text="Kết quả", font='tahoma 12 italic',
                            bg='#fff', fg='#000', width=520).pack(side='right', fill="y")
img_result = None
img_save = None
label_image_result = tk.Label(right_frame)
label_image_result.place(x=740, y=80)

text_var = tk.StringVar()
# label biển số xe
tk.Label(right_frame, text="Biển số xe:",
         font="tahoma 14", fg="blue", bg='#fff').place(x=745, y=420)
label_plate = tk.Entry(right_frame, font='tahoma 14', fg='blue', width=30, textvariable=text_var, highlightthickness=2,
                       highlightcolor="gray", highlightbackground="gray", state="readonly")

label_plate.place(x=845, y=420)

# frame chứa các button xử lý
frame_button = tk.LabelFrame(
    right_frame, text="", bg="#fff", fg="#000", font="tahoma 14", borderwidth=2,
    padx=8, pady=8)
frame_button.place(x=800, y=480)


def handle():
    global img_result, label_image_result, label_plate, img_save, text_var
    # đặt state của ô input về normal mới thêm được text
    label_plate.configure(state="normal")
    text_var.set("")
    image_plate = detect.detect_plate(cv2.imread(path_img))
    if image_plate is not None:
        #text = pytesseract.image_to_string(image_plate, config='--psm 6')
        text = pytesseract.image_to_string(image_plate, config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.- --psm 7') 
        if (len(text) > 6):
            img_save = cv2.resize(image_plate, (300, 100))
            img_result = Image.fromarray(img_save)
            img_result = ImageTk.PhotoImage(img_result)
            label_image_result.config(image=img_result)
            text_var.set(text)
            print('Plate number: ', text)
        else:
            text_var.set("Không nhận dạng được")
    else :
        text_var.set("Không nhận dạng được")
    # sau khi thêm text đặt lại chỉ được đọc, ko được chỉnh sửa
    label_plate.configure(state="readonly")

# button xử lý để nhận được biển số xe
btn_hanle = tk.Button(frame_button, text="Nhận dạng",
                      width=10, padx=4, pady=4, command=handle)
btn_hanle.grid(row=0, column=0, padx=8, pady=8)



# function choose file image

def select_file():
    file_type = [('Image files', '.png .jpg .jpeg .gif')]
    file_name = filedialog.askopenfilename(initialdir=initial_dir,
                                           title='Choose image file',
                                           filetypes=file_type)
    if (file_name != ""):
        # change image in left and right frame
        global path_img, label_original_image, label_image_result, img_result, img_original, label_plate, img_save, text_var
        path_img = file_name
        text_var.set("")
        # change image original
        img = Image.open(path_img)
        img_resize = img.resize((670, 600))
        img_original = ImageTk.PhotoImage(img_resize)
        label_original_image.config(image=img_original)

        # change image result
        img_result = None
        label_image_result.config(image="")
        img_save = None

# button chọn ảnh
btn_choose_image = tk.Button(
    frame_button, text="Chọn ảnh", width=10, padx=4, pady=4, command=select_file)
btn_choose_image.grid(row=0, column=1, padx=8, pady=8)


def camera(): 
    cap = cv2.VideoCapture(0)
    new_width = 440
    new_height = 380
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)
# Thiết lập kích thước khung hình và độ phân giải
    while True:
        # Đọc khung hình từ webcam
        ret, frame = cap.read()
        # Chuyển khung hình sang định dạng xám
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Làm mịn ảnh bằng phương pháp Gaussian Blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # ảnh nhị phân
        _, thresholded = cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY)
        # Áp dụng phép lọc Canny để phát hiện cạnh
        canny = cv2.Canny(blur, 50, 150)
        # Tìm contour của đối tượng trong ảnh
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Lặp qua các contour để tìm biển số xe
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            area = w * h
         
            # Kiểm tra kích thước của contour
            if area > 1000 and area < 5000:
                # Xấp xỉ contour thành đa giác
                epsilon = 0.018 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                # Kiểm tra xem đa giác có 4 đỉnh hay không và có chiều dài và chiều rộng phù hợp
                if len(approx) == 4 and (w > 2.5 * h and w < 4 * h):
                    # Vẽ đường bao quanh contour lên khung hình gốc
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                    # Cắt ảnh phần biển số xe
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_color = frame[y:y + h, x:x + w]
                    # Nhận diện chữ số và ký tự trên biển số xe
                    text = pytesseract.image_to_string(roi_gray, config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.- --psm 7')  
                    # Hiển thị kết quả
                    if len(text)>6:
                        print('Biển số: ',text)
                        cv2.imshow('Number Plate', roi_color)  # Hiển thị vùng chứa biển số
                        cv2.waitKey(0)  # Chờ người dùng ấn một phím bất kỳ để tiếp tục

        cv2.imshow('frame', frame)

        # Nhấn phím 'q' để thoát chương trình
        if cv2.waitKey(1) == ord('q'):
            break
# Giải phóng bộ nhớ và đóng kết nối
    cap.release()

# button camera
btn_camera = tk.Button(
    frame_button, text="Camera", width=10, padx=4, pady=4, command=camera)
btn_camera.grid(row=0, column=2, padx=8, pady=8)

window.mainloop()
