import cv2
import win32con
import win32gui
import win32ui
import win32api
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class RGBFinder:
	def __init__(self):
		self.top = 268
		self.left = 649
		self.w = 907 - 651  # 904-651
		self.h = 524 - 268  # 498-268+37
		self.x = 0
		self.y = 0
		self.vindictus_w = 0
		self.vindictus_h = 0
		self.colors = [["black", 25, 25, 25, 765, 0, 0], ["white", 230, 230, 230, 765, 0, 0],
					   ["pink", 200, 110, 200, 765, 0, 0], ["red", 200, 15, 15, 765, 0, 0]]
		self.locks = {}
		for color in self.colors:
			color_name = color[0]
			self.locks[color_name] = threading.Lock()

	def int8(self, x):
		if x < 0:
			return int(256 + x)
		return int(x)

	def get_screencap(self):
		hwnd = win32gui.FindWindow(None, "Vindictus")
		if not hwnd:
			img = cv2.imread("screencap.bmp")
			w = img.shape[1]
			h = img.shape[0]
			return cv2.imread("screencap.bmp"), w, h, None, None, None, None

		rect = win32gui.GetWindowRect(hwnd)
		self.x = rect[0]
		self.y = rect[1]
		self.vindictus_w = rect[2] - self.x
		self.vindictus_h = rect[3] - self.y

		w = self.w
		h = self.h
		left = self.left
		top = self.top

		wDC = win32gui.GetWindowDC(hwnd)
		dcObj = win32ui.CreateDCFromHandle(wDC)
		cDC = dcObj.CreateCompatibleDC()
		dataBitMap = win32ui.CreateBitmap()
		dataBitMap.CreateCompatibleBitmap(dcObj, w, h)

		cDC.SelectObject(dataBitMap)
		cDC.BitBlt((0, 0), (w, h), dcObj, (left, top), win32con.SRCCOPY)
		dataBitMap.SaveBitmapFile(cDC, "screencap.bmp")

		dcObj.DeleteDC()
		cDC.DeleteDC()
		win32gui.ReleaseDC(hwnd, wDC)
		win32gui.DeleteObject(dataBitMap.GetHandle())

		bmpRGB = dataBitMap.GetBitmapBits(True)
		img = np.frombuffer(bmpRGB, dtype='uint8')
		img.shape = (h, w, 4)
		return img, x, y, left, top, w, h

	def check_pixel(self, pixel, i, j):
		[b, g, r] = pixel
		for color in self.colors:
			r_diff = abs(r - color[1])
			g_diff = abs(g - color[2])
			b_diff = abs(b - color[3])
			tot_diff = r_diff + g_diff + b_diff
			# print("x=",i,", y=",j,"(",int8(r),int8(g),int8(b),")",abs(int8(r) - color[1]),abs(int8(g) - color[2]),abs(int8(b) - color[3]))
			#self.locks[color[0]].acquire()
			if tot_diff < color[4]:
				color[4] = tot_diff
				color[5] = i
				color[6] = j
			#self.locks[color[0]].release()

	def run(self):
		img, w, h, x, y, left, top = self.get_screencap()
		start = datetime.now()
		print("Checking for colors")
		
		with ThreadPoolExecutor(max_workers=10) as ex:
			for i in range(w):
				for j in range(h):
					ex.submit(self.check_pixel, img[j,i], i, j)
		end = datetime.now()
		duration = (end - start).total_seconds()
		print("{}s elapsed".format(duration))
		for color in self.colors:
			print(color[0], "at(", color[5], ",", color[6], ")", img[color[6], color[5]])

		if x is not None:
			uin = input("Enter the color: ")
			for color in self.colors:
				if uin == color[0]:
					win32api.SetCursorPos((x+left+color[5], y+top+color[6]))
		#print(colors[i][0],"at(",colors[i][5],",",colors[i][6],")", image[colors[i][6],colors[i][5]])
		#win32api.SetCursorPos((x+left+colors[i][5],y+top+colors[i][6]))

		print("Done checking for colors")


if __name__ == '__main__':
	rgb_finder = RGBFinder()
	rgb_finder.run()
