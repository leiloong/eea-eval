import random
from collections import Counter

import data_utils as u


def get_type(value):
    value = value.strip()
    # if value.endswith("@en") or value.endswith("@de") or value.endswith("@fr") or value.endswith("@zh"):
    #     return 0  # "String"
    if value.endswith("^^<http://www.w3.org/2001/XMLSchema#integer>") \
            or value.endswith("^^<http://www.w3.org/2001/XMLSchema#decimal>") \
            or value.endswith("^^<http://www.w3.org/2001/XMLSchema#double>"):
        return 1  # "Double"
    if value.endswith("^^<http://www.w3.org/2001/XMLSchema#date>"):
        return 2  # "Date"
    return 0  # "String"


def generate_range_type_one_kb(kb_attr_triples, kb_attrs_ids):
    # 投票机制
    raw_type_dic, type_dic, uri_type_dic = dict(), dict(), dict()
    for ent, attr, val in kb_attr_triples:
        typ = get_type(val)
        types = raw_type_dic.get(attr, list())
        types.append(typ)
        raw_type_dic[attr] = types
    for attr, types in raw_type_dic.items():
        attr_id = kb_attrs_ids.get(attr)
        assert attr_id is not None
        type_dic[attr_id] = Counter(types).most_common(1)[0][0]
        uri_type_dic[attr] = Counter(types).most_common(1)[0][0]
    return type_dic, uri_type_dic


def dict_2file(dic, file_path):
    file = open(file_path, 'w', encoding='utf8')
    for key, value in dic.items():
        file.write(str(key) + '\t' + str(value) + '\n')
    file.close()


def generate_range_type(folder, supervised_radio, kb1_attrs_ids, kb2_attrs_ids, matched_attrs):
    kb1_attr_triples_file = folder + "attr_triples_1"
    kb2_attr_triples_file = folder + "attr_triples_2"
    kb1_attr_triples = list(u.read_triples(kb1_attr_triples_file))
    kb2_attr_triples = list(u.read_triples(kb2_attr_triples_file))
    attr_type_dic1, uri_type_dic1 = generate_range_type_one_kb(kb1_attr_triples, kb1_attrs_ids)
    attr_type_dic2, uri_type_dic2 = generate_range_type_one_kb(kb2_attr_triples, kb2_attrs_ids)
    dict_2file(attr_type_dic1, u.radio_2file(supervised_radio, folder + 'sharing/', subfolder='jape/') + "attr_range_type_1")
    dict_2file(attr_type_dic2, u.radio_2file(supervised_radio, folder + 'sharing/', subfolder='jape/') + "attr_range_type_2")
    dict_2file(uri_type_dic1, folder + 'jape/' + "uri_attr_range_type_1")
    dict_2file(uri_type_dic2, folder + 'jape/' + "uri_attr_range_type_2")

    print("====")
    n = 0
    for a1, a2 in matched_attrs:
        a1_id = kb1_attrs_ids.get(a1)
        a2_id = kb2_attrs_ids.get(a2)
        a1_type = attr_type_dic1.get(a1_id)
        a2_type = attr_type_dic2.get(a2_id)
        if a1_type == a2_type:
            n += 1
            # print(a1_type)
    print("range type same", n, len(matched_attrs))


def generate_sharing_id(ill_pairs, sup_pairs, kb1_eles, kb2_eles, file_path):
    """
    构造数据的id, 这一步是关键, 构造方法是:
    1) 先构造待匹配元素的id, 两个知识库的待匹配元素的id是有一个差值的, 即待匹配对的数量
    2) 再构造监督元素对的id, 两个知识库的监督元素的id相同
    3) 最后是其他的id
    :param ill_pairs:
    :param sup_pairs:
    :param kb1_eles:
    :param kb2_eles:
    :param file_path:
    :return:
    """
    print(len(ill_pairs), len(sup_pairs))
    latent_ref_ents_id_diff = len(ill_pairs) - len(sup_pairs)
    print("id index diff:", latent_ref_ents_id_diff)
    latent_ref_pairs = list(set(ill_pairs) ^ set(sup_pairs))
    assert latent_ref_ents_id_diff == len(latent_ref_pairs)
    ids1, ids2 = dict(), dict()
    index = 0
    # 构造潜在待匹配的元素的id
    for ref_pair in latent_ref_pairs:
        assert ref_pair[0] in kb1_eles
        assert ref_pair[1] in kb2_eles
        ids1[ref_pair[0]] = index
        ids2[ref_pair[1]] = index + latent_ref_ents_id_diff
        index += 1
    index += latent_ref_ents_id_diff
    # 构造监督元素的id
    for ref_pair in sup_pairs:
        assert ref_pair[0] in kb1_eles
        assert ref_pair[1] in kb2_eles
        ids1[ref_pair[0]] = index
        ids2[ref_pair[1]] = index
        index += 1

    print(len(ids1), len(ill_pairs), len(ids2))
    # 构造其他的id
    for ele in kb1_eles:
        if ele not in ids1:
            ids1[ele] = index
            index += 1
    for ele in kb2_eles:
        if ele not in ids2:
            ids2[ele] = index
            index += 1
    print(len(ids1), len(kb1_eles))
    print(len(ids2), len(kb2_eles))
    assert len(ids1) == len(kb1_eles)
    assert len(ids2) == len(kb2_eles)
    u.ids_2file(ids1, file_path + '_1')
    u.ids_2file(ids2, file_path + '_2')
    return ids1, ids2


def filter_ills(kb1_eles, kb2_eles, matched_eles):
    ills = set()
    filtered = set()
    for link in matched_eles:
        if link[0] in kb1_eles and link[1] in kb2_eles and link[0] not in filtered and link[1] not in filtered:
            ills.add(link)
            filtered.add(link[0])
            filtered.add(link[1])
    return list(ills)


def generate_mapping_id(ref_pairs, latent_ref_pairs, sup_pairs, kb1_eles, kb2_eles, file_path):
    latent_ref_ents_id_diff = len(ref_pairs) - len(sup_pairs)
    print("id index diff:", latent_ref_ents_id_diff)
    assert latent_ref_ents_id_diff == len(latent_ref_pairs)
    ids1, ids2 = dict(), dict()
    index = 0
    # 构造潜在待匹配的元素的id
    for ref_pair in latent_ref_pairs:
        ids1[ref_pair[0]] = index
        ids2[ref_pair[1]] = index + latent_ref_ents_id_diff
        index += 1
    index += latent_ref_ents_id_diff
    # 构造其他的id
    for ele in kb1_eles:
        if ele not in ids1:
            ids1[ele] = index
            index += 1
    for ele in kb2_eles:
        if ele not in ids2:
            ids2[ele] = index
            index += 1
    u.ids_2file(ids1, file_path + '_1')
    u.ids_2file(ids2, file_path + '_2')
    return ids1, ids2


def generate_train_data(folder, supervised_radio):
    kb1_triples_file = folder + "triples_1"
    kb2_triples_file = folder + "triples_2"
    matched_ents_file = folder + "ent_links"
    kb1_attrs_file = folder + "jape/ent_attrs_1"
    kb2_attrs_file = folder + "jape/ent_attrs_2"

    ori_folder = folder
    mapping_folder = folder + "mapping/"
    folder = folder + "sharing/"

    kb1_triples = list(u.read_triples(kb1_triples_file))
    kb2_triples = list(u.read_triples(kb2_triples_file))
    matched_ents = u.read_pairs(matched_ents_file)

    kb1_ent_attrs = u.read_attrs(kb1_attrs_file)
    kb2_ent_attrs = u.read_attrs(kb2_attrs_file)

    print("num of triples in kb1:", len(kb1_triples))
    print("num of triples in kb2:", len(kb2_triples))
    kb1_ents, kb1_rels = u.parse_triples(kb1_triples)
    kb2_ents, kb2_rels = u.parse_triples(kb2_triples)
    print("num of ents and rels in kb1:", len(kb1_ents), len(kb1_rels))
    print("num of ents and rels in kb2:", len(kb2_ents), len(kb2_rels))

    print("num of ent links:", len(matched_ents))

    kb1_attrs = u.parse_ent_attrs(kb1_ent_attrs)
    kb2_attrs = u.parse_ent_attrs(kb2_ent_attrs)

    sup_ents_pairs_num = int(len(matched_ents) * supervised_radio)
    sup_ents_pairs = random.sample(matched_ents, sup_ents_pairs_num)
    print("num of sup ent pairs:", len(sup_ents_pairs))

    kb1_ents_ids, kb2_ents_ids = generate_sharing_id(matched_ents, sup_ents_pairs, kb1_ents, kb2_ents,
                                             u.radio_2file(supervised_radio, folder) + 'ent_ids')
    kb1_rels_ids, kb2_rels_ids = generate_sharing_id(set(), set(), kb1_rels, kb2_rels,
                                             u.radio_2file(supervised_radio, folder) + 'rel_ids')
    kb1_attrs_ids, kb2_attrs_ids = generate_sharing_id(set(), set(), kb1_attrs, kb2_attrs,
                                               u.radio_2file(supervised_radio, folder) + 'attr_ids')

    u.pairs_ids_2file(sup_ents_pairs, kb1_ents_ids, kb2_ents_ids,
                      u.radio_2file(supervised_radio, folder) + 'sup_ent_ids')

    latent_ref_ents_pairs = list(set(matched_ents) ^ set(sup_ents_pairs))
    print("num of ref ents", len(latent_ref_ents_pairs))

    latent_ent_ref, latent_rel_ref, latent_attr_ref = list(), list(), list()
    for pair in latent_ref_ents_pairs:
        id1 = kb1_ents_ids.get(pair[0])
        id2 = kb2_ents_ids.get(pair[1])
        latent_ent_ref.append((id1, id2))
    u.pairs_2file(latent_ent_ref, u.radio_2file(supervised_radio, folder) + 'ref_ent_ids')

    u.ent_attrs_2file(kb1_ent_attrs, kb1_ents_ids, kb1_attrs_ids, u.radio_2file(supervised_radio, folder,
                                                                                subfolder='jape/') + 'ent_attrs_1')
    u.ent_attrs_2file(kb2_ent_attrs, kb2_ents_ids, kb2_attrs_ids, u.radio_2file(supervised_radio, folder,
                                                                                subfolder='jape/') + 'ent_attrs_2')

    u.pairs_2file(latent_ref_ents_pairs, u.radio_2file(supervised_radio, folder) + 'ref_ents')
    u.pairs_2file(sup_ents_pairs, u.radio_2file(supervised_radio, folder) + 'sup_ents')

    u.triples_2id_2file(kb1_triples, kb1_ents_ids, kb1_rels_ids, u.radio_2file(supervised_radio, folder) + 'triples_1')
    u.triples_2id_2file(kb2_triples, kb2_ents_ids, kb2_rels_ids, u.radio_2file(supervised_radio, folder) + 'triples_2')

    # mapping 数据 id
    kb1_ents_ids, kb2_ents_ids = generate_mapping_id(matched_ents, latent_ref_ents_pairs, sup_ents_pairs, kb1_ents,
                                                     kb2_ents, u.radio_2file(supervised_radio, mapping_folder) + 'ent_ids')
    kb1_rels_ids, kb2_rels_ids = generate_mapping_id(set(), set(), set(), kb1_rels,
                                                     kb2_rels, u.radio_2file(supervised_radio, mapping_folder) + 'rel_ids')
    latent_ref = list()
    for pair in latent_ref_ents_pairs:
        ent1_id = kb1_ents_ids.get(pair[0])
        ent2_id = kb2_ents_ids.get(pair[1])
        latent_ref.append((ent1_id, ent2_id))
    u.pairs_2file(latent_ref, u.radio_2file(supervised_radio, mapping_folder) + 'ref_ent_ids')
    sup_ref = list()
    for pair in sup_ents_pairs:
        ent1_id = kb1_ents_ids.get(pair[0])
        ent2_id = kb2_ents_ids.get(pair[1])
        sup_ref.append((ent1_id, ent2_id))
    u.pairs_2file(sup_ref, u.radio_2file(supervised_radio, mapping_folder) + 'sup_ent_ids')

    u.triples_2id_2file(kb1_triples, kb1_ents_ids, kb1_rels_ids, u.radio_2file(supervised_radio, mapping_folder) + 'triples_1')
    u.triples_2id_2file(kb2_triples, kb2_ents_ids, kb2_rels_ids, u.radio_2file(supervised_radio, mapping_folder) + 'triples_2')

    generate_range_type(ori_folder, supervised_radio, kb1_attrs_ids, kb2_attrs_ids, set())


if __name__ == '__main__':
    '''
    folder下面至少有五个文件：
    triples_1, triples_2
    attr_triples_1, attr_triples_2
    ent_links
    '''
    folder = '../dbp_wd_15k_V1/'
    for i in [0.1, 0.2, 0.3, 0.4, 0.5]:
        generate_train_data(folder, i)

