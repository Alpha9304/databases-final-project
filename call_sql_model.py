#pip install ollama

import ollama
import sys
from ollama import chat
from ollama import ChatResponse

ollama.pull('sqlcoder')

prompt = f""" 
### Instructions:
Your task is to convert a question into a SQL query, given a Postgres database schema.
Adhere to these rules:
- **Deliberately go through the question and database schema word by word** to appropriately answer the question
- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
- When creating a ratio, always cast the numerator as float
- Do not abbreviate state names; they should be strings longer than 2 characters
- Try your hardest to avoid subqueries in your SQL queries

### Input:
Generate a SQL query that answers the question `{sys.argv[1]}.`
This query will run on a database whose schema is represented in this string:
CREATE TABLE gun_range (
       rid 	       INTEGER PRIMARY KEY NOT NULL,
       name		VARCHAR(65532) NOT NULL,
       phone		INTEGER NOT NULL,
       nssf_member   VARCHAR(1),
       email		VARCHAR(65532),
       state    VARCHAR(65532) NOT NULL
);


CREATE TABLE location (
       postcode		VARCHAR(11) PRIMARY KEY NOT NULL,
       state		VARCHAR(65532) NOT NULL,
       city		VARCHAR(65532) NOT NULL,
       country		VARCHAR(65532) NOT NULL,
       address  VARCHAR(65532) NOT NULL,
       distance_from_user    INTEGER NOT NULL
);


CREATE TABLE facility_details (
       frid 	       INTEGER NOT NULL,
       indoors       VARCHAR(1) NOT NULL,
       members_only		VARCHAR(1) NOT NULL,
       public_events   VARCHAR(1) NOT NULL,
       membership_available		VARCHAR(1) NOT NULL,
       handicap_accessible    VARCHAR(1) NOT NULL,
       FOREIGN KEY (frid) REFERENCES gun_Range(rid)
);


CREATE TABLE facility_instance (
       iid	 INTEGER NOT NULL,
       Shooting_Type		VARCHAR(65532) NOT NULL,
       Maximum_Distance		INTEGER NOT NULL,
       FOREIGN KEY (iid) REFERENCES gun_Range(rid)
);


CREATE TABLE competition (
       rcid 	 INTEGER NOT NULL,
       competition_type		VARCHAR(65532) NOT NULL,
       FOREIGN KEY (rcid) REFERENCES gun_Range(rid)
);


CREATE TABLE Competition (
       orid 	 INTEGER NOT NULL,
       option_type		VARCHAR(65532) NOT NULL,
       FOREIGN KEY (orid) REFERENCES gun_Range(rid)
);

-- rid can be joined with frid
-- frid can be joined with iid
-- rid can be joined with orid
-- rid can be joined with rcid
--- state from gun_range can be joined with state from location
--- the opposite of indoors is outdoors, so indoors with a value of 'N' means outdoors and with a vlaue of 'Y' means indoors
--- postcode cannot be joined with anything


### Response:
Based on your instructions, here is the SQL query I have generated to answer the question `{sys.argv[1]}`:
```sql
"""


response: ChatResponse = chat(model='sqlcoder', messages=[
  {
    'role': 'user',
    'content': prompt,
  },
])

print(response['message']['content'])


#print(prompt)
# or access fields directly from the response object

#print(response.message.content)



