from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests
import json
from datetime import datetime
from time import sleep
import sys, os
import wget
import zipfile
import shutil

def loadBrowser():
    print("""
What browser do you want to use?

""")
    drivers = ['Firefox','Chrome','Edge','Internet_Explorer']

    driversInt = []
    for i, driver in enumerate(drivers):
        if os.path.exists(f'./drivers/{driver.lower()}driver.exe'):
            print(f'{i + 1}) {driver}')
            driversInt.append(str(i + 1))

    if len(driversInt) <= 4:
        driversInt.append('5')
        print('5) Install different driver')
    
    output = input('>> ')
    if output in driversInt:
        PROXY = "socks5://localhost:9050"

        def startDriver(browserName):
            PROXY = 'socks5://127.0.0.1:9050'
            PROXIES = {
                'http': PROXY,
                'https': PROXY
            }

            
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_capabilities['marionette'] = True

            firefox_capabilities['proxy'] = {
                "proxyType": "MANUAL",
                "httpProxy": PROXY,
                "ftpProxy": PROXY,
                "sslProxy": PROXY
            }

            works = False
            try:
                response = requests.get("http://ip-api.com/json/", proxies=PROXIES)
                result = json.loads(response.content)

                print(f'TOR IP [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]: {result["query"]} | {result["country"]} {result["regionName"]} ({result["lat"]}, {result["lon"]}) | Zip: {result["zip"]} | ISP: {result["isp"]}')
                works = True
            except:
                torexe = os.popen(r'.\tor\tor.exe')

            if not works:
                sleep(10)
                response = requests.get("http://ip-api.com/json/", proxies=PROXIES)
                result = json.loads(response.content)

                print(f'TOR IP [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]: {result["query"]} | {result["country"]} {result["regionName"]} ({result["lat"]}, {result["lon"]}) | Zip: {result["zip"]} | ISP: {result["isp"]}')
                works = True

            if works:
                options = eval(f"webdriver.{browserName}Options()")
                if browserName == 'Firefox':
                    driver = webdriver.Firefox(capabilities=firefox_capabilities)
                else:
                    options.add_argument('--proxy-server=%s' % PROXY)
                if browserName == 'Chrome':
                    options.add_experimental_option('excludeSwitches', ['enable-logging'])
                driver = eval(f"webdriver.{browserName}(options=options, service=Service('./drivers/{browserName}driver.exe'))")
                driver.get("http://check.torproject.org")
                input()
                return driver
            else:
                sys.exit()

        if output == '1':
            startDriver('Firefox')
        elif output == '2':
            startDriver('Chrome')
        elif output == '3':
            startDriver('Edge')
        elif output == '4':
            startDriver('Ie')
        elif output == '5':
            os.system('cls')
            print("""
browser do you want to use?

            """)
            for i, driver in enumerate(drivers):
                if not os.path.exists(f'./drivers/{driver}driver.exe'):
                    print(f'{i + 1}) {driver}')
            option = input(">> ")
            if option == "1":
                downloadDriver('https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-win64.zip', 'firefox')
                print("Done!")
            elif option == "2":
                downloadDriver('https://chromedriver.storage.googleapis.com/103.0.5060.134/chromedriver_win32.zip', 'chrome')
                print("Done!")
            elif option == "3":
                downloadDriver('https://msedgedriver.azureedge.net/103.0.1264.71/edgedriver_win64.zip', 'edge')
                print("Done!")
            elif option == "4":
                downloadDriver('https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.3.0/IEDriverServer_Win32_4.3.0.zip', 'ie')
                print("Done!")

    else:
        print("You do not have those drivers installed")
        input()
        sys.exit()

def downloadDriver(url, browerName):
    tmp = './tmp'
    tmpzip = tmp + '/zipfiles'
    wget.download(url, f'{tmp}/{browerName}.zip')
    print('\n')
    with zipfile.ZipFile(f'{tmp}/{browerName}.zip', 'r') as zip_ref:
        zip_ref.extractall(tmpzip)
    for file in os.listdir(tmpzip):
        print(file)
        if file.endswith('.exe'):
            print(file)
            os.replace(f'{tmpzip}/{file}', f'./drivers/{browerName}driver.exe')
            shutil.rmtree(tmp)

def start():
    os.system('cls')
    newpaths = ['tmp','tmp/zipfiles','drivers']
    for newpath in newpaths:
        newpath = './' + newpath
        if not os.path.exists(newpath):
            os.makedirs(newpath)

    if not os.path.isdir('./tor'):
        tmp = './tmp'
        tmpzip = tmp + '/zipfiles'
        wget.download('https://github.com/ohyicong/Tor/archive/refs/heads/master.zip', f'{tmp}/torapi.zip')
        with zipfile.ZipFile(f'{tmp}/torapi.zip', 'r') as zip_ref:
            zip_ref.extractall(tmpzip)
        shutil.move(f'{tmpzip}/Tor-master/tor', './')
        shutil.rmtree(tmp)
        start()

    if not os.listdir('./drivers'):
        print("""
What browser do you want to use?
It has to already be downloaded. But we will download the drivers.
1) Firefox (Recommended)
2) Chrome
3) Edge
4) Internet Explorer
""")
        option = input(">> ")
        if option == "1":
            downloadDriver('https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-win64.zip', 'firefox')
            print("Done!")
            loadBrowser()
        elif option == "2":
            downloadDriver('https://chromedriver.storage.googleapis.com/103.0.5060.134/chromedriver_win32.zip', 'chrome')
            print("Done!")
            loadBrowser()
        elif option == "3":
            downloadDriver('https://msedgedriver.azureedge.net/103.0.1264.71/edgedriver_win64.zip', 'edge')
            print("Done!")
            loadBrowser()
        elif option == "4":
            downloadDriver('https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.3.0/IEDriverServer_Win32_4.3.0.zip', 'ie')
            print("Done!")
            loadBrowser()
        

    else:
        loadBrowser()

start()