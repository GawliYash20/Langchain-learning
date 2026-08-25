from typing import Any
from langchain_openai import ChatOpenAI
import streamlit as st
from pydantic import SecretStr
from langchain_core.prompts import PromptTemplate, load_prompt
import re
from dotenv import load_dotenv


# Helpers
def clean_latex_for_streamlit(text: str | list[str | dict[str, Any]]) -> str:
    """
    Convert common LLM LaTeX delimiters into
    Streamlit-compatible delimiters.
    """

    if isinstance(text, list):
        parts: list[str] = []
        for item in text:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                if isinstance(item.get('text'), str):
                    parts.append(item['text'])
                elif isinstance(item.get('content'), str):
                    parts.append(item['content'])
                else:
                    parts.append(str(item))
            else:
                parts.append(str(item))
        text = ''.join(parts)
    elif not isinstance(text, str):
        text = str(text)

    # Convert \[ ... \] -> $$ ... $$
    text = re.sub(
        r"\\\[\s*(.*?)\s*\\\]",
        r"$$\n\1\n$$",
        text,
        flags=re.DOTALL
    )

    # Convert \( ... \) -> $ ... $
    text = re.sub(
        r"\\\(\s*(.*?)\s*\\\)",
        r"$\1$",
        text,
        flags=re.DOTALL
    )

    # Remove \boxed{...}
    text = re.sub(
        r"\\boxed\{(.*?)\}",
        r"\1",
        text,
        flags=re.DOTALL
    )

    return text



st.header('Research Tool', text_alignment='center')

# model = ChatOpenAI(
#     model='gemma-4-E2B-it-qat-UD-Q4_K_XL.gguf',
#     base_url='http://localhost:8080/v1',
#     api_key=SecretStr('not-needed'),
#     temperature=1.5
# )

load_dotenv()

model = ChatOpenAI(
    model='gpt-5.6-luna',
    temperature=1.5
)


paper_input = st.selectbox(
    'Select Research Paper Name:',
    [
        'Attention is All You Need',
        'BERT: Pre-training of Deep Bidirectional Transformers',
        'GPT-3: Language models are Few-Shot learners',
        'Diffusion Models beat GANs on Image Synthesis'
    ]
)

style_input = st.selectbox(
    'Select Explanation style:',
    [
        'Begineer-Friendly',
        'Technical',
        'Code-oriented',
        'Mathematical'
    ]
)

length_input = st.selectbox(
    'Select Explanation style:',
    [
        'Short (1-2 paragraphs)',
        'Medium (3-5 paragraphs)',
        'Long (detailed explanation)'
    ]
)

template = load_prompt('template.json')




if st.button('Summarize'):
    chain = template | model
    result = chain.invoke({
        'paper_input': paper_input,
        'style_input': style_input,
        'length_input': length_input
    })

    raw_input = result.content
    clear_input = clean_latex_for_streamlit(raw_input)
    st.markdown(clear_input)