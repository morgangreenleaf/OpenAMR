-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 31, 2018 at 08:39 PM
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
-- Table structure for table `bacteria`
--

CREATE TABLE `bacteria` (
  `bacteria_id` int(50) NOT NULL,
  `bacteria_name` varchar(100) NOT NULL,
  `timelimit` int(3) NOT NULL DEFAULT '24'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bacteria`
--

INSERT INTO `bacteria` (`bacteria_id`, `bacteria_name`, `timelimit`) VALUES
(1, 'Acetobacter aurantius', 24),
(2, 'Acinetobacter baumannii', 24),
(3, 'Anaplasma', 24),
(4, 'Bartonella', 24),
(5, 'Bordetella', 24),
(6, 'Bartonella henselae', 24),
(7, 'Azotobacter vinelandii', 24),
(8, 'Anaplasma phagocytophilum', 24),
(10, 'Brucella', 24),
(11, 'Bacillus subtilis', 24),
(12, 'Bordetella bronchiseptica', 24),
(13, 'Bordetella pertussis', 24),
(14, 'Borrelia burgdorfer', 24),
(15, 'Brucella abortus ', 24),
(16, 'Burkholderia  ', 24),
(18, 'Anaplasma Cannon', 24),
(19, 'Escherichia Coli', 24),
(20, 'Staphlococci Aureus', 24);

-- --------------------------------------------------------

--
-- Table structure for table `discs`
--

CREATE TABLE `discs` (
  `disc_id` int(50) NOT NULL,
  `abx_id` int(50) NOT NULL,
  `diameter` int(3) DEFAULT NULL,
  `dish_id` int(50) NOT NULL,
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
-- Table structure for table `flags`
--

CREATE TABLE `flags` (
  `disc_id` int(50) DEFAULT NULL,
  `colonies` tinyint(1) DEFAULT NULL,
  `double_innoc` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
-- Table structure for table `petri_dish`
--

CREATE TABLE `petri_dish` (
  `petri_dishID` int(100) NOT NULL,
  `dish_id` int(50) NOT NULL,
  `state` tinyint(1) DEFAULT '1',
  `exec_state` tinyint(1) NOT NULL DEFAULT '0',
  `sample_id` int(50) NOT NULL,
  `tested_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `endTime` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `pocket_state`
--

CREATE TABLE `pocket_state` (
  `pocket_id` int(1) NOT NULL,
  `state` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pocket_state`
--

INSERT INTO `pocket_state` (`pocket_id`, `state`) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1);

-- --------------------------------------------------------

--
-- Table structure for table `samples`
--

CREATE TABLE `samples` (
  `sample_id` int(50) NOT NULL,
  `accession_number` varchar(50) NOT NULL,
  `bacteria_id` int(50) NOT NULL,
  `note` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `zones`
--

CREATE TABLE `zones` (
  `discId` int(200) NOT NULL,
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
  ADD KEY `dish_id` (`dish_id`),
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
-- Indexes for table `flags`
--
ALTER TABLE `flags`
  ADD KEY `test_id` (`disc_id`);

--
-- Indexes for table `images`
--
ALTER TABLE `images`
  ADD PRIMARY KEY (`image_id`),
  ADD KEY `dish_id` (`sample_id`);

--
-- Indexes for table `petri_dish`
--
ALTER TABLE `petri_dish`
  ADD PRIMARY KEY (`petri_dishID`),
  ADD KEY `sample_id` (`sample_id`),
  ADD KEY `dish_id` (`dish_id`);

--
-- Indexes for table `pocket_state`
--
ALTER TABLE `pocket_state`
  ADD PRIMARY KEY (`pocket_id`);

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
  ADD PRIMARY KEY (`discId`),
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
-- AUTO_INCREMENT for table `petri_dish`
--
ALTER TABLE `petri_dish`
  MODIFY `petri_dishID` int(100) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `pocket_state`
--
ALTER TABLE `pocket_state`
  MODIFY `pocket_id` int(1) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `samples`
--
ALTER TABLE `samples`
  MODIFY `sample_id` int(50) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `zones`
--
ALTER TABLE `zones`
  MODIFY `discId` int(200) NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `discs`
--
ALTER TABLE `discs`
  ADD CONSTRAINT `discs_ibfk_3` FOREIGN KEY (`sample_id`) REFERENCES `samples` (`sample_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `discs_ibfk_4` FOREIGN KEY (`abx_id`) REFERENCES `antibiotics` (`abx_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `eucast`
--
ALTER TABLE `eucast`
  ADD CONSTRAINT `eucast_ibfk_1` FOREIGN KEY (`abx_id`) REFERENCES `antibiotics` (`abx_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `eucast_ibfk_2` FOREIGN KEY (`bacteria_id`) REFERENCES `bacteria` (`bacteria_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `flags`
--
ALTER TABLE `flags`
  ADD CONSTRAINT `flags_ibfk_1` FOREIGN KEY (`disc_id`) REFERENCES `discs` (`disc_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `images`
--
ALTER TABLE `images`
  ADD CONSTRAINT `images_ibfk_1` FOREIGN KEY (`sample_id`) REFERENCES `samples` (`sample_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `petri_dish`
--
ALTER TABLE `petri_dish`
  ADD CONSTRAINT `petri_dish_ibfk_1` FOREIGN KEY (`sample_id`) REFERENCES `samples` (`sample_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `samples`
--
ALTER TABLE `samples`
  ADD CONSTRAINT `samples_ibfk_1` FOREIGN KEY (`bacteria_id`) REFERENCES `bacteria` (`bacteria_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `zones`
--
ALTER TABLE `zones`
  ADD CONSTRAINT `zones_ibfk_1` FOREIGN KEY (`sample_id`) REFERENCES `samples` (`sample_id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
