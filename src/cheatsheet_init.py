from models.OpenAI import OpenAIModel
from memories.CheatsheetManager import CheatsheetManager

import os
import json

def read_files_from_directory(directory: str) -> list:
    file_contents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt") or file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    file_contents.append(content)
    return file_contents

def read_files_with_filter(directory: str, prefix: str) -> list:
    file_contents = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt") or file.endswith(".md"):
                if file.startswith(prefix):
                    filepath = os.path.join(root, file)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        file_contents.append(content)
    return file_contents

if __name__ == "__main__":
    # with open("./first_cheatsheet.json", "r", encoding="utf-8") as f:
    #     data = json.load(f)
    #     global_cheatsheet = CheatsheetManager(data)
    global_cheatsheet = CheatsheetManager()
    #     print("Initial Cheatsheet Stats:", global_cheatsheet.get_stats())

    model = OpenAIModel(api_key=os.environ.get("OPENAI_API_KEY"), model_id="gpt-4.1-mini")

    # docs = read_files_from_directory("./triton_example_codes")
    # docs = read_files_from_directory("./triton_docs_markdown")
    docs = read_files_with_filter("./triton_docs_markdown", "main_getting-started_tutorials_")
    # docs = read_files_with_filter("./triton_docs_markdown", "main_python-api_")

    # doc_1 = read_files_with_filter("./tilelang_docs_markdown", "programming_guides")
    # doc_2 = read_files_with_filter("./tilelang_docs_markdown", "deeplearning_operators")
    
    # docs = doc_1 + doc_2

    print(len(docs), "documents loaded into cheatsheet.")

    for content in docs:
        prompt = global_cheatsheet.build_prompt_relation_no_qa(raw_prompt=content)
        msg = [
            {"role": "user", "content": prompt},
        ]
        response = model.generate(msg, temperature=1.0, max_tokens=10000)

        global_cheatsheet.apply_operations(response)
        print("Cheatsheet updated. Current stats:", global_cheatsheet.get_stats())
        
        # global_cheatsheet._op_add({
        #     "section": "API_usage",
        #     "content": content
        # })
        # print("Cheatsheet updated. Current stats:", global_cheatsheet.get_stats())

    # Save the final cheatsheet to a file
    with open("cheatsheet_relation.json", "w", encoding="utf-8") as f:
        json.dump(global_cheatsheet.data, f, indent=4)

    # with open("/data/wentao/GEAK-agent/outputs/test/optimagent_gpt41_mini_init_combined_dc_reorder_cheatsheet_4.json", "r", encoding="utf-8") as f:
    #     data = json.load(f)
    #     global_cheatsheet = CheatsheetManager(data)

    print("Final Cheatsheet Stats:", global_cheatsheet.get_stats())

    # for section in data:
    #     original_items = data[section]
    #     keep_items = []
    #     for idx, item in enumerate(original_items):
    #         # add a new field 'edge_cases' if not exist
    #         data[section][idx] = {
    #             "id": item['id'],
    #             "content": item['content'],
    #             "usage_count": 0,
    #             "last_used_iter": -1,
    #             "created_iter": 0,
    #             "variations": [],
    #             "edge_cases": []
    #         }

    # new_data = {'meta_reasoning': data['meta_reasoning'], 'solutions_and_patterns': data['solutions_and_patterns'], 'failed_attempts': []}

    # with open('./new_first_cheatsheet.json', 'w', encoding='utf-8') as f:
    #     json.dump(new_data, f, indent=4)

    