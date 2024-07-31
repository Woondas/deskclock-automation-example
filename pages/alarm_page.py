import random
import yaml
from datetime import datetime, timedelta
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AlarmPage:
    ID_PREFIX = "com.google.android.deskclock:id"

    ADD_ALARM_BUTTON = f"{ID_PREFIX}/fab"
    HOUR_PICKER = f"{ID_PREFIX}/material_hour_tv"
    MINUTE_PICKER = f"{ID_PREFIX}/material_minute_tv"
    AM_BUTTON = f"{ID_PREFIX}/material_clock_period_am_button"
    PM_BUTTON = f"{ID_PREFIX}/material_clock_period_pm_button"
    HEADER_TITLE = f"{ID_PREFIX}/header_title"
    CONFIRM_BUTTON = f"{ID_PREFIX}/material_timepicker_ok_button"
    DIGITAL_CLOCK = f"{ID_PREFIX}/digital_clock"
    SNACKBAR_TEXT = f"{ID_PREFIX}/snackbar_text"
    ARROW_BUTTON = f"{ID_PREFIX}/arrow"
    DELETE_BUTTON = f"{ID_PREFIX}/delete"
    CARD_VIEW = "androidx.cardview.widget.CardView"
    NO_ALARMS_TEXT = f"{ID_PREFIX}/alarm_empty_view"
    TIMEPICKER_BUTTON  = f"{ID_PREFIX}/material_timepicker_mode_button"

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def load_config(self, filepath):
        with open(filepath, 'r') as file:
            self.config = yaml.safe_load(file)

    def add_alarm(self):
        self.driver.find_element(AppiumBy.ID, self.ADD_ALARM_BUTTON).click()
        self.verify_header_title

    def pick_random_hour(self):
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, self.HOUR_PICKER))).click()
        self.random_hour = random.randint(1, 12)
        hour_button_xpath = f'//android.widget.TextView[@content-desc="{self.random_hour} o\'clock"]'
        
        # Create a tuple representing the hour button element
        hour_button = (AppiumBy.XPATH, hour_button_xpath)
        self.wait.until(EC.element_to_be_clickable(hour_button)).click()

    def pick_random_minute(self):
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, self.MINUTE_PICKER))).click()
        
        # Get all TextView elements within material_clock_face
        clock_face = self.wait.until(EC.presence_of_element_located((AppiumBy.ID, f"{self.ID_PREFIX}/material_clock_face")))
        minute_elements = clock_face.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")
        
        # Extract all available minutes from content-desc
        available_minutes = [el.get_attribute("content-desc") for el in minute_elements if 'minutes' in el.get_attribute("content-desc")]
        print(f"Available minutes: {available_minutes}")  

        # Select a random minute
        random_minute_desc = random.choice(available_minutes)
        self.random_minute = int(random_minute_desc.split()[0])
        print(f"Selected random minute: {random_minute_desc}") 
        
        # Use the full text instead of converting to int and back
        minute_button_xpath = f'//android.widget.TextView[@content-desc="{random_minute_desc}"]'
        print(f"Generated XPath for minute: {minute_button_xpath}") 
        
        minute_button = (AppiumBy.XPATH, minute_button_xpath)
        self.wait.until(EC.element_to_be_clickable(minute_button)).click()

    def select_random_clock_format(self):
        if random.choice([True, False]):
            self.am_pm = "AM"
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, self.AM_BUTTON))).click()
        else:
            self.am_pm = "PM"
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, self.PM_BUTTON))).click()

    def verify_header_title(self):
        header = self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, self.HEADER_TITLE)))
        assert "Select time" in header.text, "Header does not contain 'Select time'"

    def confirm_alarm(self):
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, self.CONFIRM_BUTTON))).click()

    def verify_alarm(self):
        # Remove leading zero for single digit hour
        expected_hour = self.random_hour if self.random_hour >= 10 else f"{self.random_hour}"
        expected_all_time = f"{expected_hour}:{self.random_minute:02d} {self.am_pm}"
        expected_time = f"{expected_hour}:{self.random_minute:02d}"
        print(f"Expected time: {expected_time}")  

        # Construct XPath to find the digital clock element with the correct time using contains
        digital_clock_xpath = (f"//android.widget.ImageButton[@resource-id='{self.ARROW_BUTTON}' and contains(@content-desc, 'Collapse')]"
                           f"/following-sibling::android.widget.TextView[@resource-id='{self.DIGITAL_CLOCK}' and contains(@text, '{expected_time}')]")

        # Wait for the element to be visible
        digital_clock = self.wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, digital_clock_xpath)))
        
        # Normalize spaces to handle special characters
        normalized_expected_time = " ".join(expected_all_time.split())
        normalized_actual_time = " ".join(digital_clock.text.split())

        assert normalized_expected_time in normalized_actual_time, f"Alarm time mismatch: expected {normalized_expected_time}, found {normalized_actual_time}"
    
    def verify_snackbar_message(self):
        # Current time
        now = datetime.now()

        # Convert random_hour to 24-hour format
        alarm_hour = self.random_hour
        if self.am_pm == "PM" and self.random_hour != 12:
            alarm_hour += 12
        elif self.am_pm == "AM" and self.random_hour == 12:
            alarm_hour = 0

        # Create datetime object for alarm time
        alarm_time = now.replace(hour=alarm_hour, minute=self.random_minute, second=0, microsecond=0)

        # If alarm time is earlier than now, it means the alarm is set for the next day
        if alarm_time < now:
            alarm_time += timedelta(days=1)

        # Calculate difference in minutes
        delta_minutes = int((alarm_time - now).total_seconds() / 60)
        expected_message_minutes = f"Alarm set for {delta_minutes} minutes from now."

        # Calculate difference in hours and minutes
        delta_hours = delta_minutes // 60
        delta_remaining_minutes = delta_minutes % 60

        # Handle singular and plural forms for hours and minutes
        hour_text = "hour" if delta_hours == 1 else "hours"
        minute_text = "minute" if delta_remaining_minutes == 1 else "minutes"
        expected_message_hours_minutes = f"Alarm set for {delta_hours} {hour_text} and {delta_remaining_minutes} {minute_text} from now."

        print(f"Expected snackbar message (minutes): {expected_message_minutes}")  
        print(f"Expected snackbar message (hours and minutes): {expected_message_hours_minutes}")  

        snackbar_text = self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, self.SNACKBAR_TEXT)))
        snackbar_message = snackbar_text.text

        # Generate tolerances
        tolerances = range(-2, 3)
        acceptable_messages = [
            expected_message_minutes,
            *[
                f"Alarm set for {delta_hours + (delta_remaining_minutes + tolerance) // 60} {hour_text} and {(delta_remaining_minutes + tolerance) % 60} {minute_text} from now." for tolerance in tolerances
            ]
        ]

        assert any(msg in snackbar_message for msg in acceptable_messages), \
            f"Snackbar message mismatch: expected one of '{acceptable_messages}', found '{snackbar_message}'"

        
    def delete_all_alarms(self):
        card_views = self.driver.find_elements(AppiumBy.XPATH, f"//{self.CARD_VIEW}")
        for card_view in card_views:
            arrow_button = card_view.find_element(AppiumBy.ID, self.ARROW_BUTTON)
            self.wait.until(EC.element_to_be_clickable(arrow_button)).click()
            delete_button = self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, self.DELETE_BUTTON)))
            delete_button.click()
            self.verify_snackbar_message_deletion()

    def verify_snackbar_message_deletion(self):
        expected_message = "Alarm deleted"
        snackbar = self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, self.SNACKBAR_TEXT)))
        assert expected_message in snackbar.text, f"Snackbar message mismatch: expected '{expected_message}', found '{snackbar.text}'"

    def get_all_alarms(self):
        return self.driver.find_elements(AppiumBy.XPATH, f"//{self.CARD_VIEW}")

    def verify_all_alarms_deleted(self):
        remaining_alarms = self.get_all_alarms()
        assert len(remaining_alarms) == 0, "Alarms were not deleted"
        no_alarms_message = self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, self.NO_ALARMS_TEXT)))
        assert "No Alarms" in no_alarms_message.text, "No Alarms message not displayed"

    def set_specific_time(self, am_pm, hour, minute):

        # Check if the button has the content-desc
        try:
            button = self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, self.TIMEPICKER_BUTTON)))
            content_desc = button.get_attribute("content-desc")
            if content_desc != "Switch to clock mode for the time input.":
                self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, self.TIMEPICKER_BUTTON))).click()
        except:
            pass  

        hour_edit_text = self.wait.until(EC.visibility_of_element_located(
        (AppiumBy.XPATH, "//android.widget.FrameLayout[@resource-id='com.google.android.deskclock:id/material_hour_text_input']//android.widget.EditText")))
        hour_edit_text.click()
        hour_edit_text.clear()
        hour_edit_text.send_keys(f"{hour:02d}")

        self.wait.until(EC.element_to_be_clickable
        ((AppiumBy.XPATH, "//android.widget.FrameLayout[@resource-id='com.google.android.deskclock:id/material_minute_text_input']//android.view.View"))).click()
        minute_edit_text = self.wait.until(EC.visibility_of_element_located(
        (AppiumBy.XPATH, "//android.widget.FrameLayout[@resource-id='com.google.android.deskclock:id/material_minute_text_input']//android.widget.EditText")))
        minute_edit_text.click()
        minute_edit_text.clear()
        minute_edit_text.send_keys(f"{minute:02d}")

        # Select AM or PM
        if am_pm == "AM":
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, self.AM_BUTTON))).click()
        else:
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, self.PM_BUTTON))).click()

        self.am_pm = am_pm
        self.random_hour = hour
        self.random_minute = minute