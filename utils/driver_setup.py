import logging
from appium import webdriver
from appium.options.common import AppiumOptions
import yaml

class DriverSetup:
    def __init__(self):
        try:
            with open('config/config.yaml') as config_file:
                self.config = yaml.safe_load(config_file)['appium']
            
            # Set up logging based on the configuration
            if self.config.get('appium_server_logging', False):
                logging.basicConfig(level=logging.DEBUG)
            else:
                logging.basicConfig(level=logging.CRITICAL)  
            self.logger = logging.getLogger(__name__)
            self.logger.debug(f"Loaded configuration: {self.config}")
        except Exception as e:
            logging.basicConfig(level=logging.CRITICAL)
            logging.error("Error loading configuration:", exc_info=True)
            raise e

    def get_driver(self):
        desired_caps = {
            "platformName": self.config['platformName'],
            "appium:deviceName": self.config['deviceName'],
            "appium:appPackage": self.config['appPackage'],
            "appium:appActivity": self.config['appActivity'],
            "appium:automationName": self.config['automationName']
        }

        options = AppiumOptions().load_capabilities(desired_caps)
        self.logger.debug(f"Desired capabilities: {desired_caps}")

        try:
            driver = webdriver.Remote(command_executor=self.config['server'], options=options)
            self.logger.info("Driver initialized")
            return driver
        except Exception as e:
            self.logger.error("Error initializing driver:", exc_info=True)
            raise e
