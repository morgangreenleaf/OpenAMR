-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 15, 2018 at 06:49 PM
-- Server version: 5.7.14
-- PHP Version: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `incubator`
--

-- --------------------------------------------------------

--
-- Table structure for table `antibiotics`
--

CREATE TABLE `antibiotics` (
  `abx_id` int(50) NOT NULL,
  `abx_name` varchar(100) NOT NULL,
  `abx_content` varchar(20) NOT NULL,
  `abx_code` varchar(20) NOT NULL,
  `abx_descriptor` mediumtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `antibiotics`
--

INSERT INTO `antibiotics` (`abx_id`, `abx_name`, `abx_content`, `abx_code`, `abx_descriptor`) VALUES
(7, 'Trimeth-Sulfamethox', '1.25/23.75ug', 'TS25', ''),
(8, 'Erythromycin', '15ug', 'E15', ''),
(9, 'Penicillin G', '1ug', 'PG1', ''),
(10, 'Gentamicin', '10ug', 'GM10', ''),
(11, 'Clindamycin', '2ug', 'CD2', ''),
(12, 'Fusidic Acid', '10ug', 'CF10', ''),
(13, 'Ceftriaxone', '30ug', 'CRO30', ''),
(14, 'Piperacillin(Tazobactam)', '75-10ug', 'PTZ85C', ''),
(15, 'Cefoxitin', '10ug', 'FOX10', ''),
(16, 'Ceftazidime', '30ug', 'CAZ30', '');

-- --------------------------------------------------------

--
-- Table structure for table `bacteria`
--

CREATE TABLE `bacteria` (
  `bacteria_id` int(50) NOT NULL,
  `bacteria_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bacteria`
--

INSERT INTO `bacteria` (`bacteria_id`, `bacteria_name`) VALUES
(1, 'Acetobacter aurantius'),
(2, 'Acinetobacter baumannii'),
(3, 'Anaplasma'),
(18, 'Anaplasma Cannon'),
(8, 'Anaplasma phagocytophilum'),
(7, 'Azotobacter vinelandii'),
(11, 'Bacillus subtilis'),
(4, 'Bartonella'),
(6, 'Bartonella henselae'),
(5, 'Bordetella'),
(12, 'Bordetella bronchiseptica'),
(13, 'Bordetella pertussis'),
(14, 'Borrelia burgdorfer'),
(10, 'Brucella'),
(15, 'Brucella abortus '),
(16, 'Burkholderia  '),
(19, 'Escherichia Coli'),
(20, 'Staphlococci Aureus');

-- --------------------------------------------------------

--
-- Table structure for table `discs`
--

CREATE TABLE `discs` (
  `disc_id` int(50) NOT NULL,
  `abx_id` int(50) NOT NULL,
  `diameter` int(3) DEFAULT NULL,
  `sample_id` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `eucast`
--

CREATE TABLE `eucast` (
  `eu_id` int(50) NOT NULL,
  `bacteria_id` int(50) NOT NULL,
  `abx_id` int(50) NOT NULL,
  `susceptible` int(3) NOT NULL DEFAULT '0',
  `resistance` int(3) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `eucast`
--

INSERT INTO `eucast` (`eu_id`, `bacteria_id`, `abx_id`, `susceptible`, `resistance`) VALUES
(1, 20, 12, 24, 24),
(2, 20, 11, 22, 19),
(3, 20, 10, 18, 18),
(4, 20, 9, 26, 26),
(5, 20, 8, 21, 18),
(6, 20, 7, 17, 14);

-- --------------------------------------------------------

--
-- Table structure for table `images`
--

CREATE TABLE `images` (
  `image_id` int(50) NOT NULL,
  `sample_id` int(50) NOT NULL,
  `imagelocation` varchar(200) NOT NULL,
  `state` tinyint(1) NOT NULL DEFAULT '0',
  `img_date` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `samples`
--

CREATE TABLE `samples` (
  `sample_id` int(50) NOT NULL,
  `uniquecode` varchar(50) NOT NULL,
  `bacteria_id` int(50) NOT NULL,
  `note` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `zones`
--

CREATE TABLE `zones` (
  `zone_id` int(200) NOT NULL,
  `disc` varchar(20) NOT NULL,
  `sample_id` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `antibiotics`
--
ALTER TABLE `antibiotics`
  ADD PRIMARY KEY (`abx_id`);

--
-- Indexes for table `bacteria`
--
ALTER TABLE `bacteria`
  ADD PRIMARY KEY (`bacteria_id`),
  ADD UNIQUE KEY `bacteria_name` (`bacteria_name`),
  ADD UNIQUE KEY `bacteria_name_2` (`bacteria_name`);

--
-- Indexes for table `discs`
--
ALTER TABLE `discs`
  ADD PRIMARY KEY (`disc_id`),
  ADD KEY `abx_id` (`abx_id`),
  ADD KEY `sample_id` (`sample_id`);

--
-- Indexes for table `eucast`
--
ALTER TABLE `eucast`
  ADD PRIMARY KEY (`eu_id`),
  ADD KEY `abx_id` (`abx_id`),
  ADD KEY `bacteria_id` (`bacteria_id`);

--
-- Indexes for table `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`image_id`),
  ADD KEY `dish_id` (`sample_id`);

--
-- Indexes for table `samples`
--
ALTER TABLE `samples`
  ADD PRIMARY KEY (`sample_id`),
  ADD KEY `bacteria_id` (`bacteria_id`);

--
-- Indexes for table `zones`
--
ALTER TABLE `zones`
  ADD PRIMARY KEY (`zone_id`),
  ADD KEY `sample_id` (`sample_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `antibiotics`
--
ALTER TABLE `antibiotics`
  MODIFY `abx_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
--
-- AUTO_INCREMENT for table `bacteria`
--
ALTER TABLE `bacteria`
  MODIFY `bacteria_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
--
-- AUTO_INCREMENT for table `discs`
--
ALTER TABLE `discs`
  MODIFY `disc_id` int(50) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `eucast`
--
ALTER TABLE `eucast`
  MODIFY `eu_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `images`
--
ALTER TABLE `images`
  MODIFY `image_id` int(50) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `samples`
--
ALTER TABLE `samples`
  MODIFY `sample_id` int(50) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `zones`
--
ALTER TABLE `zones`
  MODIFY `zone_id` int(200) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
