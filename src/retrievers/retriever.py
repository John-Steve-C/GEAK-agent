import json
import numpy as np
from typing import Any, Dict, List
from rank_bm25 import BM25Okapi
from .retrieve_utils import cosine_sim, get_embedding, split_core_auxiliary

class BM25Retriever:
    def __init__(self, mode="instruction"):
        assert mode in ("instruction", "code")
        self.bm25: BM25Okapi = None
        self.content_input_path: str = ""
        self.mode = mode
    
    def process(self, content_input_path: str):
        self.content_input_path = content_input_path
        with open(content_input_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        
        # to ensure the order
        self.chunks = []
        self.corpus = []
        for c in content:
            self.chunks.append(c["code"])
            self.corpus.append(c["description_1"])

        # frequency-based metric, need tokenization for each document
        if self.mode == "instruction" and self.corpus:
            tokenized_corpus = [co.split(" ") for co in self.corpus]
            self.bm25 = BM25Okapi(tokenized_corpus)
        elif self.mode == "code" and self.chunks:
            tokenized_corpus = [co.split(" ") for co in self.chunks]
            self.bm25 = BM25Okapi(tokenized_corpus)
        else:
            self.bm25 = None

    def query(
            self,
            query: str,
            top_k: int = 1
    ) -> List[Dict[str, Any]]:
        
        if top_k <= 0:
            raise ValueError("top_k must be a positive integer.")
        if self.bm25 is None or not self.chunks:
            raise ValueError(
                "BM25 model is not initialized. Call `process` first."
            )
        
        # Preprocess query similarly to how documents were processed
        processed_query = query.split(" ")
        # Retrieve documents based on BM25 scores
        scores = self.bm25.get_scores(processed_query)

        top_k_indices = np.argpartition(scores, -top_k)[-top_k:]

        formatted_results = []
        for i in top_k_indices:
            result_dict = {
                    "similarity score": scores[i],
                    "original instruction": self.corpus[i],
                    "code": self.chunks[i]
            }
            formatted_results.append(result_dict)
        
        # Sort the list of dictionaries by 'similarity score' from high to low
        formatted_results.sort(
            key=lambda x: x['similarity score'], reverse=True
        )

        return formatted_results

class EmbeddingRetriever:
    def __init__(self, mode="instruction"):
        self.mode = mode
        assert mode in ("instruction", "code")
        self.chunks = []
        self.corpus = []
        self.embed_chunk = []
        self.embed_corpus = []
        # self.embedder = pipeline("feature-extraction", model="/shared/models/hf/jina-embeddings-v3", trust_remote_code=True)
    
    def process(self, content_input_path: str):
        with open(content_input_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        print('Original total number: ', len(content))
 
        for c in content:
            self.corpus.append(c["description_1"])
            self.chunks.append(c["code"])
            # if self.mode == "instruction":
            #     self.embed_corpus.append(self.get_embedding(c["description_1"]))
            # elif self.mode == "code":
            #     self.embed_chunk.append(self.get_embedding(c["code"]))
        
        # parse all previously and load from file
        # must ensure the embed_chunk is ordered the same as dataset content
        with open("/home/wentao/GEAK-agent/src/retrievers/parsed_corpus_embeddings_ordered.json", "r", encoding="utf-8") as f:
            parsed_embedding = json.load(f)
        if self.mode == "instruction":
            self.embed_corpus = parsed_embedding["corpus_text"]
        elif self.mode == "code":
            self.embed_chunk = parsed_embedding["chunks_code"]

        print('Actual corpus number: ', len(self.chunks))
    
    def query(
            self,
            query: str,
            top_k: int = 1
    ) -> List[Dict[str, Any]]:
        if top_k <= 0:
            raise ValueError("top_k must be a positive integer.")
        if not self.chunks:
            raise ValueError("Corpus is empty. Load corpus first.")
        
        # processed_query = query
        results = []
        
        embed_query = get_embedding(query)

        for i in range(len(self.chunks)):
            # print('calculating similarity with chunk ', i)
            sim = cosine_sim(
                embed_query,
                self.embed_chunk[i] if self.mode == "code" else self.embed_corpus[i]
            )
            # print(f"Similarity with chunk {i}: {sim}")
            result_dict = {
                "similarity score": sim,
                "original instruction": self.corpus[i],
                "code": self.chunks[i]
            }
            results.append(result_dict)

        # Sort results by similarity score in descending order
        results.sort(key=lambda x: x['similarity score'], reverse=True)
        return results[:top_k]

class coreSplitRetriever:
    def __init__(self, mode="code"):
        self.corpus = []
        self.chunks_core = []
        self.chunks_auxiliary = []
        self.embed_core = []
        self.embed_aux = []
        # self.embedder = pipeline("feature-extraction", model="/shared/models/hf/jina-embeddings-v3", trust_remote_code=True)

    def process(self, content_input_path: str):
        with open(content_input_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        print('Original total number: ', len(content))
        for c in content:
            self.corpus.append(c["description_1"])

            # feed code into parser
            # print(c["description_1"])
            # print(c["code"])
            # core, auxiliary = split_core_auxiliary(c["code"]).values()
            # print("Core part:\n", core)
            # print("Auxiliary part:\n", auxiliary)
            # input("Press Enter to continue...")

            # if core not in self.chunks_core:
            # self.chunks_core.append(core)
            # if auxiliary not in self.chunks_auxiliary:
            # self.chunks_auxiliary.append(auxiliary)
        
        with open("/home/wentao/GEAK-agent/src/retrievers/parsed_corpus_embeddings_split_ordered.json", "r", encoding="utf-8") as f:
            parsed_embedding = json.load(f)
        self.chunks_core = parsed_embedding["core_code"]
        self.chunks_auxiliary = parsed_embedding["aux_code"]
        self.embed_core = parsed_embedding["core_embed"]
        self.embed_aux = parsed_embedding["aux_embed"]
        print("Actual core number: ", len(self.chunks_core))
        print("Actual auxiliary number: ", len(self.chunks_auxiliary))

    def query(
                self,
                query: str,
                top_k: int = 1
        ) -> List[Dict[str, Any]]:
        if top_k <= 0:
            raise ValueError("top_k must be a positive integer.")
        if not self.chunks_auxiliary or not self.chunks_core:
            raise ValueError("Corpus is empty. Load corpus first.")
        
        processed_query = split_core_auxiliary(query)
        # print("Processed query core part:", processed_query["core"])
        # print("Processed query auxiliary part:", processed_query["auxiliary"])
        # input("Press Enter to continue...")
        results_core = []
        results_aux = []
        embed_query_core = get_embedding(processed_query["core"])
        embed_query_aux = get_embedding(processed_query["auxiliary"]) if processed_query["auxiliary"].strip() else None
        
        if processed_query["core"] == None:
            raise ValueError("================Empty core code!===============")
            
        # combined_sim = 0.7 * sim_core + 0.3 * sim_aux  # weighted sum
        
        for i in range(len(self.chunks_core)):
            if self.embed_core[i] == None:
                raise ValueError("corpus core empty!")
            sim_core = cosine_sim(
                embed_query_core,
                self.embed_core[i]
            )
            # print(f"Core similarity with chunk {i}: {sim_core}")
            
            result_dict = {
                "similarity score": sim_core,
                # "original instruction": self.corpus[i],
                "core code": self.chunks_core[i],
                # "auxiliary code": self.chunks_auxiliary[i]
            }
            results_core.append(result_dict)

        if embed_query_aux:
            for i in range(len(self.chunks_auxiliary)):
                sim_aux = cosine_sim(
                    embed_query_aux,
                    self.embed_aux[i]
                )
                # print(f"Auxiliary similarity with chunk {i}: {sim_aux}")
                
                result_dict = {
                    "similarity score": sim_aux,
                    # "original instruction": self.corpus[i],
                    # "core code": self.chunks_core[i],
                    "auxiliary code": self.chunks_auxiliary[i]
                }
                results_aux.append(result_dict)

        # Sort results by similarity score in descending order
        results_core.sort(key=lambda x: x['similarity score'], reverse=True)
        results_aux.sort(key=lambda x: x['similarity score'], reverse=True)
        # need to merge results, but we can choose top_k = 1 only
        # results = []
        # for idx in range(top_k):
        #     results.append({**results_core[idx], **results_aux[idx]})
        
        # 两段分开取再拼接，可能完全无法运行，效果太差
        # if embed_query_aux:
        #     ret_dict = {
        #         "similarity score core": results_core[0]["similarity score"],
        #         "similarity score aux": results_aux[0]["similarity score"],
        #         "code": results_aux[0]["auxiliary code"] + "\n" + results_core[0]["core code"]
        #     }
        # else:
        ret_dict = {
            "similarity score core": results_core[0]["similarity score"],
            "similarity score aux": None,
            "code": results_core[0]["core code"]
        }

        # print(results_core[0]["core code"])
        return [ret_dict]

class coreToWholeRetriever:
    def __init__(self, mode="code"):
        self.corpus = []
        self.chunks = []
        self.chunks_core = []
        self.chunks_auxiliary = []
        self.embed_core = []
        self.embed_aux = []
        # self.embedder = pipeline("feature-extraction", model="/shared/models/hf/jina-embeddings-v3", trust_remote_code=True)

    def process(self, content_input_path: str):
        with open(content_input_path, "r", encoding="utf-8") as f:
            content = json.load(f)
        print('Original total number: ', len(content))
        for c in content:
            self.corpus.append(c["description_1"])
            self.chunks.append(c["code"])

        with open("/home/wentao/GEAK-agent/src/retrievers/parsed_corpus_embeddings_split_ordered_whole.json", "r", encoding="utf-8") as f:
            parsed_embedding = json.load(f)
        self.chunks_core = parsed_embedding["core_code"]
        self.chunks_auxiliary = parsed_embedding["aux_code"]
        self.embed_core = parsed_embedding["core_embed"]
        self.embed_aux = parsed_embedding["aux_embed"]

        print("Actual core number: ", len(self.chunks_core), len(self.embed_core))
        print("Actual auxiliary number: ", len(self.chunks_auxiliary), len(self.embed_aux))

    def query(
                self,
                query: str,
                top_k: int = 1
        ) -> List[Dict[str, Any]]:
        if top_k <= 0:
            raise ValueError("top_k must be a positive integer.")
        if not self.chunks_auxiliary or not self.chunks_core:
            raise ValueError("Corpus is empty. Load corpus first.")
        
        processed_query = split_core_auxiliary(query)
        # print("Processed query core part:", processed_query["core"])
        # print("Processed query auxiliary part:", processed_query["auxiliary"])
        # input("Press Enter to continue...")
        results_core = []
        results_aux = []
        embed_query_core = get_embedding(processed_query["core"])
        # embed_query_aux = get_embedding(processed_query["auxiliary"]) if processed_query["auxiliary"].strip() else None
        
        if processed_query["core"] == None:
            raise ValueError("================Empty core code!===============")
        
        
        # combined_sim = 0.7 * sim_core + 0.3 * sim_aux  # weighted sum
        
        for i in range(len(self.chunks_core)):
            if self.embed_core[i] == None:
                raise ValueError("corpus core empty!")
            sim_core = cosine_sim(
                embed_query_core,
                self.embed_core[i]
            )
            # print(f"Core similarity with chunk {i}: {sim_core}")
            
            result_dict = {
                "similarity score": sim_core,
                "original instruction": self.corpus[i],
                "code": self.chunks[i],
                "core code": self.chunks_core[i],
                "auxiliary code": self.chunks_auxiliary[i]
            }
            results_core.append(result_dict)


        # if embed_query_aux:
        #     for i in range(len(self.chunks_auxiliary)):
        #         sim_aux = cosine_sim(
        #             embed_query_aux,
        #             self.embed_aux[i]
        #         )
        #         # print(f"Auxiliary similarity with chunk {i}: {sim_aux}")
                
        #         result_dict = {
        #             "similarity score": sim_aux,
        #             "original instruction": self.corpus[i],
        #             "code": self.chunks[i],
        #             "core code": self.chunks_core[i],
        #             "auxiliary code": self.chunks_auxiliary[i]
        #         }
        #         results_aux.append(result_dict)

        # Sort results by similarity score in descending order
        results_core.sort(key=lambda x: x['similarity score'], reverse=True)
        # results_aux.sort(key=lambda x: x['similarity score'], reverse=True)
        # need to merge results, but we can choose top_k = 1 only
        # results = []
        # for idx in range(top_k):
        #     results.append({**results_core[idx], **results_aux[idx]})

        for idx in range(10):
            print("Top ", idx)
            print("With similarity score: ", results_core[idx]["similarity score"])
            # input("Press Enter to continue...")
        
        # 两段分开取再拼接，可能完全无法运行，效果太差
        # if embed_query_aux:
        #     ret_dict = {
        #         "similarity score core": results_core[0]["similarity score"],
        #         "similarity score aux": results_aux[0]["similarity score"],
        #         "code": results_aux[0]["auxiliary code"] + "\n" + results_core[0]["core code"]
        #     }
        # else:
        # ret_dict = {
        #     "similarity score core": results_core[0]["similarity score"],
        #     "similarity score aux": None,
        #     "code": results_core[0]["code"]
        # }

        # with open("/home/wentao/GEAK-agent/outputs/retrieved_score/debug_core_to_whole.json", "w") as f:
        #     json.dump(results_core, f, indent=4)
            
        # print('best result: ', results_core[0])
        return results_core[:top_k]

class combineRetriever:
    def __init__(self, mode="instruction"):
        self.mode = mode
        assert mode in ("instruction", "code")
        # self.chunks = []
        # self.corpus = []
        # self.embed_chunk = []
        # self.embed_corpus = []

        self.bm25 = BM25Retriever(mode=mode)

    def process(self, content_input_path: str):
        self.bm25.process(content_input_path=content_input_path)
    
    def query(
            self,
            query: str,
            top_k1: int = 100,
            top_k2: int = 1,
        ) -> List[Dict[str, Any]]:
        # first filter
        results = self.bm25.query(query=query, top_k=top_k1)
        key_name = 'code' if self.mode == 'code' else 'original instruction'
        query_embed = get_embedding(query)
        # second re-rank
        for idx, item in enumerate(results):
            results[idx]["similarity score"] = cosine_sim(
                query_embed, get_embedding(results[idx][key_name]))
        
        results.sort(key=lambda x: x['similarity score'], reverse=True)
        return results[:top_k2]

if __name__ == "__main__":
    # retriever = BM25Retriever(mode="code")
    # retriever.process("../dataloaders/TB_eval/train_crawl.json")


    # retriever = EmbeddingRetriever()
    retriever = coreSplitRetriever()
    retriever.process("../dataloaders/TB_eval/train_crawl.json")

    results = retriever.query("import triton\nimport triton.language as tl\n\n# triton kernel\n@triton.jit\ndef kernel(X, stride_xm,\n           Z, stride_zn,\n           BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr):\n    off_m = tl.arange(0, BLOCK_M)\n    off_n = tl.arange(0, BLOCK_N)\n    Xs = X + off_m[:, None] * stride_xm + off_n[None, :] * 1\n    Zs = Z + off_m[:, None] * 1 + off_n[None, :] * stride_zn\n    tl.store(Zs, tl.load(Xs))\n\n\nret = triton.compile(kernel, signature=\"*fp32,i32,*fp32,i32\", constants={\"BLOCK_M\": 64, \"BLOCK_N\": 64}, output=\"ttgir\")\n\nprint(ret)\n", top_k=2)
    for res in results:
        print(res)

    # code = "import torch\nimport triton\nimport triton.language as tl\n\n@triton.jit\ndef _layer_norm_fwd_fused(\n    Out,\n    A,\n    Weight,\n    Bias,\n    Mean, Rstd,\n    stride, N, eps,\n    BLOCK_SIZE: tl.constexpr,\n):\n    # position of elements processed by this program\n    row = tl.program_id(0)\n    Out += row * stride\n    A += row * stride\n    # compute mean\n    mean = 0\n    _mean = tl.zeros([BLOCK_SIZE], dtype=tl.float32)\n    for off in range(0, N, BLOCK_SIZE):\n        cols = off + tl.arange(0, BLOCK_SIZE)\n        a = tl.load(A + cols, mask=cols < N, other=0., eviction_policy=\"evict_last\").to(tl.float32)\n        _mean += a\n    mean = tl.sum(_mean, axis=0) / N\n    # compute variance\n    _var = tl.zeros([BLOCK_SIZE], dtype=tl.float32)\n    for off in range(0, N, BLOCK_SIZE):\n        cols = off + tl.arange(0, BLOCK_SIZE)\n        a = tl.load(A + cols, mask=cols < N, other=0., eviction_policy=\"evict_last\").to(tl.float32)\n        a = tl.where(cols < N, a - mean, 0.)\n        _var += a * a\n    var = tl.sum(_var, axis=0) / N\n    rstd = 1 / tl.sqrt(var + eps)\n    # write-back mean/rstd\n    tl.store(Mean + row, mean)\n    tl.store(Rstd + row, rstd)\n    # multiply by weight and add bias\n    for off in range(0, N, BLOCK_SIZE):\n        cols = off + tl.arange(0, BLOCK_SIZE)\n        mask = cols < N\n        weight = tl.load(Weight + cols, mask=mask)\n        bias = tl.load(Bias + cols, mask=mask)\n        a = tl.load(A + cols, mask=mask, other=0., eviction_policy=\"evict_first\").to(tl.float32)\n        a_hat = (a - mean) * rstd\n        out = a_hat * weight + bias\n        # # write-back\n        tl.store(Out + cols, out, mask=mask)\n\n@triton.jit\ndef _layer_norm_bwd_dx_fused(\n    _DA,\n    _DOut,\n    _A,\n    Weight,\n    Mean, Rstd,\n    stride, NumRows, NumCols, eps,\n    BLOCK_SIZE_N: tl.constexpr,\n):\n    # position of elements processed by this program\n    pid = tl.program_id(0)\n    row = pid\n    A = _A + row * stride\n    DOut = _DOut + row * stride\n    DA = _DA + row * stride\n    mean = tl.load(Mean + row)\n    rstd = tl.load(Rstd + row)\n    # load data to SRAM\n    _mean1 = tl.zeros([BLOCK_SIZE_N], dtype=tl.float32)\n    _mean2 = tl.zeros([BLOCK_SIZE_N], dtype=tl.float32)\n    for off in range(0, NumCols, BLOCK_SIZE_N):\n        cols = off + tl.arange(0, BLOCK_SIZE_N)\n        mask = cols < NumCols\n        a = tl.load(A + cols, mask=mask, other=0).to(tl.float32)\n        dout = tl.load(DOut + cols, mask=mask, other=0).to(tl.float32)\n        weight = tl.load(Weight + cols, mask=mask, other=0).to(tl.float32)\n        a_hat = (a - mean) * rstd\n        wdout = weight * dout\n        _mean1 += a_hat * wdout\n        _mean2 += wdout\n    mean1 = tl.sum(_mean1, axis=0) / NumCols\n    mean2 = 0.\n    mean2 = tl.sum(_mean2, axis=0) / NumCols\n    for off in range(0, NumCols, BLOCK_SIZE_N):\n        cols = off + tl.arange(0, BLOCK_SIZE_N)\n        mask = cols < NumCols\n        a = tl.load(A + cols, mask=mask, other=0).to(tl.float32)\n        dout = tl.load(DOut + cols, mask=mask, other=0).to(tl.float32)\n        weight = tl.load(Weight + cols, mask=mask, other=0).to(tl.float32)\n        a_hat = (a - mean) * rstd\n        wdout = weight * dout\n        da = (wdout - (a_hat * mean1 + mean2)) * rstd\n        # write-back dx\n        tl.store(DA + cols, da, mask=mask)\n\n@triton.jit\ndef _layer_norm_bwd_dwdb(\n    A, DOut,\n    Mean, Var,\n    DW,\n    DB,\n    M, N,\n    BLOCK_SIZE_M: tl.constexpr,\n    BLOCK_SIZE_N: tl.constexpr,\n):\n    pid = tl.program_id(0)\n    cols = pid * BLOCK_SIZE_N + tl.arange(0, BLOCK_SIZE_N)\n    dw = tl.zeros((BLOCK_SIZE_M, BLOCK_SIZE_N), dtype=tl.float32)\n    db = tl.zeros((BLOCK_SIZE_M, BLOCK_SIZE_N), dtype=tl.float32)\n    UNROLL: tl.constexpr = 4\n    for i in range(0, M, BLOCK_SIZE_M * UNROLL):\n        for j in range(UNROLL):\n            rows = i + j * BLOCK_SIZE_M + tl.arange(0, BLOCK_SIZE_M)\n            mask = (rows[:, None] < M) & (cols[None, :] < N)\n            offs = rows[:, None] * N + cols[None, :]\n            a = tl.load(A + offs, mask=mask, other=0.).to(tl.float32)\n            dout = tl.load(DOut + offs, mask=mask, other=0.).to(tl.float32)\n            mean = tl.load(Mean + rows, mask=rows < M, other=0.)\n            rstd = tl.load(Var + rows, mask=rows < M, other=0.)\n            a_hat = (a - mean[:, None]) * rstd[:, None]\n            dw += dout * a_hat\n            db += dout\n    sum_dw = tl.sum(dw, axis=0)\n    sum_db = tl.sum(db, axis=0)\n    tl.store(DW + cols, sum_dw, mask=cols < N)\n    tl.store(DB + cols, sum_db, mask=cols < N)\n\nclass LayerNorm(torch.autograd.Function):\n    @staticmethod\n    def forward(ctx, a, normalized_shape, weight, bias, eps):\n        # allocate output\n        out = torch.empty_like(a)\n        # reshape input data into 2D tensor\n        a_arg = a.reshape(-1, a.shape[-1])\n        M, N = a_arg.shape\n        mean = torch.empty((M,), dtype=torch.float32, device=\"cuda\")\n        rstd = torch.empty((M,), dtype=torch.float32, device=\"cuda\")\n        # Less than 64KB per feature: enqueue fused kernel\n        MAX_FUSED_SIZE = 65536 // a.element_size()\n        BLOCK_SIZE = min(MAX_FUSED_SIZE, triton.next_power_of_2(N))\n        BLOCK_SIZE = max(BLOCK_SIZE, 128)\n        BLOCK_SIZE = min(BLOCK_SIZE, 4096)\n        # heuristics for number of warps\n        num_warps = min(max(BLOCK_SIZE // 256, 1), 8)\n        _layer_norm_fwd_fused[(M,)](\n            out,\n            a_arg,\n            weight,\n            bias,\n            mean, rstd,\n            a_arg.stride(0), N, eps,\n            BLOCK_SIZE=BLOCK_SIZE,\n            num_warps=num_warps,\n        )\n        ctx.save_for_backward(\n            a, weight, bias, mean, rstd,\n        )\n        ctx.BLOCK_SIZE = BLOCK_SIZE\n        ctx.num_warps = num_warps\n        ctx.eps = eps\n        if hasattr(bias, \"config\"):\n            assert bias.config.grad_scale_name == weight.config.grad_scale_name\n            grad_scale_name = bias.config.grad_scale_name\n        else:\n            grad_scale_name = None\n        ctx.grad_scale_gain_bias_name = grad_scale_name\n        return out\n\n    @staticmethod\n    def backward(ctx, dout):\n        assert dout.is_contiguous()\n        a, weight, bias, mean, var = ctx.saved_tensors\n        # heuristics for amount of parallel reduction stream for DG/DB\n        N = weight.shape[0]\n        # allocate output\n        da = torch.empty_like(dout)\n        # enqueue kernel using forward pass heuristics\n        # also compute partial sums for DW and DB\n        x_arg = a.reshape(-1, a.shape[-1])\n        M, N = x_arg.shape\n        dweight = torch.empty((weight.shape[0],), dtype=weight.dtype, device=weight.device)\n        dbias = torch.empty((weight.shape[0],), dtype=weight.dtype, device=weight.device)\n        _layer_norm_bwd_dx_fused[(M,)](\n            da,\n            dout,\n            a,\n            weight,\n            mean, var,\n            x_arg.stride(0), M, N,\n            ctx.eps,\n            BLOCK_SIZE_N=ctx.BLOCK_SIZE,\n            num_warps=ctx.num_warps,\n        )\n        if N > 10240:\n            BLOCK_SIZE_N = 128\n            BLOCK_SIZE_M = 32\n            num_warps = 4\n        else:\n            # maximize occupancy for small N\n            BLOCK_SIZE_N = 16\n            BLOCK_SIZE_M = 16\n            num_warps = 8\n        grid = lambda meta: [triton.cdiv(N, meta[\"BLOCK_SIZE_N\"])]\n        _layer_norm_bwd_dwdb[grid](\n            a, dout,\n            mean, var,\n            dweight,\n            dbias,\n            M,\n            N,\n            BLOCK_SIZE_M=BLOCK_SIZE_M,\n            BLOCK_SIZE_N=BLOCK_SIZE_N,\n            num_warps=num_warps\n        )\n        return (da, None, dweight, dbias, None)\n\ndef layer_norm(a, normalized_shape, weight, bias, eps):\n    return LayerNorm.apply(a, normalized_shape, weight, bias, eps)\n"

    # # result = split_core_auxiliary(code)
    # result = split_code_by_rules(code)

    # print("=== CORE ===")
    # print(result["core"])
    # print("\n=== AUXILIARY ===")
    # print(result["auxiliary"])