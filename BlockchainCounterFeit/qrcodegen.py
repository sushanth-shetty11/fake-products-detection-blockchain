# importing the qrcode library  
import qrcode
def process(pid,pname):
    inp=str(pid)+":"+str(pname)
    # generating a QR code using the make() function  
    qr_img = qrcode.make(inp)  
    # saving the image file  
    qr_img.save("./Upload/"+pname+".png")
#process(1234567890,"cinthol")
