import pkg_resources
import frida

from frida_android_helper.utils import eprint

def destroyed_callback(reason):
    print("🔰 Destroyed! Reason: {}".format(reason))


def message_callback(message, data):
    if message["type"] == "send":
        print("🔥 {}".format(message["payload"]))
    else:
        print("🐛 ".format(message))


def get_js_hook(js_filename):
    return pkg_resources.resource_string("frida_android_helper", "frida_hooks/{}".format(js_filename)).decode("utf-8")


def load_script_with_device(device, pid, js_file):
    js_code = get_js_hook(js_file)
    device = frida.get_device(device.get_serial_no())
    procs = device.enumerate_processes([int(pid)])
    session = device.attach(procs[0].name)
    script = session.create_script(js_code)
    script.on("message", message_callback)
    script.load()
    return script


def disable_secure_flag(device, pid, app, activity_name):
    eprint('📦 PID: {} APP: {}'.format(pid, app))
    script = load_script_with_device(device, pid, "disable_secure_flag.js")
    script.exports.disablesecureflag(activity_name)


def copy_from_clipboard(device, pid, app):
    eprint('📦 PID: {} APP: {}'.format(pid, app))
    script = load_script_with_device(device, pid, "clipboard.js")
    script.exports.copyfromclipboard()


def paste_to_clipboard(device, pid, app, data):
    print("data: '{}'".format(data))
    eprint('📦 PID: {} APP: {}'.format(pid, app))
    
    script = load_script_with_device(device, pid, "clipboard.js")
    script.exports.pastetoclipboard(data)
