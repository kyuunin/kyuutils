-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Erstellungszeit: 12. Nov 2021 um 22:43
-- Server-Version: 10.3.31-MariaDB-0+deb10u1
-- PHP-Version: 7.3.29-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `kyuutils_test`
--
CREATE DATABASE IF NOT EXISTS `kyuutils_test` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `kyuutils_test`;

--
-- User: `kyuutils_test`
--

DROP USER IF EXISTS 'kyuutils_test';
CREATE USER 'kyuutils_test'@'localhost' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON `kyuutils_test` . * TO 'kyuutils_test'@'localhost';


-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `message`
--

DROP TABLE IF EXISTS `message`;
CREATE TABLE `message` (
  `message_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `message`
--

INSERT INTO `message` (`message_id`, `user_id`, `text`) VALUES
(1, 1, 'Hello'),
(1, 2, 'Baum'),
(2, 1, 'Fish'),
(2, 2, 'Hi'),
(3, 2, 'Hullu');

-- --------------------------------------------------------

--
-- Stellvertreter-Struktur des Views `message_view`
-- (Siehe unten für die tatsächliche Ansicht)
--
DROP VIEW IF EXISTS `message_view`;
CREATE TABLE `message_view` (
`text` text
,`name` varchar(20)
);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `passwd` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `user`
--

INSERT INTO `user` (`id`, `name`, `passwd`) VALUES
(1, 'user1', 'test1'),
(2, 'user2', 'test2');

-- --------------------------------------------------------

--
-- Struktur des Views `message_view`
--
DROP TABLE IF EXISTS `message_view`;

CREATE ALGORITHM=UNDEFINED DEFINER=`bresli`@`localhost` SQL SECURITY DEFINER VIEW `message_view`  AS  select `message`.`text` AS `text`,`user`.`name` AS `name` from (`message` join `user` on(`message`.`user_id` = `user`.`id`)) ;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`message_id`,`user_id`),
  ADD KEY `user` (`user_id`);

--
-- Indizes für die Tabelle `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `message`
--
ALTER TABLE `message`
  ADD CONSTRAINT `user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
