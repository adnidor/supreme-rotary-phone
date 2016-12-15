-- MySQL dump 10.13  Distrib 5.5.53, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: network
-- ------------------------------------------------------
-- Server version	5.5.53-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aps`
--

DROP TABLE IF EXISTS `aps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` varchar(20) NOT NULL,
  `channel` int(11) NOT NULL,
  `radiussecret` varchar(30) NOT NULL,
  `radiusserver` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `vlans` varchar(50) NOT NULL,
  `mvlan` int(11) NOT NULL,
  `switch` varchar(50) NOT NULL,
  `model` varchar(20) NOT NULL,
  `interfaces` varchar(30) NOT NULL,
  `wifi_enabled` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cnames`
--

DROP TABLE IF EXISTS `cnames`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cnames` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `target` varchar(30) NOT NULL,
  `context` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contexts`
--

DROP TABLE IF EXISTS `contexts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contexts` (
  `i` int(10) NOT NULL,
  `name` varchar(20) NOT NULL,
  `iprange` varchar(20) NOT NULL,
  `description` varchar(50) NOT NULL,
  `dhcp` tinyint(1) NOT NULL,
  `parent` int(10) DEFAULT NULL,
  `email` text NOT NULL,
  `admin_user` int(11) NOT NULL,
  PRIMARY KEY (`i`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices` (
  `identifier` varchar(40) NOT NULL,
  `ip` varchar(15) NOT NULL,
  `context` varchar(10) NOT NULL,
  `hostname` varchar(20) NOT NULL,
  `altname` varchar(20) NOT NULL,
  `description` varchar(100) NOT NULL,
  `ip6` varchar(36) NOT NULL,
  `type` varchar(10) NOT NULL DEFAULT 'dhcp',
  `devicetype` int(11) NOT NULL,
  `connection` varchar(20) NOT NULL,
  `ports` varchar(40) NOT NULL,
  `internet` int(11) NOT NULL DEFAULT '1',
  `alwayson` tinyint(1) NOT NULL DEFAULT '0',
  `formfactor` varchar(40) NOT NULL,
  PRIMARY KEY (`identifier`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `devicetypes`
--

DROP TABLE IF EXISTS `devicetypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devicetypes` (
  `number` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `os` varchar(20) NOT NULL,
  `platform` varchar(20) NOT NULL,
  PRIMARY KEY (`number`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `switches`
--

DROP TABLE IF EXISTS `switches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `switches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `description` varchar(30) NOT NULL,
  `nports` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(40) NOT NULL,
  `name` varchar(40) NOT NULL,
  `email` varchar(40) NOT NULL,
  `pushover` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vlans`
--

DROP TABLE IF EXISTS `vlans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vlans` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wifis`
--

DROP TABLE IF EXISTS `wifis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wifis` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ssid` varchar(32) NOT NULL,
  `vlan` int(11) NOT NULL,
  `authmethod` varchar(20) NOT NULL,
  `aps` varchar(20) NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  `passphrase` varchar(63) NOT NULL,
  `mode` varchar(10) NOT NULL,
  `whitelist` tinyint(1) NOT NULL,
  `enabled` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-12-11 12:34:55
