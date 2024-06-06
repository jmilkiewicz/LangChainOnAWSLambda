from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.globals import set_debug
from langchain.globals import set_verbose
from dotenv import load_dotenv
from pathlib import Path

from getApiKey import getApiKey

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

assistantId = "asst_m8J3tJSwgrG82mXLfURQL4cI"


def tunePost(openApiClient, params):
    threadId = params["threadId"]
    userMsg = params["postFeedback"]

    openApiClient.beta.threads.messages.create(
        thread_id=threadId,
        role="user",
        content=userMsg
    )

    run = openApiClient.beta.threads.runs.create_and_poll(
        thread_id=threadId,
        assistant_id=assistantId,
    )

    if run.status == 'completed':
        messages = openApiClient.beta.threads.messages.list(
            thread_id=threadId, run_id=run.id
        )
        result = {
            "threadId": threadId, "messages": [{"role": m.role, "text": m.content[0].text.value} for m in messages]
        }
        return result
    else:

        print("!!!!!! error !!!!!!!")
        print(run.status)
        raise Exception(f"!!!!!! error !!!!!!! {run.status}")
