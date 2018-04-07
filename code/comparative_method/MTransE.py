import time

import sys

import math

import gc

from MTransE_func import *
from eval_results import eval_alignment_multi_embed, eval_alignment_mul, early_stop, generate_res_folder, radio2str


def mtranse(folder1, radio):
    res_folder = generate_res_folder(folder1, "mtranse", radio)
    folder1 = folder1 + "mapping/" + radio2str(radio) + "/"
    print("res folder:", res_folder)

    triples1, triples2, sup_ents_pairs, ref_ent1, ref_ent2, triples_num, ent_num, rel_num = \
        generate_input(folder1)
    mat_m = random_orthogonal_matrix(embed_size)
    graph = tf.Graph()

    small = ent_num < 50000

    with graph.as_default():
        pos_hs = tf.placeholder(tf.int32, shape=[None])
        pos_rs = tf.placeholder(tf.int32, shape=[None])
        pos_ts = tf.placeholder(tf.int32, shape=[None])
        sup_hs = tf.placeholder(tf.int32, shape=[None])
        sup_ts = tf.placeholder(tf.int32, shape=[None])
        train = tf.placeholder(tf.bool)

        with tf.variable_scope('relation2vec' + 'embedding'):
            ent_embeddings = tf.Variable(tf.truncated_normal([ent_num, embed_size],
                                                             stddev=1.0 / math.sqrt(embed_size), dtype=tf.float64))
            rel_embeddings = tf.Variable(tf.truncated_normal([rel_num, embed_size],
                                                             stddev=1.0 / math.sqrt(embed_size), dtype=tf.float64))
            ent_embeddings = tf.nn.l2_normalize(ent_embeddings, 1)
            rel_embeddings = tf.nn.l2_normalize(rel_embeddings, 1)
        with tf.variable_scope('translation' + 'embedding'):
            m = tf.Variable(mat_m)
            eye = tf.constant(np.eye(embed_size))

        phs = tf.nn.embedding_lookup(ent_embeddings, pos_hs)
        prs = tf.nn.embedding_lookup(rel_embeddings, pos_rs)
        pts = tf.nn.embedding_lookup(ent_embeddings, pos_ts)
        e1s = tf.nn.embedding_lookup(ent_embeddings, sup_hs)
        e2s = tf.nn.embedding_lookup(ent_embeddings, sup_ts)
        optimizer, loss = tf.cond(train, lambda: relation_loss(phs, prs, pts), lambda: m_loss(e1s, e2s, m, eye))

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        with tf.Session(graph=graph, config=config) as sess:
            tf.global_variables_initializer().run()
            num_steps = triples_num // batch_size
            sup_batch_size = len(sup_ents_pairs) // num_steps
            assert sup_batch_size > 1
            # print("num of steps:", num_steps)
            # print("sup batch size", sup_batch_size)

            ppre_hits1, pre_hits1 = -1, -1
            is_early = False

            for e in range(1, epochs+1):
                triple_loss = 0
                mapping_loss = 0
                start = time.time()
                for b in range(num_steps * 2):
                    loss_type = True if b % 2 == 0 else False
                    batch_pos, sup_batch = generate_triple_batch(batch_size, triples1, triples2, sup_batch_size,
                                                                 sup_ents_pairs)
                    feed_dict = {pos_hs: [x[0] for x in batch_pos],
                                 pos_rs: [x[1] for x in batch_pos],
                                 pos_ts: [x[2] for x in batch_pos],
                                 sup_hs: [x[0] for x in sup_batch],
                                 sup_ts: [x[1] for x in sup_batch],
                                 train: loss_type}
                    (_, loss_val) = sess.run([optimizer, loss], feed_dict=feed_dict)
                    if loss_type:
                        triple_loss += loss_val
                    else:
                        mapping_loss += loss_val
                end = time.time()
                print("{}/{}, rel_loss = {:.3f}, trans_loss = {:.3f}, time = {:.3f} s".
                      format(e, epochs, triple_loss, mapping_loss, end - start))
                if e % print_loss == 0:
                    embed1 = tf.nn.embedding_lookup(ent_embeddings, ref_ent1).eval()
                    embed2 = tf.nn.embedding_lookup(ent_embeddings, ref_ent2).eval()
                    embed12 = np.matmul(embed1, m.eval())
                    prec_set1, hits1 = eval_alignment_multi_embed(embed12, embed2)
                    # prec_set1, hits1 = eval_alignment_mul(np.matmul(embed12, embed2.T), d=True)
                    embed21 = np.matmul(embed2, tf.matrix_inverse(m).eval())
                    prec_set2, hits12 = eval_alignment_multi_embed(embed21, embed1)
                    # prec_set2, hits12 = eval_alignment_mul(np.matmul(embed21, embed1.T), d=True)
                    gc.collect()

                    if not is_early:
                        ppre_hits1, pre_hits1, is_early = early_stop(ppre_hits1, pre_hits1, hits1, small=small)
                        if is_early:
                            out_path = radio_2file(e, res_folder)
                            pair2file(out_path + "res1", prec_set1)
                            pair2file(out_path + "res2", prec_set2)
                            np.save(out_path + "ents_vec", ent_embeddings.eval())
                            sys.exit(0)

                    if e % save_hits1 == 0:
                        out_path = radio_2file(e, res_folder)
                        pair2file(out_path + "res1", prec_set1)
                        pair2file(out_path + "res2", prec_set2)
                        # np.save(out_path + "ents_vec", ent_embeddings.eval())


if __name__ == '__main__':
    if len(sys.argv) == 3:
        data_folder = sys.argv[1]
        radio = sys.argv[2]
        mtranse(data_folder, radio)
    elif len(sys.argv) == 1:
        mtranse("../ISWC2018/en_fr_15k_V1_1/", 0.3)
