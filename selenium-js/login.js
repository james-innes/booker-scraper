const { Builder, firefox, webdriver } = require("selenium-webdriver");

(async function () {
  let driver = await new Builder().forBrowser("firefox").build();

  await driver.get(
    "https://www.booker.co.uk/account/loginregister/UserLogin.aspx"
  );

  driver
    .findElement(webdriver.By.id("LoginControl_CustomerNumberSingle"))
    .sendKeys("303182030", webdriver.Key.RETURN);

  driver
    .findElement(webdriver.By.id("LoginControl_EmailSingle"))
    .sendKeys("nigelsr@gmail.com");
  driver
    .findElement(webdriver.By.id("LoginControl_PasswordSingle"))
    .sendKeys("drvLNXzExJ6J96zn", webdriver.key.RETURN);

  driver.quit();
})();
