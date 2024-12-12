#pip install ollama


import ollama
import sys
from ollama import chat
from ollama import ChatResponse
import numpy as np

import difflib

straight_swap_dict =  { #is he going to unify the yes/no to the schema or leave it?
    "no" : "N",
    "NO" : "N",
    "yes" : "Y",
    "YES" : "Y"
}

state_dict = {
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
    for abbrev, state in state_dict.items():
       output = output.replace("'" + state + "'", "'"  + abbrev + "'" ) #need to surrounding ticks or elese it will replace things like CO in COUNT
    
    for replace, goal in straight_swap_dict.items(): #ended up seprating them because they are actually abbreviated states
        output = output.replace("'" + replace + "'", "'"  + goal + "'" ) 

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

def cosine_similarity_mine(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    return dot_product / (magnitude_a * magnitude_b)

ollama.pull('sqlcoder')
ollama.pull("all-minilm")

prompt = f""" 
### Instructions:
Your task is to convert a question into a SQL query, given a Postgres database schema.
Adhere to these rules:
- **Deliberately go through the question and database schema word by word** to appropriately answer the question
- **Use Table Aliases** to prevent ambiguity. For example, `SELECT table1.col1, table2.col1 FROM table1 JOIN table2 ON table1.id = table2.id`.
- Do not abbreviate state names; they should be strings longer than 2 characters
- Try your hardest to avoid subqueries in your SQL queries, and make queries as short as possible
- Only answer the question asked and only output the SQL query

### Input:
Generate a SQL query that answers the question `{sys.argv[1]}.`
This query will run on a database whose schema is represented in this string:
CREATE TABLE gun_range (
       rid 	       INTEGER PRIMARY KEY NOT NULL,
       name		VARCHAR(8000) NOT NULL,
       phone		INTEGER NOT NULL,
       nssf_member   VARCHAR(1),
       email		VARCHAR(8000),
       address    VARCHAR(255) NOT NULL UNIQUE
);


CREATE TABLE location (
       address  VARCHAR(255) PRIMARY KEY NOT NULL,
       state		TEXT(8000) NOT NULL,
       postcode	VARCHAR(11) NOT NULL,
       city		TEXT(8000) NOT NULL,
       country		TEXT(8000) NOT NULL,
       FOREIGN KEY (address) REFERENCES gun_range(address)
);


CREATE TABLE facility_details (
       frid 	       INTEGER PRIMARY KEY NOT NULL,
       indoors       VARCHAR(1) NOT NULL,
       members_only		VARCHAR(1) NOT NULL,
       public_events   VARCHAR(1) NOT NULL,
       membership_available		VARCHAR(1) NOT NULL,
       handicap_accessible    VARCHAR(1) NOT NULL,
       FOREIGN KEY (frid) REFERENCES gun_range(rid)
);


CREATE TABLE gun_type (
       gid	 INTEGER NOT NULL,
       type		VARCHAR(8000) NOT NULL,
       FOREIGN KEY (gid) REFERENCES gun_range(rid)
);

CREATE TABLE distance (
       did	 INTEGER NOT NULL,
       type		VARCHAR(8000) NOT NULL,
       FOREIGN KEY (did) REFERENCES gun_range(rid)
);


CREATE TABLE competition (
       rcid 	 INTEGER NOT NULL,
       competition_type		VARCHAR(8000) NOT NULL,
       FOREIGN KEY (rcid) REFERENCES gun_range(rid)
);


CREATE TABLE other_options (
       orid 	 INTEGER NOT NULL,
       option_type		VARCHAR(8000) NOT NULL,
       FOREIGN KEY (orid) REFERENCES gun_range(rid)
);

-- rid can be joined with frid
-- frid can be joined with iid
-- rid can be joined with orid
-- rid can be joined with rcid
--- state from gun_range can be joined with state from location
--- indoors with a value of 'N' means outdoors and indoors with a value of 'Y' means indoors
--- postcode cannot be joined with anything
--- shooting_types include handgun, rifle, shotgun, center-fire rifle, and smallbore rifle
--- non-member events are the same as public events, and non-member events does not mean that members_only = 'N'

### Response:
Based on your instructions, here is the SQL query I have generated to answer the question `{sys.argv[1]}`:
```sql
"""

#do a few tries and get best
responses = []
while(len(responses) < 3):
   response = get_response(prompt)
   if(response != ''):
      responses.append(response)

best_score = 0
best_response = ''
for i in range(len(responses)):
    res_em = ollama.embeddings(model='all-minilm', prompt=responses[i])
    nl_em = ollama.embeddings(model='all-minilm', prompt=sys.argv[1])
    score = cosine_similarity_mine(np.array(res_em['embedding']).reshape(1,-1), np.array(nl_em['embedding']).reshape(-1,1))
    if(score > best_score):
       best_score = score
       best_response = responses[i]

sql = best_response

'''
response = ''

while(response == ''): #prevent empty response, not working? when it is empty, it is not even going throught python file?? I think fixed with loop in php...
   response = get_response(prompt)

sql = response
'''

#sql = "SELECT COUNT(DISTINCT gr.rid) AS number_of_ranges FROM gun_range gr JOIN facility_details fd ON gr.rid = fd.frid JOIN location l ON fd.indoor_accessible = 'Y' AND l.state = 'IL' WHERE gr.nssf_member = 'Y' AND gr.handicap_accessible = 'Y' AND gr.membership_available = 'Y' AND gr.public_events = 'Y'; ```"
sql = correct_model_output(sql)

print(sql)


#print(prompt)
# or access fields directly from the response object

#print(response.message.content)



