-- ---------------------------
-- Table structure for `fort_functions`
-- ---------------------------
CREATE TABLE IF NOT EXISTS `fort_functions` (
  `fort_id` int(2) NOT NULL default '0',
  `type` int(1) NOT NULL default '0',
  `lvl` int(3) NOT NULL default '0',
  `lease` int(10) NOT NULL default '0',
  `rate` decimal(20,0) NOT NULL default '0',
  `endTime` decimal(20,0) NOT NULL default '0',
  PRIMARY KEY (`fort_id`,`type`)
);
