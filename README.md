## How to Run This Project
- Make sure you have Xampp 
- Clone repo into C:/xampp/htdocs
- In settings.json of vscode, set: "php.validate.executablePath": "C:/xampp/php/php.exe" (not sure if this is necessary, but if it is VSCode will prompt you)
- pip install ollama to the interpreter you are using
- Open Xampp Control Panel app
- In the Control Panel, in the MySQL row, click admin. This will open phpMyAdmin
- Click the Databases tab. Under create new database, enter the database name in the index.php file and hit create
- Click the created database. Click the SQL tab. Enter the DDL SQL queries into the box and click "Go"
- Run Apache from Xampp Control Panel 
- Run MySql from Xampp Control Panel 
- Navigate to: http://localhost/gun-range-website/index.html

## Notes
- Not currently using main.ts
