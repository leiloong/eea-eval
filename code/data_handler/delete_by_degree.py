import generator_entities as ge
import config
import numpy as np
from pagerank import PRIterator
import random


degree_max = 100


def count_degree(entities):
    entity_degree = dict()
    degree_entities = dict()
    for head, prop_tails in entities.items():
        for prop, tails in prop_tails.items():
            if head in entity_degree:
                entity_degree[head] += len(tails)
            else:
                entity_degree[head] = len(tails)
            # for tail in tails:
            #     if tail in entity_degree:
            #         entity_degree[tail] += 1
            #     else:
            #         entity_degree[tail] = 1
    for entity, degree in entity_degree.items():
        ents = set()
        degree = min(degree_max, degree)
        if degree in degree_entities:
            ents = degree_entities[degree]
        ents.add(entity)
        degree_entities[degree] = ents

    link_num = np.zeros((degree_max+1, degree_max+1))
    for i in range(1, degree_max+1):
        if i not in degree_entities:
            continue
        ents = degree_entities[i]
        for ent in ents:
            degree = min(entity_degree[ent], degree_max)
            link_num[i][degree] += 1
    matrix = np.zeros((degree_max+1, degree_max+1))
    for i in range(1, degree_max+1):
        if i not in degree_entities:
            continue
        link_sum = sum(link_num[i])
        for j in range(1, degree_max+1):
            if j not in degree_entities:
                continue
            matrix[j][i] = link_num[i][j] / link_sum
    return entity_degree, degree_entities, matrix


def delete_by_pagerank(entities, degree_entities, pagerank, ent_sum):
    delete_ents_set = set()
    delete_sum = 0
    delete_sum_need = (ent_sum-config.ENT_LINKS_NUM)/ent_sum
    for degree in range(1, degree_max+1):
        if degree not in degree_entities:
            continue
        ents = degree_entities[degree]
        delete_num = int(delete_sum_need*len(ents)*config.REMOVE_NUM_RATE*(1-pagerank[degree]))
        delete_sum += delete_num
        delete_ents_set = delete_ents_set | set(random.sample(list(ents), delete_num))
    print('delete_sum:', delete_sum)
    for ent in delete_ents_set:
        if ent in entities:
            entities.pop(ent)
    # for head, prop_tails in entities.items():
    #     for prop, tails in prop_tails.items():
    #         for tail in delete_ents_set:
    #             if tail in tails:
    #                 tails.remove(tail)
    #         prop_tails[prop] = tails
    #     entities[head] = prop_tails
    # print('remove')
    return entities


def generate(db_in_path, wd_in_path, triples_out_path1, triples_out_path2, temp_ent_path1, temp_ent_path2,
             ent_links_out_path, ent_links, min_degree, max_degree):
    ent_set1 = set(ent_links.keys())
    ent_set2 = set(ent_links.values())
    print('len(ent_links):', len(ent_links))
    entities1 = ge.read_ent_by_triples_file(db_in_path, ent_set1)
    entities2 = ge.read_ent_by_triples_file(wd_in_path, ent_set2)
    print("raw : ")
    print("ent 1 : ", len(entities1))
    print("ent 2 : ", len(entities2))

    entities1 = ge.head_tail_set_deal(entities1)
    entities2 = ge.head_tail_set_deal(entities2)
    print("head_tail_set_deal : ")
    print("ent 1 : ", len(entities1))
    print("ent 2: ", len(entities2))
    entities1, entities2 = ge.get_entities_new_by_link(ent_links, entities1, entities2)
    print("get_entities_new_by_link : ")
    print("ent 1 : ", len(entities1))
    print("ent 2 : ", len(entities2))

    len1 = 0
    cnt = 0
    remove_num_rate = config.REMOVE_NUM_RATE
    while len1 != len(entities1) and len(entities2) >= config.ENT_LINKS_NUM + 1:
        if len(entities1) <= config.ENT_LINKS_NUM+1 or len(entities2) <= config.ENT_LINKS_NUM+1:
            break
        cnt += 1
        print('\n\n', cnt)
        if config.IS_REMOVE_BY_RANDOM and len(entities1) > config.RANDOM_DELETE_LIMIT:
            entities1 = ge.remove_by_random(entities1)
            entities2 = ge.remove_by_random(entities2)
            print("remove_by_random : ")
            print("len(entities1) = ", len(entities1))
            print("len(entities2) = ", len(entities2))
        len1 = len(entities1)
        # remove_num = int((len1-config.ENT_LINKS_NUM)*remove_num_rate)
        # remove_num = max(1, remove_num)
        # print("remove_num = ", remove_num)
        entity_degree_1, degree_entities_1, matrix1 = count_degree(entities1)
        entity_degree_2, degree_entities_2, matrix2 = count_degree(entities2)

        page_rank_1 = PRIterator(matrix1).page_rank()
        entities1 = delete_by_pagerank(entities1, degree_entities_1, page_rank_1, len(entity_degree_1))

        page_rank_2 = PRIterator(matrix2).page_rank()

        entities2 = delete_by_pagerank(entities2, degree_entities_2, page_rank_2, len(entity_degree_2))
        print("delete_by_pagerank : ")
        print('ent1 : ', len(entities1))
        print('ent2 : ', len(entities2))

        if len(entities1) <= config.ENT_LINKS_NUM+1 or len(entities2) <= config.ENT_LINKS_NUM+1:
            break
        entities1 = ge.head_tail_set_deal(entities1)
        entities2 = ge.head_tail_set_deal(entities2)
        print("head_tail_set_deal : ")
        print('ent1 : ', len(entities1))
        print('ent2 : ', len(entities2))
        if len(entities1) <= config.ENT_LINKS_NUM+1 or len(entities2) <= config.ENT_LINKS_NUM+1:
            break
        entities1, entities2 = ge.get_entities_new_by_link(ent_links, entities1, entities2)
        print("get_entities_new_by_link : ")
        print('ent1 : ', len(entities1))
        print('ent2 : ', len(entities2))

    # 按度数
    len1 = 0
    cnt = 0
    remove_num_rate = config.REMOVE_NUM_RATE
    while len1 != len(entities1) and len(entities2) >= config.ENT_LINKS_NUM + 1:
        if len(entities1) <= config.ENT_LINKS_NUM + 1 or len(entities2) <= config.ENT_LINKS_NUM + 1:
            break
        cnt += 1
        print('\n\n', cnt)
        if config.IS_REMOVE_BY_RANDOM and len(entities1) > config.RANDOM_DELETE_LIMIT:
            entities1 = ge.remove_by_random(entities1)
            entities2 = ge.remove_by_random(entities2)
            print("remove_by_random : ")
            print("len(entities1) = ", len(entities1))
            print("len(entities2) = ", len(entities2))
        len1 = len(entities1)
        remove_num = int((len1 - config.ENT_LINKS_NUM) * remove_num_rate)
        remove_num = max(1, remove_num)
        print("remove_num = ", remove_num)
        entity_degree_1 = ge.count_degree(entities1)
        entity_degree_2 = ge.count_degree(entities2)
        if len(entities1) < config.REMOVE_SORTED_LIMIT:
            entities1 = ge.remove_by_min_degree_sorted(entities1, entity_degree_1, min_degree, max_degree, remove_num)
            entities2 = ge.remove_by_min_degree_sorted(entities2, entity_degree_2, min_degree, config.WD_MAX_DEGREE,
                                                    remove_num)
        else:
            entities1 = ge.remove_by_min_degree(entities1, entity_degree_1, min_degree, max_degree, remove_num)
            entities2 = ge.remove_by_min_degree(entities2, entity_degree_2, min_degree, config.WD_MAX_DEGREE, remove_num)
        print("remove_by_min_degree : ")
        print('ent1 : ', len(entities1))
        print('ent2 : ', len(entities2))
        if len(entities1) <= config.ENT_LINKS_NUM + 1 or len(entities2) <= config.ENT_LINKS_NUM + 1:
            break
        entities1 = ge.head_tail_set_deal(entities1)
        entities2 = ge.head_tail_set_deal(entities2)
        print("head_tail_set_deal : ")
        print('ent1 : ', len(entities1))
        print('ent2 : ', len(entities2))
        if len(entities1) <= config.ENT_LINKS_NUM + 1 or len(entities2) <= config.ENT_LINKS_NUM + 1:
            break
        entities1, entities2 = ge.get_entities_new_by_link(ent_links, entities1, entities2)
        print("get_entities_new_by_link : ")
        print('ent1 : ', len(entities1))
        print('ent2 : ', len(entities2))

    len_deal_1, len_deal_2 = 0, 0
    while len_deal_1 != len(entities1) or len_deal_1 != len_deal_2 or len_deal_2 != len(entities2):
        entities1 = ge.head_tail_set_deal(entities1)
        entities2 = ge.head_tail_set_deal(entities2)
        len_deal_1 = len(entities1)
        len_deal_2 = len(entities2)
        entities1, entities2 = ge.get_entities_new_by_link(ent_links, entities1, entities2)
        print("zqh")

    entity_degree_1, _, _ = count_degree(entities1)
    entity_degree_2, _, _ = count_degree(entities2)
    ge.write_to_file(entities1, entity_degree_1, temp_ent_path1)
    ge.write_to_file(entities2, entity_degree_2, temp_ent_path2)
    ge.write_triples(triples_out_path1, entities1)
    ge.write_triples(triples_out_path2, entities2)
    ge.write_link(ent_links, entities1, entities2, ent_links_out_path)
    print('\nfinal ent1 : ', len(entities1))
    print('final ent2 : ', len(entities2))