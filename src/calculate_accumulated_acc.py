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

def get_accumulated_acc(data):
    total = len(data)
    correct = sum(1 for item in data if item.get("pass_exe", False))
    return correct / total if total > 0 else 0.0

if __name__ == "__main__":

    # root = "../outputs/optimagent_gpt41_mini_mem"
    # root = "../outputs/_embed_optimagent_gpt41_mini_mem"

    # root = "../outputs/test/embed_optimagent_gpt41_mini_mem"
    # root = "../outputs/test/compare_split_embed_optimagent_gpt41_mini_mem"
    # root = "../outputs/test/true_embed_optimagent_gpt41_mini_mem"
    
    # root = "../outputs/test/optimagent_gpt41_mini_pipeline_dc_mem"
    # root = "../outputs/test/optimagent_gpt41_mini_answer_pipeline_dc_mem"
    # root = "../outputs/test/optimagent_gpt41_mini_origin_mem"
    # root = "../outputs/test/optimagent_gpt41_mini_serial_dc_mem"
    # root = "../outputs/test/optimagent_gpt41_mini_init_combined_dc_reorder_mem"
    # root = "../outputs/test/optimagent_gpt41_mini_api_init_combined_dc_reorder_mem"
    # root = "../outputs/test/optimagent_gpt41_mini_init_combined_dc_reorder_prune_mem"
    # root = "../outputs/test/optimagent_gpt41_mini_init_combined_dc_reorder_llm_prune_mem"
    root = "../outputs/test/optimagent_gpt41_mini_api_append_mem"

    flag_pass_exe = [0] * 184   # total 184 samples
    flag_pass_call = [0] * 184
    solutions = [None] * 184
    
    output_results = []
    accum_acc = []
    # # load json file
    # data = load_json('../outputs/optimagent_gpt41_mini_mem_4.json')
    # print(len(data))
    # # print the first entry
    # file_names = data.keys()
    # # print(data.keys())
    # print(data["lightning_attention.py"].keys())

    for iter in range(20):
        file_path = f'{root}_{iter}.json'
        data = load_json(file_path)

        for idx, key in enumerate(data):
            # print(idx, key, data[key])
            if data[key]['pass_call']:
                flag_pass_call[idx] = 1
            if data[key]["pass_exe"] or data[key]["pass_perf"]:
                flag_pass_exe[idx] = 1
                if len(data[key]["perf_candidates"]) > 0:
                    solutions[idx] = data[key]["perf_candidates"][-1][0]
                elif data[key]["exe_candidate"] is not None:
                    solutions[idx] = data[key]["exe_candidate"]
                else:
                    print(f"Warning: No valid solution for {key} at iter {iter}")
        # print(cnt)
        acc = sum(flag_pass_exe) / len(flag_pass_exe)
        accum_acc.append(acc)
        print(f"iter {iter}, acc: {acc:.4f}, number pass_exe: {sum(flag_pass_exe)}, number pass_call: {sum(flag_pass_call)}")
    
    input("Press Enter to save final results...")

    with open(f"{root}_final_solutions.jsonl", "w") as f:
        for idx, key in enumerate(data):
            output_results.append({
                "filename": key,
                "pass_exe": bool(flag_pass_exe[idx]),
                "solution": solutions[idx]
            })
            f.write(json.dumps(output_results[-1]) + "\n")
    
    with open(f"{root}_accumulated_acc_2.txt", "w") as f:
        for iter, acc in enumerate(accum_acc):
            f.write(f"Iter {iter}: accumulated exe acc: {acc:.4f}\n")