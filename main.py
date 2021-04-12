from CalendarZoomUpdator.mail_handling import Mail_Finder
from CalendarZoomUpdator.calendar_handling import Calendar_Updator
from CalendarZoomUpdator.string_handling import String_Handler

'''
Download chromeriver.exe from: https://chromedriver.chromium.org/downloads
I used chromedriver_win32
Insert the path including \chromedriver.exe
'''

path = ""
login = "" # the student number
password = ""

if __name__ == "__main__":
    mail_finder = Mail_Finder(path, login, password)
    mails = mail_finder.read_mails(30)
    string_handler = String_Handler()
    data = string_handler.get_dates(mails)
    cal = Calendar_Updator()
    cal.edit_events(data)
