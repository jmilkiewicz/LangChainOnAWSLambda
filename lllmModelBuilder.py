from langchain_openai import ChatOpenAI

def buildLLM(key, temperature=0.0):
    return ChatOpenAI(temperature=temperature, model="gpt-4o", openai_api_key=key)