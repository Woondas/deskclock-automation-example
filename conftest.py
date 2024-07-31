import pytest
import subprocess
from utils.driver_setup import DriverSetup
from utils.appium_server import start_appium_server

@pytest.fixture(scope="session", autouse=True)
def appium_service():
    service = start_appium_server()
    yield service
    service.stop()

@pytest.fixture(scope="class")
def driver(request, appium_service):
    driver = DriverSetup().get_driver()
    request.cls.driver = driver
    yield driver
    driver.quit()
