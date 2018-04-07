import math
import sys
from JAPE_loss import *
from JAPE_func import *
from eval_results import generate_res_folder, radio2str


def structure_embedding(folder, radio):
    res_folder = generate_res_folder(folder, "jape", radio)
    folder = folder + "sharing/" + radio2str(radio) + "/"
    print("res folder:", res_folder)
    triples_data1, triples_data2, sup_ents_pairs, ref_ent1, ref_ent2, triples_num, ent_num, rel_num = generate_input(
        folder)
    small = ent_num < 50000
    cross_sim_mat, kb1_sim_mat, kb2_sim_mat = get_all_sim_mat_sparse(folder)
    ids_list1, ids_list2 = get_ids_by_order(folder)
    graph = tf.Graph()
    with graph.as_default():
        pos_hs = tf.placeholder(tf.int32, shape=[None])
        pos_rs = tf.placeholder(tf.int32, shape=[None])
        pos_ts = tf.placeholder(tf.int32, shape=[None])
        neg_hs = tf.placeholder(tf.int32, shape=[None])
        neg_rs = tf.placeholder(tf.int32, shape=[None])
        neg_ts = tf.placeholder(tf.int32, shape=[None])
        flag = tf.placeholder(tf.bool)

        with tf.variable_scope('relation2vec' + 'embedding'):
            ent_embeddings = tf.Variable(tf.truncated_normal([ent_num, embed_size], stddev=1.0 / math.sqrt(embed_size)))
            rel_embeddings = tf.Variable(tf.truncated_normal([rel_num, embed_size], stddev=1.0 / math.sqrt(embed_size)))
            ent_embeddings = tf.nn.l2_normalize(ent_embeddings, 1)
            rel_embeddings = tf.nn.l2_normalize(rel_embeddings, 1)
            ref_ent_s = tf.constant(ref_ent1, dtype=tf.int32)
            ref_ent_t = tf.constant(ref_ent2, dtype=tf.int32)

        with tf.variable_scope('sparse' + 'sim'):
            cross_sparse_sim = sparse_mat_2sparse_tensor(cross_sim_mat)
            kb1_sparse_sim = sparse_mat_2sparse_tensor(kb1_sim_mat)
            kb2_sparse_sim = sparse_mat_2sparse_tensor(kb2_sim_mat)

        ents_1 = tf.nn.embedding_lookup(ent_embeddings, ids_list1)
        ents_2 = tf.nn.embedding_lookup(ent_embeddings, ids_list2)
        phs = tf.nn.embedding_lookup(ent_embeddings, pos_hs)
        prs = tf.nn.embedding_lookup(rel_embeddings, pos_rs)
        pts = tf.nn.embedding_lookup(ent_embeddings, pos_ts)
        nhs = tf.nn.embedding_lookup(ent_embeddings, neg_hs)
        nrs = tf.nn.embedding_lookup(rel_embeddings, neg_rs)
        nts = tf.nn.embedding_lookup(ent_embeddings, neg_ts)

        optimizer, loss = tf.cond(flag, lambda: loss_with_neg(phs, prs, pts, nhs, nrs, nts),
                                  lambda: sim_loss_sparse_with_kb12(ents_1, ents_2, cross_sparse_sim, kb1_sparse_sim,
                                                                    kb2_sparse_sim))

        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        with tf.Session(graph=graph, config=config) as sess:
            tf.global_variables_initializer().run()
            num_steps = triples_num // batch_size

            ppre_hits1, pre_hits1 = -1, -1
            is_early = False

            for epoch in range(1, epochs+1):
                train_loss = 0
                start = time.time()
                if epoch % 2 == 0:
                    for step in range(num_steps):
                        batch_pos, batch_neg = generate_pos_neg_batch(triples_data1, triples_data2, step)
                        feed_dict = {pos_hs: [x[0] for x in batch_pos],
                                     pos_rs: [x[1] for x in batch_pos],
                                     pos_ts: [x[2] for x in batch_pos],
                                     neg_hs: [x[0] for x in batch_neg],
                                     neg_rs: [x[1] for x in batch_neg],
                                     neg_ts: [x[2] for x in batch_neg],
                                     flag: True}
                        (_, loss_val) = sess.run([optimizer, loss], feed_dict=feed_dict)
                        train_loss += loss_val
                else:
                    batch_pos, batch_neg = generate_pos_neg_batch(triples_data1, triples_data2, 1)
                    feed_dict = {pos_hs: [x[0] for x in batch_pos],
                                 pos_rs: [x[1] for x in batch_pos],
                                 pos_ts: [x[2] for x in batch_pos],
                                 neg_hs: [x[0] for x in batch_neg],
                                 neg_rs: [x[1] for x in batch_neg],
                                 neg_ts: [x[2] for x in batch_neg],
                                 flag: False}
                    (_, loss_val) = sess.run([optimizer, loss], feed_dict=feed_dict)
                    train_loss += loss_val
                random.shuffle(triples_data1.train_triples)
                random.shuffle(triples_data2.train_triples)
                end = time.time()
                loss_print = "rel loss" if epoch % 2 == 0 else "sim loss"
                loss_print = "rel loss" if epoch % 2 == 0 else "sim loss"
                print("{}/{}, {} = {:.3f}, time = {:.3f} s".format(epoch, epochs, loss_print, train_loss,
                                                                   end - start))
                if epoch % print_loss == 0:
                    ppre_hits1, pre_hits1, is_early = jape_eva(ent_embeddings, ref_ent_s, ref_ent_t, epoch, res_folder,
                                                               ppre_hits1, pre_hits1, is_early, small)
                    if is_early:
                        break

if __name__ == '__main__':
    if len(sys.argv) == 3:
        data_folder = sys.argv[1]
        radio = sys.argv[2]
        structure_embedding(data_folder, radio)
    elif len(sys.argv) == 1:
        structure_embedding("../dbp_wd_15k_V1/", 0.3)