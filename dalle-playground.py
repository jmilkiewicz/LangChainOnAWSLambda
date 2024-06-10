from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


client = OpenAI()
import requests

response = client.images.generate(
    model='dall-e-3',
    prompt="Chciałbym image który mógłbym umieścić w poście na instagram. Post jest związany z obchodzonym niedługo Międzynarodowy Dzień Pomocy Ofiarom Tortur. "
           "Image ma być związany z poniższym tekstem: 'Czasem, słowa nie wystarczają, by opisać ból i cierpienie, jakie niosą za sobą tortury. W Międzynarodowy Dzień Pomocy Ofiarom Tortur, 26 czerwca, 🕊️ przypomnijmy o sile ludzkiego ducha i o konieczności niesienia wsparcia tym, którzy przeżyli niewyobrażalne. ❤️‍🩹 Pomoc psychologiczna i psychoterapia mogą być kluczowe w procesie powrotu do życia po traumatycznych doświadczeniach. Każdy krok w stronę zdrowienia jest krokiem ku odzyskaniu kontroli nad własnym życiem. 🌱🧠 Pamiętajmy, że jesteśmy tu razem, by pomagać i dawać nadzieję. 🌟 Nie bądźmy obojętni wobec cierpienia innych. 🤝 Jeśli potrzebujesz wsparcia, mój gabinet psychoterapii jest zawsze otwarty. Możesz się ze mną skontaktować, jesteś ważny/a. 🫂 #gabinetgestalt #psychoterapiagestalt #psychoterapiaberlin'",
    size="1024x1024",
    quality="standard",
    n=1
)
image_url = response.data[0].url

dalle_img_path = 'dalle_image.png'
img = requests.get(image_url)

# Save locally
with open(dalle_img_path, 'wb') as file:
    file.write(img.content)
