import win32api
import win32gui
from win32con import WM_INPUTLANGCHANGEREQUEST


def shift_language(lang_tag="en-US"):
    """Shift input language of current window.

    Language data from: https://msdn.microsoft.com/en-us/library/cc233982.aspx
    :param lang_tag: tag of target language
    """
    # Tag, ID, fullname of language
    LANG_DICT = {
        "zh-CN": {
            'id': 0x0804,
            'fullname': "Chinese (Simplified) (People's Republic of China)",
        },
        "en-US": {
            'id': 0x0409,
            'fullname': 'English (United States)'
        },
    }

    # Get the foreground window handle
    hwnd = win32gui.GetForegroundWindow()

    # Get the foreground window title
    title = win32gui.GetWindowText(hwnd)
    print('The current window: ' + title)

    '''
    # Get the keyboard layout list
    im_list = win32api.GetKeyboardLayoutList()
    im_list = list(map(hex, im_list))
    print(im_list)
    '''

    # Shift input language
    result = win32api.SendMessage(
        hwnd,
        WM_INPUTLANGCHANGEREQUEST,
        0,
        LANG_DICT[lang_tag]['id'])
    if result == 0:
        print('Tried shifting input language to: ' + LANG_DICT[lang_tag]['fullname'])
