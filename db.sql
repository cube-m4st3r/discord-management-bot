-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema met11
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `met11` ;

-- -----------------------------------------------------
-- Schema met11
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `met11` DEFAULT CHARACTER SET utf8 ;
USE `met11` ;

-- -----------------------------------------------------
-- Table `met11`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `met11`.`user` (
  `idUser` BIGINT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `discriminator` VARCHAR(4) NOT NULL,
  PRIMARY KEY (`idUser`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `met11`.`location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `met11`.`location` (
  `idLocation` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idLocation`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `met11`.`postal_code`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `met11`.`postal_code` (
  `idPostal_code` INT NOT NULL AUTO_INCREMENT,
  `code` INT(11) NOT NULL,
  PRIMARY KEY (`idPostal_code`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `met11`.`address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `met11`.`address` (
  `idAddress` INT NOT NULL AUTO_INCREMENT,
  `street` VARCHAR(45) NOT NULL,
  `house_number` INT(11) NOT NULL,
  `idLocation` INT NOT NULL,
  `idPostal_code` INT NOT NULL,
  PRIMARY KEY (`idAddress`),
  INDEX `fk_Address_location1_idx` (`idLocation` ASC) ,
  INDEX `fk_Address_postal_code1_idx` (`idPostal_code` ASC) ,
  CONSTRAINT `fk_Address_location1`
    FOREIGN KEY (`idLocation`)
    REFERENCES `met11`.`location` (`idLocation`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Address_postal_code1`
    FOREIGN KEY (`idPostal_code`)
    REFERENCES `met11`.`postal_code` (`idPostal_code`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `met11`.`person`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `met11`.`person` (
  `idPerson` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `idAddress` INT NULL,
  `email` VARCHAR(45) NULL,
  PRIMARY KEY (`idPerson`),
  INDEX `fk_Person_Address1_idx` (`idAddress` ASC) ,
  CONSTRAINT `fk_Person_Address1`
    FOREIGN KEY (`idAddress`)
    REFERENCES `met11`.`address` (`idAddress`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `met11`.`student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `met11`.`student` (
  `idStudent` INT NOT NULL AUTO_INCREMENT,
  `idUser` BIGINT NOT NULL,
  `idPerson` INT NOT NULL,
  PRIMARY KEY (`idStudent`),
  INDEX `fk_student_user_idx` (`idUser` ASC) ,
  INDEX `fk_student_Person1_idx` (`idPerson` ASC) ,
  CONSTRAINT `fk_student_user`
    FOREIGN KEY (`idUser`)
    REFERENCES `met11`.`user` (`idUser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_student_Person1`
    FOREIGN KEY (`idPerson`)
    REFERENCES `met11`.`person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `met11`.`teacher`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `met11`.`teacher` (
  `idTeacher` INT NOT NULL,
  `idPerson` INT NOT NULL,
  PRIMARY KEY (`idTeacher`),
  INDEX `fk_teacher_Person1_idx` (`idPerson` ASC) ,
  CONSTRAINT `fk_teacher_Person1`
    FOREIGN KEY (`idPerson`)
    REFERENCES `met11`.`person` (`idPerson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `met11`.`lesson`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `met11`.`lesson` (
  `idLesson` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `idTeacher` INT NOT NULL,
  PRIMARY KEY (`idLesson`),
  INDEX `fk_lesson_teacher1_idx` (`idTeacher` ASC) ,
  CONSTRAINT `fk_lesson_teacher1`
    FOREIGN KEY (`idTeacher`)
    REFERENCES `met11`.`teacher` (`idTeacher`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `met11`.`student_has_lesson`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `met11`.`student_has_lesson` (
  `idRel` INT NOT NULL AUTO_INCREMENT,
  `idStudent` INT NOT NULL,
  `idLesson` INT NOT NULL,
  `grade` INT NULL,
  INDEX `fk_student_has_lesson_lesson1_idx` (`idLesson` ASC) ,
  INDEX `fk_student_has_lesson_student1_idx` (`idStudent` ASC) ,
  PRIMARY KEY (`idRel`),
  CONSTRAINT `fk_student_has_lesson_student1`
    FOREIGN KEY (`idStudent`)
    REFERENCES `met11`.`student` (`idStudent`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_student_has_lesson_lesson1`
    FOREIGN KEY (`idLesson`)
    REFERENCES `met11`.`lesson` (`idLesson`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
