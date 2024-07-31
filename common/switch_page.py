from appium.webdriver.common.appiumby import AppiumBy

ID_PREFIX = "com.google.android.deskclock:id/"

TAB_MENU_ALARM = f"{ID_PREFIX}tab_menu_alarm"
TAB_MENU_CLOCK = f"{ID_PREFIX}tab_menu_clock"
TAB_MENU_TIMER = f"{ID_PREFIX}tab_menu_timer"
TAB_MENU_STOPWATCH = f"{ID_PREFIX}tab_menu_stopwatch"
TAB_MENU_BEDTIME = f"{ID_PREFIX}tab_menu_bedtime"
ACTIVE_INDICATOR = f"{ID_PREFIX}navigation_bar_item_active_indicator_view"

def switch_to_alarm(driver):
    frame_layout = driver.find_element(AppiumBy.ID, TAB_MENU_ALARM)
    frame_layout.click()
    assert driver.find_element(AppiumBy.ID, ACTIVE_INDICATOR), "Alarm view not displayed"
    assert frame_layout.get_attribute("selected") == "true", "Alarm view not selected"

def switch_to_clock(driver):
    frame_layout = driver.find_element(AppiumBy.ID, TAB_MENU_CLOCK)
    frame_layout.click()
    assert driver.find_element(AppiumBy.ID, ACTIVE_INDICATOR), "Clock view not displayed"
    assert frame_layout.get_attribute("selected") == "true", "Clock view not selected"

def switch_to_timer(driver):
    frame_layout = driver.find_element(AppiumBy.ID, TAB_MENU_TIMER)
    frame_layout.click()
    assert driver.find_element(AppiumBy.ID, ACTIVE_INDICATOR), "Timer view not displayed"
    assert frame_layout.get_attribute("selected") == "true", "Timer view not selected"

def switch_to_stopwatch(driver):
    frame_layout = driver.find_element(AppiumBy.ID, TAB_MENU_STOPWATCH)
    frame_layout.click()
    assert driver.find_element(AppiumBy.ID, ACTIVE_INDICATOR), "Stopwatch view not displayed"
    assert frame_layout.get_attribute("selected") == "true", "Stopwatch view not selected"

def switch_to_bedtime(driver):
    frame_layout = driver.find_element(AppiumBy.ID, TAB_MENU_BEDTIME)
    frame_layout.click()
    assert driver.find_element(AppiumBy.ID, ACTIVE_INDICATOR), "Bedtime view not displayed"
    assert frame_layout.get_attribute("selected") == "true", "Bedtime view not selected"
