from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint, HuggingFacePipeline
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

# Hugging Face API call

llm = HuggingFacePipeline.from_model_id(
    model_id='google/gemma-4-E2B-it', 
    task='text-generation',
    pipeline_kwargs={
        'temprature': 1,
        'return_full_text': False
    }
)

model = ChatHuggingFace(llm=llm)

# model = ChatOpenAI(
#     model='gpt-5.6-luna'
# )

# 1st -> detailed report
template1 = PromptTemplate(
    template='Write a detailed report on {topic}',
    input_variables=['topic']
)

# 2nd prompt -> summary report
template2 = PromptTemplate(
    template='Write a 5 line summary on the following text. /n {text}',
    input_variables=['text']
)

parser = StrOutputParser()

chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({'topic': 'black hole'})

print({result})