from datetime import datetime
from frida_android_helper.utils import *
from frida_android_helper.frida_utils import *


def take_screenshot(filename=None):
    eprint("⚡️ Taking a screenshot...")
    for device in get_devices():
        signature = get_device_model(device).replace(" ", "")
        if filename is None:
            filename = "{}_{}.png".format(signature, datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))
        else:
            filename = "{}_{}.png".format(signature, filename)

        try:
            pid, app, activity = get_current_app_focus(device)
            eprint("🔥 Trying to disable SECURE flag for {}.{}...".format(app, activity))
            disable_secure_flag(device, pid, activity)
            result = device.screencap()
            with open(filename, "wb") as f:
                f.write(result)
            eprint("🔥 Screenshot saved {}".format(filename))
        except:
            eprint("❌️ Failed...")
            raise
