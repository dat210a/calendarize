CREATE DATABASE  IF NOT EXISTS `calendarize_db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `calendarize_db`;
-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: localhost    Database: calendarize_db
-- ------------------------------------------------------
-- Server version	5.7.17-log

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
-- Table structure for table `calendars`
--

DROP TABLE IF EXISTS `calendars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `calendars` (
  `calendarID` int(11) NOT NULL,
  `calendarName` varchar(45) NOT NULL,
  `calendarDateCreated` date NOT NULL,
  `calendarDetails` varchar(45) NOT NULL,
  `calendarOwner` varchar(45) NOT NULL,
  `calendarMembers` varchar(45) DEFAULT NULL,
  `calendarTime` int(11) DEFAULT NULL,
  `calendarDay` int(11) DEFAULT NULL,
  `calendearMonth` int(11) DEFAULT NULL,
  `calendarYear` int(11) DEFAULT NULL,
  `calendarExtra` varchar(45) DEFAULT NULL,
  `deleted` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`calendarID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calendars`
--

LOCK TABLES `calendars` WRITE;
/*!40000 ALTER TABLE `calendars` DISABLE KEYS */;
/*!40000 ALTER TABLE `calendars` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `events` (
  `EventID` int(11) NOT NULL,
  `EventName` varchar(45) NOT NULL,
  `EventDateCreated` date NOT NULL,
  `EventDetails` varchar(45) NOT NULL,
  `EventLocation` varchar(45) DEFAULT NULL,
  `EventStart` date DEFAULT NULL,
  `EventEnd` date DEFAULT NULL,
  `EventTime` varchar(45) DEFAULT NULL,
  `EventMembers` varchar(45) NOT NULL,
  `EventIsUnderThisCalender` varchar(45) NOT NULL,
  `EventExtra` varchar(45) DEFAULT NULL,
  `deleted` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`EventID`),
  UNIQUE KEY `deleted_UNIQUE` (`deleted`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userconfig`
--

DROP TABLE IF EXISTS `userconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userconfig` (
  `UserConfiqID` int(11) NOT NULL,
  `UserConfigPassword` varchar(45) DEFAULT NULL,
  `UserConfigExtra` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`UserConfiqID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userconfig`
--

LOCK TABLES `userconfig` WRITE;
/*!40000 ALTER TABLE `userconfig` DISABLE KEYS */;
/*!40000 ALTER TABLE `userconfig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `UserID` int(11) NOT NULL,
  `UserType` int(11) NOT NULL,
  `UserName` varchar(45) NOT NULL,
  `UserEmail` varchar(45) NOT NULL,
  `UserPhone` int(11) DEFAULT NULL,
  `UserRole` varchar(45) NOT NULL,
  `UserRecord` varchar(45) DEFAULT NULL,
  `UserPassword` varchar(45) NOT NULL,
  `UserFriendList` varchar(45) DEFAULT NULL,
  `UserCalendars` varchar(45) DEFAULT NULL,
  `UserSubscribedToThisCalender` varchar(45) DEFAULT NULL,
  `UserEvents` varchar(45) DEFAULT NULL,
  `UserExtra` varchar(45) DEFAULT NULL,
  `deleted` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'calendarize_db'
--

--
-- Dumping routines for database 'calendarize_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-04 19:36:32
