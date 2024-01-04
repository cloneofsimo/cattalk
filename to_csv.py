import pandas as pd
import re

def preprocess_txt(filepath):
    # Regex pattern to capture datetime and optionally username and chat
    pattern = r'(\d{4}년 \d{1,2}월 \d{1,2}일 (?:오전|오후) \d{1,2}:\d{2}), ([^:]+) :'
    
    
    is_datetime = lambda x : re.match(r'\d{4}년 \d{1,2}월 \d{1,2}일 (?:오전|오후) \d{1,2}:\d{2}', x)
    
    # Read the file content
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read()
        
    
    # first remove any line that just have datetime and nothing else
    text = re.sub(r'\d{4}년 \d{1,2}월 \d{1,2}일 (?:오전|오후) \d{1,2}:\d{2}\n', '', text)    
    

    # Split the text into messages
    messages = re.split(pattern, text)
    messages = [m for m in messages if m]  # Remove empty strings

    # Process each message
    data = []
    current_data = []
    print(messages[:4])
    for i in range(0, len(messages)):
        if is_datetime(messages[i]):
            if len(current_data):
                data.append(current_data)
            current_data = [messages[i]]
        else:
            current_data.append(messages[i])
        
    # Create DataFrame
    df = pd.DataFrame(data, columns=['datetime', 'username', 'message'])

    return df

df = preprocess_txt('data/2023_2024.txt')
df.to_csv('data/2023_2024.csv', index=False)
print(df.head())