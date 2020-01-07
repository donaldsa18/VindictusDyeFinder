import cv2
import win32con
import win32gui
import win32ui
import win32api
import numpy as np


class RGBFinder:
	def __init__(self, gui=None):
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

		self.gui = gui
		if gui is not None:
			gui.set_rgb_finder(self)

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
		self.x = x = rect[0]
		self.y = y = rect[1]
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

	def find_color(self, color, img):
		b, g, r = cv2.split(img)
		channels = [r, g, b]
		diffs = []
		for i in range(3):
			diffs.append(cv2.absdiff(channels[2-i], color[i+1]))
		dist = cv2.add(diffs[0], cv2.add(diffs[1], diffs[2]))
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(dist)
		color[5] = min_loc[0]
		color[6] = min_loc[1]

	def run(self):
		img, w, h, x, y, left, top = self.get_screencap()
		print("Checking for colors")
		for color in self.colors:
			self.find_color(color, img)
		for color in self.colors:
			print("{} at ({},{}) {}".format(color[0], color[5], color[6], img[color[6], color[5]]))

		if x is not None:
			uin = input("Enter the color: ")
			for color in self.colors:
				if uin == color[0]:
					win32api.SetCursorPos((x+left+color[5], y+top+color[6]))
		#print(colors[i][0],"at(",colors[i][5],",",colors[i][6],")", image[colors[i][6],colors[i][5]])
		#win32api.SetCursorPos((x+left+colors[i][5],y+top+colors[i][6]))


		if self.gui is not None:
			self.gui.insert_colors(self.colors)
		else:
			print("Done checking for colors")

	def move_mouse(self, pix_x, pix_y):
		x = 0
		y = 0
		hwnd = win32gui.FindWindow(None, "Vindictus")
		if not hwnd:
			hwnd = win32gui.FindWindow(None, "Vindictus Dye Finder")
			# move mouse to the image instead of the actual Vindictus window
			x -= self.left - 29
			y -= self.top - 75

		rect = win32gui.GetWindowRect(hwnd)
		x += rect[0]
		y += rect[1]
		win32api.SetCursorPos((x + self.left + pix_x, y + self.top + pix_y))


if __name__ == '__main__':
	rgb_finder = RGBFinder()
	rgb_finder.run()
