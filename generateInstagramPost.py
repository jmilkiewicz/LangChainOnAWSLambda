from dotenv import load_dotenv
from pathlib import Path


dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
import chevron

generatePostPromptTmpl = "chciałbym post na instagram który to będzie związany z wydarzeniem {{name}} odbywającym się {{date}}. "
"Jeżeli znasz możesz dodać jakiś pasujący cytat. Ideą tego posta ma być dotrarcie do jak największej liczby potencjalnych klientów "
"gabinetu psychoterapi. Użyj znanych ci metod i technik wpływu na decyzje ludzkie. "
" Staraj się spersonalizować ten wpis, zwracjąc się bezpośrednio do czytelnika posta "

assistantId = "asst_m8J3tJSwgrG82mXLfURQL4cI"


def generateInstagramPost(openApiClient, params):
    thread = openApiClient.beta.threads.create()
    generatePostPrompt = chevron.render(generatePostPromptTmpl, params)
    openApiClient.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=generatePostPrompt
    )

    run = openApiClient.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistantId,
    )

    if run.status == 'completed':
        messages = openApiClient.beta.threads.messages.list(
            thread_id=thread.id, run_id=run.id
        )
        result = {
            "threadId": thread.id, "messages": [{"role": m.role, "text": m.content[0].text.value} for m in messages]
        }
        return result
    else:

        print("!!!!!! error !!!!!!!")
        print(run.status)
        raise Exception(f"!!!!!! error !!!!!!! {run.status}")
