import cv2
import win32con
import win32gui
import win32ui
import win32api
import numpy
from PIL import ImageGrab

def int8(x):
	if x<0:
		return int(256+x)
	return int(x)

hwnd = win32gui.FindWindow(None,"Vindictus")
rect = win32gui.GetWindowRect(hwnd)
x = rect[0]
y = rect[1]
#w = rect[2] - x
#h = rect[3] - y
top = 268
left = 649
w = 907-651#904-651
h = 524-268 # 498-268+37
wDC = win32gui.GetWindowDC(hwnd)
dcObj=win32ui.CreateDCFromHandle(wDC)
cDC=dcObj.CreateCompatibleDC()
dataBitMap = win32ui.CreateBitmap()
dataBitMap.CreateCompatibleBitmap(dcObj, w, h)

cDC.SelectObject(dataBitMap)
cDC.BitBlt((0,0),(w, h) , dcObj, (left,top), win32con.SRCCOPY)
dataBitMap.SaveBitmapFile(cDC, "screencap.bmp")
bmpRGB = dataBitMap.GetBitmapBits(False)
#print(bmpRGB)
# Free Resources


dcObj.DeleteDC()
cDC.DeleteDC()
win32gui.ReleaseDC(hwnd, wDC)
win32gui.DeleteObject(dataBitMap.GetHandle())
image = cv2.imread("screencap.bmp")

#cv2.imshow("cropped",crop)
#cv2.waitKey(0)

#pilimg = ImageGrab.grab(bbox=(x+left,y+top,w,h))
#pilimgrgb = pilimg.convert('RGB')
#img = numpy.array(pilimgrgb)
#image = cv2.CreateImageHeader(pil_img.size, cv.IPL_DEPTH_8U, 3)  # RGB image
#cv2.SetData(image, pilImg.tostring(), pilImg.size[0]*3)
#imgW,imgH,imgP = img.shape
#cv2.NamedWindow("pil2ipl")
#cv2.ShowImage("pil2ipl", image)
#cv2.waitKey(0)
colors = [["black",25,25,25,765,0,0],["white",230,230,230,765,0,0],["pink",200,110,200,765,0,0],["red",200,15,15,765,0,0]]
#,["yellow",230,230,25,765,0,0]
print("Checking for colors")
for i in range(w):
	for j in range(h):
		[b,g,r] = image[j,i]#bmpRGB[j*w+i:j*w+i+3]
		
		for color in colors:
			rdiff = abs(r - color[1])
			gdiff = abs(g - color[2])
			bdiff = abs(b - color[3])
			totdiff = rdiff +gdiff + bdiff
			#print("x=",i,", y=",j,"(",int8(r),int8(g),int8(b),")",abs(int8(r) - color[1]),abs(int8(g) - color[2]),abs(int8(b) - color[3]))
			if totdiff < color[4]:
				color[4] = totdiff
				color[5] = i
				color[6] = j
closestColor = 765
#for i in range(4):
#	if colors[i][4] < closestColor:
#		closestColor = i
uin = input("Enter the color: ");
for color in colors:
	if uin == color[0]:
		print(color[0],"at(",color[5],",",color[6],")", image[color[6],color[5]])
		win32api.SetCursorPos((x+left+color[5],y+top+color[6]))
#print(colors[i][0],"at(",colors[i][5],",",colors[i][6],")", image[colors[i][6],colors[i][5]])
#win32api.SetCursorPos((x+left+colors[i][5],y+top+colors[i][6]))

print("Done checking for colors")

		
