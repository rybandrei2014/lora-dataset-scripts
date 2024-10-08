import ollama
import os

directory_path = r'input'
counter = 0
model = "llava:13b"

for filename in os.listdir(directory_path):
    
    full_path = os.path.join(directory_path, filename)
    
    if not full_path.endswith('.txt'):
       
        if os.path.isfile(full_path):
            print(f"Processing {full_path}...")

            base_name = os.path.splitext(filename)[0]
            output_file_name = f"{base_name}.txt"
            output_file_path = os.path.join(directory_path, output_file_name)

            output_file_name_short = f"{base_name}_short.txt"
            output_file_path_short = os.path.join(directory_path, output_file_name_short)

            output_file_name_keywords = f"{base_name}_keywords.txt"
            output_file_path_keywords = os.path.join(directory_path, output_file_name_keywords)

            image_path = full_path

            print(f"Prompting Ollama to acquire long caption for {image_path}...")

            res = ollama.chat(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': 'Describe this image :',
                        'images': [full_path],
                        'keep_alive' : '5m'
                    }
                ]
            )

            print(f"Prompting Ollama to acquire short caption for {image_path}...")

            res2 = ollama.chat(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': 'Describe this image :',
                    },
                    {
                        'role': 'assistant',
                        'content': res['message']['content']
                    },
                    {
                        'role': 'user',
                        'content': 'Do not use words like The Image is. Use 40 words.',
                        'keep_alive' : '5m'
                    }
                ]
            )

            print(f"Prompting Ollama to acquire keywords for {image_path}...")

            res3 = ollama.chat(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': 'Describe this image :',
                    },
                    {
                        'role': 'assistant',
                        'content': res['message']['content']
                    },
                    {
                        'role': 'user',
                        'content':  'keywords',
                        'keep_alive' : '5m'
                    }
                ]
            )

            content = res['message']['content']
            content_short = res2['message']['content']
            content_keywords = res3['message']['content']

            counter = counter + 1

            with open(output_file_path, 'w', encoding="utf-8") as f:
                f.write(content)
            with open(output_file_path_short, 'w', encoding="utf-8") as f:
                f.write(content_short)
            with open(output_file_path_keywords, 'w', encoding="utf-8") as f:
                f.write(content_keywords)