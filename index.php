<?php

# PHP+SQLite3 code from: http://www.tutorialspoint.com/sqlite/sqlite_php.htm

   class MyDB extends SQLite3
   {
      function __construct()
      {
         $this->open('/home/pi/OBD2SDK_Python/gps.db', SQLITE3_OPEN_READONLY);
      }
   }

   $db = new MyDB();
   if(!$db){
      echo $db->lastErrorMsg();
   } else {
      #echo "Opened database successfully\n";
   }

   $sql = "select count(*) as count from gps;";

$db->busyTimeout(5000);

try {
   $ret = $db->query($sql);
}

catch(Exception $e) {
  echo 'Exception Message: ' .$e->getMessage();
	return false;
}
	if($db->lastErrorMsg() <> "not an error"){
		echo $db->lastErrorMsg();
		return false;
	}

	#if (!$ret){
	#	return false;
	#}

   while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
      #echo "COUNT = ". $row['count'] . "\n";
	$records=$row['count'];
  }
   $db->close();
?>


<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
        <title>Black Box Pi - Status Page</title>
</head>
<body>
<h1>Black Box Pi</h1>
Raspberry Pi status page for the <a href="http://www.blackboxpi.com">Black Box Pi</a> software. 
<h2>Status</h2>
GPS records to sync: <?php echo($records);?><br>
<br>
GPS records are stored locally on the Pi in a database. The daemon <i>gpssync</i> syncs these to the Black Box Pi server any time the Pi is connected to the internet.  
</body>
</html>
