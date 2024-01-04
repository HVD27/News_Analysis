import openai
import csv

openai.api_key = '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'
with open('data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    discussions = list(reader)

prompt = "\n\n".join([f"Discussion {i+1}: {row['title']}\n{row['Comment']}" for i, row in enumerate(discussions)])
prompt += "\n\nWhat are the different perspectives and insights from these discussions?"

response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=0.7,
    max_tokens=500,
)

print(response.choices[0].text.strip())
