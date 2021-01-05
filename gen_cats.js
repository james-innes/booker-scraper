var fs = require("fs");
var csvWriter = require("csv-write-stream");
var writer = csvWriter({ sendHeaders: false });

const catalog = [
  ["Cadburys", "Chocolate"],
  ["Galaxy", "Chocolate"],
  ["Fanta", "Drink"],
];

const [name, cat] = [...Array(catalog[0].length).keys()];
let cats = new Set([]);

catalog.forEach((_p) => {
  cats = cats.add(_p[cat]);
  _p[cat] = cats.size;
});

writer.pipe(fs.createWriteStream("./cats.csv", { flags: "a" }));
cats.forEach((_cat) => writer.write({ cat: _cat }));
writer.end();

console.log(catalog);
console.log(cats);
