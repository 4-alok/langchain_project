import json
import os
import openai
import pandas as pd
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]


def extract_financial_data(text):
    prompt = get_prompt_financial() + text
    response = openai.ChatCompletion.create(  # type: ignore
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    print(response)
    content = response.choices[0]['message']['content'] # type: ignore
    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=['Measure', 'Value'])
    except (json.decoder.JSONDecodeError, IndexError):
        pass
    
    return pd.DataFrame({
        "Measure": ['Company Name', "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "Value": ["", "", "", "", ""]
    })


def get_prompt_financial():
    return '''Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following news article. If you can't find the information from this article 
    then return "". Do not make things up.    
    Then retrieve a stock symbol corresponding to that company. For this you can use
    your general knowledge (it doesn't have to be from this article). Always return your
    response as a valid JSON string. The format of that string should be this, 
    {
        "Company Name": "Walmart",
        "Stock Symbol": "WMT",
        "Revenue": "12.34 million",
        "Net Income": "34.78 million",
        "EPS": "2.1 $"
    }
    News Article:
    ============

    '''
