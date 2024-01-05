import openai
import pandas as pd

openai.api_key = "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"

def get_discussion_summary(thread_name, discussions):
    prompt_col3 = f"{thread_name}\n{discussions}\n\nWhat are the different perspectives and insights from these discussions? Quote the lines from which you summarised these insights? Answer in this structure:\n1. **Desire for Prestige and Validation:** Some individuals may be driven by a desire for prestige and validation, seeking a perceived higher status by immigrating to the USA. The Gujrati community, in particular, is mentioned to have a penchant for living together and maintaining a homogeneous community, contributing to the motivation for immigration.\n   quote> \"Yes but living in the USA carries prestige you cannot otherwise buy. And these people crave that prestige.\""

    response_col3 = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_col3,
        max_tokens=500,
        temperature=0.7
    )
    summary_col3 = response_col3['choices'][0]['text'].strip()

    prompt_col4 = f"{summary_col3}\n\nBased on these perspectives, provide me with your insights on each of them from your own knowledge base to help a political candidate out?"

    response_col4 = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_col4,
        max_tokens=500,
        temperature=0.7
    )
    insights_col4 = response_col4['choices'][0]['text'].strip()

    prompt_col5 = f"{prompt_col3}\n\n{prompt_col4}\n\nWhere did the information come from? Is the source reliable, and is there any indication of bias?\n- Are the comments from a diverse range of perspectives, or is there a potential bias in the sample?\n- Is there enough context provided to fully understand the viewpoints expressed?\n- Are the perspectives reflective of the general public sentiment or a specific subgroup?\n- Are the comments nuanced, or do they oversimplify complex issues?\n- How might the passage of time influence the relevance of the insights?\n- Can statistical information provide a broader context for the qualitative insights?\n- Is there an opportunity to seek feedback from the community or participants in the discussion to refine or validate the insights?\n- How might incorporating user feedback enhance the accuracy of the analysis?"

    response_col5 = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt_col5,
        max_tokens=800,
        temperature=0.7
    )
    answers_col5 = response_col5['choices'][0]['text'].strip()

    return summary_col3, insights_col4, answers_col5

df = pd.read_csv("data.csv")

for index, row in df.iterrows():
    thread_name = row['title']
    discussions = row['discussions']

    if pd.isnull(thread_name) or pd.isnull(discussions):
        continue

    summary, insights, answers = get_discussion_summary(thread_name, discussions)

    df.at[index, 'perspective'] = summary
    df.at[index, 'insight'] = insights
    df.at[index, 'question_and_answers'] = answers

df.to_csv("data.csv", index=False)