import openai
import os
from dotenv import load_dotenv
import time

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def create_content(keywords, article_length = 6000):
    keywords = ', '.join(keywords)
    total_text = ''

    dialogue = [
        {'role': 'system',
         'content': 'You are a helpful assistant specialized in generating SEO-optimized content for blogs.'},
        {'role': 'user',
         'content': f'I own a company and I need an SEO-optimized article for my website. The article should be about {article_length} characters long and include the keywords {keywords}. Return the article and end with "##STOP##" when it\'s complete.'}
    ]

    stop_phrase = "##STOP##"
    while stop_phrase not in total_text:
        time.sleep(1.5)
        response = openai.ChatCompletion.create(
            model=os.getenv('NEW_MODEL_NAME'),
            messages=dialogue,
            temperature=0.7,
            max_tokens=2000
        )

        part_of_article = response.choices[0].message['content'].strip()

        total_text += part_of_article

        if len(total_text) < article_length:
            dialogue.append({
                "role": "user",
                "content": "Please continue the article."
            })
        else:
            dialogue.append({
                "role": "user",
                "content": "End your article in a coherent and meaningful way. Use one paragraph and a maximum of 500 characters."
            })

    total_text = total_text.replace(stop_phrase, '')

    return {'len' : len(total_text), 'text' : total_text }

print(create_content(['cleancommit', 'job', 'developer'], 2500))