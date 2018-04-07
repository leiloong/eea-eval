import random

import gc
import numpy as np
import tensorflow as tf
from scipy import io
from sklearn import preprocessing
from cmp_model_utils import *
from triples_data import *
import time

from JAPE_loss import batch_size
from params import save_hits1

from eval_results import eval_alignment_multi_embed, early_stop, eval_alignment_mul


def jape_eva(ent_embeddings, ref_ent_s, ref_ent_t, e, res_folder, ppre_hits1, pre_hits1, is_early, small):
    embed1 = tf.nn.embedding_lookup(ent_embeddings, ref_ent_s).eval()
    embed2 = tf.nn.embedding_lookup(ent_embeddings, ref_ent_t).eval()
    prec_set1, hits1 = eval_alignment_multi_embed(embed1, embed2)
    prec_set2, hits12 = eval_alignment_multi_embed(embed2, embed1)
    # sim_mat = np.matmul(embed1, embed2.T)
    # prec_set1, hits1 = eval_alignment_mul(sim_mat)
    # prec_set2, hits12 = eval_alignment_mul(sim_mat.T)
    gc.collect()

    if not is_early:
        ppre_hits1, pre_hits1, is_early = early_stop(ppre_hits1, pre_hits1, hits1, small=small)
        if is_early:
            out_path = radio_2file(e, res_folder)
            pair2file(out_path + "res1", prec_set1)
            pair2file(out_path + "res2", prec_set2)
            np.save(out_path + "ents_vec", ent_embeddings.eval())
            return ppre_hits1, pre_hits1, is_early

    if e % save_hits1 == 0:
        out_path = radio_2file(e, res_folder)
        pair2file(out_path + "res1", prec_set1)
        pair2file(out_path + "res2", prec_set2)

    return ppre_hits1, pre_hits1, is_early


def pair2file(file, pairs):
    with open(file, 'w', encoding='utf8') as f:
        for i, j in pairs:
            f.write(str(i) + '\t' + str(j) + '\n')
        f.close()


def random_unit_embeddings(dim1, dim2):
    vectors = list()
    for i in range(dim1):
        vectors.append([random.gauss(0, 1) for j in range(dim2)])
    return preprocessing.normalize(np.matrix(vectors))


def generate_input(folder):
    print(folder)
    triples1 = read_triples_ids(folder + 'triples_1')
    triples_data1 = Triples_Data(triples1)

    triples2 = read_triples_ids(folder + 'triples_2')
    triples_data2 = Triples_Data(triples2)

    ent_num = len(triples_data1.ents | triples_data2.ents)
    rel_num = len(triples_data1.rels | triples_data2.rels)
    triples_num = len(triples1) + len(triples2)
    print('all ents:', ent_num)
    print('all rels:', len(triples_data1.rels), len(triples_data2.rels), rel_num)
    print('all triples: %d + %d = %d' % (len(triples1), len(triples2), triples_num))

    ref_ent1, ref_ent2 = read_ref(folder + 'ref_ent_ids')
    # ref_rel1, ref_rel2 = read_ref(folder + 'ref_rel_ids')
    assert len(ref_ent1) == len(ref_ent2)
    # assert len(ref_rel1) == len(ref_rel2)
    print("To aligned entities:", len(ref_ent1))
    # print("To aligned relations:", len(ref_rel1))
    sup_ents_pairs = read_pair_ids(folder + 'sup_ent_ids')

    return triples_data1, triples_data2, sup_ents_pairs, ref_ent1, ref_ent2, triples_num, ent_num, rel_num


def generate_pos_batch_of2KBs(triples_data1, triples_data2, step):
    # print(triples_data1.train_triples[0: 2])
    # print(triples_data2.train_triples[0: 2])
    assert batch_size % 2 == 0
    num1 = int(triples_data1.train_triples_num / (
        triples_data1.train_triples_num + triples_data2.train_triples_num) * batch_size)
    num2 = batch_size - num1
    start1 = step * num1
    start2 = step * num2
    end1 = start1 + num1
    end2 = start2 + num2
    if end1 > triples_data1.train_triples_num:
        end1 = triples_data1.train_triples_num
    if end2 > triples_data2.train_triples_num:
        end2 = triples_data2.train_triples_num
    pos_triples1 = triples_data1.train_triples[start1: end1]
    pos_triples2 = triples_data2.train_triples[start2: end2]
    return pos_triples1, pos_triples2


def generate_pos_batch(triples_data1, triples_data2, step):
    pos_triples1, pos_triples2 = generate_pos_batch_of2KBs(triples_data1, triples_data2, step)
    pos_triples1.extend(pos_triples2)
    assert len(pos_triples1) == batch_size
    return pos_triples1


def generate_pos_neg_batch(triples_data1, triples_data2, step, is_half=False, multi=1):
    pos_triples1, pos_triples2 = generate_pos_batch_of2KBs(triples_data1, triples_data2, step)
    if is_half:
        pos_triples11 = random.sample(pos_triples1, len(pos_triples1) // 2)
        pos_triples22 = random.sample(pos_triples2, len(pos_triples2) // 2)
        neg_triples1 = generate_neg_triples(pos_triples11, triples_data1)
        neg_triples2 = generate_neg_triples(pos_triples22, triples_data2)
    else:
        neg_triples1 = generate_neg_triples(pos_triples1, triples_data1)
        neg_triples2 = generate_neg_triples(pos_triples2, triples_data2)
    neg_triples1.extend(neg_triples2)
    if multi > 1:
        for i in range(multi - 1):
            neg_triples1.extend(generate_neg_triples(pos_triples1, triples_data1))
            neg_triples1.extend(generate_neg_triples(pos_triples2, triples_data2))
    pos_triples1.extend(pos_triples2)
    return pos_triples1, neg_triples1


def generate_neg_triples_overall(pos_triples, all_ents_list, all_triples_set):
    neg_triples = list()
    for (h, r, t) in pos_triples:
        h2, r2, t2 = h, r, t
        num = 0
        while True:
            choice = random.randint(0, 999)
            if choice < 500:
                h2 = random.sample(all_ents_list, 1)[0]
            elif choice >= 500:
                t2 = random.sample(all_ents_list, 1)[0]
            if (h2, r2, t2) not in all_triples_set:
                break
            else:
                num += 1
                if num > 10:
                    break
        neg_triples.append((h2, r2, t2))
    return neg_triples


def generate_neg_triples(pos_triples, triples_data):
    neg_triples = list()
    for (h, r, t) in pos_triples:
        h2, r2, t2 = h, r, t
        choice = random.randint(0, 999)
        if choice < 500:
            h2 = random.sample(triples_data.ents_list, 1)[0]
        elif choice >= 500:
            t2 = random.sample(triples_data.ents_list, 1)[0]
        # if not triples_data.exist(h2, r2, t2):
        neg_triples.append((h2, r2, t2))
    return neg_triples


def get_e_e_pairs(folder, file='ents_sim.mtx'):
    cross_sim_mat = io.mmread(folder + file).todense()
    ids1 = read_ids2list(folder + "ent_ids_1")
    ids2 = read_ids2list(folder + "ent_ids_2")
    l1, l2 = np.where(cross_sim_mat > 0)
    print(l1)
    print(l2)
    pairs = list()
    for i in range(len(l1)):
        pairs.append((ids1[l1[i]], ids2[l2[i]]))
    return pairs


def get_all_pairs(folder):
    ids1 = read_ids2list(folder + "ent_ids_1")
    ids2 = read_ids2list(folder + "ent_ids_2")
    pairs12 = list()

    cross_sim_mat = io.mmread(folder + 'ents_sim.mtx').todense()
    l1, l2 = np.where(cross_sim_mat > 0)
    for i in range(len(l1)):
        pairs12.append((ids1[l1[i]], ids2[l2[i]]))
    print(len(pairs12))

    sim_mat1 = io.mmread(folder + 'kb1_ents_sim.mtx').todense()
    l1, l2 = np.where(sim_mat1 > 0)
    for i in range(len(l1)):
        pairs12.append((ids1[l1[i]], ids1[l2[i]]))
    print(len(pairs12))

    sim_mat2 = io.mmread(folder + 'kb2_ents_sim.mtx').todense()
    l1, l2 = np.where(sim_mat2 > 0)
    for i in range(len(l1)):
        pairs12.append((ids2[l1[i]], ids2[l2[i]]))
    print(len(pairs12))

    return pairs12


def get_all_sim_mat_sparse(folder):
    folder += "jape/"
    cross_sim_mat = preprocessing.normalize(io.mmread(folder + 'ents_sim.mtx'), norm='l1')
    kb1_sim_mat = preprocessing.normalize(io.mmread(folder + 'kb1_ents_sim.mtx'), norm='l1')
    kb2_sim_mat = preprocessing.normalize(io.mmread(folder + 'kb2_ents_sim.mtx'), norm='l1')
    return cross_sim_mat, kb1_sim_mat, kb2_sim_mat


def sparse_mat_2sparse_tensor(sparse_mat):
    print("sparse sim mat to sparse tensor")
    indices = list()
    values = list()
    shape = sparse_mat.shape
    for i in range(shape[0]):
        cols = sparse_mat.indices[sparse_mat.indptr[i]:sparse_mat.indptr[i + 1]]
        if len(cols) > 0:
            data = sparse_mat.data[sparse_mat.indptr[i]:sparse_mat.indptr[i + 1]]
            assert len(data) == len(cols)
            for j in range(len(data)):
                values.append(data[j])
                indices.append([i, cols[j]])
    print("end sparse sim mat to sparse tensor")
    return tf.SparseTensor(indices=indices, values=values, dense_shape=shape)


def get_ids_by_order(folder):
    ids_list1 = read_ents_by_order(folder + 'ent_ids_1')
    ids_list2 = read_ents_by_order(folder + 'ent_ids_2')
    return ids_list1, ids_list2


def save_embeddings(folder, ent_embeddings, rel_embeddings, references_s, references_t_list):
    print("save embeddings...")
    final_ent_embeddings = ent_embeddings.eval()
    final_rel_embeddings = rel_embeddings.eval()
    ref1_ents_embeddings = tf.nn.embedding_lookup(ent_embeddings, references_s).eval()
    ref2_ents_embeddings = tf.nn.embedding_lookup(ent_embeddings, references_t_list).eval()
    np.save(folder + "ents_vec", final_ent_embeddings)
    np.save(folder + "rels_vec", final_rel_embeddings)
    np.save(folder + "ref1_vec", ref1_ents_embeddings)
    np.save(folder + "ref2_vec", ref2_ents_embeddings)


def read_ids2list(ids_file):
    """
    读取id文件, 每行的格式是 id, \t, uri
    :param ids_file:
    :return:
    """
    file = open(ids_file, 'r', encoding='utf8')
    ids_list = list()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        id = int(params[0])
        ids_list.append(id)
    return ids_list


def embedding2file(embeddings, embeddings_out_file):
    print("Embedding:", embeddings.shape)
    fw = open(embeddings_out_file, 'w', encoding='utf8')
    for i in range(embeddings.shape[0]):
        line = ''
        for j in range(embeddings.shape[1]):
            line = line + str(embeddings[i, j]) + '\t'
        fw.write(line.strip() + '\n')
    fw.close()


def print_time(t):
    print('总耗时:{:.3f} s'.format(t))


def radio_2file(radio, folder):
    path = folder + str(radio).replace('.', '_')
    if not os.path.exists(path):
        os.makedirs(path)
    return path + '/'


def read_pairs(file_path):
    file = open(file_path, 'r', encoding='utf8')
    pairs = list()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        pairs.append((params[0], params[1]))
    file.close()
    return pairs


def read_attr_links(file_path):
    file = open(file_path, 'r', encoding='utf8')
    pairs = list()
    linked1, linked2 = set(), set()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        pairs.append((params[0], params[1]))
        linked1.add(params[0])
        linked2.add(params[1])
    file.close()
    return pairs, linked1, linked2


def read_pair_ids(file_path):
    file = open(file_path, 'r', encoding='utf8')
    pairs = list()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        pairs.append((int(params[0]), int(params[1])))
    file.close()
    return pairs


def pair_2set(pairs):
    s1, s2 = set(), set()
    for pair in pairs:
        s1.add(pair[0])
        s2.add(pair[1])
    return s1, s2


def read_triples_ids(file_path):
    triples = list()
    file = open(file_path, 'r', encoding='utf8')
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 3
        h = int(params[0])
        r = int(params[1])
        t = int(params[2])
        triples.append((h, r, t))
    return triples


def read_ref(file_path):
    refs = list()
    reft = list()
    file = open(file_path, 'r', encoding='utf8')
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        e1 = int(params[0])
        e2 = int(params[1])
        refs.append(e1)
        reft.append(e2)
    assert len(refs) == len(reft)
    return refs, reft


def read_ents_by_order(ids_file):
    """
    读取id文件, 每行的格式是 id, \t, uri
    :param ids_file:
    :return:
    """
    file = open(ids_file, 'r', encoding='utf8')
    ids_list = list()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        ids_list.append(int(params[0]))
    return ids_list


def read_ents_by_order_dic(ids_file):
    file = open(ids_file, 'r', encoding='utf8')
    id_list = list()
    ids_uris_dict = dict()
    uris_ids_dict = dict()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        id_list.append(int(params[0]))
        ids_uris_dict[int(params[0])] = params[1]
        uris_ids_dict[params[1]] = int(params[0])
    return id_list, ids_uris_dict, uris_ids_dict


def pair_2_rev_dict(pairs):
    d = dict()
    for pair in pairs:
        if pair[1] not in d:
            d[pair[1]] = pair[0]
        else:
            print("Error")
    return d


def pair_2int_set(pairs):
    s1, s2 = set(), set()
    for pair in pairs:
        s1.add(int(pair[0]))
        s2.add(int(pair[1]))
    return s1, s2


def div_list(ls, n):
    # if not isinstance(ls, list) or not isinstance(n, int):
    #     return []
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
        ### j,j,j,...(前面有n-1个j),j+k
        # 步长j,次数n-1
        ls_return = []
        for i in range(0, (n - 1) * j, j):
            ls_return.append(ls[i:i + j])
        # 算上末尾的j+k
        ls_return.append(ls[(n - 1) * j:])
        return ls_return


def read_attrs(attrs_file):
    attrs_dic = dict()
    with open(attrs_file, 'r', encoding='utf8') as file:
        for line in file:
            params = line.strip().strip('\n').split('\t')
            if len(params) >= 2:
                attrs_dic[params[0]] = set(params[1:])
            else:
                print(line)
    return attrs_dic


def read_triple_ids(triples_file_path):
    if triples_file_path is None:
        return set()
    file = open(triples_file_path, 'r', encoding='utf8')
    triples = set()
    for line in file.readlines():
        ent_h, prop, ent_t = line.strip('\n').split('\t')
        triples.add((int(ent_h), int(prop), int(ent_t)))
    file.close()
    return triples


def read_attrs_range(file_path):
    dic = dict()
    lines = read_lines(file_path)
    for line in lines:
        line = line.strip()
        params = line.split('\t')
        assert len(params) == 2
        dic[int(params[0])] = int(params[1])
    return dic


def read_lines(file_path):
    if file_path is None:
        return []
    file = open(file_path, 'r', encoding='utf8')
    return file.readlines()


def merge_dicts(dict1, dict2):
    for k in dict1.keys():
        vs = dict1.get(k)
        dict2[k] = dict2.get(k, set()) | vs
    return dict2
