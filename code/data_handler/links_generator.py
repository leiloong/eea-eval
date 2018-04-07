import data_utils as u
import config

links = dict()


def extract_links_by_dbp_raw_links_file(ent_set_1, ent_set_2):
    with open(config.ENT_LINKS_RAW_PATH, encoding='utf8') as input_file:
        if config.KB_TYPE_2 != 'wd':
            tail_prefix = "http://"+config.KB_TYPE_2+".dbpedia.org/resource/"
        else:
            tail_prefix = "http://www.wikidata.org/entity/Q"
        for line in input_file:
            is_relational, head, prop, tail = u.parse_ttl_lines(line)
            if head not in ent_set_1:
                continue
            if tail.startswith(tail_prefix) and tail in ent_set_2:
                links[head] = tail
    print("len(links) = ", len(links))
    return links


def extract_links_by_dbp_raw_links_file_for_fr_wd(ent_set_fr, ent_set_wd):
    links_en_fr, links_en_wd = dict(), dict()
    links_fr_wd = dict()
    file = open(config.TEMP_ENT_LINKS, 'w', encoding='utf-8')

    with open(config.ENT_LINKS_RAW_PATH, encoding='utf8') as input_file:
        for line in input_file:
            is_relational, head, prop, tail = u.parse_ttl_lines(line)
            if tail in ent_set_fr and tail.startswith("http://"+config.KB_TYPE_1+".dbpedia.org/resource/"):
                links_en_fr[head] = tail
            elif tail in ent_set_wd and tail.startswith("http://www.wikidata.org/entity/Q"):
                links_en_wd[head] = tail

    ent_en_set1 = set(links_en_fr.keys())
    ent_en_set2 = set(links_en_wd.keys())
    ent_en_set = ent_en_set1 & ent_en_set2
    for ent_en in ent_en_set:
        ent_fr = links_en_fr[ent_en]
        ent_wd = links_en_wd[ent_en]
        links_fr_wd[ent_fr] = ent_wd
        file.write(ent_fr+"\t"+ent_wd+"\n")
    file.close()
    print("len(links_"+config.KB_TYPE_1+"_wd) = ", len(links_fr_wd))
    return links_fr_wd


def write_links_by_2_links(file_path, links1, links2):
    file = open(file_path, "w", encoding="utf-8")
    cnt = 0
    for head in links:
        if head in links1 and head in links2:
            file.write(links1[head]+'\t'+links2[head]+'\n')
            cnt += 1
    print(file_path)
    print(cnt, '\n')


def write_links(file_path, links_matched):
    file = open(file_path, "w", encoding="utf-8")
    cnt = 0
    for head, tail in links_matched.items():
        if head in links:
            file.write(head+'\t'+tail+'\n')
            cnt += 1
    print(file_path)
    print(cnt, '\n')


def read_links(file_path_en_en, file_path_en_other):
    links_other_wd = dict()
    links_en_wd = dict()
    with open(file_path_en_en, encoding='utf8') as file1:
        for line in file1:
            data = line.strip('\n').split('\t')
            links_en_wd[data[0]] = data[1]
    with open(file_path_en_other, encoding='utf8') as file2:
        for line in file2:
            data = line.strip('\n').split('\t')
            if data[0] in links_en_wd:
                links_other_wd[data[1]] = links_en_wd[data[0]]
    return links_other_wd


def get_triples_by_links(file_path, out_path_triples, out_path_links, links):
    file = open(out_path_triples, 'w', encoding='utf-8')
    file_links = open(out_path_links, 'w', encoding='utf-8')
    links_set = set()
    cnt = 0
    with open(file_path, encoding='utf8') as file1:
        for line in file1:
            is_relational, head, prop, tail = u.parse_ttl_lines(line)
            if head not in links:
                continue
            if head not in links_set:
                print(head)
                file_links.write(head + '\t' + links[head] + '\n')
                links_set.add(head)
            if prop.startswith("http://www.wikidata.org/entity/P") or prop.startswith("http://dbpedia.org/ontology/"):
                file.write(head+'\t'+prop+'\t'+tail+'\n')
                cnt += 1
    file.close()
    file_links.close()
    print(cnt)


def generate_prop_links_fr_wd():
    cnt = 0
    prop_links_en_fr, prop_links_en_wd = dict(), dict()
    file = open(config.PORP_LINKS_PATH_FR_WD, 'w', encoding='utf8')
    with open(config.PORP_LINKS_PATH_EN_FR, encoding='utf8') as input_file:
        for line in input_file:
            data = line.strip('\n').split('\t')
            prop_links_en_fr[data[0]] = data[1]
    with open(config.PORP_LINKS_PATH_EN_WD, encoding='utf8') as input_file:
        for line in input_file:
            data = line.strip('\n').split('\t')
            prop_links_en_wd[data[0]] = data[1]
    prop_en_set1 = set(prop_links_en_fr.keys())
    prop_en_set2 = set(prop_links_en_wd.keys())
    prop_en_set = prop_en_set1 & prop_en_set2
    for prop_en in prop_en_set:
        file.write(prop_links_en_fr[prop_en]+'\t'+prop_links_en_wd[prop_en]+'\n')
        cnt += 1
    print(cnt)


def update_prop_links_by_official(out_path, props1, props2):
    # print(props2)
    cnt = 0
    file = open(out_path, 'w', encoding='utf-8')
    prop_link_set = set()
    with open("F:\data2\\final\prop_links_all_en_wd_new", encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            data = line.split('\t')
            if data[0] in props1 and data[1] in props2 and \
                            data[0] not in prop_link_set and data[1] not in prop_link_set:
                prop_link_set.add(data[0])
                prop_link_set.add(data[1])
                file.write(line+'\n')
                cnt += 1
    print(cnt)
    file.close()


def read_prop_by_triples(file_path):
    props = set()
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            data = line.strip('\n').split('\t')
            props.add(data[1])
    return props


if __name__ == "__main__":
    # generate_prop_links_fr_wd()
    folder = "F:\data2\\final\en_wd\\"
    rels1 = read_prop_by_triples(folder+"triples_1")
    rels2 = read_prop_by_triples(folder+"triples_2")
    update_prop_links_by_official(folder+"rel_links", rels1, rels2)
    attrs1 = read_prop_by_triples(folder+"attr_triples_1")
    attrs2 = read_prop_by_triples(folder+"attr_triples_2")
    update_prop_links_by_official(folder+'attr_links', attrs1, attrs2)

