from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

from findRelevantDaysFromCalendar import findRelevantDays

model = ChatOpenAI(temperature=0.0, model="gpt-4o", ).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",
        name="LLM Temperature",
        description="The temperature of the LLM",
    )
)

days = findRelevantDays(model,"10")
dicts = [relevantDay.dict()  for relevantDay in days]
# posts = [generateInstagramPost(day) for day in days]



