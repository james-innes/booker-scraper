var webdriver = require('selenium-webdriver');

//create driver object for chromedriver
var driver = new webdriver.Builder()
.forBrowser('chrome')
.build();

function searchForCrossBrowserTesting() {

searchbar = driver.wait(webdriver.until.elementLocated(webdriver.By.name('q')), 500)
.then(function(searchbar) {
searchbar.sendKeys('SmartBear.com');
searchbar.submit();
});
}

function clickCrossBrowserTesting() {
clickLink = driver.wait( webdriver.until.elementLocated(webdriver.By.linkText("Cross Browser Testing Tool: 1500+ Real Browsers & Devices")),
.then(function(clickLink) {
clickLink.click();
});
}
driver.get('http://google.com')
.then(searchForCrossBrowserTesting())
.then(clickCrossBrowserTesting());
driver.quit();