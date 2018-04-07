import collections
import itertools
import math

import sys

from JAPE_func import *
from JAPE_attr2vec_func import *

data_frequent_p = 0.9
batch_size = 600
num_sampled_negs = 200
num_train = 100
min_frequency = 2
min_props = 2
lr = 0.01
v = 1.5

embedding_size = 75
valid_size = 16
valid_window = 100
valid_examples = np.random.choice(valid_window, valid_size, replace=False)


def get_common(props_list, props_set, linked_attrs):
    print("总属性数量:", len(props_set))
    print("属性频数总和:", len(props_list))
    n = int(data_frequent_p * len(props_set))
    most_frequent_props = collections.Counter(props_list).most_common(n)
    print(most_frequent_props[0:10])
    most_frequent_props = most_frequent_props[len(props_set) - n:]
    common_props_ids = dict()
    for prop, freq in most_frequent_props:
        if freq >= min_frequency and prop not in common_props_ids:
            common_props_ids[prop] = len(common_props_ids)
    for attr in linked_attrs:
        if attr not in common_props_ids.keys():
            common_props_ids[attr] = len(common_props_ids)
    return common_props_ids


def read_ids(ids_file):
    file = open(ids_file, 'r', encoding='utf8')
    dic, reversed_dic, ids_set, uris_set = dict(), dict(), set(), set()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        id = int(params[0])
        uri = params[1]
        dic[id] = uri
        reversed_dic[uri] = id
        ids_set.add(id)
        uris_set.add(uri)
    assert len(dic) == len(reversed_dic)
    assert len(ids_set) == len(uris_set)
    return dic, reversed_dic, ids_set, uris_set


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


def load_data(rel_train_data_folder, attrs_range_file, en_attrs_range_file):
    ref_attr1, ref_attr2 = read_ref(rel_train_data_folder + 'ref_attr_ids')
    print("To aligned attributes:", len(ref_attr1))
    ent_attrs1, attrs1 = read_ent_attr_ids(rel_train_data_folder + 'ent_attrs_1')
    ent_attrs2, attrs2 = read_ent_attr_ids(rel_train_data_folder + 'ent_attrs_2')

    sup_ents_pairs = read_pair_ids(rel_train_data_folder + 'sup_ent_ids')
    attr1_ids, _, _, _ = read_ids(rel_train_data_folder + 'attr_ids_1')
    attr2_ids, _, _, _ = read_ids(rel_train_data_folder + 'attr_ids_2')
    sup_ents_dict = pair_2dict(sup_ents_pairs)

    attrs_num = len(attrs1 | attrs2)
    total_ref_attrs = set(ref_attr1) | set(ref_attr2)

    attrs_list = list()
    attrs_set = set()
    for ent, attrs in ent_attrs1.items():
        attrs_list.extend(list(attrs))
        attrs_set |= attrs
    for ent, attrs in ent_attrs2.items():
        attrs_list.extend(list(attrs))
        attrs_set |= attrs
    print("total attrs:", len(attrs_set))
    print("total attr freq:", len(attrs_list))
    n = int(data_frequent_p * len(attrs_set))
    most_frequent_attrs = collections.Counter(attrs_list).most_common(n)
    most_frequent_attrs = most_frequent_attrs[len(attrs_set) - n:]
    selected_attrs = set()
    for attr, freq in most_frequent_attrs:
        if freq > min_frequency:
            selected_attrs.add(attr)
    selected_attrs |= total_ref_attrs
    print("selected attrs", len(selected_attrs))

    data = list()
    for ent, attrs in ent_attrs1.items():
        assert len(attrs) > 0
        attrs &= selected_attrs
        if len(attrs) > 0:
            for p_id, context_p in itertools.combinations(list(attrs), 2):
                if p_id != context_p:
                    data.append((p_id, context_p))
    for ent, attrs in ent_attrs2.items():
        assert len(attrs) > 0
        attrs &= selected_attrs
        if len(attrs) > 0:
            for p_id, context_p in itertools.combinations(list(attrs), 2):
                if p_id != context_p:
                    data.append((p_id, context_p))
    print("Number of attr training data:", len(data))

    # print(sup_ents_pairs)
    for ent in sup_ents_dict:
        kb2_ent = sup_ents_dict.get(ent)
        ent_props = ent_attrs1.get(ent)
        ent2_props = ent_attrs2.get(kb2_ent)
        ent_props &= selected_attrs
        ent2_props &= selected_attrs
        if len(ent_props) > 0 and len(ent2_props) > 0:
            for p_id, context_p in itertools.product(ent_props, ent2_props):
                if p_id != context_p:
                    data.append((p_id, context_p))
                    data.append((context_p, p_id))
    num_steps = num_train * int(len(data) / batch_size)

    range_dict = read_attrs_range(attrs_range_file)
    en_range_dict = read_attrs_range(en_attrs_range_file)
    range_vec = list()
    for i in range(attrs_num):
        if i in range_dict:
            range_vec.append(range_dict.get(i))
        elif i in en_range_dict:
            range_vec.append(en_range_dict.get(i))
        else:
            range_vec.append(0)

    return data, attrs_num, selected_attrs, num_steps, range_vec, ref_attr1, ref_attr2


def get_range_weight(range_vec, id1, id2):
    if range_vec[id1] == range_vec[id2]:
        return v
    return 1.0


def generate_batch_random(data_list, batch_size, range_vec):
    batch_data = random.sample(data_list, batch_size)
    batch = np.ndarray(shape=(batch_size), dtype=np.int32)
    labels = np.ndarray(shape=(batch_size, 1), dtype=np.int32)
    range_type = np.ndarray(shape=(batch_size, 1), dtype=np.float32)
    for i in range(len(batch_data)):
        batch[i] = batch_data[i][0]
        labels[i, 0] = batch_data[i][1]
        range_type[i, 0] = get_range_weight(range_vec, batch[i], labels[i, 0])
    return batch, labels, range_type


def set2file(ss, meta_out_file):
    fw = open(meta_out_file, 'w', encoding='utf8')
    for i in ss:
        fw.write(str(i) + "\n")
    fw.close()


def embedding2file(embeddings, embeddings_out_file):
    print("Embedding:", embeddings.shape)
    fw = open(embeddings_out_file, 'w', encoding='utf8')
    for i in range(embeddings.shape[0]):
        line = ''
        for j in range(embeddings.shape[1]):
            line = line + str(embeddings[i, j]) + '\t'
        fw.write(line.strip() + '\n')
    fw.close()


def learn_vec(rel_train_data_folder):
    init_width = 1.0 / math.sqrt(embedding_size)
    vec_folder = rel_train_data_folder + 'jape/'
    if not os.path.exists(vec_folder):
        os.makedirs(vec_folder)
    prop_vec_file = vec_folder + 'attrs_vec'
    prop_embeddings_file = vec_folder + 'attrs_embeddings'
    meta_out_file = vec_folder + 'attrs_meta'
    attrs_range_file = rel_train_data_folder + 'attr_range_type_1'
    en_attrs_range_file = rel_train_data_folder + 'attr_range_type_2'

    data, props_size, selected_attrs, num_steps, range_vecss, ref_attr_id1, ref_attr_id2= \
        load_data(rel_train_data_folder, attrs_range_file, en_attrs_range_file)
    if num_steps < 50000:
        num_steps = 50000
    print("number of steps:", num_steps)
    # print(ref_attr_id1)
    # print(ref_attr_id2)

    graph = tf.Graph()
    with graph.as_default():
        # 输入变量
        train_inputs = tf.placeholder(tf.int32, shape=[batch_size])
        train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
        range_vecs = tf.placeholder(tf.float32, shape=[batch_size, 1])
        valid_dataset = tf.constant(valid_examples, dtype=tf.int32)
        ref_s = tf.constant(ref_attr_id1, dtype=tf.int32)
        ref_t = tf.constant(ref_attr_id2, dtype=tf.int32)

        with tf.variable_scope('props' + 'embedding'):
            embeddings = tf.Variable(tf.random_uniform([props_size, embedding_size], -init_width, init_width))
            embeddings = tf.nn.l2_normalize(embeddings, 1)
            nce_weights = tf.Variable(tf.truncated_normal([props_size, embedding_size], stddev=init_width))
            # nce_weights = tf.Variable(tf.zeros([props_size, embedding_size]))
            nce_biases = tf.Variable(tf.zeros([props_size]))

        embed = tf.nn.embedding_lookup(embeddings, train_inputs)
        loss = nce_loss(nce_weights, nce_biases, train_labels, embed, num_sampled_negs, props_size, v=range_vecs)
        optimizer = tf.train.AdagradOptimizer(lr).minimize(loss)

        init = tf.global_variables_initializer()

    with tf.Session(graph=graph) as session:
        init.run()
        average_loss = 0
        t = time.time()
        for step in range(num_steps):
            batch_inputs, batch_labels, range_types = generate_batch_random(data, batch_size, range_vecss)
            feed_dict = {train_inputs: batch_inputs,
                         train_labels: batch_labels,
                         range_vecs: range_types}
            _, loss_val = session.run([optimizer, loss], feed_dict=feed_dict)
            average_loss += loss_val
            if step % 2000 == 0:
                if step > 0:
                    average_loss /= 2000
                print("average loss at step", step, ":", average_loss, "time = ", round(time.time() - t, 2))
                t = time.time()
                average_loss = 0

            if step % 10000 == 0:
                final_embeddings = embeddings.eval()
                np.save(prop_vec_file, final_embeddings)
                embedding2file(final_embeddings, prop_embeddings_file)
                set2file(selected_attrs, meta_out_file)
                valid_results(embeddings, ref_s, ref_t, "Rel")

        valid_results(embeddings, ref_s, ref_t, "Rel")
        final_embeddings = embeddings.eval()
        np.save(prop_vec_file, final_embeddings)
        embedding2file(final_embeddings, prop_embeddings_file)
        set2file(selected_attrs, meta_out_file)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        folder = sys.argv[1]
        learn_vec(folder)
    elif len(sys.argv) == 1:
        folder = "../en_fr_15k/0_2/"
        learn_vec(folder)
