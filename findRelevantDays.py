
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

    name: str = Field(..., description="nazwa święta")
    description: Optional[str] = Field(..., description="krótki opis święta")


class RelevantDaysResponse(BaseModel):
    """Zwraca listę dni/świąt w kalendarzu"""

    days: List[RelevantDay] = Field([], description="lista znalezionych świąt")


model = ChatOpenAI(model="gpt-4o")


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Jesteś pomocnym asystentem. Znasz wszystkie dni w kalendarzu i chętnie się dzielisz informacjami na ich temat",
        ),
        ("human", "{query}"),
    ]
)

chain = prompt | model.with_structured_output(RelevantDaysResponse)

print(chain.invoke({"query":" Chciałbym wiedzieć kiedy w kalendarzu przypadają dni związane ze zdrowiem, szczególnie psychicznym i "
                    "wszelkimi tematami związanymi z psychologią lub psychoterapią. Chodzi mi o szystkie dni "
                    "którch celem jest zwiększanie świadomości, edukacji i wsparcia dla osób zmagających się z różnymi "
                    "problemami psychicznymi oraz promowania zdrowia psychicznego na całym świecie."}))

