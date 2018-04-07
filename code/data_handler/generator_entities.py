import random
import config


def count_degree(entities):
    entity_degree = dict()
    for head, prop_tails in entities.items():
        for prop, tails in prop_tails.items():
            if head in entity_degree:
                entity_degree[head] += len(tails)
            else:
                entity_degree[head] = len(tails)
            for tail in tails:
                if tail in entity_degree:
                    entity_degree[tail] += 1
                else:
                    entity_degree[tail] = 1

    # entity_degree = sorted(entity_degree.items(), key=lambda x: x[1], reverse=True)
    # entity_degree_dict = dict()
    # for e_d in entity_degree:
    #     entity_degree_dict[e_d[0]] = e_d[1]
    return entity_degree


def write_to_file(entities, entity_degree, out_path):
    file = open(out_path, 'w', encoding='utf-8')
    for k, v in entity_degree.items():
        if k.endswith('\n'):
            k = k.strip('\n')
        output = k + '\t' + str(v)
        # print(k)
        if k in entities:
            prop_tails = entities[k]
            for prop, tails in prop_tails.items():
                if prop.endswith('\n'):
                    prop = prop.strip('\n')
                output += '\t' + prop
                for tail in tails:
                    if tail.endswith('\n'):
                        tail = tail.strip('\n')
                    output += '@#@' + tail
            file.write(output + '\n')
    file.close()


def read_ent_by_triples_file(file_path, ent_set):
    entities = dict()
    hs, ts = set(), set()
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n').split('\t')
            head = line[0]
            prop = line[1]
            tail = line[2]
            # if not prop.startswith("http://www.wikidata.org/entity/P") and not prop.startswith(
            #         "http://dbpedia.org/ontology/") and 'yago' not in file_path:
            #     continue
            if head in ent_set:
                hs.add(head)
                prop_tails = dict()
                tails = set()
                if head in entities:
                    prop_tails = entities[head]
                    if prop in prop_tails:
                        tails = prop_tails[prop]
                tails.add(tail)
                prop_tails[prop] = tails
                entities[head] = prop_tails

            if tail in ent_set:
                if tail not in entities:
                    entities[tail] = dict()
                ts.add(tail)
    print('len(hs):', len(hs))
    print('len(ts):', len(ts))
    return entities


def head_tail_set_deal(entities):
    heads_set, tails_set = set(), set()
    for head, prop_tails in entities.items():
        heads_set.add(head)
        for prop, tails in prop_tails.items():
            for tail in tails:
                tails_set.add(tail)
    if config.TAIL_IN_HEAD:
        head_tail_set = heads_set & tails_set
    else:
        head_tail_set = heads_set
    entities_new = dict()
    for head, prop_tails in entities.items():
        if head in head_tail_set:
            prop_tails_new = dict()
            for prop, tails in prop_tails.items():
                tails_new = set()
                for tail in tails:
                    if tail in head_tail_set:
                        tails_new.add(tail)
                if len(tails_new) != 0:
                    prop_tails_new[prop] = tails_new
            if len(prop_tails_new) != 0:
                entities_new[head] = prop_tails_new
    return entities_new


def get_entities_new_by_link(ent_links, entities1, entities2):
    entities1_new = dict()
    entities2_new = dict()
    for ent1, ent2 in ent_links.items():
        if ent1 in entities1 and ent2 in entities2:
            entities1_new[ent1] = entities1[ent1]
            entities2_new[ent2] = entities2[ent2]
    return entities1_new, entities2_new


def write_triples(file_path, entities):
    file = open(file_path, 'w', encoding='utf-8')
    for head, prop_tails in entities.items():
        for prop, tails in prop_tails.items():
            for tail in tails:
                output = head+'\t'+prop+'\t'+tail+'\n'
                file.write(output)
    file.close()


def write_link(ent_links, entities1, entities2, out_path):
    file = open(out_path, 'w', encoding='utf-8')
    for ent1, ent2 in ent_links.items():
        if ent1 in entities1 and ent2 in entities2:
            output = ent1 + '\t' + ent2 + '\n'
            file.write(output)
    file.close()


def remove_by_min_degree(entities, degrees, min_degree, max_degree, remove_num):
    entities_new = dict()
    remove_cnt = 0

    for entity, degree in degrees.items():
        if remove_cnt >= remove_num:
            break
        if entity not in entities:
            continue
        if degree > max_degree:
            entities.pop(entity)
            remove_cnt += 1
        elif degree <= min_degree:
            entities.pop(entity)
            remove_cnt += 1

    for head, prop_tails in entities.items():
        prop_tails_new = dict()
        for prop, tails in prop_tails.items():
            tails_new = set()
            for tail in tails:
                if tail in entities:
                    tails_new.add(tail)
            if len(tails_new) != 0:
                prop_tails_new[prop] = tails_new
        if len(prop_tails_new) != 0:
            entities_new[head] = prop_tails_new
    return entities_new


# 有序删除，即先遍历删除度数小的
def remove_by_min_degree_sorted(entities, degrees, min_degree, max_degree, remove_num):
    entities_new = dict()
    remove_cnt = 0
    for i_min_degree in range(0, min_degree+1):
        if remove_cnt >= remove_num:
            break
        for entity, degree in degrees.items():
            if remove_cnt >= remove_num:
                break
            if entity not in entities:
                continue
            if degree > max_degree:
                entities.pop(entity)
                remove_cnt += 1
            elif degree <= i_min_degree:
                entities.pop(entity)
                remove_cnt += 1

    for head, prop_tails in entities.items():
        prop_tails_new = dict()
        for prop, tails in prop_tails.items():
            tails_new = set()
            for tail in tails:
                if tail in entities:
                    tails_new.add(tail)
            if len(tails_new) != 0:
                prop_tails_new[prop] = tails_new
        if len(prop_tails_new) != 0:
            entities_new[head] = prop_tails_new
    return entities_new


def remove_by_random(entities, p=config.RANDOM_REMOVE_RATE):
    num = int((len(entities)-15000) * p)
    removed_ents = set(random.sample(list(entities.keys()), num))
    entities_new = dict()
    for head, prop_tails in entities.items():
        if head in removed_ents:
            continue
        prop_tails_new = dict()
        for prop, tails in prop_tails.items():
            tails_new = set()
            for tail in tails:
                if tail not in removed_ents:
                    tails_new.add(tail)
            if len(tails_new) != 0:
                prop_tails_new[prop] = tails_new
        if len(prop_tails_new) != 0:
            entities_new[head] = prop_tails_new
    return entities_new


def remove_by_out_in_degree(entities, degrees, times=1000):
    entities_new = dict()
    out_degrees = dict()
    for head, prop_tails in entities.items():
        out_degree = 0
        for prop, tails in prop_tails.items():
            out_degree += len(tails)
        out_degrees[head] = out_degree
    for entity, degree in degrees.items():
        if entity not in out_degrees:
            continue
        out_degree = out_degrees[entity]
        if out_degree == 0 or (degree-out_degree)/out_degree > times:
            entities.pop(entity)
    for head, prop_tails in entities.items():
        prop_tails_new = dict()
        for prop, tails in prop_tails.items():
            tails_new = set()
            for tail in tails:
                if tail in entities:
                    tails_new.add(tail)
            if len(tails_new) != 0:
                prop_tails_new[prop] = tails_new
        if len(prop_tails_new) != 0:
            entities_new[head] = prop_tails_new
    return entities_new


def special_handle(ents1, ents2, ent_links, min_degree):
    print("in special_handle ...")
    degrees1 = count_degree(ents1)
    degrees2 = count_degree(ents2)
    cnt = 0
    for ent, prop_tails in ents1.items():
        cnt += 1
        if cnt % 1500 == 0:
            print("已遍历 ： ", cnt)
        if degrees1[ent] > min_degree:
            continue
        temp_ents1 = dict()
        temp_ents2 = dict()
        temp_ents1.update(ents1)
        temp_ents2.update(ents2)
        temp_ents1.pop(ent)
        temp_ents1 = head_tail_set_deal(temp_ents1)
        temp_ents2 = head_tail_set_deal(temp_ents2)
        len1 = len(temp_ents1)
        len2 = len(temp_ents2)
        temp_ents1, temp_ents2 = get_entities_new_by_link(ent_links, temp_ents1, temp_ents2)
        # print("len(temp_ents1) = ", len(temp_ents1))
        # print("len(temp_ents2) = ", len(temp_ents2))

        if len(temp_ents1) == config.ENT_LINKS_NUM and len(temp_ents2) == config.ENT_LINKS_NUM:
            # print("bingo")
            # return temp_ents1, temp_ents2
            if len1 == config.ENT_LINKS_NUM and len2 == config.ENT_LINKS_NUM:
                print("bingo")
                return temp_ents1, temp_ents2
            else:
                temp_ents1 = head_tail_set_deal(temp_ents1)
                temp_ents2 = head_tail_set_deal(temp_ents2)
                if len(temp_ents1) == config.ENT_LINKS_NUM and len(temp_ents2) == config.ENT_LINKS_NUM:
                    print("bingo")
                    return temp_ents1, temp_ents2
    print("not bingo")
    return ents1, ents2


def generate(db_in_path, wd_in_path, triples_out_path1, triples_out_path2, temp_ent_path1, temp_ent_path2,
             ent_links_out_path, ent_links, min_degree, max_degree):
    ent_set1 = set(ent_links.keys())
    ent_set2 = set(ent_links.values())
    print('len(ent_links):', len(ent_links))
    entities1 = read_ent_by_triples_file(db_in_path, ent_set1)
    entities2 = read_ent_by_triples_file(wd_in_path, ent_set2)
    print("raw : ")
    print("ent 1 : ", len(entities1))
    print("ent 2 : ", len(entities2))

    entities1 = head_tail_set_deal(entities1)
    entities2 = head_tail_set_deal(entities2)
    print("head_tail_set_deal : ")
    print("ent 1 : ", len(entities1))
    print("ent 2: ", len(entities2))
    entities1, entities2 = get_entities_new_by_link(ent_links, entities1, entities2)
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
            entities1 = remove_by_random(entities1)
            entities2 = remove_by_random(entities2)
            print("remove_by_random : ")
            print("len(entities1) = ", len(entities1))
            print("len(entities2) = ", len(entities2))
        len1 = len(entities1)
        remove_num = int((len1-config.ENT_LINKS_NUM)*remove_num_rate)
        remove_num = max(1, remove_num)
        print("remove_num = ", remove_num)
        entity_degree_1 = count_degree(entities1)
        entity_degree_2 = count_degree(entities2)
        if len(entities1) < config.REMOVE_SORTED_LIMIT:
            entities1 = remove_by_min_degree_sorted(entities1, entity_degree_1, min_degree, max_degree, remove_num)
            entities2 = remove_by_min_degree_sorted(entities2, entity_degree_2, min_degree, config.WD_MAX_DEGREE, remove_num)
        else:
            entities1 = remove_by_min_degree(entities1, entity_degree_1, min_degree, max_degree, remove_num)
            entities2 = remove_by_min_degree(entities2, entity_degree_2, min_degree, config.WD_MAX_DEGREE, remove_num)
        print("remove_by_min_degree : ")
        print('ent1 : ', len(entities1))
        print('ent2 : ', len(entities2))
        if len(entities1) <= config.ENT_LINKS_NUM+1 or len(entities2) <= config.ENT_LINKS_NUM+1:
            break
        entities1 = head_tail_set_deal(entities1)
        entities2 = head_tail_set_deal(entities2)
        print("head_tail_set_deal : ")
        print('ent1 : ', len(entities1))
        print('ent2 : ', len(entities2))
        if len(entities1) <= config.ENT_LINKS_NUM+1 or len(entities2) <= config.ENT_LINKS_NUM+1:
            break
        entities1, entities2 = get_entities_new_by_link(ent_links, entities1, entities2)
        print("get_entities_new_by_link : ")
        print('ent1 : ', len(entities1))
        print('ent2 : ', len(entities2))
    # if len(entities1) >= config.ENT_LINKS_NUM+1:
    #     entities1, entities2 = special_handle(entities1, entities2, ent_links, config.SPECIAL_HANDLE_DEGREE)

    len_deal_1, len_deal_2 = 0, 0
    while len_deal_1 != len(entities1) or len_deal_1 != len_deal_2 or len_deal_2 != len(entities2):
        entities1 = head_tail_set_deal(entities1)
        entities2 = head_tail_set_deal(entities2)
        len_deal_1 = len(entities1)
        len_deal_2 = len(entities2)
        entities1, entities2 = get_entities_new_by_link(ent_links, entities1, entities2)

    entity_degree_1 = count_degree(entities1)
    entity_degree_2 = count_degree(entities2)
    write_to_file(entities1, entity_degree_1, temp_ent_path1)
    write_to_file(entities2, entity_degree_2, temp_ent_path2)
    write_triples(triples_out_path1, entities1)
    write_triples(triples_out_path2, entities2)
    write_link(ent_links, entities1, entities2, ent_links_out_path)
    print('\nfinal ent1 : ', len(entities1))
    print('final ent2 : ', len(entities2))


if __name__ == '__main__':
    # link_path = "F:\data2\zqsun\\new\links\en_fr_wd\ent_links_en_en_attr1"
    # wikidata_path = "F:\data2\zqsun\\new\zqh\\raw\wikidata_entities"
    # dbpedia_path = "F:\data2\zqsun\\new\zqh\\raw\dbpedia_entities"
    wikidata_path = "F:\data2\zqsun\\new\zqh\en\\result_attr2\wikidata_entities"
    dbpedia_path = "F:\data2\zqsun\\new\zqh\en\\result_attr2\dbpedia_entities"

    # run(dbpedia_path, wikidata_path, link_path, 1, 10000)

