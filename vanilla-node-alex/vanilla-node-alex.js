const fs = require("fs");
const fetch = require("node-fetch");
const { parse } = require("node-html-parser");

const URL =
  "https://www.asos.com/women/new-in/cat/?cid=27108&nlid=ww|new+in|new+products";

(async () => {
  const res = await fetch(URL);
  const text = await res.text();
  const root = parse(text);
  const productTiles = root.querySelectorAll(`[data-auto-id="productTile"]`);
  const productPromises = [];
  for (let productTile of productTiles) {
    productPromises.push(
      new Promise(async (res, rej) => {
        const productLink = productTile.querySelector("a").getAttribute("href");
        const productRes = await fetch(productLink);
        const productText = await productRes.text();
        const productPage = parse(productText);
        const hasProductDetails = productPage.querySelector(".product-details");
        if (!hasProductDetails) {
          res(null);
          return;
        }
        res({
          name: productPage.querySelector(".product-hero").text.trim(),
          productCode: productPage
            .querySelector(".product-code")
            .querySelector("p")
            .text.trim(),
          productImage: productPage
            .querySelector(".product-carousel img")
            .getAttribute("src"),
          price: productTile
            .querySelector(`[data-auto-id="productTilePrice"]`)
            .text.trim(),
        });
      })
    );
  }
  const products = await Promise.all(productPromises);
  fs.writeFileSync(
    "products.json",
    JSON.stringify(products.filter(Boolean)),
    "utf8"
  );
})();
