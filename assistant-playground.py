from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

import chevron

client = OpenAI()

system_instruction = "Jesteś pomocnym asystentem - ekspertem w dziedzinie psychologi i psychoterapi gestalt. " \
                     "Prowadzisz jedno osobowy gabinet gdzie jesteś psychoterapeutą i psychologiem. " \
                     "Potrafisz tworzyć zwięzłe, ale intersujące i niebanalne posty na instagram o tematyce związanej " \
                     "z szeroką pojętą psychologią, zrdrowiem psychicznym i psychoterapią. " \
                     "Zawsze odpowiadasz w języku polskim w pierwszej osobie liczby pojednczej, tzn ja a nie my." \
                     "Wszystko co wygenerujesz ma być subtelną promocją gabinetu psychoterapi i promowanie psychoterapi w społeczeństwie." \
                     "Na końcu każdego postu dodaj następujące hashtagi: #gabinetgestalt, #psychoterapiagestalt, #psychoterapiaberlin "

# assistant = client.beta.assistants.create(
#     name="Instagram Post Generator",
#     instructions=system_instruction,
#     tools=[],
#     model="gpt-4o",
# )

# print(assistant)
# asst_m8J3tJSwgrG82mXLfURQL4cI


generatePostPromptTmpl = "chciałbym post na instagram który to będzie związany z wydarzeniem {{name}} odbywającym się {{date}}. "
"Jeżeli znasz możesz dodać jakiś pasujący cytat. Ideą tego posta ma być dotrarcie do jak największej liczby potencjalnych klientów "
"gabinetu psychoterapi. Użyj znanych ci metod i technik wpływu na decyzje ludzkie. "
" Staraj się spersonalizować ten wpis, zwracjąc się bezpośrednio do czytelnika posta "

generatePostPrompt = chevron.render(generatePostPromptTmpl,
                                    {"name": "Międzynarodowy Dzień Pomocy Ofiarom Tortur", "date": "26 czerwca"})

# thread = client.beta.threads.create()
# print(thread.id)


# thread_message = client.beta.threads.messages.create(
#     thread.id,
#     role="user",
#     content=generatePostPrompt,
# )

threadId = "thread_CLiYfAbb49yhJV2fupVERCBO"
thread_message = client.beta.threads.messages.create(
    threadId,
    role="user",
    content="ok, ale bardzie formalnie. Zaproś do gabinetu na linienstrase w Berlinie",
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=threadId,
    assistant_id="asst_m8J3tJSwgrG82mXLfURQL4cI",
)

if run.status == 'completed':
    messages = client.beta.threads.messages.list(
        thread_id=threadId, run_id=run.id
    )

    result = [{"role": m.role, "text": m.content[0].text.value} for m in messages]
    print(result)
else:
    print(run.status)
