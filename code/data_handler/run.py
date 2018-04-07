import config
import attr
import generator_entities as g
import links_generator as elg
import datetime
import os
import data_utils as u
import delete_by_degree as d


def write_attr(ent_attrs_dict_1, ent_attrs_dict_2, ent_links):
    link_set_1 = set(ent_links.keys())
    link_set_2 = set(ent_links.values())
    attrs_1, attrs_2 = set(), set()
    for ent in link_set_1:
        ent_attrs = ent_attrs_dict_1[ent]
        attrs_1 = attrs_1 | ent_attrs
    for ent in link_set_2:
        ent_attrs = ent_attrs_dict_2[ent]
        attrs_2 = attrs_2 | ent_attrs


def save_temp_file(out_path, ent_links):
    file = open(out_path, 'w', encoding='utf-8')
    for ent1, ent2 in ent_links.items():
        file.write(ent1 + "\t" + ent2 + "\n")
    file.close()


def generate_raw_data():
    attr_num = config.ATTR_NUM
    ent_attrs_dict_1 = attr.get_ent_by_attr_num(config.TRIPLES_ATTR_RAW_PATH_1, attr_num)
    print("len(ent_attrs_dict_1) = ", len(ent_attrs_dict_1))
    ent_attrs_dict_2 = attr.get_ent_by_attr_num(config.TRIPLES_ATTR_RAW_PATH_2, attr_num)
    print("len(ent_attrs_dict_2) = ", len(ent_attrs_dict_2))
    print("attr.get_ent_by_attr_num")

    # 提取 ent_links
    ent_links = elg.extract_links_by_dbp_raw_links_file(set(ent_attrs_dict_1.keys()), set(ent_attrs_dict_2.keys()))
    # if config.KB_TYPE_1 == 'en':
    #    ent_links = elg.extract_links_by_dbp_raw_links_file(set(ent_attrs_dict_1.keys()), set(ent_attrs_dict_2.keys()))
    # else:
    #     ent_links = elg.extract_links_by_dbp_raw_links_file_for_fr_wd(set(ent_attrs_dict_1.keys()),
    #                                                                   set(ent_attrs_dict_2.keys()))
    print("len(ent_links) = ", len(ent_links))
    print("elg.extract_links_by_dbp_raw_links_file")

    # 生成2个attr文件、1个link_attr文件
    # write_attr(ent_attrs_dict_1, ent_attrs_dict_2, ent_links)
    # print("write_attr")
    # 保存中间结果
    save_temp_file(config.TEMP_ENT_LINKS, ent_links)


def read_temp_file(file_path):
    ent_links = dict()
    with open(file_path, encoding='utf-8') as file:
        for line in file:
            data = line.strip('\n').split('\t')
            ent_links[data[0]] = data[1]
    return ent_links


def statistics(folder):
    triples1 = u.read_triples(folder + 'triples_1')
    triples2 = u.read_triples(folder + 'triples_2')
    print('\nlen(triples1): ', len(triples1))
    print('len(triples2): ', len(triples2))


def run():
    if not os.path.exists(config.FOLDER_IN):
        os.makedirs(config.FOLDER_IN)
    if not os.path.exists(config.FOLDER_OUT):
        os.makedirs(config.FOLDER_OUT)
    if not os.path.exists(config.FOLDER_TEMP):
        os.makedirs(config.FOLDER_TEMP)
    # 读取中间结果
    ent_links_en_wd = read_temp_file(config.TEMP_ENT_LINKS)
    print("read_temp_file")

    # 生成15k数据，包括2个triples文件、1个ent_link文件
    if config.SAMPLE_TYPE == 1:
        g.generate(config.TRIPLES_REL_RAW_PATH_1, config.TRIPLES_REL_RAW_PATH_2, config.TRIPLES_OUT_PATH_1,
                   config.TRIPLES_OUT_PATH_2, config.TEMP_ENTS_1, config.TEMP_ENTS_2, config.ENT_LINKS_PATH,
                   ent_links_en_wd, config.MIN_DEGREE, config.MAX_DEGREE)
    else:
        g.generate(config.TRIPLES_REL_RAW_PATH_1, config.TRIPLES_REL_RAW_PATH_2, config.TRIPLES_OUT_PATH_1,
                   config.TRIPLES_OUT_PATH_2, config.TEMP_ENTS_1, config.TEMP_ENTS_2, config.ENT_LINKS_PATH,
                   ent_links_en_wd, config.MIN_DEGREE, config.MAX_DEGREE)
    print("g.generate")


if __name__ == "__main__":

    print(config.KB_TYPE_1 + " - " + config.KB_TYPE_2)

    start_time = datetime.datetime.now()
    if config.IS_GENERATE_RAW_DATA:
        generate_raw_data()
    run()

    statistics(config.FOLDER_OUT)
    end_time = datetime.datetime.now()
    print("\ndegree:", config.MIN_DEGREE, "-", config.MAX_DEGREE)
    print("remove num rate:", config.REMOVE_NUM_RATE)
    print("random delete rate:", config.RANDOM_REMOVE_RATE if config.IS_REMOVE_BY_RANDOM else 'False')
    print("RANDOM_DELETE_LIMIT:", config.RANDOM_DELETE_LIMIT)
    print("REMOVE_SORTED_LIMIT:", config.REMOVE_SORTED_LIMIT)
    # print("remove num rate:", config.REMOVE_NUM_RATE)
    # print("remove num rate:", config.REMOVE_NUM_RATE)
    print("start time :", start_time)
    print("end time :", end_time)
    print("run_time :", end_time - start_time)
    print(config.FOLDER_OUT)
