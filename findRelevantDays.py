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
from typing import List, Optional

from langchain_core.pydantic_v1 import BaseModel, Field


class RelevantDay(BaseModel):
    """opisuje pojedynczy dzień/święto"""

    name: str = Field(..., description="nazwa ochodzonego dnia")
    description: Optional[str] = Field(..., description="krótki opis")


class RelevantDays(BaseModel):
    """Zwraca listę dni/świąt w kalendarzu"""

    days: List[RelevantDay] = Field([], description="lista dni")


model = ChatOpenAI(model="gpt-4o", temperature=0)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Jesteś pomocnym asystentem. Znasz wszystkie dni w kalendarzu i chętnie się dzielisz informacjami na ich temat. "
            "Zawsze odpowiadasz w języku polskim",
        ),
        ("human", "{query}"),
    ]
)

chain = prompt | model.with_structured_output(RelevantDays)

print(chain.invoke({
                       "query": " Chciałbym poznać wszystkie święta w kalendarzu w których to ustanowiono święta związane ze zdrowiem psychicznym,"
                                " zaburzeniami psychicznymi, dni upamiętnieniające ofiary które doznały krzywd psychicznych, "
                                "dni związane z promowaniem zdrowia psychicznego oraz wszelkimi tematami związanymi z psychologią lub rozwojem wewnętrznym."
                                "Chodzi o dni ustanowione na szczeblu międzynarodowym lub europejskim w miesiącu czerwiec. Chcę jak najpełniejszą listę - minimum 7 dni"
                       }))
