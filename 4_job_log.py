import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
job_id = os.getenv('JOB_ID')

print(openai.FineTuningJob.list_events(id=job_id, limit=10))