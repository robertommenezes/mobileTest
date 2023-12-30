import time
from datetime import date

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

SLEEP_TIME = 1
options = AppiumOptions()
options.load_capabilities({
    "platformName": "Android",
    "appium:deviceName": "Android",
    "appium:appPackage": "com.google.android.calendar",
    "appium:automationName": "UiAutomator2",
    "appium:äppActivity": "android.intent.action.MAIN",
    "appium:noReset": True,
    "appium:ensureWebviewsHavePages": True,
    "appium:nativeWebScreenshot": True,
    "appium:newCommandTimeout": 3600,
    "appium:connectHardwareKeyboard": True
})

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)


class TestCalendar:

    def test_creat_event(self):
        event_name = "Réveillon"

        btn_add = driver.find_element(by=AppiumBy.ID, value="com.google.android.calendar:id/floating_action_button")
        btn_add.click()
        time.sleep(SLEEP_TIME)
        btn_event = driver.find_element(by=AppiumBy.ID, value="com.google.android.calendar:id/speed_dial_event_container")
        btn_event.click()
        time.sleep(SLEEP_TIME)
        event_title = driver.find_element(by=AppiumBy.ID, value="com.google.android.calendar:id/title")
        event_title.send_keys(event_name)
        all_day = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.Switch")
        all_day.click()
        time.sleep(SLEEP_TIME)
        btn_save = driver.find_element(by=AppiumBy.ID, value="com.google.android.calendar:id/save")
        btn_save.click()
        time.sleep(SLEEP_TIME)
        page = driver.find_element(by=AppiumBy.XPATH, value="//android.support.v7.widget.RecyclerView")
        event_list = page.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")
        event_found = False
        for i in event_list:
            event_found = event_name + ',' in i.get_attribute("content-desc")
            if event_found:
                break
        assert event_found, 'Não foi possível criar o evento ' + event_name

        driver.quit()

    def test_edit_event(self):
        old_event_name = "Réveillon"
        event_name = "Réveillon 2023"

        page = driver.find_element(by=AppiumBy.XPATH, value="//android.support.v7.widget.RecyclerView")
        event_list = page.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")

        for i in event_list:
            if old_event_name + ',' in i.get_attribute("content-desc"):
                i.click()
                time.sleep(SLEEP_TIME)
                break
        btn_edit = driver.find_element(by=AppiumBy.ID, value="com.google.android.calendar:id/header_action_bar_actions")
        btn_edit.click()
        time.sleep(SLEEP_TIME)
        event_title = driver.find_element(by=AppiumBy.ID, value="com.google.android.calendar:id/title")
        event_title.send_keys(event_name)
        time.sleep(SLEEP_TIME)
        btn_save = driver.find_element(by=AppiumBy.ID, value="com.google.android.calendar:id/save")
        btn_save.click()
        time.sleep(SLEEP_TIME)
        page = driver.find_element(by=AppiumBy.XPATH, value="//android.support.v7.widget.RecyclerView")
        event_list = page.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")
        event_found = False
        for i in event_list:
            event_found = event_name + ',' in i.get_attribute("content-desc")
            if event_found:
                break
        assert event_found, 'Não foi possível editar o evento ' + old_event_name

        driver.quit()

    def test_delete_event(self):
        event_name = "Réveillon 2023"
        page = driver.find_element(by=AppiumBy.XPATH, value="//android.support.v7.widget.RecyclerView")
        event_list = page.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")
        for i in event_list:
            if event_name + ',' in i.get_attribute("content-desc"):
                i.click()
                time.sleep(SLEEP_TIME)
                break
        btn_more = driver.find_element(by=AppiumBy.ID, value="com.google.android.calendar:id/info_action_overflow")
        btn_more.click()
        time.sleep(SLEEP_TIME)
        delete_option = driver.find_element(by=AppiumBy.XPATH, value='(//android.widget.LinearLayout[@resource-id="com.google.android.calendar:id/content"])[1]')
        delete_option.click()
        time.sleep(SLEEP_TIME)
        confirm_delete = driver.find_element(by=AppiumBy.ID, value="android:id/button1")
        confirm_delete.click()
        time.sleep(SLEEP_TIME)
        page = driver.find_element(by=AppiumBy.XPATH, value="//android.support.v7.widget.RecyclerView")
        event_list = page.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")
        event_found = False
        for i in event_list:
            event_found = event_name + ',' in i.get_attribute("content-desc")
            if event_found:
                break
        assert not event_found, 'Não foi possível deletar o evento ' + event_name

        driver.quit()

    def test_today_button(self):
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(536, 1461)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(549, 621)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(570, 1653)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(672, 383)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        el1 = driver.find_element(by=AppiumBy.ID, value="com.google.android.calendar:id/action_today")
        el1.click()
        time.sleep(SLEEP_TIME)
        current_full_day = driver.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")
        current_day = current_full_day[1]
        day = int(current_day.get_attribute("content-desc").split(' ')[1])
        today = date.today()
        assert today.day == day, "Não foi possível retornar ao dia atual"
