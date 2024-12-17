<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Gun Range Results</title>
  <link href="./src/output.css" rel="stylesheet">
  <link rel="icon" href="./public/icon.png" />
 </head>
 <body class = "bg-amber-100">
  <nav class="bg-emerald-800 rounded-sm border-gray-200 flex items-center justify-between">
          <img src="./public/icon.png" style="width: 50px; height: 50px;" class="ml-2 mb-4" alt="Gun Range Search Site Logo" />
          <div class="hidden w-full md:block md:w-auto" id="navbar-default">
              <ul class="font-medium flex flex-row p-4 md:p-0 ml-4 mr-16 mt-12">
              <li>
                  <a href="http://localhost/gun-range-website/index.html" class="block py-2 px-3 text-white hover:underline" aria-current="page">Home</a>
              </li>
              </ul>
          </div>
          </div>
    </nav>
    <h1 class="text-6xl font-bold italic font-mono text-center text-yellow-950 pt-4">
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
        //echo $query;
      } else {
  
        //will be user input in future
        //$question = "How many gun ranges in Illinois provide facilities for handguns, rifles, and are certified by the NSSF?";

        $question = $_POST['query'];
        
        $escaped_question = escapeshellarg($question);

        
        
        while($query == "") { 
          $query = shell_exec("python call_sql_model.py " .$escaped_question);
        }

      }

      mysqli_select_db($db, "cs415_fa24_sola_alex_db");

      try {
        //$throwing_result = mysqli_query($db, "SELECT * FROM Dne");
        $result = mysqli_query($db, $query);
        

        if (!$result) {

          echo "Query failed!\n";
          print mysqli_error($db);
        
        } else {
 
          if($result->num_rows === 0) {
            echo "No results";
          } else {
            
            $get_cols = mysqli_fetch_assoc($result);
            $col_names = array_keys($get_cols);

            echo "<table class='ml-2 mt-2 border-2 border-black shadow-lg' style='border: border-collapse: collapse; margin-left: auto; margin-right: auto; width: 50%;'>\n"; //why is the table not showing
            echo "<tr>";
            foreach($col_names as $name) {
              echo "<th style='border: 1px solid black; padding: 8px;'>" . $name . "</th>";
            }
            echo "</tr>\n";

            // Reset the result pointer
            mysqli_data_seek($result, 0);
          
            while ($myrow = mysqli_fetch_array($result)) {
              echo "<tr>";
              foreach($col_names as $name) {
                echo "<td style='border: 1px solid black; padding: 8px;'>" . $myrow[$name] . "</td>";
              }
              echo "</tr>\n";
            }
          
            echo "</table>\n";
          }
        
        }
      } catch (mysqli_sql_exception $e) {
        $no_stack_trace = trim(explode('Stack trace:', $e)[0]);
        $no_path = trim(explode('in C:', $no_stack_trace)[0]);
        $just_info = trim(explode(':', $no_path)[1]);
        echo "<div class = 'ml-2 mt-4 font-bold text-center'>";
        echo "<p>Something went wrong. Please refer to this error to edit your query: </p>";
        echo "<p> ". $just_info . "</p>";
        echo "</div>";
      }     
    }
  ?>
  <div class = "flex relative">
    <div id = "re-query_area" class = "mt-8 ml-8 p-2">
          <p class = "text-xl font-bold italic mb-2">Edit and retry your query:</p>
          <form action="index.php" method="post" accept-charset="utf-8" class="inline-flex items-end space-x-4">
              <textarea class = "outline rounded shadow-lg" name="sql_query" rows="9" cols="50"><?php echo htmlspecialchars($query, ENT_QUOTES, 'UTF-8'); ?></textarea>
          <input type="Submit" class = "outline rounded bg-white p-2">
          </form>
    </div>
    <!--it messes up join keys the most, so give the user this to help-->
    <div id = "hint-box" class = "border border-black border-2 rounded-lg bg-white w-80 ml-96 pl-8 pr-8 pb-2 mt-36 mb-8 absolute right-5 shadow-lg">
      <h3 class = "font-bold italic text-center">Helpful Info (Joinable Keys): </h3>
      <ul class="font-medium flex flex-col list-disc">
        <li>gun_range table key: rid</li>
        <li>location table key: address (foreign) </li>
        <li>facility_details key: frid (foreign) </li>
        <li>gun_type table key: gid (foreign) </li>
        <li> (shooting) distance table key: did (foreign) </li>
        <li>gun_type types are plural (eg. handguns)</li>
      </ul>
    </div>
  </div>

</body>
