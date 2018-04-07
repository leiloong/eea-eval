import os


def filter_ttl_lines_by_heads(line, heads, ent_prefix='http://'):
    params = line.strip().strip('\n').split(' ')[0:3]
    head = params[0].lstrip('<').rstrip('>').strip()
    if head not in heads:
        return False, None, None, None
    prop = params[1].lstrip('<').rstrip('>').strip()
    tail = params[2].strip()
    if tail.startswith('<' + ent_prefix):
        is_relational = True
        tail = tail.lstrip('<').rstrip('>').strip()
    else:
        is_relational = False
    return is_relational, head, prop, tail


def filter_ttl_lines_by_props(line, props, ent_prefix='http://'):
    params = line.strip().strip('\n').split(' ')[0:3]
    head = params[0].lstrip('<').rstrip('>').strip()
    prop = params[1].lstrip('<').rstrip('>').strip()
    if prop not in props:
        return False, None, None, None
    tail = params[2].strip()
    if tail.startswith('<' + ent_prefix):
        is_relational = True
        tail = tail.lstrip('<').rstrip('>').strip()
    else:
        is_relational = False
    return is_relational, head, prop, tail


def parse_ttl_lines(line, ent_prefix='http://'):
    """
    解析原始的ttl一行,得到其三元组及其类别
    :param line:
    :param ent_prefix:
    :return:如果是relation triple返回True; 如果是attribute triple返回False; 如果是文件开头的标记,返回None; 然后返回三元组
    """
    if line.strip().startswith('#'):
        return None, None, None, None
    params = line.strip().strip('\n').split(' ')
    head = params[0].lstrip('<').rstrip('>').strip()
    prop = params[1].lstrip('<').rstrip('>').strip()
    tail = params[2].strip()
    if tail.startswith('<' + ent_prefix):
        is_relational = True
        tail = tail.lstrip('<').rstrip('>').strip()
    else:
        is_relational = False
        if len(params) > 3:
            for p in params[3:]:
                tail = tail + ' ' + p.strip()
        tail = tail.strip().rstrip('.').strip()
    return is_relational, head, prop, tail


def read_links(links_file):
    links_dic = dict()
    with open(links_file, encoding='utf8') as f:
        for line in f:
            params = line.strip('\n').split('\t')
            assert len(params) == 2
            links_dic[params[0].strip()] = params[1].strip()
        f.close()
    return links_dic


def read_pairs(file_path):
    file = open(file_path, 'r', encoding='utf8')
    pairs = list()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        pairs.append((params[0].strip(), params[1].strip()))
    file.close()
    return pairs


def parse_relation_triple_line(line):
    params = line.strip().strip('\n').split('\t')
    assert len(params) == 3
    head = params[0].strip()
    rel = params[1].strip()
    tail = params[2].strip()
    return head, rel, tail


def triples_2file(triples, file_path):
    file = open(file_path, 'w', encoding='utf8')
    for triple in triples:
        file.write(triple[0].strip() + '\t' + triple[1].strip() + '\t' + triple[2].strip() + '\n')
    file.close()


def links_2file(links, file_path):
    file = open(file_path, 'w', encoding='utf8')
    for link in links:
        file.write(link[0].strip() + '\t' + link[1].strip() + '\n')
    file.close()


def pairs_2file(pairs, file_path):
    file = open(file_path, 'w', encoding='utf8')
    for pair in pairs:
        file.write(str(pair[0]) + '\t' + str(pair[1]) + '\n')
    file.close()


def dict_2file(dic, file_path):
    file = open(file_path, 'w', encoding='utf8')
    for key, value in dic.items():
        line = key.strip()
        for v in value:
            line = line + '\t' + v.strip()
        file.write(line + '\n')
    file.close()


def read_triples(triples_file_path):
    if triples_file_path is None:
        return set()
    file = open(triples_file_path, 'r', encoding='utf8')
    triples = set()
    for line in file.readlines():
        ent_h, prop, ent_t = line.strip('\n').split('\t')
        triples.add((ent_h.strip(), prop.strip(), ent_t.strip()))
    file.close()
    return triples


def read_attrs(attrs_file_path):
    if attrs_file_path is None:
        return set()
    file = open(attrs_file_path, 'r', encoding='utf8')
    attrs = dict()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        # assert len(params) >= 2
        if len(params) >= 2:
            attrs[params[0]] = set(params[1:])
    file.close()
    return attrs


def parse_triples(triples):
    ents, rels = set(), set()
    for triple in triples:
        ents.add(triple[0])
        rels.add(triple[1])
        ents.add(triple[2])
    return ents, rels


def parse_ent_attrs(ent_attrs):
    all_attrs = set()
    for attrs in ent_attrs.values():
        all_attrs |= attrs
    return all_attrs


def ids_2file(ids_mapping, path):
    if ids_mapping is None or len(ids_mapping) == 0:
        return
    ids_mapping = sorted(ids_mapping.items(), key=lambda d: d[1])
    fw = open(path, 'w', encoding='utf8')
    max = -1
    for uri, id in ids_mapping:
        if id > max:
            max = id
        fw.write(str(id) + '\t' + uri + '\n')
    print("max id:", max)
    fw.close()


def radio_2file(radio, folder, subfolder=None):
    path = folder + str(radio).replace('.', '_') + '/'
    if subfolder is not None:
        path = path + subfolder
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def pairs_ids_2file(pairs, dic1, dic2, file_path):
    file = open(file_path, 'w', encoding='utf8')
    for pair in pairs:
        assert pair[0] in dic1 and pair[1] in dic2
        file.write(str(dic1[pair[0]]) + '\t' + str(dic2[pair[1]]) + '\n')
    file.close()


def triples_2id_2file(triples, ents_ids, rels_ids, file_path):
    """
    将id三元组写入文件
    :param triples:
    :param ents_ids:
    :param rels_ids:
    :param file_path:
    :return:
    """
    file = open(file_path, 'w', encoding='utf8')
    for triple in triples:
        assert triple[0] in ents_ids
        assert triple[1] in rels_ids
        assert triple[2] in ents_ids
        h = str(ents_ids.get(triple[0]))
        p = str(rels_ids.get(triple[1]))
        t = str(ents_ids.get(triple[2]))
        file.write(h + '\t' + p + '\t' + t + '\n')
    file.close()


def ent_attrs_2file(kb_ent_attrs, ents_ids, attrs_ids, file_path):
    file = open(file_path, 'w', encoding='utf8')
    for key, value in kb_ent_attrs.items():
        assert key in ents_ids
        line = str(ents_ids[key])
        for v in value:
            assert v in attrs_ids
            line = line + '\t' + str(attrs_ids[v])
        file.write(line + '\n')
    file.close()


if __name__ == '__main__':
    folder = "/media/sloriac/存储/DBpedia201604/en/mappingbased_literals_en.ttl"
    # folder = "/media/sloriac/存储/EA_Exp/mappingbased_objects_fr.ttl"
    n = 0
    with open(folder, 'r', encoding='utf8') as f:
        for line in f:
            n += 1
            if n == 1000:
                exit()
            print(line.strip())
            is_relational, head, prop, tail = parse_ttl_lines(line)
            print(is_relational, head, prop, tail, '\n')
