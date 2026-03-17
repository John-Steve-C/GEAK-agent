import json
import os


# add the parent directory to the path
import sys
sys.path.append("/data/wentao/GEAK-agent/src/")
from models.OpenAI import OpenAIModel

# with open("data.jsonl", "r") as f:
#     data = [json.loads(line) for line in f]

model = OpenAIModel(model_id="gpt-4o", api_key=os.environ.get("OPENAI_API_KEY"))

output_dict = []

# traverse all py file in the data folder
prefix = "./solutions/"
for root, dirs, files in os.walk(prefix):
    for file in files:
        if file.endswith(".py"):
            with open(os.path.join(root, file), "r") as f:
                code = f.read()
            # file_name = os.path.join(root, file)
            # print(f"File: {file}")
            # print(code)

            # generate instruction for each file
            response = model.generate(messages=[
                {
                    "role": "system", 
                    "content": """You are an expert in high-performance GPU programming and code understanding. I will show you a tilelang code, then please generate a detailed task description for this code. 
The task description should be detailed and specific, and should cover the following aspects: 
1) what is the functionality of the code? 
2) what are the inputs and outputs of the code? 
3) what are the key algorithms and techniques used in the code?
4) The response should start with: "You are an expert in high-performance GPU programming and Tile-lang kernel code generation. Your task is to..."
Please provide a comprehensive task description based on these aspects. Here is the content of the code: ",
"""
                },
                {
                    "role": "user",
                    "content": code
                }
            ]
            )

            print(response)


            output_dict.append({
                "instruction": response,
                "input": "",
                "output": code,
                "file": file
            })

# with open("data.jsonl", "w") as f:
#     for item in output_dict:
#         f.write(json.dumps(item) + "\n")

with open("data.json", "w") as f:
    json.dump(output_dict, f, indent=4)