import pytest
from pages.alarm_page import AlarmPage
from common.switch_page import switch_to_alarm

@pytest.mark.usefixtures("driver")
class TestAddAlarm:
    def test_add_alarm_with_random_time(self):
        switch_to_alarm(self.driver)
        alarm_page = AlarmPage(self.driver)
        alarm_page.add_alarm()
        alarm_page.select_random_clock_format()
        alarm_page.pick_random_hour()
        alarm_page.pick_random_minute()
        alarm_page.confirm_alarm()
        alarm_page.verify_alarm()
        alarm_page.verify_snackbar_message()

    def test_add_alarm_with_specific_times(self):
        switch_to_alarm(self.driver)
        alarm_page = AlarmPage(self.driver)
        alarm_page.load_config('config/alarm.yaml')

        for alarm in alarm_page.config['alarms']:
            am_pm = alarm['am_pm']
            hour = alarm['hour']
            minute = alarm['minute']

            alarm_page.add_alarm()
            alarm_page.set_specific_time(am_pm, hour, minute)
            alarm_page.confirm_alarm()
            alarm_page.verify_alarm()
            alarm_page.verify_snackbar_message()

@pytest.mark.usefixtures("driver")
class TestDeleteAlarms:
    def test_delete_all_alarms(self):
        switch_to_alarm(self.driver)
        alarm_page = AlarmPage(self.driver)
        alarm_page.delete_all_alarms()
        alarm_page.verify_all_alarms_deleted()