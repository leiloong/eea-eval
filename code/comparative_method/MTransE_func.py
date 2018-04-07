import tensorflow as tf
import random
from cmp_model_utils import *
from sklearn import preprocessing

import numpy as np
from scipy import linalg

from params import *

alpha = 0.005


def pair2file(file, pairs):
    with open(file, 'w', encoding='utf8') as f:
        for i, j in pairs:
            f.write(str(i) + '\t' + str(j) + '\n')
        f.close()


def read_iswc_input(folder):
    print(folder)
    triples1, ents1, rels1 = read_triples(folder + 'triples_1')
    triples2, ents2, rels2 = read_triples(folder + 'triples_2')
    triples_num = len(triples1) + len(triples2)
    print('total triples: %d + %d = %d' % (len(triples1), len(triples2), triples_num))
    ent_num = len(ents1) + len(ents2)
    print("ent num", ent_num)
    rel_num = len(rels1) + len(rels2)
    print("rel num", rel_num)
    ref_ent1, ref_ent2 = read_ref(folder + 'ref_pairs')
    assert len(ref_ent1) == len(ref_ent2)
    print("To aligned entities:", len(ref_ent1))
    sup_ents_pairs = read_pair_ids(folder + 'sup_pairs')
    return triples1, triples2, sup_ents_pairs, ref_ent1, ref_ent2, triples_num, ent_num, rel_num


def generate_input(folder):
    print(folder)

    if "dbp15k" in folder:
        return read_iswc_input(folder)

    triples1, ents1, rels1 = read_triples(folder + 'triples_1')
    triples2, ents2, rels2 = read_triples(folder + 'triples_2')
    triples_num = len(triples1) + len(triples2)
    print('total triples: %d + %d = %d' % (len(triples1), len(triples2), triples_num))
    ent_num = len(ents1) + len(ents2)
    print("ent num", ent_num)
    rel_num = len(rels1) + len(rels2)
    print("rel num", rel_num)
    ref_ent1, ref_ent2 = read_ref(folder + 'ref_ent_ids')
    assert len(ref_ent1) == len(ref_ent2)
    print("To aligned entities:", len(ref_ent1))
    sup_ents_pairs = read_pair_ids(folder + 'sup_ent_ids')
    return triples1, triples2, sup_ents_pairs, ref_ent1, ref_ent2, triples_num, ent_num, rel_num


def random_unit_embeddings(dim1, dim2):
    vectors = list()
    for i in range(dim1):
        vectors.append([random.gauss(0, 1) for j in range(dim2)])
    return preprocessing.normalize(np.matrix(vectors))


def random_orthogonal_matrix(n):
    """Returns a random, orthogonal matrix of n by n."""
    a = np.random.randn(n, n)
    U, _, _ = linalg.svd(a)
    assert U.shape == (n, n)
    return U


def generate_m(k):
    # mat = np.random.randint(0, k, size=[k, k])
    mat = np.random.randn(k, k)
    m = np.linalg.qr(mat)[0]
    return m


def relation_loss(phs, prs, pts):
    opt_vars = [v for v in tf.trainable_variables() if v.name.startswith("relation2vec")]
    # print("relation_loss_vars", opt_vars)
    base_loss = tf.reduce_sum(tf.reduce_sum(tf.pow(phs + prs - pts, 2), 1))
    loss = base_loss
    optimizer = tf.train.AdagradOptimizer(learning_rate).minimize(loss, var_list=opt_vars)
    return optimizer, loss


def m_loss(e1s, e2s, M, eye):
    mapping = tf.matmul(e1s, M)
    # mapping = tf.nn.l2_normalize(mapping, 1)
    trans_loss = tf.reduce_sum(tf.reduce_sum(tf.pow(mapping - e2s, 2), 1))
    base_loss = trans_loss + 5 * tf.reduce_sum(tf.reduce_sum(tf.pow(tf.matmul(M, M, transpose_b=True) - eye, 2), 1))
    # norm_loss = tf.reduce_sum(tf.reduce_sum(tf.pow(M, 2), 1))
    loss = 5 * base_loss  # + alpha * norm_loss
    optimizer = tf.train.AdagradOptimizer(learning_rate).minimize(loss)
    return optimizer, loss


def read_triples(file_path):
    triples = list()
    file = open(file_path, 'r', encoding='utf8')
    ents, rels = set(), set()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 3
        h = int(params[0])
        r = int(params[1])
        t = int(params[2])
        triples.append((h, r, t))
        ents.add(h)
        ents.add(t)
        rels.add(r)
    return triples, ents, rels


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


def generate_triple_batch(batch_size, triples1, triples2, sup_batch_size, sups):
    """
    从两个知识库的三元组构造batch,每次按照数量比例随机抽取和构造训练数据
    :param neg_scope:
    :param neg_type:
    :param batch_size:
    :param triples_data1:
    :param triples_data2:
    :return:
    """
    assert batch_size % 2 == 0
    num1 = int(len(triples1) / (len(triples1) + len(triples2)) * batch_size)
    num2 = batch_size - num1

    pos_triples1 = random.sample(triples1, num1)
    pos_triples2 = random.sample(triples2, num2)
    pos_triples1.extend(pos_triples2)
    assert len(pos_triples1) == batch_size

    sup_batch = random.sample(sups, sup_batch_size)

    return pos_triples1, sup_batch


def generate_triple_batch_neg(batch_size, triples1, triples2, sup_batch_size, sups):
    assert batch_size % 2 == 0
    num1 = int(len(triples1) / (len(triples1) + len(triples2)) * batch_size)
    num2 = batch_size - num1

    pos_triples1 = random.sample(triples1, num1)
    pos_triples2 = random.sample(triples2, num2)
    pos_triples1.extend(pos_triples2)
    assert len(pos_triples1) == batch_size

    sup_batch = random.sample(sups, sup_batch_size)

    return pos_triples1, sup_batch

