import io
import os
import time
import numpy as np
import Levenshtein as lev

from sklearn import preprocessing

from eval_results import eval_alignment_mul


def edit_distance(str1, str2):
    return round(lev.ratio(str1, str2), 4)


def cal_sim_mat_lev(labels1, labels2):
    mat = np.zeros((len(labels1), len(labels2)))
    for i in range(len(labels1)):
        for j in range(len(labels2)):
            mat[i, j] = edit_distance(labels1[i], labels2[j])
    eval_alignment_mul(mat)
    return mat


def load_vectors(fname):
    t = time.time()
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    print("num of word vectors:", n)
    print("dim:", d)
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = np.array([list(map(float, tokens[1:]))], dtype=np.float64)
        # print(data[tokens[0]])
    assert len(data) == n
    print("load word vectors cost: {:.3f} s".format(time.time() - t))
    return data


def read_ref_pairs(file_path):
    file = open(file_path, 'r', encoding='utf8')
    pairs = list()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        pairs.append((int(params[0].strip()), int(params[1].strip())))
    file.close()
    print("num of pairs:", len(pairs))
    return pairs


def read_ids(file_path, ns):
    file = open(file_path, 'r', encoding='utf8')
    dic = dict()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        if ns is None:
            label = params[1].strip()
        else:
            label = params[1].lstrip(ns).strip()
        dic[int(params[0].strip())] = label
    file.close()
    print("num of id:", len(dic))
    return dic


def read_wd_labels(file_path):
    t = time.time()
    file = open(file_path, 'r', encoding='utf8')
    dic = dict()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        dic[params[0].strip()] = params[1].strip()
    file.close()
    print("num of wd labels:", len(dic))
    print("read wd labels cost: {:.3f} s".format(time.time() - t))
    return dic


def get_label_vec(dic, label, split='_'):
    if label is '' or label == '':
        return np.zeros([1, 300], dtype=np.float64)
    names = label.split(split)
    vec = None
    for name in names:
        if name in dic.keys():
            if vec is None:
                vec = dic[name]
            else:
                vec += dic[name]
    if vec is None:
        # print(label)
        return np.zeros([1, 300], dtype=np.float64)
    try:
        return vec / np.sqrt(np.sum(vec * vec))
    except ValueError:
        print(label)
        print(vec)


def cal_sim_mat(dic, labels1, labels2, folder):
    label_mat1, label_mat2 = None, None
    for i in range(len(labels1)):
        label_vec1 = get_label_vec(dic, labels1[i])
        if label_mat1 is None:
            label_mat1 = label_vec1
        else:
            # print(label_mat1.shape, label_vec1.shape)
            label_mat1 = np.row_stack((label_mat1, label_vec1))
    for j in range(len(labels2)):
        label_vec2 = get_label_vec(dic, labels2[j], split=' ')
        if label_mat2 is None:
            label_mat2 = label_vec2
        else:
            label_mat2 = np.row_stack((label_mat2, label_vec2))
    print("label mat:", label_mat1.shape, label_mat2.shape)
    sim_mat = np.matmul(label_mat1, label_mat2.T)
    eval_alignment_mul(sim_mat)
    np.save(folder + "label_sim", sim_mat)
    return sim_mat


def train(folder, labels, word_vecs, ns1):
    ref_ents = read_ref_pairs(folder + "ref_ent_ids")
    ids1 = read_ids(folder + "ent_ids_1", ns1)
    ids2 = read_ids(folder + "ent_ids_2", None)
    ref_ents_labels1, ref_ents_labels2 = list(), list()
    for id1, id2 in ref_ents:
        assert id1 in ids1
        assert id2 in ids2
        ref_ents_labels1.append(ids1.get(id1))
        ref_ents_labels2.append(labels.get(ids2.get(id2), ''))
    assert len(ref_ents_labels1) == len(ref_ents_labels2)
    # if os.path.exists(folder + "label_sim.npy"):
    #     sim_mat = np.load(folder + "label_sim.npy")
    # else:
    sim_mat = cal_sim_mat(word_vecs, ref_ents_labels1, ref_ents_labels2, folder)
    eval_alignment_mul(sim_mat)


if __name__ == '__main__':
    word_vecs_folder = '/media/sloirac/存储/Anls_Alignment/Anls_Alignment/wiki-news-300d-1M.vec'
    word_vecs = load_vectors(word_vecs_folder)

    labels = read_wd_labels('/media/sloirac/存储/Anls_Alignment/Anls_Alignment/wd_labels')

    ns1 = 'http://dbpedia.org/resource/'
    ns2 = ''

    folder = '../ISWC2018/dbp_wd_15k_V1/sharing/0_3/'
    train(folder, labels, word_vecs, ns1)

    folder = '../ISWC2018/dbp_wd_15k_V2/sharing/0_3/'
    train(folder, labels, word_vecs, ns1)

    folder = '../ISWC2018/dbp_wd_15k_V1_1/sharing/0_3/'
    train(folder, labels, word_vecs, ns1)

    folder = '../ISWC2018/dbp_wd_15k_V2_1/sharing/0_3/'
    train(folder, labels, word_vecs, ns1)

    folder = '../ISWC2018/dbp_wd_15k_V1_2/sharing/0_3/'
    train(folder, labels, word_vecs, ns1)

    folder = '../ISWC2018/dbp_wd_15k_V2_2/sharing/0_3/'
    train(folder, labels, word_vecs, ns1)


