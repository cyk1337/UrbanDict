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

 Date: 24/05/2018 15:22:22
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for UD_full
-- ----------------------------
DROP TABLE IF EXISTS `UD_full`;
CREATE TABLE `UD_full` (
  `defid` int(20) unsigned NOT NULL COMMENT 'unique defid for each definition in UrbanDict',
  `label` tinyint(1) unsigned DEFAULT NULL COMMENT 'label of whether this definition has spelling variants',
  `word` varchar(150) NOT NULL,
  `definition` longtext NOT NULL COMMENT 'each definition for the dictionary word entry',
  `thumbs_up` int(15) DEFAULT NULL,
  `thumbs_down` int(15) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL COMMENT 'UrbanDict webpage URL for the word entry, i.e. https://www.urbandictionary.com/define.php?term={word}',
  `permalink` varchar(100) DEFAULT NULL COMMENT 'API permalink',
  `author` varchar(50) DEFAULT NULL,
  `written_date` date DEFAULT NULL,
  `example` longtext COMMENT 'dictionary example',
  PRIMARY KEY (`defid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
