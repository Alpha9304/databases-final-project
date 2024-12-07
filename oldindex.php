<body>
  <?php

  echo "Before calling Python file";

  echo "<br>";

  //will be user input in future
  $instructions = "### Instructions:\nYour task is to convert a question into a SQL query, given a Postgres database schema.\nAdhere to these rules: \n- **Deliberately go through the question and database schema word by word** to appropriately answer the question\n- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.\n- When creating a ratio, always cast the numerator as float\n- Do not abbreviate state names; they should be strings longer than 2 characters\n- Try your hardest to avoid subqueries in your SQL queries\n";
  $in = "### Input:\nGenerate a SQL query that answers the question";
  $question = "`How many gun ranges in Illinois provide facilities for handguns, rifles, and are certified by the NSSF?`.\n";
  $table = "This query will run on a database whose schema is represented in this string:\nCREATE TABLE gun_range (\n   rid 	       INTEGER PRIMARY KEY NOT NULL,\n  name		VARCHAR(65532) NOT NULL,\n   phone		INTEGER NOT NULL,\n   nssf_member   VARCHAR(1),\n  email		VARCHAR(65532),\n   state    VARCHAR(65532) NOT NULL\n);\n\nCREATE TABLE location (\n   postcode		VARCHAR(11) PRIMARY KEY NOT NULL,\nstate		VARCHAR(65532) NOT NULL,\n   city		VARCHAR(65532) NOT NULL,\n  country		VARCHAR(65532) NOT NULL,\n    address  VARCHAR(65532) NOT NULL,\n    distance_from_user    INTEGER NOT NULL\n);\n\nCREATE TABLE facility_details (\n    frid 	       INTEGER NOT NULL,\n    indoors       VARCHAR(1) NOT NULL,\n    members_only		VARCHAR(1) NOT NULL,\n    public_events   VARCHAR(1) NOT NULL,\nmembership_available		VARCHAR(1) NOT NULL,\nhandicap_accessible    VARCHAR(1) NOT NULL,\nFOREIGN KEY (frid) REFERENCES gun_Range(rid)\n);\n\nCREATE TABLE facility_instance (\n    iid	 INTEGER NOT NULL,\n    Shooting_Type		VARCHAR(65532) NOT NULL,\n    Maximum_Distance		INTEGER NOT NULL,\n    FOREIGN KEY (iid) REFERENCES gun_Range(rid)\n);\n\nCREATE TABLE competition (\n    rcid 	 INTEGER NOT NULL,\n    competition_type		VARCHAR(65532) NOT NULL,\n    FOREIGN KEY (rcid) REFERENCES gun_Range(rid)\n);\n\nCREATE TABLE Competition (\n     orid 	 INTEGER NOT NULL,\n      option_type		VARCHAR(65532) NOT NULL,\n     FOREIGN KEY (orid) REFERENCES gun_Range(rid)\n);\n-- rid can be joined with frid\n-- frid can be joined with iid\n-- rid can be joined with orid\n-- rid can be joined with rcid\n--- state from gun_range can be joined with state from location\n--- the opposite of indoors is outdoors, so indoors with a value of 'N' means outdoors and with a vlaue of 'Y' means indoors\n--- postcode cannot be joined with anything\n";
  $response = "### Response:\nBased on your instructions, here is the SQL query I have generated to answer the question";
  $end = "```sql";

  $data = $instructions.$in.$question.$table.$response.$question.$end;

  $output = shell_exec("python call_sql_model.py " .$data);

  echo "Output is: ".$output;
  echo "<br>";

  echo "After calling Python file";

  /*will it connect from here or do I have to use the school folder?
  // PHP code just started

  ini_set('error_reporting', E_ALL);
  ini_set('display_errors', true);
  // display errors

  $db = mysqli_connect("dbase.cs.jhu.edu", "cs415_fa24_gbemisola", "OSEkPJSjqF");
  // ********* Remember to use your MySQL username and password here ********* //

  if (!$db) {

    echo "Connection failed!";

  } else {

    $pass = $_POST['pass'];
    $s_ssn = $_POST['s_ssn'];
    $assign = $_POST['assign'];
    $new_score = $_POST['new_score'];

    if (!is_numeric($s_ssn)) {
      echo "<h2>Error</h2>";
      echo "<table border=1>\n";
      echo "<tr><td>Error Message</td></tr>\n";
      echo "<tr><td>Invalid last 4 digits of SSN</td></tr>\n";
    } else if (!is_numeric($new_score)) {
      echo "<h2>Error</h2>";
      echo "<table border=1>\n";
      echo "<tr><td>Error Message</td></tr>\n";
      echo "<tr><td>Score must be a numeric value</td></tr>\n";
    } else {
      mysqli_select_db($db, "cs415_fa24_gbemisola_db");
      // ********* Remember to use the name of your database here ********* //
      
      $stmt1 = mysqli_prepare($db, "CALL ShowRawScoresPermitted('".$pass."', '".$s_ssn."')");
      $stmt2 = mysqli_prepare($db, "CALL ChangeScoresShow('".$pass."', '".$s_ssn."', '".$assign."', '".$new_score."')");

      mysqli_stmt_execute($stmt1);
      $result1 = mysqli_stmt_get_result($stmt1); 
      mysqli_stmt_close($stmt1);

      mysqli_stmt_execute($stmt2);
      $result2 = mysqli_stmt_get_result($stmt2);
      mysqli_stmt_close($stmt2);

      if (!$result1) {
        echo "Query failed 1!\n";
        print mysqli_error($db);

      } else if (!$result2) {
        echo "Query failed 2!\n";
        print mysqli_error($db);
      } else {

        $colCount1 = mysqli_num_fields($result1);
        $colCount2 = mysqli_num_fields($result2);

        if($colCount1 === 1 ) {
          echo "<h2>Error</h2>";
          echo "<table border=1>\n";
          echo "<tr><td>Error Message</td></tr>\n";

          while ($myrow = mysqli_fetch_array($result1)) {
            printf("<tr><td>%s</td></tr>\n", 
            $myrow["Error Message"]);
          }

          echo "</table>\n";
        } else if ($colCount2 === 1) {
          echo "<h2>Error</h2>";
          echo "<table border=1>\n";
          echo "<tr><td>Error Message</td></tr>\n";

          while ($myrow = mysqli_fetch_array($result2)) {
            printf("<tr><td>%s</td></tr>\n", 
            $myrow["Error Message"]);
          }

          echo "</table>\n";
        } else {

          echo "<h2>Before Change</h2>";
          echo "<table border=1>\n";
          echo "<tr><td>SSN</td><td>LName</td><td>FName</td><td>Section</td><td>HW1</td><td>HW2a</td><td>HW2b</td><td>Midterm</td><td>HW3</td><td>FExam</td></tr>\n";

          while ($myrow = mysqli_fetch_array($result1)) {
            printf("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n", 
            $myrow["SSN"], $myrow["LName"], $myrow["FName"], $myrow["Section"], $myrow["HW1"], $myrow["HW2a"], $myrow["HW2b"], $myrow["Midterm"], $myrow["HW3"], $myrow["FExam"]);
          }

          echo "</table>\n";

          //
          
          //
          echo "<h2> After Change </h2>";
          echo "<table border=1>\n";
          echo "<tr><td>SSN</td><td>LName</td><td>FName</td><td>Section</td><td>HW1</td><td>HW2a</td><td>HW2b</td><td>Midterm</td><td>HW3</td><td>FExam</td></tr>\n";

          while ($myrow = mysqli_fetch_array($result2)) {
            printf("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n", 
            $myrow["SSN"], $myrow["LName"], $myrow["FName"], $myrow["Section"], $myrow["HW1"], $myrow["HW2a"], $myrow["HW2b"], $myrow["Midterm"], $myrow["HW3"], $myrow["FExam"]);
          }

          echo "</table>\n";
        }
      }
    }

  }

  // PHP code about to end
  */
  ?>
</body>
