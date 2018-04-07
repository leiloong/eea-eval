import os


def read_pair_ids(file_path):
    file = open(file_path, 'r', encoding='utf8')
    pairs = list()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        pairs.append((int(params[0]), int(params[1])))
    file.close()
    return pairs


def print_line():
    print()
    print("====================")
    print()


def read_pairs(file_path):
    file = open(file_path, 'r', encoding='utf8')
    pairs = list()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        pairs.append((params[0], params[1]))
    file.close()
    return pairs


def pairs_2file(pairs, file_path):
    file = open(file_path, 'w', encoding='utf8')
    for pair in pairs:
        file.write(str(pair[0]) + '\t' + str(pair[1]) + '\n')
    file.close()


def parse_ttl_lines(line):
    params = line.strip().strip('\n').split(' ')[0:3]
    ent_h = params[0].lstrip('<').rstrip('>').strip()
    prop = params[1].lstrip('<').rstrip('>').strip()
    ent_t = params[2].lstrip('<').rstrip('>').strip()
    return ent_h, prop, ent_t


def read_ttl_triples(ttl_file_path):
    ttl_file = open(ttl_file_path, 'r', encoding='utf8')
    triples = list()
    for line in ttl_file.readlines():
        ent_h, prop, ent_t = parse_ttl_lines(line)
        triples.append((ent_h, prop, ent_t))
    ttl_file.close()
    return triples


def read_triples(triples_file_path):
    file = open(triples_file_path, 'r', encoding='utf8')
    triples = list()
    for line in file.readlines():
        ent_h, prop, ent_t = line.strip('\n').split('\t')
        triples.append((ent_h, prop, ent_t))
    file.close()
    return triples


def triples_2file(triples, file_path):
    file = open(file_path, 'w', encoding='utf8')
    for triple in triples:
        file.write(triple[0] + '\t' + triple[1] + '\t' + triple[2] + '\n')
    file.close()


def pair_2dict(pairs):
    d = dict()
    for pair in pairs:
        if pair[0] not in d:
            d[pair[0]] = pair[1]
        else:
            print("Error")
    return d


def pair_2set(pairs):
    s1, s2 = set(), set()
    for pair in pairs:
        s1.add(pair[0])
        s2.add(pair[1])
    return s1, s2


def pair_2int_set(pairs):
    s1, s2 = set(), set()
    for pair in pairs:
        s1.add(int(pair[0]))
        s2.add(int(pair[1]))
    return s1, s2


def parse_triples(triples):
    ents, rels = set(), set()
    for triple in triples:
        ents.add(triple[0])
        rels.add(triple[1])
        ents.add(triple[2])
    return ents, rels


def ids_2file(ids_mapping, path):
    ids_mapping = sorted(ids_mapping.items(), key=lambda d: d[1])
    fw = open(path, 'w', encoding='utf8')
    max = -1
    for uri, id in ids_mapping:
        if id > max:
            max = id
        fw.write(str(id) + '\t' + uri + '\n')
    print("max id:", max)
    fw.close()


def radio_2file(radio, folder):
    path = folder + str(radio).replace('.', '_')
    if not os.path.exists(path):
        os.makedirs(path)
    return path + '/'


def is_suffix_equal(uri1, uri2):
    uri1_suffix = uri1.split('/')[-1]
    uri2_suffix = uri2.split('/')[-1]
    return uri1_suffix == uri2_suffix