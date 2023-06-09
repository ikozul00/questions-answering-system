import openai
from openai.error import APIError
from dotenv import dotenv_values

config = dotenv_values()

openai.api_key = config["OPENAI_API_KEY"]

def clean_text(text):
    task_content = "Očisti teskt:"
    context = "You are a program using natural language processing techniques on text in Croatian language."
    tokens = 2 * len(text) + len(task_content) + len(context)
    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        temperature = 0.2,
        n=1,
        max_tokens = tokens,
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": task_content + '\n' + text},
        ]
    )  
   
    
    if completion.choices[0].finish_reason=="stop":
        return completion.choices[0].message.content
    else:
        return("error")


def get_answers(text):
    task_content = "Odgovori na pitanja sa maksimalno 3 rečenice, pitanja i odgovore vrati u JSON formatu:"
    context = "You are a student writing a quiz in Croatian language."
    tokens = 5 * len(text) + len(task_content) + len(context)

    completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        temperature = 0.2,
        n=1,
        max_tokens = tokens,
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": task_content + '\n' + text},
        ]
    )  
    if completion.choices[0].finish_reason=="stop":
        return completion.choices[0].message.content
    else:
        return("error")