CREATE DATABASE booker;
USE booker;

CREATE TABLE barcode (
  barcode_id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
  barcode VARCHAR(80) NOT NULL,
  code INT(11) NOT NULL,
  PRIMARY KEY (barcode_id)
);

CREATE TABLE cat (
  cat_id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
  cat_code VARCHAR(20) NOT NULL,
  cat_name VARCHAR(40) NOT NULL,
  PRIMARY KEY (cat_id)
);


CREATE TABLE sub_cat (
  sub_cat_id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
  sub_cat_code VARCHAR(20) NOT NULL,
  sub_cat_name VARCHAR(40) NOT NULL,
  PRIMARY KEY (sub_cat_id)
);


CREATE TABLE shelf (
  shelf_id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
  shelf_code VARCHAR(20) NOT NULL,
  shelf_name VARCHAR(40) NOT NULL,
  PRIMARY KEY (shelf_id)
);


CREATE TABLE product (
  product_id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
  code INT(11) NOT NULL,
  name VARCHAR(40) NOT NULL,

  cat_id MEDIUMINT UNSIGNED NOT NULL,
  sub_cat_id MEDIUMINT UNSIGNED NOT NULL,
  shelf_id MEDIUMINT UNSIGNED NOT NULL,

  wsp_exl_vat INT(11) NOT NULL,
  wsp_inc_vat INT(11) NOT NULL,
  rrp INT(11) NOT NULL,
  por INT(11) NOT NULL,
  vat INT(11) NOT NULL,

  size VARCHAR(40) NOT NULL,
  ws_qty INT(11) NOT NULL,
  rt_qty INT(11) NOT NULL,
  pack_type VARCHAR(40) NOT NULL,
  unit_description VARCHAR(40) NOT NULL,
  on_offer VARCHAR(40) NOT NULL,
  additives VARCHAR(40) NOT NULL,

  img_small_guid VARCHAR(20) NOT NULL,
  img_big_guid VARCHAR(20) NOT NULL,

  /* Possible lookup tables */
  brand VARCHAR(20) NOT NULL,
  origin_country VARCHAR(20) NOT NULL,
  packed_country VARCHAR(20) NOT NULL,
  storage_type VARCHAR(20) NOT NULL,

  /* Product type specific */
  beverage_type VARCHAR(20) NOT NULL,
  alcohol_volume INT(11) NOT NULL,
  alcohol_units  INT(11) NOT NULL,

  /* Descriptive sections */
  description VARCHAR(80) NOT NULL,
  allergy_advice VARCHAR(80) NOT NULL,
  ingredients VARCHAR(80) NOT NULL,
  nutrition VARCHAR(80) NOT NULL,
  manufacturer VARCHAR(80) NOT NULL,
  packaging VARCHAR(80) NOT NULL,
  alternative_products VARCHAR(80) NOT NULL,
  prepare_and_use VARCHAR(80) NOT NULL,
  storage_information VARCHAR(80) NOT NULL,
  freezing_guidelines VARCHAR(80) NOT NULL,
  additional_information VARCHAR(80) NOT NULL,
  recycling
  /* Very product Specific */
  tasting_notes VARCHAR(80) NOT NULL,
  current_vintage VARCHAR(80) NOT NULL,
  wine_colour VARCHAR(80) NOT NULL,
  producer VARCHAR(80) NOT NULL,
  grape_variety VARCHAR(80) NOT NULL,
  closure_type VARCHAR(80) NOT NULL,
  wine_maker VARCHAR(80) NOT NULL,

  PRIMARY KEY (product_id),
  FOREIGN KEY (cat_id) REFERENCES cat(cat_id),
  FOREIGN KEY (sub_cat_id) REFERENCES sub_cat(sub_cat_id),
  FOREIGN KEY (shelf_id) REFERENCES shelf(shelf_id),
  UNIQUE (code)
);








