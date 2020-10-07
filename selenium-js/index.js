const {
  Builder,
  By,
  Key,
  until,
  TimeUnit,
  chrome,
} = require("selenium-webdriver");

(async function () {
  let options = new chrome.Options();
  let nextPort = 9222; //for example
  options.addArguments(["--remote-debugging-port=" + nextPort]);
  let driver = await new Builder()
    .forBrowser("chrome")
    .setChromeOptions(options)
    .build();

  url =
    "https://www.booker.co.uk/catalog/productinformation.aspx?code=606053&settype=23&categoryName=307954&CSUrl=https%3a%2f%2fwww.booker.co.uk%2fcatalog%2fproducts.aspx%3fcategoryName%3dCS13_200001%26view%3dUnGrouped%26sortField%3dCore%26SortDirection%3dAscending%26multi%3dFalse%26pageIndex%3d3";

  try {
    await driver.manage().setTimeouts({ implicit: 5000 });

    await driver.get(
      "https://www.booker.co.uk/account/loginregister/UserLogin.aspx"
    );
    // driver.wait(driver.findElement(By.id('LoginControl_CustomerNumberSingle')).sendKeys("BOOKER_ACCOUNT", Key.RETURN), 1000)
    driver
      .findElement(By.id("LoginControl_CustomerNumberSingle"))
      .sendKeys("BOOKER_ACCOUNT", Key.RETURN);
    // driver.sleep(100000)

    // driver.findElement(By.id("LoginControl_EmailSingle")).sendKeys("BOOKER_PASSWORD")

    // driver.wait(driver.findElement(By.id("LoginControl_EmailSingle")).sendKeys("BOOKER_EMAIL"), 5000)
    // await driver.findElement(By.id("LoginControl_EmailSingle")).sendKeys("BOOKER_PASSWORD")
    // await driver.findElement(By.id("LoginControl_PasswordSingle")).sendKeys("BOOKER_PASSWORD")
    // await driver.findElement(By.id("LoginControl_EnterEmailPasswordSubmit")).click()
  } finally {
    await driver.quit();
  }
})();
