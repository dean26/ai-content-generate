import openai
import json
import os
from transformers import GPT2Tokenizer
from dotenv import load_dotenv
import time

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def truncate_text(text, max_tokens=3800):
    tokens = tokenizer.tokenize(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        token_ids = tokenizer.convert_tokens_to_ids(tokens)
        truncated_text = tokenizer.decode(token_ids)
        return truncated_text
    return text

with open('blogs.json', 'r', encoding='utf-8') as file:
    blogs = json.load(file)


def extract_keywords(text):
    dialogue = [
        {'role': 'system',
         'content': 'You will be provided with a block of text, and your task is to extract a six of keywords from it.Return only 6 keywords and nothing more. Don\'t return "Keyword" at the beginning. Don\'t return list with digits.'},
        {'role': 'user',
         'content': text}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=dialogue,
        temperature=0.7,
        max_tokens=256
    )

    reply = response.choices[0].message['content'].strip().split(", ")

    return reply

final_results = []

licznik = 1
for blog in blogs:
    time.sleep(1.5)

    try:
        print("----")

        title = blog["title"]
        print("title:", title)

        text = truncate_text(blog["plaintext"])
        article_length = len(text)
        keywords = extract_keywords(text)
        formatted_keywords = ', '.join(keywords)
        print("keywords:", formatted_keywords)

        print("----")

        message_structure = {
            "role": "system",
            "content": "You are a helpful assistant specialized in generating SEO-optimized content for blogs."
        }

        result = {"messages": []}
        result["messages"].append(message_structure)

        user_message = {
            "role": "user",
            "content": f"I own a company and I need an SEO-optimized article for my website. The article should include the keywords {formatted_keywords}. Return only the article without any additional content. Generate the article and end with '##STOP##' when it's complete."
        }
        result["messages"].append(user_message)

        assistant_message = {
            "role": "assistant",
            "content": f"Title:\n{title}\n\nContent:\n{text}\n\n##STOP##"
        }
        result["messages"].append(assistant_message)
        final_results.append(result)

    except Exception as e:
        print("Error:", e)
        #traceback.print_exc()
        time.sleep(4)

with open('result.jsonl', 'w') as file:
    for dialogue in final_results:
        json.dump(dialogue, file)
        file.write('\n')
