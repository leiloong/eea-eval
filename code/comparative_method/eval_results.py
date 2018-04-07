import gc
import numpy as np
import time
import multiprocessing
valid_mul = 2

top_k = [1, 5, 10, 50]


def radio2str(radio):
    return str(radio).replace('.', '_')


def generate_res_folder(training_data_path, method_name, radio):
    path = training_data_path.strip('/').split('/')[-1]
    return "res/" + method_name + '/' + path + "/" + radio2str(radio) + "/" + str(time.strftime("%Y%m%d%H%M")) + "/"


def div_list(ls, n):
    ls_len = len(ls)
    if n <= 0 or 0 == ls_len:
        return []
    if n > ls_len:
        return []
    elif n == ls_len:
        return [[i] for i in ls]
    else:
        j = ls_len // n
        k = ls_len % n
        ls_return = []
        for i in range(0, (n - 1) * j, j):
            ls_return.append(ls[i:i + j])
        ls_return.append(ls[(n - 1) * j:])
        return ls_return


def cal_rank_multi_embed(frags, dic, sub_embed, embed, top_k):
    mean = 0
    mrr = 0
    num = np.array([0 for k in top_k])
    sim_mat = np.matmul(sub_embed, embed.T)
    prec_set = set()
    for i in range(len(frags)):
        ref = frags[i]
        rank = (-sim_mat[i, :]).argsort()
        aligned_e = rank[0]
        assert ref in rank
        rank_index = np.where(rank == ref)[0][0]
        mean += (rank_index + 1)
        mrr += 1 / (rank_index + 1)
        for j in range(len(top_k)):
            if rank_index < top_k[j]:
                num[j] += 1
        prec_set.add((ref, aligned_e))
    del sim_mat
    return mean, mrr, num, prec_set


def eval_alignment_multi_embed(embed1, embed2):
    t = time.time()
    ref_num = embed1.shape[0]
    t_num = np.array([0 for k in top_k])
    t_mean = 0
    t_mrr = 0
    t_prec_set = set()
    frags = div_list(np.array(range(ref_num)), valid_mul)
    pool = multiprocessing.Pool(processes=len(frags))
    reses = list()
    for frag in frags:
        reses.append(pool.apply_async(cal_rank_multi_embed, (frag, None, embed1[frag, :], embed2, top_k)))
    pool.close()
    pool.join()

    for res in reses:
        mean, mrr, num, prec_set = res.get()
        t_mean += mean
        t_mrr += mrr
        t_num += num
        t_prec_set |= prec_set

    assert len(t_prec_set) == ref_num

    acc = t_num / ref_num
    for i in range(len(acc)):
        acc[i] = round(acc[i], 4)
    t_mean /= ref_num
    t_mrr /= ref_num
    print("hits@{} = {}, mr = {:.3f}, mrr = {:.3f}, time = {:.3f} s ".format(top_k, acc, t_mean, t_mrr,
                                                                                 time.time() - t))
    return t_prec_set, acc[0]


def cal_rank(task, sim):
    mean = 0
    mrr = 0
    num = np.array([0 for k in top_k])
    prec_set = set()
    for i in range(len(task)):
        ref = task[i]
        rank = (-sim[i, :]).argsort()
        aligned_e = rank[0]
        assert ref in rank
        rank_index = np.where(rank == ref)[0][0]
        mean += (rank_index + 1)
        mrr += 1 / (rank_index + 1)
        for j in range(len(top_k)):
            if rank_index < top_k[j]:
                num[j] += 1
        prec_set.add((ref, aligned_e))
    return mean, mrr, num, prec_set


def eval_alignment_mul(sim_mat, d=False):
    t = time.time()
    ref_num = sim_mat.shape[0]
    t_num = [0 for k in top_k]
    t_mean = 0
    t_mrr = 0
    t_prec_set = set()
    tasks = div_list(np.array(range(ref_num)), valid_mul)
    pool = multiprocessing.Pool(processes=len(tasks))
    reses = list()
    for task in tasks:
        reses.append(pool.apply_async(cal_rank, (task, sim_mat[task, :])))
    pool.close()
    pool.join()

    for res in reses:
        mean, mrr, num, prec_set = res.get()
        t_mean += mean
        t_mrr += mrr
        t_num += num
        t_prec_set |= prec_set

    assert len(t_prec_set) == ref_num

    acc = t_num / ref_num
    for i in range(len(acc)):
        acc[i] = round(acc[i], 4)
    t_mean /= ref_num
    t_mrr /= ref_num
    print("hits@{} = {}, mr = {:.3f}, mrr = {:.3f}, time = {:.3f} s ".format(top_k, acc, t_mean, t_mrr,
                                                                                 time.time() - t))
    if d:
        del sim_mat
        gc.collect()
    return t_prec_set, acc[0]


def early_stop(ppre_hits1, pre_hits1, hits1, small=True):
    if small:
        if hits1 < pre_hits1 < ppre_hits1:
            print("\n == should early stop == \n")
            return pre_hits1, hits1, True
        else:
            return pre_hits1, hits1, False
    else:
        if hits1 < pre_hits1:
            print("\n == should early stop == \n")
            return pre_hits1, hits1, True
        else:
            return pre_hits1, hits1, False
