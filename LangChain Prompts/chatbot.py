from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model='gpt-5.6-luna'
)

chat_history: list[BaseMessage] = [
    SystemMessage(content='You are a helpfull assistant')
]

while True:
    user_input = input('You: ')
    if user_input.lower() == 'exit':
        break
    chat_history.append(HumanMessage(content=user_input))
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print('AI:',result.content)