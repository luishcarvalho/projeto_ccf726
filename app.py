from langchain_community.llms import Ollama
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
import gradio as gr


template= """# <|system|>
You are a chatbot with the function of returning whether a smart contract contains vulnerabilities. 
Your responses should only be related to this.

# <|ddl|>
The smart contract is as follows:
{contract}

# <|user|>
{question}

# <|assistant|>
"""




llm = LlamaCpp(
    model_path="FP16.gguf",
    temperature=0.3,
    max_tokens=2048,
    top_p=1,
    n_ctx=2048,
    stop=["."],
 # Verbose is required to pass to the callback manager
)

prompt = PromptTemplate.from_template(template)
chain = (prompt | llm)

def fn_chain(contract, question):
    return chain.invoke({"contract":contract, "question":'Does this contract contain vulnerabilities?'}).split(";")[0] + ";"

# Gradio interface
iface = gr.Interface(
    fn=fn_chain,
    inputs=["text"],
    outputs="text",
    title="Smart Detector",
    description="Digite o econtrato inteligente.",
)

# Launch the app
iface.launch(server_name = "0.0.0.0", 
    server_port= 5000)
