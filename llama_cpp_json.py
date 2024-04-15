from langchain_community.llms import LlamaCpp
from structure import ExecutorSchema, SimpleExecutorSchema
from llama_cpp_agent.gbnf_grammar_generator.gbnf_grammar_from_pydantic_models import (
    generate_gbnf_grammar_and_documentation,
)
import json

# generates the gbnf file
grammer, doctument = generate_gbnf_grammar_and_documentation([ExecutorSchema])

with open("grammer.gbnf", "w") as f:
    f.write(grammer)

kwargs = {"grammer_path": "grammer.gbnf"}

llm = LlamaCpp(
    model_path="mistral-7b-instruct-v0.2.Q4_0.gguf",
    # f16_kv=True,
    max_tokens=512,
    model_kwargs=kwargs,
)

QUERY = "Laws and regulations for formal clothing brand."  # put test QUERY
# Example template
template = (
    f"""<s>[INST] Complete the given TASK like a market analyst, and return findings as detailed bullet points, a descriptive and detailed summary, and some year on year data on diffenrent fields if possible, dont respond fake data .Bullet points should sounds professional, include names and should be in correct order. Summary should be crisp. And year on year data should be justified, fields of data should be well descriptive. These key-points, summary and data will be important hence respond correctly. Response must be in valid JSON format including strings, lists and dictionary objects. [/INST]</s>\n"""
    + f"""[INST] TASK:\n{QUERY}\n[/INST]\n"""
)

response = llm.invoke(template)

print(response)
with open("gbnf_output.json", "w") as file:
    json.dump(eval(response), file, indent=4)
