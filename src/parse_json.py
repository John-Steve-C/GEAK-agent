import json

def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def load_jsonl(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        data = [json.loads(line) for line in lines]
    return data


# load json file
data = load_json('../outputs/optimagent_gpt41_mem_4.json')

# print the first entry
# print(data.keys())
print(data["lightning_attention.py"].keys())
# print(data["lightning_attention.py"]["oneshot"])

# load jsonl file
data_1 = load_jsonl('../outputs/optimagent_gpt41_1.jsonl')

print(data_1[0].keys())
# print(data_1[0]["label"])

# data_2 = load_jsonl('../outputs/optimagent_gpt41_2.jsonl')
# if data_1[0]["label"] != data_2[0]["label"]:
#     print("Different labels!")
# else:
#     print("Same labels!")

# check code similarity
previous_example = ""
cnt = 0
for i in range(184):
    # i = 170
    filename = data_1[i]["filename"]
    # print(filename)

    ref = data_1[i]["label"]
    example = data[filename]["oneshot"]
    
    if previous_example != example:
        print("Not same example as previous!")
        cnt += 1

    previous_example = example

    # with open("out_ref.txt", "w") as f:
    #     f.write(ref)
    
    # with open("out_example.txt", "w") as f:
    #     f.write(example)
    
    # exit(0)
print(f"Number of unique examples: {cnt}")