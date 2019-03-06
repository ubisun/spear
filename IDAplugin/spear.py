import idaapi
import binascii

def slog(msg):
    idaapi.msg("[Spear] " + msg + "\n")

class DataImportForm(Form):
    def __init__(self, start_ea, end_ea):
        Form.__init__(self,
r"""BUTTON YES* Import
Import data

{FormChangeCb}
<##Start EA   :{intStartEA}>
<##End EA     :{intEndEA}>

Import type:                    Patching options:
<hex string:{rHex}><##Trim to selection:{cSize}>{cGroup}>
<string literal:{rString}>
<binary file:{rFile}>{rGroup}>

<:{strPatch}>
<##Import BIN file:{impFile}>
""", {
        'intStartEA': Form.NumericInput(swidth=40,tp=Form.FT_ADDR,value=start_ea),
        'intEndEA': Form.NumericInput(swidth=40,tp=Form.FT_ADDR,value=end_ea),

        'cGroup': Form.ChkGroupControl(("cSize",)),
        'rGroup': Form.RadGroupControl(("rHex", "rString", "rFile")),

        'strPatch': Form.MultiLineTextControl(swidth=80, flags=Form.MultiLineTextControl.TXTF_FIXEDFONT),
        'impFile': Form.FileInput(swidth=50, open=True),

        'FormChangeCb': Form.FormChangeCb(self.OnFormChange),
        })

        self.Compile()

    def OnFormChange(self, fid):
        # Form initialization
        if fid == -1:
            self.SetFocusedField(self.strPatch)
            self.EnableField(self.strPatch, True)
            self.EnableField(self.impFile, False)

        # Form OK pressed
        elif fid == -2:
            pass

        # Form from text box
        elif fid == self.rHex.id or fid == self.rString.id:
            self.SetFocusedField(self.strPatch)
            self.EnableField(self.strPatch, True)
            self.EnableField(self.impFile, False)

        # Form import from file
        elif fid == self.rFile.id:
            self.SetFocusedField(self.rFile)
            self.EnableField(self.impFile, True)
            self.EnableField(self.strPatch, False)

        return 1


def show_import_form():
    selection, start_ea, end_ea = idaapi.read_selection()

    if not selection:
        start_ea = idaapi.get_screen_ea()
        end_ea = start_ea + 1

    # Create the form
    f = DataImportForm(start_ea, end_ea);

    # Execute the form
    ok = f.Execute()
    if ok == 1:

        start_ea = f.intStartEA.value
        end_ea = f.intEndEA.value

        if f.rFile.selected:
            imp_file = f.impFile.value

            try:
                f_imp_file = open(imp_file, 'rb')
            except Exception, e:
                idaapi.warning("File I/O error({0}): {1}".format(e.errno, e.strerror))
                return
            else:
                buf = f_imp_file.read()
                f_imp_file.close()

        else:

            buf = f.strPatch.value

            # Hex values, unlike string literal, needs additional processing
            if f.rHex.selected:
                buf = buf.replace(' ', '')  # remove spaces
                buf = buf.replace('\\x', '')  # remove '\x' prefixes
                buf = buf.replace('0x', '')  # remove '0x' prefixes
                try:
                    buf = binascii.unhexlify(buf)  # convert to bytes
                except Exception, e:
                    idaapi.warning("Invalid input: %s" % e)
                    f.Free()
                    return

        if not len(buf):
            idaapi.warning("There was nothing to import.")
            return

        # Trim to selection if needed:
        if f.cSize.checked:
            buf_size = end_ea - start_ea
            buf = buf[0:buf_size]

        # Now apply newly patched bytes
        idaapi.patch_many_bytes(start_ea, buf)

    # Dispose the form
    f.Free()

class ImportData(idaapi.action_handler_t):
    def __init__(self):
        idaapi.action_handler_t.__init__(self)

    def activate(self, ctx):
        slog("ImportData activate()")
        show_import_form()
        return 1

    def update(self, ctx):
        slog("ImportData update()")
        return idaapi.AST_ENABLE_ALWAYS


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
    {
        "action_name": "sa:ImportData",
        "label": "ImportData",
        "handler": ImportData(),
        "short_cut": "Ctrl+6",
        "tooltip": "ImportData_tooltip",
        "icon": 200,
        "menu_path": "Edit/Export data"
    }
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
