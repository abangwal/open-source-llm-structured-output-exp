from langchain_experimental.llms.ollama_functions import OllamaFunctions
from regex import search
from structure import WebSearchQuery
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_text_splitters import RecursiveCharacterTextSplitter
from web_tool import WebTool
import cohere
import numpy as np

# from prompts import KeyPointsPrompt, ExcecutorPrompt
import json
import time

cohere_api = "DKiLLTRI6PG1tRGOkrAYbaVbJgC4DCb8odRDiKHI"

llm = OllamaFunctions(model="mistral")
llm = llm.bind(
    functions=[convert_to_openai_function(WebSearchQuery)],
    # function_call={"name": "ExecutorSchema"},
)

prompt = """[INST] Use the provided functions whenever needed to answer user query [/INST]</s>[INST]Web search queries for competitors in EV market[/INST]"""

response = llm.invoke(prompt)

search_queries = eval(response.additional_kwargs["function_call"]["arguments"])[
    "queries"
]
print(search_queries, "\n\n")
document = ""

for query in search_queries:
    document += WebTool().fetch_content(query)
    document += "\n\n\n"

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=128,
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.create_documents([document])
chunks = [i.page_content for i in chunks]


co = cohere.Client(api_key=cohere_api)

chunks_embedding = co.embed(texts=chunks, input_type="search_document").embeddings
embedding_vectors = np.asarray(chunks_embedding)

query = "Top competitors in EV market"
query_embedding = co.embed(
    texts=[query],
    input_type="search_query",
).embeddings
q_embedding_vector = np.asarray(query_embedding)

scores = np.dot(q_embedding_vector, embedding_vectors.T)[0]

max_idx = np.argsort(-scores)

print("Query : ", query)
print(f"Score: {scores[max_idx[0]]:.2f}")
print(chunks[max_idx[0]])
print(f"\n\nScore: {scores[max_idx[1]]:.2f}")
print(chunks[max_idx[1]])
