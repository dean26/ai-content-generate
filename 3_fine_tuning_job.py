import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
file_id = os.getenv('FILE_ID')

response = openai.FineTuningJob.create(training_file=file_id, model="gpt-3.5-turbo")
print(response)