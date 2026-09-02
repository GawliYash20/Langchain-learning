from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from typing import Annotated, Literal

load_dotenv()

model = ChatOpenAI(
    model='gpt-5.6-luna'
)

parser = StrOutputParser()

class FeedBack(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field(description='Give me the sentiment of the following feedback')

parser2 = PydanticOutputParser(pydantic_object=FeedBack)

prompt1 = PromptTemplate(
    template='Classify the sentiment of the following feedback text into positive or negative \n {feedback} \n {format_instruction}',
    input_variables=['feedback'],
    partial_variables={'format_instruction': parser2.get_format_instructions()}
)

classifier_chain = prompt1 | model | parser2

result = classifier_chain.invoke({'feedback': 'This is a wonderful smartphone'}).sentiment

print(result)




