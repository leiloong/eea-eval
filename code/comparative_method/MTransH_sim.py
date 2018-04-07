import math
import sys
from JAPE_loss import *
from JAPE_func import *

from eval_results import generate_res_folder, radio2str

from params import *


class Model:
    def __init__(self, sess, ent_num, rel_num, ref_ent1, ref_ent2, sim_mat, label_sim):
        self.session = sess
        self.ent_num = ent_num
        self.rel_num = rel_num

        # self.sup_ent1 = sup_ent1
        # self.sup_ent2 = sup_ent2
        self.ref_ent1 = ref_ent1
        self.ref_ent2 = ref_ent2
        # self.kb1_ents = kb1_ents
        # self.kb2_ents = kb2_ents

        self.sim_mat = tf.constant(sim_mat, dtype=tf.float32)
        self.label_sim = label_sim

        self.ppre_hits1, self.pre_hits1 = -1, -1
        self.is_early = False

        self._generate_variables()
        self._generate_trans_graph()
        self._generate_sim_graph()
        tf.global_variables_initializer().run(session=sess)

    def _generate_variables(self):
        with tf.variable_scope('relation' + 'embedding'):
            self.ent_embeddings = tf.Variable(tf.truncated_normal([self.ent_num, embed_size],
                                                                  stddev=1.0 / math.sqrt(embed_size)))
            self.rel_embeddings = tf.Variable(tf.truncated_normal([self.rel_num, embed_size],
                                                                  stddev=1.0 / math.sqrt(embed_size)))
            self.ent_embeddings = tf.nn.l2_normalize(self.ent_embeddings, 1)
            self.rel_embeddings = tf.nn.l2_normalize(self.rel_embeddings, 1)
            self.margin = tf.constant(1.0)

            self.normal_vector = tf.get_variable(name="normal_vector", shape=[self.rel_num, embed_size],
                                                 initializer=tf.contrib.layers.xavier_initializer(uniform=False))

    def generate_optimizer(self, loss):
        opt_vars = [v for v in tf.trainable_variables() if v.name.startswith("relation")]
        optimizer = tf.train.AdagradOptimizer(learning_rate).minimize(loss, var_list=opt_vars)
        return optimizer

    def _generate_trans_graph(self):
        def generate_trans_loss(phs, prs, pts, nhs, nrs, nts, margin):
            pos_loss = tf.sqrt(tf.reduce_sum(tf.pow(phs + prs - pts, 2), 1))
            neg_loss = tf.sqrt(tf.reduce_sum(tf.pow(nhs + nrs - nts, 2), 1))
            base_loss = tf.reduce_sum(tf.nn.relu(pos_loss + margin - neg_loss))
            return base_loss

        self.pos_hs = tf.placeholder(tf.int32, shape=[None])
        self.pos_rs = tf.placeholder(tf.int32, shape=[None])
        self.pos_ts = tf.placeholder(tf.int32, shape=[None])
        self.neg_hs = tf.placeholder(tf.int32, shape=[None])
        self.neg_rs = tf.placeholder(tf.int32, shape=[None])
        self.neg_ts = tf.placeholder(tf.int32, shape=[None])

        phs = tf.nn.embedding_lookup(self.ent_embeddings, self.pos_hs)
        prs = tf.nn.embedding_lookup(self.rel_embeddings, self.pos_rs)
        pts = tf.nn.embedding_lookup(self.ent_embeddings, self.pos_ts)
        nhs = tf.nn.embedding_lookup(self.ent_embeddings, self.neg_hs)
        nrs = tf.nn.embedding_lookup(self.rel_embeddings, self.neg_rs)
        nts = tf.nn.embedding_lookup(self.ent_embeddings, self.neg_ts)
        self.triple_loss = generate_trans_loss(phs, prs, pts, nhs, nrs, nts, self.margin)
        self.triple_optimizer = self.generate_optimizer(self.triple_loss)

    def _generate_sim_graph(self):
        ref1 = tf.nn.embedding_lookup(self.ent_embeddings, self.ref_ent1)
        ref2 = tf.nn.embedding_lookup(self.ent_embeddings, self.ref_ent2)
        ref2_trans = tf.matmul(self.sim_mat, ref2)
        ref2_trans = tf.nn.l2_normalize(ref2_trans, 1)
        self.sim_loss = tf.reduce_sum(tf.reduce_sum(tf.pow(ref1 - ref2_trans, 2), 1))
        self.sim_optimizer = self.generate_optimizer(self.sim_loss)

    def eva(self, folder, e):
        embed1 = tf.nn.embedding_lookup(self.ent_embeddings, self.ref_ent1).eval(session=self.session)
        embed2 = tf.nn.embedding_lookup(self.ent_embeddings, self.ref_ent2).eval(session=self.session)
        # prec_set1, hits1 = eval_alignment_multi_embed(embed1, embed2)
        # prec_set2, hits12 = eval_alignment_multi_embed(embed2, embed1)
        sim_mat = np.matmul(embed1, embed2.T)
        sim_mat1 = sim_mat + self.label_sim
        prec_set1, hits1 = eval_alignment_mul(sim_mat1)
        prec_set2, hits12 = eval_alignment_mul(sim_mat1.T)

        print(" == ")

        prec_set1, hits1 = eval_alignment_mul(sim_mat)
        prec_set2, hits12 = eval_alignment_mul(sim_mat.T)
        gc.collect()
        if not self.is_early:
            self.ppre_hits1, self.pre_hits1, self.is_early = early_stop(self.ppre_hits1, self.pre_hits1,
                                                                        hits1, small=self.ent_num < 50000)
            if self.is_early:
                out_path = radio_2file(e, folder)
                pair2file(out_path + "res1", prec_set1)
                pair2file(out_path + "res2", prec_set2)
                np.save(out_path + "ents_vec", self.ent_embeddings.eval(session=self.session))

        if e % save_hits1 == 0:
            out_path = radio_2file(e, folder)
            pair2file(out_path + "res1", prec_set1)
            pair2file(out_path + "res2", prec_set2)


def train_tris_1epo(model, triples1, triples2):
    triple_loss = 0
    start = time.time()
    triples_num = triples1.train_triples_num + triples2.train_triples_num
    triple_steps = math.ceil(triples_num / batch_size)
    triple_fetches = {"triple_loss": model.triple_loss, "train_op": model.triple_optimizer}
    for step in range(triple_steps):
        batch_pos, batch_neg = generate_pos_neg_batch(triples1, triples2, step, multi=1)
        triple_feed_dict = {model.pos_hs: [x[0] for x in batch_pos],
                            model.pos_rs: [x[1] for x in batch_pos],
                            model.pos_ts: [x[2] for x in batch_pos],
                            model.neg_hs: [x[0] for x in batch_neg],
                            model.neg_rs: [x[1] for x in batch_neg],
                            model.neg_ts: [x[2] for x in batch_neg]}
        vals = model.session.run(fetches=triple_fetches, feed_dict=triple_feed_dict)
        triple_loss += vals["triple_loss"]
        triple_loss /= triple_steps
    random.shuffle(triples1.train_triples)
    random.shuffle(triples2.train_triples)
    end = time.time()
    return triple_loss, round(end - start, 2)


def train_sim_1epo(model):
    fetches = {"sim_loss": model.sim_loss, "train_op": model.sim_optimizer}
    vals = model.session.run(fetches=fetches)
    print("sim loss", vals["sim_loss"])


def train(folder, radio):
    print("data:", folder)
    res_folder = generate_res_folder(folder, "mtransh_sim", radio)
    folder = folder + "sharing/" + radio2str(radio) + "/"
    print("res folder:", res_folder)
    triples1, triples2, sup_ents_pairs, ref_ent1, ref_ent2, triples_num, ent_num, rel_num = generate_input(
        folder)
    sim_mat = np.load(folder + "label_sim.npy")
    label_sim = np.load(folder + "label_sim.npy")
    sim_mat[sim_mat < 0.85] = 0
    print("label2vec:")
    eval_alignment_mul(label_sim)
    print("filtered label2vec:")
    eval_alignment_mul(sim_mat)

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    model = Model(sess, ent_num, rel_num, ref_ent1, ref_ent2, sim_mat, label_sim)
    epochs = 500
    for epo in range(1, epochs + 1):
        loss, t = train_tris_1epo(model, triples1, triples2)
        print("epoch {}: triple_loss = {:.3f}, time = {:.3f} s".format(epo, loss, t))
        if epo % 5 == 0:
            train_sim_1epo(model)
        if epo % 10 == 0:
            model.eva(res_folder, epo)
            if model.is_early:
                break


if __name__ == '__main__':
    if len(sys.argv) == 3:
        data_folder = sys.argv[1]
        radio = sys.argv[2]
        train(data_folder, radio)
    elif len(sys.argv) == 1:
        train("../ISWC2018/dbp_yg_15k_V2_1/", 0.3)


