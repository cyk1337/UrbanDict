/*
 Navicat Premium Data Transfer

 Source Server         : Local OSX
 Source Server Type    : MySQL
 Source Server Version : 50721
 Source Host           : localhost:3306
 Source Schema         : UrbanDict

 Target Server Type    : MySQL
 Target Server Version : 50721
 File Encoding         : 65001

 Date: 26/06/2018 12:47:09
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for var_index
-- ----------------------------
DROP TABLE IF EXISTS `var_index`;
CREATE TABLE `var_index` (
  `defid` int(20) unsigned NOT NULL,
  `label_index` int(11) NOT NULL,
  `variant` varchar(100) DEFAULT NULL,
  `ctx_bef` varchar(100) DEFAULT NULL,
  `ctx_aft` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`defid`,`label_index`),
  CONSTRAINT `defid` FOREIGN KEY (`defid`) REFERENCES `UrbanDict` (`defid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
