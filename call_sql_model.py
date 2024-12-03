#pip install ollama

import ollama
import sys
from ollama import chat
from ollama import ChatResponse

ollama.pull('sqlcoder')


response: ChatResponse = chat(model='sqlcoder', messages=[
  {
    'role': 'user',
    'content': sys.argv[1],
  },
])

print(response['message']['content'])
# or access fields directly from the response object

#print(response.message.content)



