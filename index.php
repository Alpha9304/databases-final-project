<head>
  <title>Gun Range Results</title>
  <link href="./src/output.css" rel="stylesheet">
 </head>
 <body class = "bg-amber-100">
    <h1 class="text-4xl font-bold text-center">
        Search Results
    </h1>
  <?php
    
    // PHP code just started

    // display errors
    ini_set('error_reporting', E_ALL);
    ini_set('display_errors', true);
    

    //enable exceptions
    mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

    $db = mysqli_connect("localhost", "root", ""); 
    // ********* Remember to use your MySQL username and password here ********* //

    if (!$db) {
      echo "Connection failed!";
    } else {
      $query = "";

      if (isset($_POST['sql_query'])) {
        //case where user chooses to edit the query if there are errors
        $query = $_POST['sql_query'];
        echo $query;
      } else {
        echo "Natural langauge";
        echo "Before calling Python file";

        echo "<br>";

        //will be user input in future
        //$question = "How many gun ranges in Illinois provide facilities for handguns, rifles, and are certified by the NSSF?";

        $question = $_POST['query'];
        
        $escaped_question = escapeshellarg($question);

        
        
        while($query == "") { 
          $query = shell_exec("python call_sql_model.py " .$escaped_question);
        }

        echo "Output is: ". $query;
        echo "<br>";

        echo "After calling Python file";
        echo "<br>";

      }

      mysqli_select_db($db, "cs415_fa24_sola_alex_db");

      try {
        //$throwing_result = mysqli_query($db, "SELECT * FROM Dne");
        $result = mysqli_query($db, $query);
        

        if (!$result) {

          echo "Query failed!\n";
          print mysqli_error($db);
        
        } else {
        
          echo "<table border=1>\n";
          echo "<tr><td>CID</td><td>CName</td></tr>\n";

          while ($myrow = mysqli_fetch_array($result)) {
            printf("<tr><td>%s</td><td>%s</td></tr><tr><td>%s</td><td>%s</td></tr>\n", $myrow["name"], $myrow["phone"], $myrow["email"], $myrow["address"]);
          }
        
          echo "</table>\n";
        
        }
      } catch (mysqli_sql_exception $e) {
        echo "Something went wrong: ".$e; //show users this in a different place for better design
      }     
    }
  ?>
  <div id = "re-query_area" class = "mt-8 p-2">
        <p class = "text-xl">Edit and retry your query:</p>
        <form action="index.php" method="post" accept-charset="utf-8">
            <textarea class = "outline rounded" name="sql_query" rows="4" cols="50"><?php echo htmlspecialchars($query, ENT_QUOTES, 'UTF-8'); ?></textarea>
        <input type="Submit" class = "outline rounded bg-white mb-4 ml-2 p-1">
        </form>
  </div>
</body>
