import os
import openai
import nltk

openai.api_key = '<OPENAI_API_KEY>'

def chunk_text(text, max_chunk_length):
    sentences = nltk.tokenize.sent_tokenize(text)
    chunks = []
    current_chunk = ''
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_length:
            current_chunk += ' ' + sentence
        else:
            chunks.append(current_chunk)
            current_chunk = sentence
    chunks.append(current_chunk)
    return chunks

def translate(text):
    messages = [
        {"role": "system", "content": f"You are a helpful assistant that translates from Turkish to academic English."},
        {"role": "user", "content": text}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=4000,
    )
    return response.choices[0].message['content']


def read_thesis_from_file(file_path):
    with open(file_path, "r") as file:
        thesis = file.read()
    return thesis
    
def write_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)
        
if __name__ == "__main__":
    
    thesis_file_path = "/path/to/your/text/file"
    thesis = read_thesis_from_file(thesis_file_path)
    
    chunks = chunk_text(thesis, 4000)
    translated_chunks = [translate(chunk) for chunk in chunks]
    translated_text = ' '.join(translated_chunks)

    write_file("translated_file.txt", translated_text)
