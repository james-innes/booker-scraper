const { Builder, firefox, webdriver } = require("selenium-webdriver");

(async function () {
  let driver = await new Builder().forBrowser("firefox").build();

  await driver.get(
    "https://www.booker.co.uk/account/loginregister/UserLogin.aspx"
  );

  driver
    .findElement(webdriver.By.id("LoginControl_CustomerNumberSingle"))
    .sendKeys("BOOKER_ACCOUNT", webdriver.Key.RETURN);

  driver
    .findElement(webdriver.By.id("LoginControl_EmailSingle"))
    .sendKeys("BOOKER_EMAIL");
  driver
    .findElement(webdriver.By.id("LoginControl_PasswordSingle"))
    .sendKeys("BOOKER_PASSWORD", webdriver.key.RETURN);

  driver.quit();
})();
