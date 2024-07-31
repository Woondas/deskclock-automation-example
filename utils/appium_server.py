from appium.webdriver.appium_service import AppiumService
import time
import requests

def is_appium_server_running():
    try:
        response = requests.get("http://localhost:4723/status")
        if response.status_code == 200:
            data = response.json()
            if 'value' in data and data['value']['ready'] == True:
                return True
    except requests.ConnectionError:
        return False
    return False

def start_appium_server():
    appium_service = AppiumService()

    if not is_appium_server_running():
        print("Starting Appium server...")
        appium_service.start(args=['--address', '127.0.0.1', '--port', '4723'])
        
        max_wait_time = 30
        wait_time = 0
        while not is_appium_server_running() and wait_time < max_wait_time:
            print("Waiting for Appium server to start...")
            time.sleep(1)
            wait_time += 1
        
        if is_appium_server_running():
            print("Appium server is running.")
        else:
            print("Failed to start Appium server.")
    else:
        print("Appium server is already running.")

    return appium_service

if __name__ == "__main__":
    service = start_appium_server()
