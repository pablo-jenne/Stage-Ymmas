-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Gegenereerd op: 13 mei 2022 om 13:44
-- Serverversie: 10.4.22-MariaDB
-- PHP-versie: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `machine_info`
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `machine_info`
--

CREATE TABLE `machine_info` (
  `ID` int(11) NOT NULL,
  `MachineIP` varchar(255) CHARACTER SET latin1 NOT NULL,
  `MachineID` varchar(255) CHARACTER SET latin1 NOT NULL,
  `Status` varchar(255) CHARACTER SET latin1 NOT NULL,
  `Bearer_token` varchar(255) CHARACTER SET latin1 NOT NULL,
  `Valid_time` varchar(255) CHARACTER SET latin1 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Gegevens worden geëxporteerd voor tabel `machine_info`
--

INSERT INTO `machine_info` (`ID`, `MachineIP`, `MachineID`, `Status`, `Bearer_token`, `Valid_time`) VALUES
(1, '192.168.0.115', '000177677507', 'bussy', '000065D76C07BFEB1C819096693354CB7E6F65AF3DB41A2EEFEFFD57BE36233424', '2022/05/13 13:26:21'),
(2, '192.168.34.52', '161228811000', 'free', '', ''),
(3, '192.168.34.53', '000000000000', 'free', '', ''),
(4, '192.168.34.54', '111111111111', 'free', '', '');

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `machine_info`
--
ALTER TABLE `machine_info`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT voor geëxporteerde tabellen
--

--
-- AUTO_INCREMENT voor een tabel `machine_info`
--
ALTER TABLE `machine_info`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
