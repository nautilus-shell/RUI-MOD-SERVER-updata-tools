import tkinter as tk
import paramiko
import datetime
import threading
import shutil
import json
import sys
import os


version = "β1.0"
title = (f"RUI-MOD-server update-tool  Ver.{version}")

normalpath = "C:/Minecraft/mod 1.12.2"
remote = "./Free-SFTP2/test/test"
local = "./tmp"



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
        self.bt["command"] = tools.test
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
    def test():
        tools.replace()

    def start():
        section = "START"
        main.callback(section, "start")
        try:
            tools.cheak()
            tools.load_setting()
            thread1 = threading.Thread(target=file_download)
            thread1.start()
        except Exception as error:
            return False

    def cheak():
        section = "CHEAK"
        try:
            main.callback(section, "cheak config")
            os.path.isfile("./config.json")
            main.callback(section, "cheak success")
        except Exception as error:
            main.callback(section,error)
            return False

    def load_setting():
        section = "CONFIG"
        try:
            main.callback(section, "load config")
            with open("config.json", "r", encoding="utf-8_sig") as f:
                tools.config = json.load(f)
            main.callback(section, "load success")
        except Exception as error:
            main.callback(section, error)
            return False
    
    def replace():
        section = "REPLACE"
        try:
            main.callback(section, "cheak mods folder")
            if os.path.isdir(f"{normalpath}/mods"):
                shutil.rmtree(f"{normalpath}/mods")
                main.callback(section, "success remove of mods folder")
                main.callback(section, "copy mods folder")
                shutil.copytree(f"{local}/pack/mods",f"{normalpath}/mods")
                main.callback(section, "success copy for mods folder")
            else:
                main.callback(section, "no mods folder")
                main.callback(section, "copy mods folder")
                shutil.copytree(f"{local}/pack/mods",f"{normalpath}/mods")
                main.callback(section, "success copy for mods folder")
            main.callback(section, "load setting")
            with open(f"{local}/pack/other/setting.json", "r", encoding="utf-8_sig") as f:
                tmp = json.load(f)
            main.callback(section, "load success")
            for file,path in tmp.items():
                main.callback(section, f"cheak {file}")
                if os.path.isdir(f"{normalpath}/{path}"):
                    main.callback(section, f"replace {file}")
                    shutil.copy(f"{local}/pack/other/{file}",f"{normalpath}/{path}/{file}")
                    main.callback(section, f"succes replace for {file}")
                else:
                    main.callback(section, f"no {path}")
                    main.callback(section, f"make {path}")
                    os.mkdir(f"{normalpath}/{path}")
                    main.callback(section, f"succes make for {path}")
                    main.callback(section, f"replace {file}")
                    shutil.copy(f"{local}/pack/other/{file}",f"{normalpath}/{path}/{file}")
                    main.callback(section, f"succes replace for {file}")
        except Exception as error:
            main.callback(section, error)
            return False


def file_download():
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
        thread2 = threading.Thread(target=file_expansion)
        thread2.start()
        return True
    except Exception as error:
        main.callback(section, error)
        return False

def file_expansion():
    section = "EXPANSION"
    try:
        main.callback(section, "zip expansion")
        shutil.unpack_archive("latest",local)
        main.callback(section, "expansion success")
    except Exception as error:
        main.callback(section, error)
        return False



if __name__ == '__main__':
    main = window(tk.Tk())
    main.mainloop()
