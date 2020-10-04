import time


def login(self):
    self.driver.get(
        "https://www.booker.co.uk/account/loginregister/UserLogin.aspx")
    self.driver.find_element_by_id("LoginControl_CustomerNumberSingle").send_keys(
        "***REMOVED***")
    self.driver.find_element_by_id(
        "LoginControl_EnterCustomerNumberSubmit").click()
    time.sleep(0.5)
    self.driver.find_element_by_id(
        "LoginControl_EmailSingle").send_keys("***REMOVED***")
    self.driver.find_element_by_id(
        "LoginControl_PasswordSingle").send_keys("drvLNXzExJ6J96zn")
    self.driver.find_element_by_id(
        "LoginControl_EnterEmailPasswordSubmit").click()
    self.parse()
