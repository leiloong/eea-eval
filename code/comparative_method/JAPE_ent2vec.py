import numpy as np
import time
import sys
from scipy import io
from sklearn import preprocessing
from JAPE_func import *
import scipy as sp

SPLIT = '\t'

beishu = 10


def read_ents_props(props_file):
    ents = dict()
    file = open(props_file, 'r', encoding='utf8')
    for line in file.readlines():
        params = line.strip().split(SPLIT)
        ents[params[0]] = params[1:]
    return ents


def read_meta_2id(meta_file):
    ids = dict()
    file = open(meta_file, 'r', encoding='utf8')
    lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i].strip('\n').strip()
        ids[line] = i
    return ids


def read_selected_attrs(meta_file):
    ids = set()
    file = open(meta_file, 'r', encoding='utf8')
    lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i].strip('\n').strip()
        ids.add(int(line))
    return ids


def vec2file(vec, title, local_ents_fw, local_meta_fw):
    line = ''
    for i in range(vec.shape[0]):
        line = line + str(vec[i]) + '\t'
    local_ents_fw.write(line.strip() + '\n')
    local_meta_fw.write(title + '\n')


def generate_kb_ents_vecs(vec_dict, ents_list, ids_uris_dict, zero_vec, ents_fw, meta_fw, npy_file):
    print("begin generate_kb_ents_vecs...")
    t = time.time()
    mat = list()
    print(len(ents_list))
    for ent in ents_list:
        if ent in vec_dict:
            vec = vec_dict.get(ent)
        else:
            vec = zero_vec
        vec2file(vec, ids_uris_dict[ent], ents_fw, meta_fw)
        mat.append(vec)
    mat = np.matrix(mat)
    mat = preprocessing.normalize(mat)
    assert mat.shape[0] == len(ents_list)
    np.save(npy_file, mat)
    print("end generate_kb_ents_vecs...cost", time.time() - t)
    print()
    return mat


def get_sim_mat(mat11, mat22, is_norm=False, is_sparse=True, is_filtered=True, th=0.8):
    print("begin dot...")
    t = time.time()
    sim = np.dot(mat11, mat22.T)
    print("max sim", np.max(sim))
    print("end dot...cost", time.time() - t)

    if is_filtered:
        print("filtered by sim th:", th)
        print(len(np.where(sim > th)[0]))
        sim[sim < th] = 0.0

    if is_norm:
        print("begin normalize...")
        t = time.time()
        sim = preprocessing.normalize(sim, norm='l1')
        print("end normalize...cost", time.time() - t)
    if is_sparse:
        print("begin sparse...")
        t = time.time()
        # sim = sp.sparse.csr_matrix(sim)
        sim = sp.sparse.lil_matrix(sim)
        print("end sparse...cost", time.time() - t)
    print()
    return sim


def add_dict_kv(dic, k, v):
    vs = dic.get(k, set())
    vs.add(v)
    dic[k] = vs


def generate_related_ents(triples):
    related_ents_dict = dict()
    for h, r, t in triples:
        add_dict_kv(related_ents_dict, h, t)
    return related_ents_dict


def to_ids(related_ents, ids_uris_dict, kb_ents):
    """
    id转换，训练数据的id转换为矩阵下标的id
    :param related_ents:
    :param ids_uris_dict:
    :param kb_ents:
    :return:
    """
    ids = set()
    for id in related_ents:
        ids.add(kb_ents.index(id))
    assert len(ids) == len(related_ents)
    return ids


def enhance_sim(sim_mat, kb1_ents, kb2_ents, ids_uris_dict1, ids_uris_dict2, sup_ents_pairs, related_ents_dict1,
                related_ents_dict2, th=0.8):
    print("begin enhance_sim...")
    t = time.time()
    total_sim = 0
    related_pair = dict()
    for e1, e2 in sup_ents_pairs:
        if e1 in related_ents_dict1.keys() and e2 in related_ents_dict2.keys():
            e1_id = kb1_ents.index(e1)
            e2_id = kb2_ents.index(e2)
            total_sim += sim_mat[e1_id, e2_id]
            sim_mat[e1_id, e2_id] = 1
            # print("sim of sups", sim_mat[e1_id, e2_id])
            related_ents1 = to_ids(related_ents_dict1.get(e1), ids_uris_dict1, kb1_ents)
            related_ents2 = to_ids(related_ents_dict2.get(e2), ids_uris_dict2, kb2_ents)
            for r1 in related_ents1:
                for r2 in related_ents2:
                    related_pair[(r1, r2)] = related_pair.get((r1, r2), 0) + 1
    print("related pairs", len(related_pair))
    avg_sim = total_sim / len(sup_ents_pairs)
    print("ava sim of sups", avg_sim)
    # sim_mat[sim_mat < th // 3] = 0.0
    for r1, r2 in related_pair:
        sim_mat[r1, r2] *= (related_pair.get((r1, r2)) + 1) * 100  # big data
        # sim_mat[r1, r2] *= pow(3, related_pair.get((r1, r2)))  # small data
        sim_mat[r1, r2] = max(1, sim_mat[r1, r2])
        # if sim_mat[r1, r2] > 0.0001:
        #     sim_mat[r1, r2] = max(1.0, sim_mat[r1, r2])
    print("filtered by sim th:", th)
    sim_mat[sim_mat < th] = 0.0
    sim_mat = preprocessing.normalize(sim_mat, norm='l1')
    sim_mat = sp.sparse.csr_matrix(sim_mat)

    print("end enhance_sim...cost", time.time() - t)
    print()
    return sim_mat


def read_ent_attr_ids(file):
    ent_attr_dic = dict()
    attrs = set()
    with open(file, 'r', encoding='utf8') as f:
        for line in f:
            params = line.strip('\n').split('\t')
            assert len(params) >= 2
            s = set()
            for a in set(params[1:]):
                s.add(int(a))
            ent_attr_dic[int(params[0])] = s
            attrs |= s
    return ent_attr_dic, attrs


def ent2vec(folder, sim_th1=0.95, sim_th2=0.95, enhance_sim_th=0.9):
    vec_folder = folder + 'jape/'
    kb1_ents_fw = open(vec_folder + 'ents_embeddings_1', 'w', encoding='utf8')
    kb2_ents_fw = open(vec_folder + 'ents_embeddings_2', 'w', encoding='utf8')
    kb1_meta_fw = open(vec_folder + 'ents_meta_1', 'w', encoding='utf8')
    kb2_meta_fw = open(vec_folder + 'ents_meta_2', 'w', encoding='utf8')

    props_embeddings_file = vec_folder + 'attrs_vec.npy'
    props_meta_file = vec_folder + 'attrs_meta'
    selected_ids = read_selected_attrs(props_meta_file)
    embddings = np.load(props_embeddings_file)
    kb1_ents, ids_uris_dict1, uris_ids_dict1 = read_ents_by_order_dic(folder + 'ent_ids_1')
    kb2_ents, ids_uris_dict2, uris_ids_dict2 = read_ents_by_order_dic(folder + 'ent_ids_2')
    triples1 = read_triple_ids(folder + 'triples_1')
    triples2 = read_triple_ids(folder + 'triples_2')
    related_ents_dict1 = generate_related_ents(triples1)
    related_ents_dict2 = generate_related_ents(triples2)

    ent_attrs1, attrs1 = read_ent_attr_ids(folder + 'ent_attrs_1')
    ent_attrs2, attrs2 = read_ent_attr_ids(folder + 'ent_attrs_2')

    sup_ents_pairs = read_pair_ids(folder + 'sup_ent_ids')
    sup_ents_dict = pair_2dict(sup_ents_pairs)
    ent_vec_dict1 = dict()
    ent_vec_dict2 = dict()

    print("全部实体:", len(attrs1))
    for ent, props in ent_attrs1.items():
        prop_indexs = set()
        for p in props:
            if p in selected_ids:
                prop_indexs.add(p)
        if len(prop_indexs) < 2:
            continue
        prop_indexs = list(prop_indexs)
        prop_embddings = embddings[prop_indexs]
        # ent_vec = np.sum(prop_embddings, axis=0)
        ent_vec = np.sum(prop_embddings, axis=0) / len(prop_indexs)
        ent_vec_dict1[ent] = ent_vec

    for ent, props in ent_attrs2.items():
        prop_indexs = set()
        for p in props:
            if p in selected_ids:
                prop_indexs.add(p)
        if len(prop_indexs) < 2:
            continue
        prop_indexs = list(prop_indexs)
        prop_embddings = embddings[prop_indexs]
        # ent_vec = np.sum(prop_embddings, axis=0)
        ent_vec = np.sum(prop_embddings, axis=0) / len(prop_indexs)
        ent_vec_dict2[ent] = ent_vec

    dim = ent_vec.shape[0]
    zero_vec = np.zeros((dim,), dtype=np.int)

    mat1 = generate_kb_ents_vecs(ent_vec_dict1, kb1_ents, ids_uris_dict1, zero_vec, kb1_ents_fw, kb1_meta_fw, vec_folder + "ents_vec_1")
    kb1_ents_sim = get_sim_mat(mat1, mat1, th=sim_th1)
    print("begin mmwrite kb1...")
    t = time.time()
    io.mmwrite(vec_folder + "kb1_ents_sim.mtx", kb1_ents_sim)
    print("end mmwrite...cost", time.time() - t)
    print()
    del kb1_ents_sim

    mat2 = generate_kb_ents_vecs(ent_vec_dict2, kb2_ents, ids_uris_dict2, zero_vec, kb2_ents_fw, kb2_meta_fw, vec_folder + "ents_vec_2")
    kb2_ents_sim = get_sim_mat(mat2, mat2, th=sim_th2)
    print("begin mmwrite kb2...")
    t = time.time()
    io.mmwrite(vec_folder + "kb2_ents_sim.mtx", kb2_ents_sim)
    print("end mmwrite...cost", time.time() - t)
    print()
    del kb2_ents_sim

    # ents_fw.close()
    kb1_ents_fw.close()
    kb2_ents_fw.close()
    # meta_fw.close()
    kb1_meta_fw.close()
    kb2_meta_fw.close()

    sim_mat = get_sim_mat(mat1, mat2, is_sparse=False, is_filtered=False)
    print(sim_mat.min(), sim_mat.max(), sim_mat.mean())
    sim_mat = enhance_sim(sim_mat, kb1_ents, kb2_ents, ids_uris_dict1, ids_uris_dict2, sup_ents_pairs,
                          related_ents_dict1, related_ents_dict2, th=enhance_sim_th)
    print("begin mmwrite kb12...")
    t = time.time()
    io.mmwrite(vec_folder + "ents_sim.mtx", sim_mat)
    print("end mmwrite...cost", time.time() - t)
    print()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        ent2vec(folder, sim_th1=1, sim_th2=1, enhance_sim_th=1)
    elif len(sys.argv) == 1:
        folder = '../en_fr_15k/0_2/'
        ent2vec(folder, sim_th1=1, sim_th2=1, enhance_sim_th=1)
