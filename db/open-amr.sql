-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 09, 2019 at 04:08 PM
-- Server version: 5.7.27-0ubuntu0.18.04.1
-- PHP Version: 7.3.7-2+ubuntu18.04.1+deb.sury.org+1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `open-amr`
--

-- --------------------------------------------------------

--
-- Table structure for table `antibiotics`
--

CREATE TABLE `antibiotics` (
  `abx_id` int(50) NOT NULL,
  `abx_name` varchar(100) NOT NULL,
  `abx_content` varchar(20) NOT NULL,
  `abx_code` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `antibiotics`
--

INSERT INTO `antibiotics` (`abx_id`, `abx_name`, `abx_content`, `abx_code`) VALUES
(1, 'Ciprofloxacin', '5ug', 'CIP5'),
(2, 'Gentamicin', '10ug', 'GM10'),
(3, 'Meropenam', '10ug', 'MEM10'),
(4, 'Ampicillin', '10ug', 'AP10'),
(5, 'Ceftriaxone', '30ug', 'CRO30'),
(6, 'Chloramphenicol', '30ug', 'C30'),
(8, 'Trimethoprim-Sulfamethoxazole', '1.25-23.75ug', 'TS25'),
(9, 'Ceftazidime', '10ug', 'CAZ10'),
(11, 'Piperacillin-Tazobactam', '30-6ug', 'PTZ30'),
(12, 'Cefotaxime', '5ug', 'CTX5'),
(13, 'Cefoxitin', '30ug', 'FOX30'),
(15, 'Amoxicillin-clavulanic acid', '20-10ug', 'AMC30'),
(16, 'Clindamycin', '2ug', 'CD2'),
(17, 'Erythromycin', '15ug', 'E15'),
(18, 'Gentamicin', '10ug', 'GMN10'),
(19, 'Fuscidic Acid', '10ug', 'FC10'),
(20, 'Cefuroxime', '30ug', 'CXM30'),
(21, 'Tobramycin', '10ug', 'TN10'),
(22, 'Tetracycline', '10ug', 'T10'),
(23, 'Piperacillin-Tazobactam', '30-6ug', 'PTZ36'),
(26, 'Cefotaxime', '30ug', 'CTX30'),
(27, 'Azithromycin', '15ug', 'ATH15'),
(28, 'Linezolid', '10ug', 'LZD10'),
(29, 'Ceftazidime', '30ug', 'CAZ30'),
(33, 'Amoxicillin/Clavulanic Acid (Augumentin)', '30ug', 'AUG30'),
(34, 'Piperacillin-Tazobactam', '85ug', 'PTZ85'),
(36, 'Piperacillin-Tazobactam-CLSI', '100-10ug', 'PTZ110');

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
(12, 'Acinetobactor baumanni'),
(1, 'Acinetobactor sp.'),
(2, 'Escherichia Coli'),
(10, 'Gram negative rods'),
(9, 'Klebsiella pneumoniae'),
(8, 'Klebsiella sp.'),
(11, 'Proteus mirabilis'),
(3, 'Proteus sp.'),
(5, 'Proteus vulgaris'),
(13, 'Pseudomonas aeruginosa'),
(6, 'Pseudomonas sp.'),
(4, 'Staphylococcus Aureus');

-- --------------------------------------------------------

--
-- Table structure for table `discs`
--

CREATE TABLE `discs` (
  `disc_id` int(10) NOT NULL,
  `abx_id` int(10) NOT NULL,
  `diameter` float(5,2) DEFAULT NULL,
  `sample_id` int(10) NOT NULL,
  `test_on` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `discs`
--

INSERT INTO `discs` (`disc_id`, `abx_id`, `diameter`, `sample_id`, `test_on`) VALUES
(1, 26, 26.11, 1, '2019-08-09'),
(2, 5, 25.43, 1, '2019-08-09'),
(3, 13, 15.59, 1, '2019-08-09'),
(4, 6, 17.09, 1, '2019-08-09'),
(5, 3, 24.20, 1, '2019-08-09');

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
(1, 1, 1, 50, 21),
(2, 1, 2, 17, 17),
(3, 1, 3, 21, 15),
(4, 2, 4, 14, 14),
(5, 2, 5, 25, 22),
(6, 2, 6, 17, 17),
(7, 2, 1, 25, 22),
(8, 2, 8, 14, 11),
(9, 2, 2, 17, 14),
(10, 2, 9, 22, 19),
(11, 2, 11, 20, 17),
(12, 2, 12, 20, 17),
(14, 2, 13, 19, 19),
(15, 2, 3, 22, 16),
(16, 2, 15, 19, 19),
(17, 3, 4, 14, 14),
(18, 3, 5, 25, 22),
(19, 3, 1, 25, 22),
(20, 3, 8, 14, 11),
(21, 3, 2, 17, 14),
(22, 3, 9, 22, 19),
(23, 3, 11, 20, 17),
(24, 3, 12, 20, 17),
(25, 3, 13, 19, 19),
(26, 3, 3, 22, 16),
(27, 3, 15, 19, 19),
(28, 4, 6, 18, 18),
(30, 4, 15, 20, 18),
(31, 4, 2, 18, 18),
(32, 4, 18, 18, 18),
(33, 4, 13, 22, 22),
(34, 4, 19, 24, 24),
(35, 4, 8, 16, 16),
(36, 4, 17, 20, 18),
(37, 5, 15, 19, 16),
(38, 5, 5, 24, 22),
(39, 5, 1, 24, 22),
(40, 5, 2, 16, 14),
(41, 5, 18, 16, 14),
(42, 5, 11, 19, 17),
(43, 5, 23, 19, 17),
(44, 5, 12, 19, 17),
(45, 5, 3, 21, 16),
(46, 5, 13, 19, 19),
(47, 5, 6, 30, 30),
(48, 5, 4, 14, 14),
(49, 5, 20, 19, 19),
(50, 6, 1, 26, 26),
(51, 6, 2, 15, 15),
(52, 6, 3, 23, 18),
(53, 6, 21, 16, 16),
(54, 6, 22, 0, 0),
(55, 6, 8, 0, 0),
(56, 1, 15, 14, 11),
(57, 1, 21, 17, 17),
(58, 1, 22, 21, 15),
(59, 7, 24, 20, 15),
(60, 7, 25, 10, 5),
(61, 8, 4, 14, 14),
(62, 8, 6, 17, 17),
(63, 8, 1, 24, 22),
(64, 8, 8, 13, 11),
(65, 8, 18, 16, 14),
(66, 8, 9, 21, 19),
(67, 8, 23, 19, 17),
(68, 8, 5, 24, 22),
(69, 8, 26, 20, 17),
(70, 8, 20, 18, 18),
(71, 8, 3, 21, 16),
(72, 1, 8, 0, 0),
(73, 6, 9, 17, 17),
(74, 6, 23, 18, 18),
(75, 2, 26, 0, 0),
(76, 2, 20, 19, 19),
(77, 2, 18, 17, 14),
(78, 6, 13, 0, 0),
(79, 3, 6, 17, 17),
(80, 3, 26, 0, 0),
(81, 10, 1, 0, 0),
(82, 10, 2, 0, 0),
(83, 10, 18, 0, 0),
(84, 10, 3, 0, 0),
(85, 2, 28, 0, 0),
(86, 1, 13, 0, 0),
(87, 2, 29, 22, 19),
(88, 2, 17, 0, 0),
(89, 4, 5, 0, 0),
(90, 4, 1, 21, 21),
(91, 4, 11, 0, 0),
(92, 4, 3, 0, 0),
(93, 5, 1, 25, 22),
(94, 5, 8, 14, 11),
(95, 5, 17, 0, 0),
(96, 12, 17, 0, 0),
(97, 12, 5, 0, 0),
(98, 12, 1, 50, 21),
(99, 12, 8, 14, 11),
(100, 12, 2, 17, 17),
(101, 12, 11, 0, 0),
(102, 12, 3, 21, 15),
(103, 12, 15, 0, 0),
(104, 9, 5, 25, 22),
(105, 9, 1, 25, 22),
(106, 9, 8, 14, 11),
(107, 9, 2, 15, 15),
(108, 9, 11, 20, 17),
(109, 9, 3, 22, 16),
(110, 9, 15, 19, 19),
(111, 9, 17, 0, 0),
(112, 13, 5, 0, 0),
(113, 13, 1, 26, 26),
(114, 13, 8, 0, 0),
(115, 13, 2, 15, 15),
(116, 13, 11, 18, 18),
(117, 13, 3, 24, 18),
(118, 13, 15, 0, 0),
(119, 13, 17, 0, 0),
(120, 2, 33, 19, 19),
(121, 2, 34, 20, 17),
(123, 2, 36, 21, 17),
(124, 4, 16, 22, 19),
(125, 11, 5, 25, 22),
(126, 11, 1, 25, 22),
(127, 11, 3, 22, 16),
(128, 11, 33, 19, 19),
(129, 11, 2, 17, 14),
(130, 11, 36, 21, 17);

-- --------------------------------------------------------

--
-- Table structure for table `ping_pi`
--

CREATE TABLE `ping_pi` (
  `ping_id` tinyint(1) NOT NULL,
  `ping_state` tinyint(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ping_pi`
--

INSERT INTO `ping_pi` (`ping_id`, `ping_state`) VALUES
(1, 4);

-- --------------------------------------------------------

--
-- Table structure for table `samples`
--

CREATE TABLE `samples` (
  `sample_id` int(10) NOT NULL,
  `uniquecode` varchar(50) NOT NULL,
  `bacteria_id` int(10) NOT NULL,
  `test_on` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `samples`
--

INSERT INTO `samples` (`sample_id`, `uniquecode`, `bacteria_id`, `test_on`) VALUES
(1, '00000', 2, '2019-08-09');

-- --------------------------------------------------------

--
-- Table structure for table `temp_abx`
--

CREATE TABLE `temp_abx` (
  `id` int(2) NOT NULL,
  `abx_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `temp_abx`
--

INSERT INTO `temp_abx` (`id`, `abx_name`) VALUES
(1, 'CTX30'),
(2, 'CRO30'),
(3, 'FOX30'),
(4, 'C30'),
(5, 'MEM10');

-- --------------------------------------------------------

--
-- Table structure for table `teststatus`
--

CREATE TABLE `teststatus` (
  `id` int(1) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `locked` tinyint(1) DEFAULT '0',
  `started` tinyint(1) DEFAULT '0',
  `prog` tinyint(1) NOT NULL DEFAULT '0',
  `link` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `teststatus`
--

INSERT INTO `teststatus` (`id`, `status`, `locked`, `started`, `prog`, `link`) VALUES
(1, 2, 0, 1, 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `zones`
--

CREATE TABLE `zones` (
  `zone_id` int(10) NOT NULL,
  `disc` varchar(20) NOT NULL,
  `sample_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `zones`
--

INSERT INTO `zones` (`zone_id`, `disc`, `sample_id`) VALUES
(1, '(589, 978)', 1),
(2, '(963, 905)', 1),
(3, '(275, 666)', 1),
(4, '(982, 407)', 1),
(5, '(524, 298)', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `antibiotics`
--
ALTER TABLE `antibiotics`
  ADD PRIMARY KEY (`abx_id`),
  ADD UNIQUE KEY `abx_code` (`abx_code`);

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
-- Indexes for table `ping_pi`
--
ALTER TABLE `ping_pi`
  ADD PRIMARY KEY (`ping_id`);

--
-- Indexes for table `samples`
--
ALTER TABLE `samples`
  ADD PRIMARY KEY (`sample_id`),
  ADD KEY `bacteria_id` (`bacteria_id`);

--
-- Indexes for table `temp_abx`
--
ALTER TABLE `temp_abx`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `teststatus`
--
ALTER TABLE `teststatus`
  ADD PRIMARY KEY (`id`);

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
  MODIFY `abx_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;
--
-- AUTO_INCREMENT for table `bacteria`
--
ALTER TABLE `bacteria`
  MODIFY `bacteria_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT for table `discs`
--
ALTER TABLE `discs`
  MODIFY `disc_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `eucast`
--
ALTER TABLE `eucast`
  MODIFY `eu_id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=131;
--
-- AUTO_INCREMENT for table `ping_pi`
--
ALTER TABLE `ping_pi`
  MODIFY `ping_id` tinyint(1) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `samples`
--
ALTER TABLE `samples`
  MODIFY `sample_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `temp_abx`
--
ALTER TABLE `temp_abx`
  MODIFY `id` int(2) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `zones`
--
ALTER TABLE `zones`
  MODIFY `zone_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
