from langchain_experimental.llms.ollama_functions import OllamaFunctions
from structure import KeyPointsSchema, ExecutorSchema
from langchain_core.utils.function_calling import convert_to_openai_function
from prompts import KeyPointsPrompt, ExcecutorPrompt
import json
import time

# entry_llm = OllamaFunctions(model="mistral")
# entry_llm = entry_llm.bind(functions=[convert_to_openai_function(KeyPointsSchema)])

detail_llm = OllamaFunctions(model="mistral")
detail_llm = detail_llm.bind(
    functions=[convert_to_openai_function(ExecutorSchema)],
    function_call={"name": "ExecutorSchema"},
)

# chain = KeyPointsPrompt() | entry_llm

chain_t = ExcecutorPrompt() | detail_llm
x = time.time()
response = chain_t.invoke(
    {
        # "objective": "do market reseach on formal clothing startup",
        "sub_task": "Customer demography for formal clothing brand.",
    }
)
y = time.time()
extracted_data = eval(response.additional_kwargs["function_call"]["arguments"])

with open("mistral_output.json", "w") as file:
    json.dump(extracted_data, file, indent=4)

print(response, f"time taken : {y-x}")

# for key points generation
"""
response = chain.invoke(
    {"objective": "do market research on formal clothing statup.", "feedback": ""}
)
steps = (response.additional_kwargs["function_call"]["arguments"],)
print(json.dumps(steps, indent=4))"""
