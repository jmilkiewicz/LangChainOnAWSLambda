from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.globals import set_debug
from langchain.globals import set_verbose
from dotenv import load_dotenv
from pathlib import Path

from dayCalendar import get_days_in

set_verbose(True)
set_debug(True)

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
from typing import List, Optional

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


class RelevantDay(BaseModel):
    """pojedyncze święto"""

    date: str = Field(..., description="kiedy przypada dane święto, np 24 stycznia")
    name: str = Field(..., description="nazwa święta np Światowy Dzień Transplantacji ")
    # description: Optional[str] = Field(..., description="krótki opis")


class RelevantDays(BaseModel):
    """lista świąt związanych ze zdrowiem psychicznym """

    days: List[RelevantDay] = Field([], description="lista świąt")


def findRelevantDays(model, fromDate, toDate):
    allDays = get_days_in(fromDate, toDate)

    parser = PydanticOutputParser(pydantic_object=RelevantDays)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Jesteś pomocnym asystentem. Na podstawie przekazanego ci kalanedarza i kryteriów umiesz wybrać odpowiednie święta."
                "Zawsze odpowiadasz w języku polskim. Opakuj odpowiedz in `json` tags\n{format_instructions}",
            ),
            ("human",
             "Z załączonej poniżej listy świąt w formacie JSON chciałbym poznać wszystkie święta związane ze zdrowiem psychicznym,"
             " depresjami, autyzmem, zaburzeniami psychicznymi, uzależnieniami, alkoholizmem, narkomanią, relacjami między ludzkimi , związkami partnerskimi,"
             "seksualnością, dni upamiętnieniające ofiary które doznały krzywd psychicznych, "
             "dni związane z promowaniem zdrowia psychicznego oraz wszelkimi tematami związanymi z psychologią lub rozwojem wewnętrznym. "
             "Opieraj się tylko na poniżej przedstawionej liście świąt."
             "List świąt jest w formacie JSON i posiada atrybut \"date\" który wskazuje na date oraz atrybut \"name\" który ma 1 lub wiele świąt które odbywają się w tym dniu. "
             "{days}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    chain = prompt | model.with_config(configurable={"llm_temperature": 0.0}) | parser

    days = chain.invoke({
        "days": allDays
    }).days

    return days
