from __future__ import print_function
import ctypes
from ctypes import wintypes
from collections import namedtuple
import pyautogui

user32 = ctypes.WinDLL('user32', use_last_error=True)
WindowInfo = namedtuple('WindowInfo', 'pid title')

WNDENUMPROC = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,    # _In_ hWnd
    wintypes.LPARAM,) # _In_ lParam

def list_windows():
    '''Return a sorted list of visible windows.'''
    result = []
    @WNDENUMPROC
    def enum_proc(hWnd, lParam):
        if user32.IsWindowVisible(hWnd):
            pid = wintypes.DWORD()
            tid = user32.GetWindowThreadProcessId(
                        hWnd, ctypes.byref(pid))
            length = user32.GetWindowTextLengthW(hWnd) + 1
            title = ctypes.create_unicode_buffer(length)
            user32.GetWindowTextW(hWnd, title, length)
            result.append(WindowInfo(pid.value, title.value))
        return True
    user32.EnumWindows(enum_proc, 0)
    return sorted(result)

#print(list_windows())

pyautogui.getWindowsWithTitle('Coil Springs México - Google Chrome')[0].maximize()
im1 = pyautogui.screenshot()
im1.save(r"screenshot.png")