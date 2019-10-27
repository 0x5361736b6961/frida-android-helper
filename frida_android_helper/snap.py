from datetime import datetime
from frida_android_helper.utils import *


def take_snapshot(packagename=None):
    print("⚡️ Taking a snapshot...")
    for device in get_devices():
        if packagename is None:  # get
            packagename, _ = get_current_app_focus(device)
            if packagename == "StatusBar":
                print("❌️ Unlock device or specify package name.")
                continue

        directory_name = "{}_{}".format(packagename, datetime.now().strftime("%Y.%m.%d_%H.%M.%S"))

        print("🔥 Copying from /data/data/{} to /sdcard/Download/{}...".format(packagename, directory_name))
        err = perform_cmd(device, "cp -Lpr /data/data/{} /sdcard/Download/{}".format(packagename, directory_name), root=True)
        if err:
            print("❌ {}".format(err))
            continue

        print("🔥 Downloading from /sdcard/Download/{}...".format(directory_name))
        # https://github.com/Swind/pure-python-adb/issues/28
        # device.pull("/sdcard/Download/{}/".format(packagename), directory_name)
        subprocess.run(["adb", "pull", "/sdcard/Download/{}".format(directory_name)])

        print("🔥 Cleaning up /sdcard/Download/{}...".format(directory_name))
        perform_cmd(device, "rm -rf /sdcard/Download/{}".format(directory_name))
