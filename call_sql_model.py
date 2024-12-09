#pip install ollama


import ollama
import sys
from ollama import chat
from ollama import ChatResponse

import difflib

replace_dict = {
    "no" : "N",
    "NO" : "N",
    "yes" : "Y",
    "YES" : "Y",
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'DC': 'District of Columbia',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah', 
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    }

def correct_model_output(output):
    for replace, goal in replace_dict.items():
       output = output.replace("'" + replace + "'", "'"  + goal + "'" ) #need to surrounding ticks or elese it will replace things like CO in COUNT
    
    output = output.replace("```", "") #get rid of the trailing backticks
    return output

def get_response(prompt):
   response: ChatResponse = chat(model='sqlcoder', messages=[
      {
          'role': 'user',
          'content': prompt,
      },
   ])
   return response['message']['content']

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
- Only answer the question asked and only output the SQL query

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
       FOREIGN KEY (frid) REFERENCES gun_range(rid)
);


CREATE TABLE facility_instance (
       iid	 INTEGER NOT NULL,
       shooting_type		VARCHAR(65532) NOT NULL,
       maximum_distance		INTEGER NOT NULL,
       FOREIGN KEY (iid) REFERENCES gun_range(rid)
);


CREATE TABLE competition (
       rcid 	 INTEGER NOT NULL,
       competition_type		VARCHAR(65532) NOT NULL,
       FOREIGN KEY (rcid) REFERENCES gun_range(rid)
);


CREATE TABLE other_options (
       orid 	 INTEGER NOT NULL,
       option_type		VARCHAR(65532) NOT NULL,
       FOREIGN KEY (orid) REFERENCES gun_range(rid)
);

-- rid can be joined with frid
-- frid can be joined with iid
-- rid can be joined with orid
-- rid can be joined with rcid
--- state from gun_range can be joined with state from location
--- the opposite of indoors is outdoors, so indoors with a value of 'N' means outdoors and with a vlaue of 'Y' means indoors
--- postcode cannot be joined with anything
--- shooting_types include handgun, rifle, shotgun, center-fire rifle, and smallbore rifle
--- non-member events are the same as public events, and non-member events does not mean that members_only = 'N'

### Response:
Based on your instructions, here is the SQL query I have generated to answer the question `{sys.argv[1]}`:
```sql
"""

'''maybe do a few tries? not sure how best to compare to natural language though
responses = []
while(len(responses) < 3):
   response = get_response(prompt)
   if(response != ''):
      responses.append(response)

best_score = 0
best_response = ''
for i in range(len(responses)):
    score = difflib.SequenceMatcher(None, sys.argv[1], responses[i]).ratio()
    if(score > best_score):
       best_score = score
       best_response = responses[i]

sql = best_response
'''

response = ''

while(response == ''): #prevent empty response
   response = get_response(prompt)

sql = response

#sql = "SELECT COUNT(DISTINCT gr.rid) AS number_of_ranges FROM gun_range gr JOIN facility_details fd ON gr.rid = fd.frid JOIN location l ON fd.indoor_accessible = 'Y' AND l.state = 'IL' WHERE gr.nssf_member = 'Y' AND gr.handicap_accessible = 'Y' AND gr.membership_available = 'Y' AND gr.public_events = 'Y'; ```"
sql = correct_model_output(sql)

print(sql)


#print(prompt)
# or access fields directly from the response object

#print(response.message.content)



