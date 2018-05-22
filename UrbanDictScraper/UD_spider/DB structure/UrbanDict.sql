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

 Date: 22/05/2018 23:41:27
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for UrbanDict
-- ----------------------------
DROP TABLE IF EXISTS `UrbanDict`;
CREATE TABLE `UrbanDict` (
  `defid` int(20) NOT NULL,
  `word` varchar(150) NOT NULL,
  `definition` longtext NOT NULL,
  `permalink` varchar(100) DEFAULT NULL,
  `thumbs_up` int(15) DEFAULT NULL,
  `thumbs_down` int(15) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL COMMENT 'Urban Dict URL',
  `author` varchar(50) DEFAULT NULL,
  `written_date` datetime DEFAULT NULL,
  `example` longtext COMMENT 'dictionary example',
  PRIMARY KEY (`defid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
