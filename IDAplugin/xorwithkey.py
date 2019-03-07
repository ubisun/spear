import idaapi

def slog(msg):
    idaapi.msg("[Spear] " + msg + "\n")

class XorWithKeyForm(Form):
    def __init__(self, start_ea):
        Form.__init__(self,
r"""BUTTON YES* XOR
XOR with Key

<##Start EA         :{intStartEA}>
<Target code length :{intLength}>
<Key                :{rString}>
""", {
        'intStartEA': Form.NumericInput(swidth=40,tp=Form.FT_ADDR,value=start_ea),
        'intLength': Form.NumericInput(swidth=40),
        'rString': Form.StringInput(swidth=40),
        })
        self.Compile()

def show_xor_with_key_form():
    selection, start_ea, end_ea = idaapi.read_selection()

    if not selection:
        start_ea = idaapi.get_screen_ea()

    # Create the form
    f = XorWithKeyForm(start_ea);

    # Execute the form
    ok = f.Execute()
    if ok == 1:
        start_ea = f.intStartEA.value
        target_length = f.intLength.value
        key = f.rString.value

        if target_length < 0 :
            slog("target lenth is wrong " + str(target_length))
            return

        if idaapi.IDA_SDK_VERSION >= 700 :
            buf = ida_bytes.get_bytes(start_ea, target_length)
        else:
            buf = ida_bytes.get_many_bytes(start_ea, target_length)

        if buf is None :
            slog("Failed to get bytes")
            return

        lbuf = list(buf)
        lkey = list(key)
        for i in range(target_length) :
            lbuf[i] = chr(ord(lbuf[i]) ^ ord(lkey[i % len(lkey)]))

        # Now apply newly patched bytes
        buf = "".join(lbuf)
        idaapi.patch_many_bytes(start_ea, buf)

    # Dispose the form
    f.Free()

class XorWithKey(idaapi.action_handler_t):
    def __init__(self):
        idaapi.action_handler_t.__init__(self)

    def activate(self, ctx):
        slog("XorWithKey activate()")
        show_xor_with_key_form()
        return 1

    def update(self, ctx):
        slog("XorWithKey update()")
        return idaapi.AST_ENABLE_ALWAYS


spear_actions = [
    {
        "action_name" : "sa:XorWithKey",
        "label" : "XorWithKey",
        "handler" : XorWithKey(),
        "short_cut" : "Ctrl+5",
        "tooltip" : "XorWithKey_tooltip",
        "icon" : 199,
        "menu_path" : "Edit/Export data"
    },
]

def register_actions():
    for i in range(len(spear_actions)):
        if idaapi.register_action(idaapi.action_desc_t(
                spear_actions[i]['action_name'],
                spear_actions[i]['label'],
                spear_actions[i]['handler'],
                spear_actions[i]['short_cut'],
                spear_actions[i]['tooltip'],
                spear_actions[i]['icon'])) :
            slog(spear_actions[i]['action_name'] + " is registered.")
        else:
            slog("Failed to register, " + spear_actions[i]['action_name'])

def unregister_actions():
    for i in range(len(spear_actions)):
        if idaapi.unregister_action(spear_actions[i]['action_name']) :
            slog(spear_actions[i]['action_name'] + " is unregistered.")

def attach_menus():
    for i in range(len(spear_actions)):
        if idaapi.attach_action_to_menu(spear_actions[i]['menu_path'],
                                        spear_actions[i]['action_name'],
                                        idaapi.SETMENU_APP) :
            slog("Menu is attached, " + spear_actions[i]['action_name'])
        else:
            slog("Failed to attach menu, " + spear_actions[i]['action_name'])


class spearPlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_UNL
    comment = "This is a comment"
    help = "This is help"
    wanted_name = "Spear plugin"
    wanted_hotkey = "Ctrl-4"

    def init(self):
        slog("init() called!")
        unregister_actions()
        register_actions()
        attach_menus()
        return idaapi.PLUGIN_OK

    def run(self, arg):
        slog("run() called!")

    def term(self):
        slog("term() called!")

def PLUGIN_ENTRY():
    return spearPlugin()

if __name__ == "__main__" :
    pass
