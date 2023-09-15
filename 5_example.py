import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def create_content(keywords, article_length = 6000):
    keywords = ', '.join(keywords)
    total_text = ''

    dialogue = [
        {'role': 'system',
         'content': 'You are a helpful assistant specialized in generating SEO-optimized content for blogs.'},
        {'role': 'user',
         'content': f'I own a company and I need an SEO-optimized {article_length} length article for my website. Include the keywords {keywords}. Return the article and end with "##STOP##" when it\'s complete.'}
    ]

    stop_phrase = "##STOP##"
    max_iteration = 10
    while stop_phrase not in total_text:
        response = openai.ChatCompletion.create(
            model=os.getenv('NEW_MODEL_NAME'),
            messages=dialogue,
            temperature=0.7,
            max_tokens=1000
        )

        part_of_article = response.choices[0].message['content'].strip()

        total_text += part_of_article

        dialogue.append({
            "role": "user",
            "content": "Please continue the article."
        })

        max_iteration -= 1

        if max_iteration < 1:
            break

    #total_text = total_text.replace(stop_phrase, '')

    return {'len' : len(total_text), 'text' : total_text }

print(create_content(['react', 'website', 'framework'], 2000))