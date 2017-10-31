-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema calendarize_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema calendarize_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `calendarize_db` DEFAULT CHARACTER SET utf8 ;
USE `calendarize_db` ;

-- -----------------------------------------------------
-- Table `calendarize_db`.`calendar_invites`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `calendarize_db`.`calendar_invites` (
  `unique_id` INT(11) NOT NULL,
  `calendar_id` INT(11) NOT NULL,
  `invited_user_id` INT(11) NOT NULL,
  `sender_user_id` INT(11) NOT NULL,
  `role` INT(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`unique_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `calendarize_db`.`calendars`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `calendarize_db`.`calendars` (
  `calendar_id` INT(11) NOT NULL AUTO_INCREMENT,
  `calendar_owner` VARCHAR(45) NOT NULL,
  `calendar_date_created` DATE NOT NULL,
  `calendar_name` VARCHAR(45) NOT NULL,
  `calendar_details` VARCHAR(45) NULL DEFAULT NULL,
  `calendar_extra` VARCHAR(45) NULL DEFAULT NULL,
  `deleted` TINYINT(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`calendar_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `calendarize_db`.`event_files`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `calendarize_db`.`event_files` (
  `event_id` INT(11) NOT NULL,
  `file_name` VARCHAR(160) NOT NULL,
  `unique_id` INT(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`unique_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `calendarize_db`.`events`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `calendarize_db`.`events` (
  `event_id` INT(11) NOT NULL AUTO_INCREMENT,
  `event_calendar_id` INT(11) NOT NULL,
  `event_date_created` DATE NOT NULL,
  `event_owner` VARCHAR(45) NOT NULL,
  `event_name` VARCHAR(45) NOT NULL,
  `event_start` DATE NOT NULL,
  `event_end` DATE NOT NULL,
  `event_recurring` TINYINT(1) NOT NULL DEFAULT '0',
  `event_location` VARCHAR(45) NULL DEFAULT NULL,
  `event_details` VARCHAR(45) NULL DEFAULT NULL,
  `event_extra` VARCHAR(45) NULL DEFAULT NULL,
  `deleted` TINYINT(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`event_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `calendarize_db`.`user_calendars`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `calendarize_db`.`user_calendars` (
  `user_id` INT(11) NOT NULL,
  `calendar_id` INT(11) NOT NULL,
  `role` INT(11) NOT NULL,
  `unique_id` INT(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`unique_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `calendarize_db`.`user_friends`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `calendarize_db`.`user_friends` (
  `user_id` INT(11) NOT NULL,
  `friend_id` INT(11) NOT NULL,
  `unique_id` INT(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`unique_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `calendarize_db`.`userconfig`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `calendarize_db`.`userconfig` (
  `user_config_id` INT(11) NOT NULL,
  `user_config_password` VARCHAR(45) NULL DEFAULT NULL,
  `user_config_extra` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`user_config_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `calendarize_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `calendarize_db`.`users` (
  `user_id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(45) NOT NULL,
  `user_email` VARCHAR(45) NOT NULL,
  `user_password` VARCHAR(80) NOT NULL,
  `user_type` INT(11) NULL DEFAULT NULL,
  `user_phone` INT(11) NULL DEFAULT NULL,
  `user_record` VARCHAR(45) NULL DEFAULT NULL,
  `user_extra` VARCHAR(45) NULL DEFAULT NULL,
  `verify_key` VARCHAR(15) NULL DEFAULT NULL,
  `resetkey` VARCHAR(80) NULL DEFAULT NULL,
  `expires` DATE NULL DEFAULT NULL,
  `active` TINYINT(1) NOT NULL DEFAULT '0',
  `deleted` TINYINT(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
