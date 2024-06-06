from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

from tunePost import tunePost
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

client = OpenAI()
# result = generateInstagramPost(client, {"date": "26 czerwca", "name": "Międzynarodowy Dzień Pomocy Ofiarom Tortur"})

# print(tunePost(client, {"threadId": "thread_4ju2waUq5QYuie1nf2cZu0e5",
#                         "userMsg": "bardziej formalnie, zaproś do gabinetu w Berlinie"}))

print(tunePost(client, {"threadId": "thread_4ju2waUq5QYuie1nf2cZu0e5",
                        "userMsg": "gabinet jest przy linienStrase, dodaj adres. Jest otwarty codziennie od 8 do 19"}))
