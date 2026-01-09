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

def save_jsonl(data, file_path):
    with open(file_path, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

def fix_truncated_json(filepath, output_path):
    with open(filepath, 'rb') as f:
        content = f.read().strip()
        
        # Look for the last successfully closed object
        last_bracket = content.rfind(b'}')
        if last_bracket != -1:
            # Keep everything up to the last closing brace and add the closing list bracket
            fixed_content = content[:last_bracket+1] + b']'
            with open(output_path, 'wb') as out:
                out.write(fixed_content)
            print(f"Fixed file saved to {output_path}")
        else:
            print("Could not find a valid closing brace.")

# fix_truncated_json('../outputs/test/optimagent_gpt41_mini_init_answer_serial_dc_mem_1.json', 'fixed_file.json')

if __name__ == "__main__":

    # root = "../outputs/optimagent_gpt41_mini_mem"

    # root = "../outputs/_embed_optimagent_gpt41_mini_mem"

    # root = "../outputs/split_embed_optimagent_gpt41_mini_mem"

    root = "../outputs/test/optimagent_gpt41_mini_origin_mem"
    root_2 = "../outputs/test/optimagent_gpt41_mini_answer_serial_dc_mem"

    # embed_full = load_json("retrievers/parsed_corpus_embeddings_ordered.json")
    # embed_split = load_json("retrievers/parsed_corpus_embeddings_split_ordered.json")
    # embed_split_whole = load_json("retrievers/parsed_corpus_embeddings_split_ordered_whole.json")
    # full_code = load_json("dataloaders/TB_eval/train_crawl.json")

    # for idx in range(len(full_code)):
    #     if embed_split_whole["aux_code"][idx] in full_code[idx]["code"] or embed_split_whole["core_code"][idx] in full_code[idx]["code"]:
    #     # if embed_split_whole["core_code"][idx] == embed_split["core_code"][idx]:
    #         # continue
    #         print(f"Match at index {idx}:")

    #     else:
    #         print(f"Mismatch at index {idx}:")
    #         # print("Core code snippet:", embed_split_whole["core_code"][idx])
    #         # print("Full code snippet:", full_code[idx]["code"])
    #         # print("==================================")

    # print("Check finished!")
    # exit(0)

    flag_pass_exe = [0] * 184   # total 184 samples
    solutions = [None] * 184
    
    output_results = []
    accum_acc = []
    failed_examples = []
    passed_examples = []
    examples = []
    # # load json file
    # data = load_json('../outputs/optimagent_gpt41_mini_mem_4.json')
    # print(len(data))
    # # print the first entry
    # file_names = data.keys()
    # # print(data.keys())
    # print(data["lightning_attention.py"].keys())

    for iter in range(0, 9):
        data = load_json(f'{root}_{iter}.json')
        data_2 = load_json(f'{root_2}_{iter}.json')
        cnt = 0
        data_next = load_json(f'{root}_{iter+1}.json') 

        for idx, key in enumerate(data):
            # if idx >= 20:
            #     break
            # filter failed examples
            if data[key]["pass_exe"] and not data_next[key]["pass_exe"]:
                failed_examples.append({
                    "file_name": key,
                    "solution": data[key],
                    "failed_response": data_next[key],
                    "failed_iter": iter + 1
                })
                print(key, iter + 1)
                print(data_2[key]['reflection'])
                # print("==================================Solution: \n", data[key]["exe_candidate"])
                # print("==================================Failed response: \n", data_next[key]["exe_candidate"])
                # if data[key]["oneshot"] == data_next[key]["oneshot"]:
                #     print("Same oneshot prompt")
                
            # filter passed examples
            # if not data[key]["pass_exe"] and data_next[key]["pass_exe"]:
            #     passed_examples.append({
            #         "file_name": key,
            #         "solution": data[key],
            #         "failed_response": data_next[key],
            #         "succeeded_iter": iter + 1
            #     })
            #     print(key, iter + 1)
            #     # print("==================================Solution: \n", data[key]["exe_candidate"])
            #     # print("==================================Failed response: \n", data_next[key]["exe_candidate"])
            #     if data[key]["oneshot"] == data_next[key]["oneshot"]:
            #         print("Same oneshot prompt")

            # if key == "dequantize_rowwise.py": # and data[key]["pass_exe"] and not data_next[key]["pass_exe"]:
            # if key == "kldiv_compute.py":
            #     print(f"Iter {iter}, key: {key}")
            #     print("Current pass_exe:", data[key]["pass_exe"])
            #     print("Next pass_exe:", data_next[key]["pass_exe"])
            # #     # print("Current exe_candidate:", data[key]["exe_candidate"])
            # #     # print("Next exe_candidate:", data_next[key]["exe_candidate"])
            # #     # print(data[key]["oneshot"])
            # #     if data_next[key]["oneshot"] == data[key]["oneshot"]:
            # #         print("Same oneshot prompt")
            # #     print("==================================")
            #     # exit(0)
            #     examples.append({
            #         "file_name": key,
            #         "iter": iter,
            #         "solution": data[key],
            #         "next_solution": data_next[key],
            #     })

            # check same example
            # if data[key]["oneshot"] == data_2[key]["oneshot"]:
            #     # print(f"Same oneshot prompt at iter {iter} for {key}")
            #     cnt += 1
        
        # if cnt == 20:
        #     print(f"All examples have the same oneshot prompt at iter {iter}")
    # with open(f"{root}_failed_examples.json", "w") as f:
    #     json.dump(failed_examples, f, indent=4)

    with open(f"{root}_tmp_examples.json", "w") as f:
        json.dump(examples, f, indent=4)