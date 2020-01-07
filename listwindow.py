import win32gui

hwnd = win32gui.FindWindow(None,"Vindictus")
rect = win32gui.GetWindowRect(hwnd)
x = rect[0]
y = rect[1]
w = rect[2] - x
h = rect[3] - y
print("Window {}:",win32gui.GetWindowText(hwnd))
print("\tLocation: (%d, %d)",x, y)
print("\t    Size: (%d, %d)",w, h)