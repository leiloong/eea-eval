import random
import math
import os

import gc
import numpy as np
import pandas as pd
import tensorflow as tf
import time
import sys

from eval_results import eval_alignment_multi_embed, early_stop, generate_res_folder, radio2str

from params import *

margin = 1
ent_top_k = [1, 5, 10, 50]
theta = 0.8
max_newly_pairs = 6000


def radio_2file(radio, folder):
    path = folder + str(radio).replace('.', '_')
    if not os.path.exists(path):
        os.makedirs(path)
    return path + '/'


def pair2file(file, pairs):
    with open(file, 'w', encoding='utf8') as f:
        for i, j in pairs:
            f.write(str(i) + '\t' + str(j) + '\n')
        f.close()


def generate_neg_triples(pos_triples, ents_list):
    neg_triples = list()
    for (h, r, t) in pos_triples:
        h2, r2, t2 = h, r, t
        choice = random.randint(0, 999)
        if choice < 500:
            h2 = random.sample(ents_list, 1)[0]
        elif choice >= 500:
            t2 = random.sample(ents_list, 1)[0]
        neg_triples.append((h2, r2, t2))
    return neg_triples


def generate_neg_triples_w(pos_triples, ents_list):
    neg_triples = list()
    for (h, r, t, w) in pos_triples:
        h2, r2, t2 = h, r, t
        choice = random.randint(0, 999)
        if choice < 500:
            h2 = random.sample(ents_list, 1)[0]
        elif choice >= 500:
            t2 = random.sample(ents_list, 1)[0]
        neg_triples.append((h2, r2, t2, w))
    return neg_triples


def generate_neg_paths(pos_paths, rels_list):
    neg_paths = list()
    for (r_x, r_y, r, _) in pos_paths:
        r2 = random.sample(rels_list, 1)[0]
        neg_paths.append((r_x, r_y, r2))
    return neg_paths


def generate_batch(triples, paths, batch_size, path_batch_size, ents_list, rels_list):
    pos_triples = random.sample(triples, batch_size)
    neg_triples = generate_neg_triples(pos_triples, ents_list)
    pos_paths = random.sample(paths, path_batch_size)
    neg_paths = generate_neg_paths(pos_paths, rels_list)
    return pos_triples, neg_triples, pos_paths, neg_paths


def generate_triple_batch(triples, batch_size, ents_list):
    if batch_size > len(triples):
        batch_size = len(triples)
    pos_triples = random.sample(triples, batch_size)
    neg_triples = generate_neg_triples_w(pos_triples, ents_list)
    return pos_triples, neg_triples


def parse_triples(triples):
    ents, rels = set(), set()
    for triple in triples:
        ents.add(triple[0])
        rels.add(triple[1])
        ents.add(triple[2])
    return ents, rels


def read_ref(file):
    ref1, ref2 = list(), list()
    with open(file, 'r', encoding='utf8') as f:
        for line in f:
            params = line.strip('\n').split('\t')
            assert len(params) == 2
            e1 = int(params[0])
            e2 = int(params[1])
            ref1.append(e1)
            ref2.append(e2)
        f.close()
        assert len(ref1) == len(ref2)
    return ref1, ref2


def read_triples(file):
    triples = set()
    with open(file, 'r', encoding='utf8') as f:
        for line in f:
            params = line.strip('\n').split('\t')
            assert len(params) == 3
            h = int(params[0])
            r = int(params[1])
            t = int(params[2])
            triples.add((h, r, t))
        f.close()
    return triples


def read_input(folder):
    triples1 = read_triples(folder + 'triples_1')
    triples2 = read_triples(folder + 'triples_2')
    triples = triples1 | triples2
    ents, rels = parse_triples(triples)
    print(len(ents), len(rels), len(triples))
    rel_num = len(rels)
    # add reverse triples
    # reversed_triples = set()
    # for h, r, t in triples:
    #     reversed_triples.add((t, r + rel_num, h))
    # triples |= reversed_triples
    # ents, rels = parse_triples(triples)
    # print(len(ents), len(rels), len(triples))

    ref_ent1, ref_ent2 = read_ref(folder + 'ref_ent_ids')
    # ref_rel1, ref_rel2 = read_ref(folder + 'ref_rel_ids')
    assert len(ref_ent1) == len(ref_ent2)
    # assert len(ref_rel1) == len(ref_rel2)
    print("To aligned entities:", len(ref_ent1))
    # print("To aligned relations:", len(ref_rel1))

    ents, rels = parse_triples(triples)
    print(len(ents), len(rels), len(triples))

    return list(ents), list(rels), list(triples), ref_ent1, ref_ent2


def generate_2steps_path(triples):
    tr = np.array([[tr[0], tr[2], tr[1]] for tr in triples])
    tr = pd.DataFrame(tr, columns=['h', 't', 'r'])
    sizes = tr.groupby(['h', 'r']).size()
    sizes.name = 'size'
    tr = tr.join(sizes, on=['h', 'r'])
    train_raw_df = tr[['h', 'r', 't', 'size']]
    two_step_df = pd.merge(train_raw_df, train_raw_df, left_on='t', right_on='h')
    print('start merge triple with path')

    two_step_df['_path_weight'] = two_step_df.size_x * two_step_df.size_y
    two_step_df = two_step_df[two_step_df['_path_weight'] < 101]
    two_step_df = pd.merge(two_step_df, train_raw_df, left_on=['h_x', 't_y'], right_on=['h', 't'], copy=False, sort=False)

    # print(two_step_df[['r_x', 'r_y', 'r', '_path_weight']])
    path_mat = two_step_df[['r_x', 'r_y', 'r', '_path_weight']].values
    print("num of path:", path_mat.shape[0])
    path_list = list()
    for i in range(path_mat.shape[0]):
        path_list.append((path_mat[i][0], path_mat[i][1], path_mat[i][2], path_mat[i][3]))
    return path_list


class IPTransE_Model:
    def __init__(self, session, ent_num, rel_num, ref_ent1, ref_ent2):
        self.session = session
        self.ent_num = ent_num
        self.rel_num = rel_num
        self.ref_ent1 = ref_ent1
        self.ref_ent2 = ref_ent2

        self._generate_variables()
        self._generate_graph()
        self._generate_alignment_graph()

        self.ppre_hits1, self.pre_hits1 = -1, -1
        self.is_early = False

        tf.global_variables_initializer().run(session=session)

    def _generate_variables(self):
        with tf.variable_scope('relation' + 'embedding'):
            self.ent_embeddings = tf.Variable(tf.truncated_normal([self.ent_num, embed_size], stddev=1.0 / math.sqrt(embed_size)))
            self.rel_embeddings = tf.Variable(tf.truncated_normal([self.rel_num, embed_size], stddev=1.0 / math.sqrt(embed_size)))
            self.ent_embeddings = tf.nn.l2_normalize(self.ent_embeddings, 1)
            self.rel_embeddings = tf.nn.l2_normalize(self.rel_embeddings, 1)

    def _generate_transe_loss(self, phs, prs, pts, nhs, nrs, nts):
        pos_loss = tf.sqrt(tf.reduce_sum(tf.pow(phs + prs - pts, 2), 1))
        neg_loss = tf.sqrt(tf.reduce_sum(tf.pow(nhs + nrs - nts, 2), 1))
        # pos_loss = tf.reduce_sum(tf.abs(phs + prs - pts), 1)
        # neg_loss = tf.reduce_sum(tf.abs(nhs + nrs - nts), 1)
        return tf.reduce_sum(tf.nn.relu(pos_loss + margin - neg_loss))

    def _generate_transe_alignment_loss(self, phs, prs, pts, nhs, nrs, nts, ws):
        pos_loss = tf.sqrt(tf.reduce_sum(tf.pow(phs + prs - pts, 2), 1))
        # neg_loss = tf.sqrt(tf.reduce_sum(tf.pow(nhs + nrs - nts, 2), 1))
        # return tf.reduce_sum(tf.nn.relu(ws * (pos_loss + margin - neg_loss)))
        # pos_loss = tf.reduce_sum(tf.abs(phs + prs - pts), 1)
        return tf.reduce_sum(ws * pos_loss)

    def _generate_path_loss(self, prx, pry, pr, nrx, nry, nr, weight):
        pos_loss = tf.reduce_sum(tf.pow(prx + pry - pr, 2), 1)
        neg_loss = tf.reduce_sum(tf.pow(nrx + nry - nr, 2), 1)
        weight = 1 / weight
        return tf.reduce_sum(weight * tf.nn.relu(pos_loss + margin - neg_loss))

    def _generate_loss(self, phs, prs, pts, nhs, nrs, nts, prx, pry, pr, nrx, nry, nr, ws):
        return self._generate_transe_loss(phs, prs, pts, nhs, nrs, nts) + \
               0.5 * self._generate_path_loss(prx, pry, pr, nrx, nry, nr, ws)

    def _generate_optimizer(self, loss):
        optimizer = tf.train.AdagradOptimizer(learning_rate).minimize(loss)
        return optimizer

    def _generate_graph(self):
        self.pos_hs = tf.placeholder(tf.int32, shape=[None])
        self.pos_rs = tf.placeholder(tf.int32, shape=[None])
        self.pos_ts = tf.placeholder(tf.int32, shape=[None])
        self.neg_hs = tf.placeholder(tf.int32, shape=[None])
        self.neg_rs = tf.placeholder(tf.int32, shape=[None])
        self.neg_ts = tf.placeholder(tf.int32, shape=[None])
        self.pos_rx = tf.placeholder(tf.int32, shape=[None])
        self.pos_ry = tf.placeholder(tf.int32, shape=[None])
        self.pos_r = tf.placeholder(tf.int32, shape=[None])
        self.neg_rx = tf.placeholder(tf.int32, shape=[None])
        self.neg_ry = tf.placeholder(tf.int32, shape=[None])
        self.neg_r = tf.placeholder(tf.int32, shape=[None])
        self.path_weight = tf.placeholder(tf.float32, shape=[None])

        phs = tf.nn.embedding_lookup(self.ent_embeddings, self.pos_hs)
        prs = tf.nn.embedding_lookup(self.rel_embeddings, self.pos_rs)
        pts = tf.nn.embedding_lookup(self.ent_embeddings, self.pos_ts)

        nhs = tf.nn.embedding_lookup(self.ent_embeddings, self.neg_hs)
        nrs = tf.nn.embedding_lookup(self.rel_embeddings, self.neg_rs)
        nts = tf.nn.embedding_lookup(self.ent_embeddings, self.neg_ts)

        prx = tf.nn.embedding_lookup(self.rel_embeddings, self.pos_rx)
        pry = tf.nn.embedding_lookup(self.rel_embeddings, self.pos_ry)
        pr = tf.nn.embedding_lookup(self.rel_embeddings, self.pos_r)

        nrx = tf.nn.embedding_lookup(self.rel_embeddings, self.neg_rx)
        nry = tf.nn.embedding_lookup(self.rel_embeddings, self.neg_ry)
        nr = tf.nn.embedding_lookup(self.rel_embeddings, self.neg_r)
        self.train_loss = self._generate_loss(phs, prs, pts, nhs, nrs, nts, prx, pry, pr, nrx, nry, nr, self.path_weight)
        self.optimizer = self._generate_optimizer(self.train_loss)

    def _generate_alignment_graph(self):
        self.new_ph = tf.placeholder(tf.int32, shape=[None])
        self.new_pr = tf.placeholder(tf.int32, shape=[None])
        self.new_pt = tf.placeholder(tf.int32, shape=[None])
        self.new_nh = tf.placeholder(tf.int32, shape=[None])
        self.new_nr = tf.placeholder(tf.int32, shape=[None])
        self.new_nt = tf.placeholder(tf.int32, shape=[None])
        self.tr_weight = tf.placeholder(tf.float32, shape=[None])

        ph_embed = tf.nn.embedding_lookup(self.ent_embeddings, self.new_ph)
        pr_embed = tf.nn.embedding_lookup(self.rel_embeddings, self.new_pr)
        pt_embed = tf.nn.embedding_lookup(self.ent_embeddings, self.new_pt)
        nh_embed = tf.nn.embedding_lookup(self.ent_embeddings, self.new_nh)
        nr_embed = tf.nn.embedding_lookup(self.rel_embeddings, self.new_nr)
        nt_embed = tf.nn.embedding_lookup(self.ent_embeddings, self.new_nt)
        self.alignment_loss = self._generate_transe_alignment_loss(ph_embed, pr_embed, pt_embed, nh_embed, nr_embed, nt_embed, self.tr_weight)
        self.alignment_optimizer = self._generate_optimizer(self.alignment_loss)

    def get_ref_embedding(self):
        refs1_embeddings = tf.nn.embedding_lookup(self.ent_embeddings, self.ref_ent1)
        refs2_embeddings = tf.nn.embedding_lookup(self.ent_embeddings, self.ref_ent2)
        return refs1_embeddings.eval(session=self.session), refs2_embeddings.eval(session=self.session)

    def eva(self, folder, e, iter=False):
        embed1 = tf.nn.embedding_lookup(self.ent_embeddings, self.ref_ent1).eval(session=self.session)
        embed2 = tf.nn.embedding_lookup(self.ent_embeddings, self.ref_ent2).eval(session=self.session)
        prec_set1, hits1 = eval_alignment_multi_embed(embed1, embed2)
        prec_set2, hits12 = eval_alignment_multi_embed(embed2, embed1)
        gc.collect()
        if not self.is_early:
            self.ppre_hits1, self.pre_hits1, self.is_early = early_stop(self.ppre_hits1, self.pre_hits1,
                                                                        hits1, small=self.ent_num < 50000)
            if self.is_early:
                if iter:
                    path = "iter/"
                else:
                    path = ""
                out_path = radio_2file(e, folder + path)
                pair2file(out_path + "res1", prec_set1)
                pair2file(out_path + "res2", prec_set2)
                np.save(out_path + "ents_vec", self.ent_embeddings.eval(session=self.session))
                return self.is_early

        if e % save_hits1 == 0:
            if iter:
                path = "iter/"
            else:
                path = ""
            out_path = radio_2file(e, folder + path)
            pair2file(out_path + "res1", prec_set1)
            pair2file(out_path + "res2", prec_set2)
        return self.is_early

    def ref_sim_mat(self, is_ent=True, is_reverse=False):
        refs1_embeddings = tf.nn.embedding_lookup(self.ent_embeddings, self.ref_ent1)
        refs2_embeddings = tf.nn.embedding_lookup(self.ent_embeddings, self.ref_ent2)
        if is_reverse:
            sim_mat = tf.matmul(refs2_embeddings, refs1_embeddings, transpose_b=True)
        else:
            sim_mat = tf.matmul(refs1_embeddings, refs2_embeddings, transpose_b=True)
        return sim_mat.eval(session=self.session)


def train_rel(model, triples, ents, rels, paths, epoch):
    current_loss = 0
    start = time.time()
    steps = math.ceil(len(triples) / batch_size)
    fetches = {"loss": model.train_loss, "train_op": model.optimizer}
    path_batch_size = len(paths) // steps
    for step in range(steps):
        pos_triples, neg_triples, pos_paths, neg_paths = generate_batch(triples, paths, batch_size, path_batch_size, ents, rels)
        feed_dict = {model.pos_hs: [x[0] for x in pos_triples],
                     model.pos_rs: [x[1] for x in pos_triples],
                     model.pos_ts: [x[2] for x in pos_triples],
                     model.neg_hs: [x[0] for x in neg_triples],
                     model.neg_rs: [x[1] for x in neg_triples],
                     model.neg_ts: [x[2] for x in neg_triples],
                     model.pos_rx: [x[0] for x in pos_paths],
                     model.pos_ry: [x[1] for x in pos_paths],
                     model.pos_r: [x[2] for x in pos_paths],
                     model.neg_rx: [x[0] for x in neg_paths],
                     model.neg_ry: [x[1] for x in neg_paths],
                     model.neg_r: [x[2] for x in neg_paths],
                     model.path_weight: [x[3] for x in pos_paths]}
        vals = model.session.run(fetches=fetches, feed_dict=feed_dict)
        current_loss += vals["loss"]
    current_loss /= batch_size
    end = time.time()
    print("{}/{}, loss = {:.3f}, time = {:.3f} s".format(epoch, epochs, current_loss, end - start))


def generate_newly_triples(ent1, ent2, w, rt_dict1, hr_dict1):
    newly_triples = set()
    for r, t in rt_dict1.get(ent1, set()):
        newly_triples.add((ent2, r, t, w))
    for h, r in hr_dict1.get(ent1, set()):
        newly_triples.add((h, r, ent2, w))
    return newly_triples


class Triples:
    def __init__(self, triples):
        self.triple_list = triples
        self.heads = set([triple[0] for triple in self.triple_list])
        self.props = set([triple[1] for triple in self.triple_list])
        self.tails = set([triple[2] for triple in self.triple_list])
        self.ents = self.heads | self.tails
        self.prop_list = list(self.props)
        self.ent_list = list(self.ents)
        self.triples = set(self.triple_list)
        self._generate_related_ents()
        self._generate_triple_dict()

    def _generate_related_ents(self):
        self.out_related_ents_dict = dict()
        self.in_related_ents_dict = dict()
        for h, r, t in self.triple_list:
            out_related_ents = self.out_related_ents_dict.get(h, set())
            out_related_ents.add(t)
            self.out_related_ents_dict[h] = out_related_ents

            in_related_ents = self.in_related_ents_dict.get(t, set())
            in_related_ents.add(h)
            self.in_related_ents_dict[t] = in_related_ents

    def _generate_triple_dict(self):
        self.rt_dict, self.hr_dict = dict(), dict()
        for h, r, t in self.triple_list:
            rt_set = self.rt_dict.get(h, set())
            rt_set.add((r, t))
            self.rt_dict[h] = rt_set
            hr_set = self.hr_dict.get(t, set())
            hr_set.add((h, r))
            self.hr_dict[t] = hr_set


def generate_triples_of_latent_ents(triples, ents1, ents2, tr_ws):
    assert len(ents1) == len(ents2)
    Tr = Triples(triples)
    newly_triples = set()
    for i in range(len(ents1)):
        newly_triples |= generate_newly_triples(ents1[i], ents2[i], tr_ws[i], Tr.rt_dict, Tr.hr_dict)
        newly_triples |= generate_newly_triples(ents2[i], ents1[i], tr_ws[i], Tr.rt_dict, Tr.hr_dict)
    print("newly triples: {}".format(len(newly_triples)))
    return newly_triples


def train_alignment_one_epoch(model, ents1, ents2, tr_ws, triples, ents_list):
    t1 = time.time()
    newly_triples = generate_triples_of_latent_ents(triples, ents1, ents2, tr_ws)
    steps = math.ceil(((len(newly_triples)) / batch_size))
    if steps == 0:
        steps = 1
    alignment_loss = 0
    for step in range(steps):
        newly_pos_batch, newly_neg_batch = generate_triple_batch(newly_triples, batch_size, ents_list)
        alignment_fetches = {"loss": model.alignment_loss, "train_op": model.alignment_optimizer}
        alignment_feed_dict = {model.new_ph: [tr[0] for tr in newly_pos_batch],
                               model.new_pr: [tr[1] for tr in newly_pos_batch],
                               model.new_pt: [tr[2] for tr in newly_pos_batch],
                               model.new_nh: [tr[0] for tr in newly_neg_batch],
                               model.new_nr: [tr[1] for tr in newly_neg_batch],
                               model.new_nt: [tr[2] for tr in newly_neg_batch],
                               model.tr_weight: [tr[3] for tr in newly_pos_batch]}
        alignment_vals = model.session.run(fetches=alignment_fetches, feed_dict=alignment_feed_dict)
        alignment_loss += alignment_vals["loss"]
    alignment_loss /= len(newly_triples)
    print("alignment_loss = {:.3f}, time = {:.3f} s".format(alignment_loss, time.time() - t1))


def check_alignment(aligned_pairs, all_n, context="", is_cal=True):
    if aligned_pairs is None or len(aligned_pairs) == 0:
        print("{}, Empty aligned pairs".format(context))
        return
    num = 0
    for x, y, z in aligned_pairs:
        if x == y:
            num += 1
    print("{}, right alignment: {}/{}={:.3f}".format(context, num, len(aligned_pairs), num / len(aligned_pairs)))
    if is_cal:
        precision = round(num / len(aligned_pairs), 6)
        recall = round(num / all_n, 6)
        if recall > 1.0:
            recall = round(num / all_n, 6)
        f1 = round(2 * precision * recall / (precision + recall), 6)
        print("precision={}, recall={}, f1={}".format(precision, recall, f1))


def dynamic_alignment(model, sim_mat, refs1, refs2, triples, ents):
    def search_nearest_k(sim_mat, th):
        neighbors = set()
        ref_num = sim_mat.shape[0]
        for i in range(ref_num):
            rank = (-sim_mat[i, :]).argsort()
            if sim_mat[i, rank[0]] >= th:
                neighbors.add((i, rank[0], sim_mat[i, rank[0]]))
        return neighbors
    pairs = search_nearest_k(sim_mat, theta)
    check_alignment(pairs, sim_mat.shape[0])
    ents1 = [refs1[pair[0]] for pair in pairs]
    ents2 = [refs2[pair[1]] for pair in pairs]
    tr_ws = [pair[2] for pair in pairs]
    train_alignment_one_epoch(model, ents1, ents2, tr_ws, triples, ents)


def train(folder, radio):
    res_folder = generate_res_folder(folder, "iptranse", radio)
    folder = folder + "sharing/" + radio2str(radio) + "/"
    print(folder)
    print("res folder:", res_folder)

    ents, rels, triples, ref_ent1, ref_ent2 = read_input(folder)
    paths = generate_2steps_path(triples)

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    early = False
    model = IPTransE_Model(sess, len(ents), len(rels), ref_ent1, ref_ent2)
    for epoch in range(1, iptranse_epoch+1):
        train_rel(model, triples, ents, rels, paths, epoch)
        if epoch % print_loss == 0 or epoch == iptranse_epoch - 1:
            early = model.eva(res_folder, epoch)
        if epoch in [600, 650, 700, 750, 800]:
            sim_mat = model.ref_sim_mat()
            dynamic_alignment(model, sim_mat, ref_ent1, ref_ent2, triples, ents)
            early = model.eva(res_folder, epoch, iter=True)
        if early:
            sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        data_folder = sys.argv[1]
        radio = sys.argv[2]
        train(data_folder, radio)
    elif len(sys.argv) == 1:
        train("../dbp_wd_15k_V1/", 0.3)