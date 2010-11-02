<?php
	$conn = mysql_connect("localhost", "root", "") or die (mysql_error ());
	$db = mysql_select_db ("extjs") or die (mysql_error ());
	
	$result=mysql_query ("SELECT * FROM strawhats") or die (mysql_error ());
	
	$data = array();
	
	while ($row=mysql_fetch_object($result))
	{
		$data [] = $row;
	}
	
	echo json_encode($data);
?>