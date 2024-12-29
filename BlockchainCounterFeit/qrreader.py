# importing the OpenCV library  
import cv2
def process(pname):
# reading the image  
    qr_img = cv2.imread(pname+".png")
    #cv2.imshow("input qr",qr_img)
    cv2.waitKey(0)  
    # using the QRCodeDetector() function  
    qr_det = cv2.QRCodeDetector()  
    # using the detectAndDecode() function  
    val, pts, st_code = qr_det.detectAndDecode(qr_img)  
    # printing the value  
    print("Information:", val)
#process("cinthol")
