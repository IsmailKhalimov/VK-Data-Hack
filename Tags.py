import requests
from bs4 import BeautifulSoup
import pandas as pd
def tags(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f'Error:{resp.status_code}. Adress:{url}')
    soup = BeautifulSoup(resp.text, 'lxml')
    try:
        block = soup.find('header')
        block1 = soup.find('main').find_all('div', {'article-item-type': 'html'})

        title = block.h1.text
        descr = block.find_all('div')[1].text

    except:
        title = soup.h1.text
        try:
            descr = soup.find('div', {'class': 'article__intro'}).text
            block1 = soup.find_all('div', {'class': 'article__item article__item_alignment_left article__item_html'})
        except:
            descr = soup.find('div', {'class': 'page-info__lead'}).text
            block1 = soup.find_all('div', {
                'class': 'article__item article__item_alignment_left article__item_text article__item_html'})

    article = ''
    for k in block1:
        j = k.text
        if 'Читайте также' in j:
            break
        article += j + '\n'

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    base_url = "http://mistral.vkcloud.eazify.net:8000/v1"

    chat = ChatOpenAI(api_key="<key>",
                    model = "tgi",
                    openai_api_base = base_url,
                    temperature=0.2)

    instruct = """
    
    Прочитай приведённый ниже в тройных обратных кавычках статью и выведи из нее пять тегов (ключевых слов) в именительном падеже
    в формате JSON следующего вида:
    {{
      "Tags": ["", "", "", "", ""]
    }}
    Статья: ```{review}```"
    """

    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system", "Ты аналитик сайта статей, и твоя задача извлекать из статей теги (ключевые слова)."),
            ("human", instruct),
        ]
    )


    from langchain_core.output_parsers import JsonOutputParser
    from tqdm.auto import tqdm

    parser = JsonOutputParser()
    res = []

    z = chat.invoke(chat_template.format_messages(review=article[:900]))
    try:
        res.append(parser.invoke(z))
    except:
        pass

    df = pd.DataFrame(res)
    df['Class'] = ''
    df['Title'] = title
    df['Description'] = descr
    df['Article Text'] = article
    print(df)
    df.to_json('datas.json')

tags(input())
