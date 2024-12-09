<head>
  <title>Gun Range Results</title>
 </head>
 <body>
  <?php

  // PHP code just started

  ini_set('error_reporting', E_ALL);
  ini_set('display_errors', true);
  // display errors

  $db = mysqli_connect("localhost", "root", ""); 
  // ********* Remember to use your MySQL username and password here ********* //

  if (!$db) {
    echo "Connection failed!";
  }

  mysqli_select_db($db, "cs415_fa24_sola_alex_db");

  echo "Before calling Python file";

  echo "<br>";

  //will be user input in future
  $question = "How many gun ranges in Illinois provide facilities for handguns, rifles, and are certified by the NSSF?";

  $escaped_question = escapeshellarg($question);

  $output = shell_exec("python call_sql_model.py " .$escaped_question);

  echo "Output is: ". $output;
  echo "<br>";

  echo "After calling Python file";
  echo "<br>";

  ?>
</body>
