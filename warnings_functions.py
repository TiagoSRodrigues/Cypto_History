def show_messagem_box(title, message, hwnd=0, mensage_style="MB_OK"):
    import ctypes.wintypes as cw  , ctypes

    HWND, LPWSTR, UINT = cw.HWND, cw.LPWSTR, cw.UINT
    _user32 = ctypes.WinDLL('user32', use_last_error=True)

    _MessageBoxW = _user32.MessageBoxW
    _MessageBoxW.restype = UINT  # default return type is c_int, this is not required
    _MessageBoxW.argtypes = (HWND, LPWSTR, LPWSTR, UINT)

    styles = {
        "MB_OK" : 0,
        "MB_OKCANCEL" : 1,
        "MB_YESNOCANCEL" : 3,
        "MB_YESNO" : 4,
        "IDOK" : 1,
        "IDCANCEL" : 2,
        "IDABORT" : 3,
        "IDYES" : 6,
        "IDNO" : 7
      }

    try:
        style=styles[mensage_style]
    except:
        style=1
        message="The message style is wrong, but the message is: \n\n"+message

    def MessageBoxW(hwnd, text, caption, style):
        result = _MessageBoxW(hwnd, text, caption, style)
        if not result:
            raise ctypes.WinError(ctypes.get_last_error())
        return result
    try:
        result = MessageBoxW(None, message, title, style)
    except WindowsError as win_err:
        print("An error occurred:\n{}".format(win_err))



# show_messagem_box(0,"Texto da mensagem", "Título da mensagem","MB_OK")



 #### SOUND  #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### #### 
import winsound, time
def play_warnning_sound():
    for a in range (2):
        for i in range(int((15))):
            duration = 100  # milliseconds
            freq = int(((1+i) )*40+30)  # Hz
            winsound.Beep(freq, duration)
            time.sleep(.05)
# play_warnning_sound()

