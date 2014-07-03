from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base import Base

# ELEMENT ID'S FOR TEXTBOXES
DOWN_PAYMENT_AMOUNT_TBOX = "down-payment"  # DOWN PAYMENT AMOUNT TEXTBOX
DOWN_PAYMENT_PERCENT_TBOX = "percent-down"  # DOWN PAYMENT PERCENTAGE TEXTBOX
HOUSE_PRICE_TBOX = "house-price"  # HOUSE PRICE TEXTBOX

# ELEMENT ID'S FOR DROP DOWN LISTS
ARM_TYPE_DDL = "arm-type"  # ARM TYPE DROPDOWN LIST
LOAN_TERM_DDL = "loan-term"  # LOAN TERM DROPDOWN LIST
LOAN_TYPE_DDL = "loan-type"  # LOAN TYPE DROPDOWN LIST
LOCATION_DDL = "location"  # LOCATION DROPDOWN LIST
RATE_STRUCTURE_DDL = "rate-structure"  # RATE STRUCTURE DROPDOWN LIST

# ELEMENT ID'S FOR LABELS
LOAN_AMOUNT_LABEL = "loan-amount-result"  # LOAN AMOUNT LABEL
# This label displays range as 700 - 720
SLIDER_RANGE_LABEL = "slider-range"

# XPATH LOCATORS
RATE_LOCATION = "//h2/*[@class ='location']"
SLIDER_HANDLE = "//div[contains(@class, 'rangeslider__handle')]"
SLIDER = "//div[@class = 'rangeslider']"
RANGE_ALERT = "//div[@class='result-alert credit-alert']/p"


class RateChecker(Base):

    def __init__(self, logger, directory, base_url=r'http://localhost/',
                 driver=None, driver_wait=-1, delay_secs=0):
        super(RateChecker, self).__init__(logger, directory, base_url,
                                          driver, driver_wait, delay_secs)
        self.logger = logger

    # ALERTS
    def get_warning_button(self):
        element = self.driver.find_element_by_xpath(SLIDER_HANDLE)
        return element.get_attribute("class")

    def get_range_alert(self):
        element = self.driver.find_element_by_xpath(RANGE_ALERT)
        return element.text

    # CHART AREA
    def get_chart_location(self):
        # This label is invisible on page load
        # We wait for the element to become visible before extracting the text
        WebDriverWait(self.driver, self.driver_wait)\
            .until(EC.visibility_of_element_located((By.XPATH, RATE_LOCATION)))

        element = self.driver.find_element_by_xpath(RATE_LOCATION)
        return element.text

    # CREDIT SCORE RANGE
    def get_credit_score_range(self):
        element = self.driver.find_element_by_id(SLIDER_RANGE_LABEL)
        # Return the entire text of the credit score range
        return element.text

    def set_credit_score_range(self, slider_direction):
        # Get the pixel width of the slider control
        slider_element = self.driver.find_element_by_xpath(SLIDER)
        slider_width = int(slider_element.get_attribute("scrollWidth"))

        element = self.driver.find_element_by_xpath(SLIDER_HANDLE)
        actions = ActionChains(self.driver)

        # Move the slider 1/4 of the total width to the right
        if(slider_direction == "right"):
            actions.drag_and_drop_by_offset(element, (slider_width/4), 0)
        # Move the slider 1/4 of the total width to the left
        elif(slider_direction == "left"):
            actions.drag_and_drop_by_offset(element, (slider_width/-4), 0)
        # Move the slider 1/2 of the total width to the left
        elif(slider_direction == "lowest"):
            actions.click_and_hold(element)
            actions.drag_and_drop_by_offset(element, (slider_width/-2), 0)
            self.logger.info("width: %s" % slider_width)

        actions.perform()

    # LOCATION
    def get_selected_location(self):
        # Wait for the Geolocator to display the location above the chart
        WebDriverWait(self.driver, self.driver_wait)\
            .until(EC.visibility_of_element_located((By.XPATH, RATE_LOCATION)))

        # Get the selected Index from the Location dropdown list
        element = Select(self.driver.find_element_by_id(LOCATION_DDL))
        option = element.first_selected_option

        # Then Get the corresponding text from the selected Index
        return option.get_attribute('text')

    def set_location(self, state_name):
        select = Select(self.driver.find_element_by_id(LOCATION_DDL))
        select.select_by_visible_text(state_name)

    # HOUSE PRICE
    def get_default_house_price(self):
        # Get the place holder attribute from the House Price textbox
        element = self.driver.find_element_by_id(HOUSE_PRICE_TBOX)
        house_price = element.get_attribute("placeholder")
        return house_price

    def set_house_price(self, house_price):
        element = self.driver.find_element_by_id(HOUSE_PRICE_TBOX)
        element.clear()  # Clear any existing text
        element.send_keys(house_price)
        element.send_keys(Keys.TAB)

    # DOWN PAYMENT PERCENT
    def get_default_down_payment_percent(self):
        # Get the place holder attribute
        # from the Down Payment Percentage textbox
        element = self.driver.find_element_by_id(DOWN_PAYMENT_PERCENT_TBOX)
        down_payment_amount = element.get_attribute("placeholder")
        return down_payment_amount

    def get_down_payment_percent(self):
        # Get the value attribute from the Down Payment Percentage textbox
        element = self.driver.find_element_by_id(DOWN_PAYMENT_PERCENT_TBOX)
        down_payment_percentage = element.get_attribute("value")
        return down_payment_percentage

    def set_down_payment_percent(self, down_payment):
        element = self.driver.find_element_by_id(DOWN_PAYMENT_PERCENT_TBOX)
        element.send_keys(down_payment)
        element.send_keys(Keys.TAB)

    # DOWN PAYMENT AMOUNT
    def get_default_down_payment_amount(self):
        # Get the place holder attribute from the Down Payment Amount textbox
        element = self.driver.find_element_by_id(DOWN_PAYMENT_AMOUNT_TBOX)
        down_payment_amount = element.get_attribute("placeholder")
        return down_payment_amount

    def get_down_payment_amount(self):
        # Get the value attribute from the Down Payment Amount textbox
        element = self.driver.find_element_by_id(DOWN_PAYMENT_AMOUNT_TBOX)
        down_payment_amount = element.get_attribute("value")
        return down_payment_amount

    def set_down_payment(self, down_payment):
        element = self.driver.find_element_by_id(DOWN_PAYMENT_AMOUNT_TBOX)
        element.clear()  # Clear any existing text
        element.send_keys(down_payment)
        element.send_keys(Keys.TAB)

    # LOAN AMOUNT
    def get_loan_amount(self):
        # Get the text from the Loan Amount label
        element = self.driver.find_element_by_id(LOAN_AMOUNT_LABEL)
        return element.text

    # RATE STRUCTURE
    def get_selected_rate_structure(self):
        # First Get the selected Index from the Location dropdown list
        element = Select(self.driver.find_element_by_id(RATE_STRUCTURE_DDL))
        option = element.first_selected_option

        # Then Get the corresponding text from the selected Index
        return option.get_attribute('text')

    def set_rate_structure(self, rate_selection):
        element = Select(self.driver.find_element_by_id(RATE_STRUCTURE_DDL))
        element.select_by_visible_text(rate_selection)

    # LOAN TERM
    def get_selected_loan_term(self):
        # First Get the selected Index from the Loan Term dropdown list
        element = Select(self.driver.find_element_by_id(LOAN_TERM_DDL))
        option = element.first_selected_option

        # Then Get the corresponding text from the selected Index
        return option.get_attribute('text')

    def set_loan_term(self, number_of_years):
        element = Select(self.driver.find_element_by_id(LOAN_TERM_DDL))
        element.select_by_visible_text(number_of_years)

    # LOAN TYPE
    def get_selected_loan_type(self):
        # First Get the selected Index from the Loan Type dropdown list
        element = Select(self.driver.find_element_by_id(LOAN_TYPE_DDL))
        option = element.first_selected_option

        # Then Get the corresponding text from the selected Index
        return option.get_attribute('text')

    def set_loan_type(self, loan_type):
        element = Select(self.driver.find_element_by_id(LOAN_TYPE_DDL))
        element.select_by_visible_text(loan_type)

    # ARM TYPE
    def get_selected_arm_type(self):
        # First Get the selected Index from the Loan Type dropdown list
        element = Select(self.driver.find_element_by_id(ARM_TYPE_DDL))
        option = element.first_selected_option

        # Then Get the corresponding text from the selected Index
        return option.get_attribute('text')

    def set_arm_type(self, arm_type):
        element = Select(self.driver.find_element_by_id(ARM_TYPE_DDL))
        element.select_by_visible_text(arm_type)
