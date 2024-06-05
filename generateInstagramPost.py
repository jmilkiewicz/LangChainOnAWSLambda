from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.globals import set_debug
from langchain.globals import set_verbose
from dotenv import load_dotenv
from pathlib import Path

set_verbose(True)
set_debug(True)

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)




def generateInstagramPost(model, relevantDay):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Jesteś pomocnym asystentem - ekspertem w dziedzinie psychologi i psychoterapi."
                "Potrafisz tworzyć zwięzłe ale intersujące i nie banalne wpisy na instagram o tematyce związanej "
                "z szeroką pojętą psychologią, zrdrowiem psychicznym i psychoterapią "
                "Zawsze odpowiadasz w języku polskim w pierwszej osobie liczby pojednczej, tzn ja a nie my. "
                "Wszystko co wygenerujesz ma być subtelną promocją gabinetu psychoterapi i promowanie psychoterapi w społeczeństwie."
            ),
            ("human",
             "chciałbym post na instagram który to będzie związany z wydarzeniem {name} odbywającym się {date}. "
             "Jeżeli znasz możesz dodać jakiś pasujący cytat. Ideą tego posta ma być dotrarcie do jak największej liczby potencjalnych klientów "
             "gabinetu psychoterapi. Użyj znanych ci metod i technik wpływu na decyzje ludzkie. "
             " Staraj się spersonalizować ten wpis, zwracjąc się bezpośrednio do czytelnika posta "
             )
        ])

    chain = prompt | model

    return chain.invoke({
        "name": relevantDay["name"],
        "date": relevantDay["date"]
    }).content

