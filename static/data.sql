CREATE TABLE IF NOT EXISTS `strawhats` (
  `id` tinyint(4) NOT NULL auto_increment,
  `name` varchar(25) NOT NULL,
  `position` varchar(25) NOT NULL,
  `ambition` text NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;


INSERT INTO `strawhats` (`id`, `name`, `position`, `ambition`) VALUES
(1, 'Monkey D Luffy', 'Captain', 'I Will become the pirate king'),
(2, 'Roronoa zoro', 'Swordman', 'Become greatet swordman'),
(3, 'Sanji', 'Cook', 'Find all blue'),
(4, 'Nami', 'Navigator', 'Draw map of the world'),
(5, 'Usopp', 'Sniper', 'Become greatest warrior');
