-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema TEST_MET11
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `TEST_MET11` ;

-- -----------------------------------------------------
-- Schema TEST_MET11
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `TEST_MET11` DEFAULT CHARACTER SET utf8 ;
USE `TEST_MET11` ;

-- -----------------------------------------------------
-- Table `TEST_MET11`.`discord_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TEST_MET11`.`discord_user` ;

CREATE TABLE IF NOT EXISTS `TEST_MET11`.`discord_user` (
  `iddiscord_user` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `userdiscriminator` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`iddiscord_user`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TEST_MET11`.`student`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TEST_MET11`.`student` ;

CREATE TABLE IF NOT EXISTS `TEST_MET11`.`student` (
  `idstudent` INT NOT NULL AUTO_INCREMENT,
  `discord_user_iddiscord_user` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idstudent`),
  INDEX `fk_student_discord_user_idx` (`discord_user_iddiscord_user` ASC),
  CONSTRAINT `fk_student_discord_user`
    FOREIGN KEY (`discord_user_iddiscord_user`)
    REFERENCES `TEST_MET11`.`discord_user` (`iddiscord_user`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TEST_MET11`.`teacher`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TEST_MET11`.`teacher` ;

CREATE TABLE IF NOT EXISTS `TEST_MET11`.`teacher` (
  `idteacher` INT NOT NULL AUTO_INCREMENT,
  `form_of_address` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idteacher`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TEST_MET11`.`lesson`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TEST_MET11`.`lesson` ;

CREATE TABLE IF NOT EXISTS `TEST_MET11`.`lesson` (
  `idlesson` INT NOT NULL AUTO_INCREMENT,
  `lesson_name` VARCHAR(45) NOT NULL,
  `teacher_idteacher` INT NOT NULL,
  PRIMARY KEY (`idlesson`),
  INDEX `fk_lesson_teacher1_idx` (`teacher_idteacher` ASC),
  CONSTRAINT `fk_lesson_teacher1`
    FOREIGN KEY (`teacher_idteacher`)
    REFERENCES `TEST_MET11`.`teacher` (`idteacher`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TEST_MET11`.`student_has_lesson`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TEST_MET11`.`student_has_lesson` ;

CREATE TABLE IF NOT EXISTS `TEST_MET11`.`student_has_lesson` (
  `idstudent_has_lesson` INT NOT NULL AUTO_INCREMENT,
  `student_idstudent` INT NOT NULL,
  `lesson_idlesson` INT NOT NULL,
  `grade` INT NOT NULL,
  PRIMARY KEY (`idstudent_has_lesson`, `student_idstudent`, `lesson_idlesson`),
  INDEX `fk_student_has_lesson_student1_idx` (`student_idstudent` ASC),
  INDEX `fk_student_has_lesson_lesson1_idx` (`lesson_idlesson` ASC),
  CONSTRAINT `fk_student_has_lesson_student1`
    FOREIGN KEY (`student_idstudent`)
    REFERENCES `TEST_MET11`.`student` (`idstudent`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_student_has_lesson_lesson1`
    FOREIGN KEY (`lesson_idlesson`)
    REFERENCES `TEST_MET11`.`lesson` (`idlesson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `TEST_MET11`.`privacy_settings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `TEST_MET11`.`privacy_settings` ;

CREATE TABLE IF NOT EXISTS `TEST_MET11`.`privacy_settings` (
  `student_idstudent` INT NOT NULL,
  `privacy_grades` TINYINT NULL,
  `privacy_followers` VARCHAR(45) NULL,
  PRIMARY KEY (`student_idstudent`),
  CONSTRAINT `fk_privacy_settings_student1`
    FOREIGN KEY (`student_idstudent`)
    REFERENCES `TEST_MET11`.`student` (`idstudent`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
