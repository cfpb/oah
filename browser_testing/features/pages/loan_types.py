
from selenium.common.exceptions import NoSuchElementException
from pages.base import *
from selenium import webdriver

class LoanTypes(Base):      

    def __init__(self, logger, base_url=r'http://localhost/', driver=None, driver_wait=-1, delay_secs=0):
        super(LoanTypes, self).__init__(logger, base_url, driver, driver_wait, delay_secs)
