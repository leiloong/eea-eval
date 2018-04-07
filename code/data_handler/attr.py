import config
import run


def extract_attributes_and_triples(file_path):
    """
    提取带有attr的三元组
    :param file_path:
    :return:
    """
    triples = set()
    attributes = set()
    with open(file_path, encoding='utf8') as f:
        for line in f:
            data = line.strip('\n').split('\t')
            head, prop, tail = data[0], data[1], data[2]
            if prop.startswith("http://www.wikidata.org/entity/P") or prop.startswith(
                    "http://dbpedia.org/ontology/"):
                attributes.add(prop)
                # print(tail)
                triple = head+"\t"+prop+"\t"+tail
                triples.add(triple)
    return attributes, triples


def extract_attributes_from_file(file_path, link_entities):
    """
    从预处理过的link的三元组中提取attr
    :param file_path:
    :return:
    """
    attributes = set()
    with open(file_path, encoding='utf8') as f:
        for line in f:
            data = line.strip('\n').split('\t')
            if data[0] in link_entities:
                attributes.add(data[1])
    return attributes


def read_link_entities_set(file_path):
    link_entities_set1, link_entities_set2 = set(), set()
    with open(file_path, encoding='utf8') as f:
        for line in f:
            data = line.strip('\n').split('\t')
            link_entities_set1.add(data[0])
            link_entities_set2.add(data[1])
    return link_entities_set1, link_entities_set2


def get_link_attributes(attributes1, attributes2):
    attributes_links = dict()
    attributes1_link_set, attributes2_link_set = set(), set()
    with open(config.PORP_LINKS_PATH, encoding='utf8') as f:
        for line in f:
            data = line.strip('\n').split('\t')
            if data[0] in attributes1 and data[1] in attributes2:
                if data[0] in attributes1_link_set or data[1] in attributes2_link_set:
                    continue
                attributes_links[data[0]] = data[1]
                attributes1_link_set.add(data[0])
                attributes2_link_set.add(data[1])
    return attributes_links


def write_link_attributes(out_path, attributes1, attributes2):
    attributes_link = get_link_attributes(attributes1, attributes2)
    file = open(out_path, 'w', encoding='utf8')
    for attr1, attr2 in attributes_link.items():
        file.write(attr1+'\t'+attr2+'\n')
    file.close()


def write_ent_attrs(out_path, ent_set, attr_triples):
    ent_attrs = dict()
    file = open(out_path, 'w', encoding='utf8')

    for attr_triple in attr_triples:
        attr_triple = attr_triple.split('\t')
        ent = attr_triple[0]
        if ent not in ent_set:
            continue
        attrs = set()
        if ent in ent_attrs:
            attrs = ent_attrs[ent]
        attrs.add(attr_triple[1])
        ent_attrs[ent] = attrs
    for ent, attrs in ent_attrs.items():
        output = ent
        for attr in attrs:
            output += '\t' + attr
        file.write(output+'\n')


def read_and_write_attr_triples(file_path, out_path, ent_set):
    file = open(out_path, 'w', encoding='utf8')
    attr_triples = set()
    attrs = set()
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            data = line.split('\t')
            if data[0] in ent_set:
                attr_triples.add(line)
                attrs.add(data[1])
    for attr_triple in attr_triples:
        file.write(attr_triple+'\n')
    return attr_triples, attrs


def generate_attr(ent_links):
    ent_set1 = set(ent_links.keys())
    ent_set2 = set(ent_links.values())
    attr_triples1, attrs1 = read_and_write_attr_triples(config.TRIPLES_ATTR_RAW_PATH_1,
                                                        config.ATTR_TRIPLES_OUT_PATH_1, ent_set1)
    attr_triples2, attrs2 = read_and_write_attr_triples(config.TRIPLES_ATTR_RAW_PATH_2,
                                                        config.ATTR_TRIPLES_OUT_PATH_2, ent_set2)
    write_ent_attrs(config.ATTR_OUT_PATH_1, ent_set1, attr_triples1)
    write_ent_attrs(config.ATTR_OUT_PATH_2, ent_set2, attr_triples2)
    write_link_attributes(config.ATTR_LINKS_OUT_PATH, attrs1, attrs2)


def remove_entity_by_attribute_num(triples, min_num):
    head_set = set()
    entities_attr_dict = dict()
    for line in triples:
        data = line.strip('\n').split('\t')
        # print(data)
        attributes = set()
        if data[0] in entities_attr_dict:
            attributes = entities_attr_dict[data[0]]
        attributes.add(data[1])
        entities_attr_dict[data[0]] = attributes
    entity_attrs_dict_new = dict()
    for entity, attributes in entities_attr_dict.items():
        if len(attributes) >= min_num:
            head_set.add(entity)
            entity_attrs_dict_new[entity] = attributes
    return entity_attrs_dict_new


def get_ent_by_attr_num(file, attr_num):
    attributes, triples = extract_attributes_and_triples(file)
    entity_attrs_dict = remove_entity_by_attribute_num(triples, attr_num)
    return entity_attrs_dict


def merge_2_file(file_path1, file_path2, out_path):
    file = open(out_path, 'w', encoding='utf-8')
    with open(file_path1, encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            file.write(line+'\n')
    with open(file_path2, encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            file.write(line+'\n')
    file.close()


if __name__ == '__main__':
    # merge_2_file("F:\data2\\final\\rel_links_same", "F:\data2\\final\\attr_links_same",
    #              "F:\data2\\final\prop_links_all_en_fr")
    ent_links_en_wd_in_15k = run.read_temp_file(config.ENT_LINKS_PATH)
    # 生成15k数据内的attr_links，以及两个attr文件
    generate_attr(ent_links_en_wd_in_15k)
    print("attr.generate_attr")
    print(len(ent_links_en_wd_in_15k))

