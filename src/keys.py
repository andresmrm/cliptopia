from Xlib import XK, X
from Xlib.protocol import event

# Copied from:
# https://github.com/guoci/autokey-py3/blob/master/src/lib/iomediator_Key.py


# Key codes enumeration
class Key:

    LEFT = "<left>"
    RIGHT = "<right>"
    UP = "<up>"
    DOWN = "<down>"
    BACKSPACE = "<backspace>"
    TAB = "<tab>"
    ENTER = "<enter>"
    SCROLL_LOCK = "<scroll_lock>"
    PRINT_SCREEN = "<print_screen>"
    PAUSE = "<pause>"
    MENU = "<menu>"

    # Modifier keys
    CONTROL = "<ctrl>"
    ALT = "<alt>"
    ALT_GR = "<alt_gr>"
    SHIFT = "<shift>"
    SUPER = "<super>"
    HYPER = "<hyper>"
    CAPSLOCK = "<capslock>"
    NUMLOCK = "<numlock>"
    META = "<meta>"

    F1 = "<f1>"
    F2 = "<f2>"
    F3 = "<f3>"
    F4 = "<f4>"
    F5 = "<f5>"
    F6 = "<f6>"
    F7 = "<f7>"
    F8 = "<f8>"
    F9 = "<f9>"
    F10 = "<f10>"
    F11 = "<f11>"
    F12 = "<f12>"

    # Other
    ESCAPE = "<escape>"
    INSERT = "<insert>"
    DELETE = "<delete>"
    HOME = "<home>"
    END = "<end>"
    PAGE_UP = "<page_up>"
    PAGE_DOWN = "<page_down>"

    # Numpad
    NP_INSERT = "<np_insert>"
    NP_DELETE = "<np_delete>"
    NP_HOME = "<np_home>"
    NP_END = "<np_end>"
    NP_PAGE_UP = "<np_page_up>"
    NP_PAGE_DOWN = "<np_page_down>"
    NP_LEFT = "<np_left>"
    NP_RIGHT = "<np_right>"
    NP_UP = "<np_up>"
    NP_DOWN = "<np_down>"
    NP_DIVIDE = "<np_divide>"
    NP_MULTIPLY = "<np_multiply>"
    NP_ADD = "<np_add>"
    NP_SUBTRACT = "<np_subtract>"
    NP_5 = "<np_5>"

    @classmethod
    def is_key(klass, keyString):
        # Key strings must be treated as case insensitive - always
        # convert to lowercase before doing any comparisons
        return (keyString.lower() in list(klass.__dict__.values()) or
                keyString.startswith("<code"))


MASK_INDEXES = [
    (X.ShiftMapIndex, X.ShiftMask),
    (X.ControlMapIndex, X.ControlMask),
    (X.LockMapIndex, X.LockMask),
    (X.Mod1MapIndex, X.Mod1Mask),
    (X.Mod2MapIndex, X.Mod2Mask),
    (X.Mod3MapIndex, X.Mod3Mask),
    (X.Mod4MapIndex, X.Mod4Mask),
    (X.Mod5MapIndex, X.Mod5Mask),
]
MODIFIERS = [Key.CONTROL, Key.ALT, Key.ALT_GR, Key.SHIFT, Key.SUPER,
             Key.HYPER, Key.META, Key.CAPSLOCK, Key.NUMLOCK]


XK.load_keysym_group('xkb')

XK_TO_AK_MAP = {
    XK.XK_Shift_L: Key.SHIFT,
    XK.XK_Shift_R: Key.SHIFT,
    XK.XK_Caps_Lock: Key.CAPSLOCK,
    XK.XK_Control_L: Key.CONTROL,
    XK.XK_Control_R: Key.CONTROL,
    XK.XK_Alt_L: Key.ALT,
    XK.XK_Alt_R: Key.ALT,
    XK.XK_ISO_Level3_Shift: Key.ALT_GR,
    XK.XK_Super_L: Key.SUPER,
    XK.XK_Super_R: Key.SUPER,
    XK.XK_Hyper_L: Key.HYPER,
    XK.XK_Hyper_R: Key.HYPER,
    XK.XK_Meta_L: Key.META,
    XK.XK_Meta_R: Key.META,
    XK.XK_Num_Lock: Key.NUMLOCK,
    # SPACE: Key.SPACE,
    XK.XK_Tab: Key.TAB,
    XK.XK_Left: Key.LEFT,
    XK.XK_Right: Key.RIGHT,
    XK.XK_Up: Key.UP,
    XK.XK_Down: Key.DOWN,
    XK.XK_Return: Key.ENTER,
    XK.XK_BackSpace: Key.BACKSPACE,
    XK.XK_Scroll_Lock: Key.SCROLL_LOCK,
    XK.XK_Print: Key.PRINT_SCREEN,
    XK.XK_Pause: Key.PAUSE,
    XK.XK_Menu: Key.MENU,
    XK.XK_F1: Key.F1,
    XK.XK_F2: Key.F2,
    XK.XK_F3: Key.F3,
    XK.XK_F4: Key.F4,
    XK.XK_F5: Key.F5,
    XK.XK_F6: Key.F6,
    XK.XK_F7: Key.F7,
    XK.XK_F8: Key.F8,
    XK.XK_F9: Key.F9,
    XK.XK_F10: Key.F10,
    XK.XK_F11: Key.F11,
    XK.XK_F12: Key.F12,
    XK.XK_Escape: Key.ESCAPE,
    XK.XK_Insert: Key.INSERT,
    XK.XK_Delete: Key.DELETE,
    XK.XK_Home: Key.HOME,
    XK.XK_End: Key.END,
    XK.XK_Page_Up: Key.PAGE_UP,
    XK.XK_Page_Down: Key.PAGE_DOWN,
    XK.XK_KP_Insert: Key.NP_INSERT,
    XK.XK_KP_Delete: Key.NP_DELETE,
    XK.XK_KP_End: Key.NP_END,
    XK.XK_KP_Down: Key.NP_DOWN,
    XK.XK_KP_Page_Down: Key.NP_PAGE_DOWN,
    XK.XK_KP_Left: Key.NP_LEFT,
    XK.XK_KP_Begin: Key.NP_5,
    XK.XK_KP_Right: Key.NP_RIGHT,
    XK.XK_KP_Home: Key.NP_HOME,
    XK.XK_KP_Up: Key.NP_UP,
    XK.XK_KP_Page_Up: Key.NP_PAGE_UP,
    XK.XK_KP_Divide: Key.NP_DIVIDE,
    XK.XK_KP_Multiply: Key.NP_MULTIPLY,
    XK.XK_KP_Add: Key.NP_ADD,
    XK.XK_KP_Subtract: Key.NP_SUBTRACT,
    XK.XK_KP_Enter: Key.ENTER,
    XK.XK_space: ' '
}

AK_TO_XK_MAP = dict((v, k) for k, v in XK_TO_AK_MAP.items())


class KeyHandler():

    def __init__(self, display):
        self.display = display
        self.rootWindow = self.display.screen().root
        self.modMasks = self.get_mod_masks()

    def get_mod_masks(self):
        modMasks = {}
        mapping = self.display.get_modifier_mapping()
        for keySym, ak in XK_TO_AK_MAP.items():
            if ak in MODIFIERS:
                keyCodeList = self.display.keysym_to_keycodes(keySym)
                found = False

                for keyCode, lvl in keyCodeList:
                    for index, mask in MASK_INDEXES:
                        if keyCode in mapping[index]:
                            modMasks[ak] = mask
                            found = True
                            break
                    if found:
                        break
        return modMasks

    def lookupKeyCode(self, char):
        if char in AK_TO_XK_MAP:
            return self.display.keysym_to_keycode(AK_TO_XK_MAP[char])
        elif char.startswith("<code"):
            return int(char[5:-1])
        else:
            try:
                return self.display.keysym_to_keycode(ord(char))
            except Exception:
                print("Unknown key name: %s", char)
                raise

    def create_event(self, event_fn, key_code, window, modifiers=0):
        return event_fn(
            detail=key_code,
            time=X.CurrentTime,
            root=self.rootWindow,
            window=window,
            child=X.NONE,
            root_x=1,
            root_y=1,
            event_x=1,
            event_y=1,
            state=modifiers,
            same_screen=1)

    def press(self, key_code, window, modifiers):
        ev = self.create_event(event.KeyPress, key_code, window, modifiers)
        window.send_event(ev)

    def release(self, key_code, window, modifiers):
        ev = self.create_event(event.KeyRelease, key_code, window, modifiers)
        window.send_event(ev)

    def tap_key(self, key, window, modifiers):
        key_code = self.lookupKeyCode(key)
        self.press(key_code, window, modifiers)
        self.release(key_code, window, modifiers)
        # xtest.fake_input(window, X.KeyPress, key_code)
        # xtest.fake_input(window, X.KeyRelease, key_code)

    def cs_tap(self, key, window, shift):
        '''Send a key adding Control and maybe Shift.'''
        modifiers = self.modMasks[Key.CONTROL]
        if shift:
            modifiers |= self.modMasks[Key.SHIFT]
        # print(key, modifiers)
        self.tap_key(key, window, modifiers)

    def paste(self, window, shift=False):
        self.cs_tap('v', window, shift)

    def copy(self, window, shift=False):
        self.cs_tap('c', window, shift)
