CREATE DATABASE `booker`;
USE `booker`;

CREATE OR REPLACE TABLE `barcode` (
  `barcode_id` INT(11) NOT NULL AUTO_INCREMENT,
  `barcode` VARCHAR(80) NOT NULL,
  `code` INT(11) NOT NUL NOT NULL,
  PRIMARY KEY (`barcode_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8;

CREATE OR REPLACE TABLE `cat` (
  `cat_id` INT(11) NOT NULL AUTO_INCREMENT,
  `cat_code` VARCHAR(20) NOT NULL,
  `cat_name` VARCHAR(40) NOT NULL,
  PRIMARY KEY (`cat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8;


CREATE OR REPLACE TABLE `sub_cat` (
  `sub_cat_id` INT(11) NOT NULL AUTO_INCREMENT,
  `sub_cat_code` VARCHAR(20) NOT NULL,
  `sub_cat_name` VARCHAR(40) NOT NULL,
  PRIMARY KEY (`sub_cat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8;


CREATE OR REPLACE TABLE `shelf` (
  `shelf_id` INT(11) NOT NULL AUTO_INCREMENT,
  `shelf_code` VARCHAR(20) NOT NULL,
  `shelf_name` VARCHAR(40) NOT NULL,
  PRIMARY KEY (`shelf_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8;


CREATE OR REPLACE TABLE `product` (
  `product_id` INT(11) NOT NULL AUTO_INCREMENT,

  `code` INT(11) NOT NUL NOT NULL,
  `name` VARCHAR(40) NOT NULL,

  `cat_id` INT(11) DEFAULT 1,
  `sub_cat_id` INT(11) DEFAULT 1,
  `shelf_id` INT(11) DEFAULT 1,

  `wsp_exl_vat` INT(11) NOT NULL,
  `wsp_inc_vat` INT(11) NOT NULL,
  `rrp` INT(11) NOT NULL,
  `por` INT(11) NOT NULL,
  `vat` INT(11) NOT NULL,

  `size` VARCHAR(40) NOT NULL,
  `ws_qty` INT(11) NOT NULL,
  `rt_qty` INT(11) NOT NULL,
  `pack_type` VARCHAR(40) NOT NULL,

  `img_small_guid` VARCHAR(20) NOT NULL,
  `img_big_guid` VARCHAR(20) NOT NULL,

  /* Possible lookup tables */
  `brand` 
  `origin_country`
  `packed_country`
  `storage_type`

  /* Product type specific */
  `beverage_type` VARCHAR(20) NOT NULL,
  `alcohol_volume` INT(11) NOT NULL,
  `alcohol_units`  INT(11) NOT NULL,

  /* Descriptive sections */
  `description` VARCHAR(80) NOT NULL,
  `tasting_notes` VARCHAR(80) NOT NULL,
  `allergy_advice` VARCHAR(80) NOT NULL,
  `ingredients` VARCHAR(80) NOT NULL,
  `nutrition` VARCHAR(80) NOT NULL,
  `manufacturer` VARCHAR(80) NOT NULL,
  `packaging` VARCHAR(80) NOT NULL,

  PRIMARY KEY (`product_id`),
  FOREIGN KEY (`cat_id`) REFERENCES `cat`(`cat_id`),
  FOREIGN KEY (`sub_cat_id`) REFERENCES `aub_cat`(`sub_cat_id`),
  FOREIGN KEY (`shelf_id`) REFERENCES `shelf_id`(`shelf_id`),
  UNIQUE (`code`)
) ENGINE=INNODB AUTO_INCREMENT=8;