## How to Run This Project
- Make sure you have Xampp 
- Put files in "databases-final-project-main" (or clone the repo) into C:/xampp/htdocs/gun-range-website (make the gun-range-website folder in htdocs to put the cloned files into)
- In settings.json of vscode, set: "php.validate.executablePath": "C:/xampp/php/php.exe" (not sure if this is necessary, but if it is VSCode will prompt you)
- Run "pnpm install" in the terminal
- run pip install ollama for the interpreter you are using in the terminal
- Open the Xampp Control Panel app
- Run Apache from Xampp Control Panel 
- Run MySql from Xampp Control Panel (If MySQL will not run, follow the steps to fix it here in the verified answer with high votes (except do not copy the db files, re-run the DDL lines): https://stackoverflow.com/questions/18022809/how-can-i-solve-error-mysql-shutdown-unexpectedly)
- In the Control Panel, in the MySQL row, click Admin. This will open phpMyAdmin
- In phpMyAdmin: Click the Databases tab. Under create new database, enter the database name matching the one in the index.php file and hit create
- Click the created database. Click the SQL tab. Enter the DDL SQL queries into the box and click "Go"
- Copy all the content of insert_ranges.sql and paste it into the SQL query box (same place you entered the DDL) and click "Go"
- Navigate to: http://localhost/gun-range-website/index.html

## To View Commit History
- View the GitHub repo: https://github.com/Alpha9304/databases-final-project

## Notes
- Not currently using main.ts
