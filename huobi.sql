/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50553
Source Host           : localhost:3306
Source Database       : huobi

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2019-04-21 07:05:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for huobi
-- ----------------------------
DROP TABLE IF EXISTS `huobi`;
CREATE TABLE `huobi` (
  `market` varchar(255) DEFAULT NULL,
  `5min` varchar(255) DEFAULT NULL,
  `15min` varchar(255) DEFAULT NULL,
  `30min` varchar(255) DEFAULT NULL,
  `60min` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of huobi
-- ----------------------------
INSERT INTO `huobi` VALUES ('htusdt', '{ts:1555801343143,open:2.5183,close:2.5194,low:2.5167,high:2.5204,amount:11917.27,vol:30009.242069,count:118}', '{ts:1555801343143,open:2.5183,close:2.5194,low:2.5167,high:2.5204,amount:11917.27,vol:30009.242069,count:118}', '{ts:1555801343144,open:2.5183,close:2.5194,low:2.5167,high:2.5204,amount:11917.27,vol:30009.242069,count:118}', '{ts:1555801343143,open:2.5183,close:2.5194,low:2.5167,high:2.5204,amount:11917.27,vol:30009.242069,count:118}');
INSERT INTO `huobi` VALUES ('btcusdt', '{ts:1555801344192,open:5270.83,close:5273.98,low:5269.6,high:5274.0,amount:9.460219759872643,vol:49866.85620755574,count:129}', '{ts:1555801344193,open:5270.83,close:5273.98,low:5269.6,high:5274.0,amount:9.460219759872643,vol:49866.85620755574,count:129}', '{ts:1555801344193,open:5270.83,close:5273.98,low:5269.6,high:5274.0,amount:9.460219759872643,vol:49866.85620755574,count:129}', '{ts:1555801344193,open:5270.83,close:5273.98,low:5269.6,high:5274.0,amount:9.460219759872643,vol:49866.85620755574,count:129}');
INSERT INTO `huobi` VALUES ('ltcusdt', '{ts:1555801347358,open:81.01,close:81.05,low:80.92,high:81.05,amount:567.3847,vol:45927.308295,count:121}', '{ts:1555801347357,open:81.01,close:81.05,low:80.92,high:81.05,amount:567.3847,vol:45927.308295,count:121}', '{ts:1555801347358,open:81.01,close:81.05,low:80.92,high:81.05,amount:567.3847,vol:45927.308295,count:121}', '{ts:1555801347358,open:81.01,close:81.05,low:80.92,high:81.05,amount:567.3847,vol:45927.308295,count:121}');
