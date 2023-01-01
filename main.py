import tkinter as tk
import paramiko
import datetime
import threading
import json
import sys
import os


version = "β1.0"
title = (f"RUI-MOD-server update-tool  Ver.{version}")

remote = "./Free-SFTP2/test/test"
local = "./test"


RUI = """################################################################################
#      __          ________ _      _____ ____  __  __ ______ _ _               #
#      \ \        / /  ____| |    / ____/ __ \|  \/  |  ____| | |              #
#       \ \  /\  / /| |__  | |   | |   | |  | | \  / | |__  | | |              #
#        \ \/  \/ / |  __| | |   | |   | |  | | |\/| |  __| | | |              #
#         \  /\  /  | |____| |___| |___| |__| | |  | | |____|_|_|              #
#      ____\/ _\/  _|______|______\_____\____/|_|__|_|______(_|_)_ _____       #
#     |  __ \| |  | |_   _|    / ____|  ____|  __ \ \    / /  ____|  __ \      #
#     | |__) | |  | | | |_____| (___ | |__  | |__) \ \  / /| |__  | |__) |     #
#     |  _  /| |  | | | |______\___ \|  __| |  _  / \ \/ / |  __| |  _  /      #
#     | | \ \| |__| |_| |_     ____) | |____| | \ \  \  /  | |____| | \ \      #
#     |_|  \_\\____/|_____|   |_____/|______|_|  \_\  \/   |______|_|  \_\      #
#                                                                              #
################################################################################

"""


class window(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title(title)
        self.master.geometry("600x500")
        self.master.resizable(width=False, height=False)
        self.master.iconbitmap(default='icon.ico')
        self.set_widget()
        self.text.insert(tk.END, RUI)

    def set_widget(self):
        self.bt = tk.Button()
        self.bt["command"] = tools.start
        self.bt["text"] = "button"
        self.bt.place(x=0, y=0)
        self.pack()

        self.log = tk.Frame()
        self.log.pack(side=tk.BOTTOM)
        self.scroll = tk.Scrollbar(self.log)
        self.scroll.pack(side=tk.RIGHT, fill="y")
        self.text = tk.Text(
            self.log, foreground='#00FF21', background='#000000', width=80, height=20)
        self.text.pack()

    def callback(self, var1, var2):
        self.text.insert(
            tk.END, f"[{datetime.datetime.now()}] section({var1}) message({var2})\n")
        self.text.see("end")


class tools():
    config = {}

    def start():
        section = "START"
        main.callback(section, "start")
        tools.load_setting()
        thread = threading.Thread(target=sftp_download)
        thread.start()

    def load_setting():
        section = "CONFIG"
        try:
            os.path.isfile("./config.json")
            with open("config.json", "r", encoding="utf-8_sig") as f:
                tools.config = json.load(f)
            print(tools.config)
            main.callback(section, "success")
        except Exception as error:
            main.callback(section, error)
            return False


def sftp_download():
    section = "SFTP"
    try:
        transport = paramiko.Transport(
            (tools.config["HOST"], tools.config["PORT"]))
        main.callback(section, f"check key file")
        rsa_private_key = paramiko.RSAKey.from_private_key_file(
            tools.config["KEY"])
        main.callback(section, f"check success")
        main.callback(section, f"connect server")
        transport.connect(username=tools.config["USER"], pkey=rsa_private_key)
        sftp = paramiko.SFTPClient.from_transport(transport)
        main.callback(section, f"connect success")
        main.callback(section, f"Downloading file")
        sftp.get(remote, local)
        main.callback(section, f"Downloading success")
        main.callback(section, f"ending section")
        sftp.close()
        transport.close()
        return True
    except Exception as error:
        main.callback(section, error)
        return False


if __name__ == '__main__':
    main = window(tk.Tk())
    #sub = tools()
    main.mainloop()
