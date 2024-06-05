from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI
import chevron

from findRelevantDaysFromCalendar import findRelevantDays
from generateInstagramPost import generateInstagramPost

model = ChatOpenAI(temperature=0.0, model="gpt-4o", ).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",
        name="LLM Temperature",
        description="The temperature of the LLM",
    )
)

days = findRelevantDays(model,"10")

dicts = [  {"event": relevantDay.dict()} | {"index":index} for index, relevantDay in enumerate(days)]


with open('templates/days.mustache', 'r') as f:
    print(chevron.render(f, dicts))


posts = [generateInstagramPost(model, dicts[0]["event"]) for day in days]



