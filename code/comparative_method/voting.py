
def read_ref_uris(ref_ent_file):
    file = open(ref_ent_file, 'r', encoding='utf8')
    uris1, uris2 = list(), list()
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        uris1.append(params[0].strip())
        uris2.append(params[1].strip())
    return uris1, uris2


def read_pairs(file_path):
    dic = dict()
    file = open(file_path + 'res1', 'r', encoding='utf8')
    for line in file.readlines():
        params = line.strip('\n').split('\t')
        assert len(params) == 2
        id1 = int(params[0])
        id2 = int(params[1])
        dic[id1] = id2
    return dic


def voting(file1, file2, file3):
    """
    file1 is the default
    """
    dic1 = read_pairs(file1)
    dic2 = read_pairs(file2)
    dic3 = read_pairs(file3)
    assert len(dic1) == len(dic2) == len(dic3)
    print("ref pairs", len(dic1))
    num = 0
    for id1, id11 in dic1.items():
        id12 = dic2.get(id1)
        id13 = dic3.get(id1)
        res = -1
        if id11 == id12:
            res = id11
        elif id11 == id13:
            res = id11
        elif id12 == id13:
            res = id12
        else:
            res = id11
        if res == id1:
            num += 1
    print("precision:", num / len(dic1))


if __name__ == '__main__':
    # file1 = '../res/v0/res/iptranse/en_fr_15k_V2/0_3/201804021628/270/'
    # file2 = '../res/v0/res/jape/en_fr_15k_V2/0_3/201804021533/270/'
    # file3 = '../res/v0/res/mtranse/en_fr_15k_V2/0_3/201804021514/420/'
    # voting(file1, file2, file3)
    #
    # file1 = '../res/v0/res/iptranse/en_fr_15k_V1/0_3/201804021457/310/'
    # file2 = '../res/v0/res/jape/en_fr_15k_V1/0_3/201804021457/360/'
    # file3 = '../res/v0/res/mtranse/en_fr_15k_V1/0_3/201804021456/450/'
    # voting(file1, file2, file3)
    #
    # file1 = '../res/v0/res/iptranse/en_de_15k_V1/0_3/201804022047/400/'
    # file2 = '../res/v0/res/jape/en_de_15k_V1/0_3/201804021958/480/'
    # file3 = '../res/v0/res/mtranse/en_de_15k_V1/0_3/201804021958/440/'
    # voting(file1, file2, file3)
    #
    # file1 = '../res/v0/res/iptranse/en_de_15k_V2/0_3/201804022131/250/'
    # file2 = '../res/v0/res/jape/en_de_15k_V2/0_3/201804022034/430/'
    # file3 = '../res/v0/res/mtranse/en_de_15k_V2/0_3/201804022017/380/'
    # voting(file1, file2, file3)
    #
    # file1 = '../res/v0/res/iptranse/dbp_wd_15k_V2/0_3/201804022234/210/'
    # file2 = '../res/v0/res/jape/dbp_wd_15k_V2/0_3/201804021702/190/'
    # file3 = '../res/v0/res/mtranse/dbp_wd_15k_V2/0_3/201804021554/300/'
    # voting(file1, file2, file3)
    #
    # file1 = '../res/v0/res/iptranse/dbp_wd_15k_V1/0_3/201804021856/220/'
    # file2 = '../res/v0/res/jape/dbp_wd_15k_V1/0_3/201804021627/280/'
    # file3 = '../res/v0/res/mtranse/dbp_wd_15k_V1/0_3/201804021535/390/'
    # voting(file1, file2, file3)
    #
    # file1 = '../res/v0/res/iptranse/dbp_yg_15k_V1/0_3/201804030057/230/'
    # file2 = '../res/v0/res/jape/dbp_yg_15k_V1/0_3/201804021752/270/'
    # file3 = '../res/v0/res/mtranse/dbp_yg_15k_V1/0_3/201804021614/380/'
    # voting(file1, file2, file3)
    #
    # file1 = '../res/v0/res/iptranse/dbp_yg_15k_V2/0_3/201804030140/140/'
    # file2 = '../res/v0/res/jape/dbp_yg_15k_V2/0_3/201804021821/200/'
    # file3 = '../res/v0/res/mtranse/dbp_yg_15k_V2/0_3/201804021632/200/'
    # voting(file1, file2, file3)

    # file1 = '../res/v1/res/iptranse/en_fr_15k_V1_1/0_3/201804041642/600/'
    # file2 = '../res/v1/res/jape/en_fr_15k_V1_1/0_3/201804041556/370/'
    # file3 = '../res/v1/res/mtranse/en_fr_15k_V1_1/0_3/201804041541/490/'
    # voting(file1, file2, file3)

    # file1 = '../res/v2/res/iptranse/en_fr_15k_V1_2/0_3/201804041204/450/'
    # file2 = '../res/v2/res/jape/en_fr_15k_V1_2/0_3/201804041156/430/'
    # file3 = '../res/v2/res/mtranse/en_fr_15k_V1_2/0_3/201804041126/420/'
    # voting(file1, file2, file3)

    # file1 = '../res/v2/res/iptranse/en_fr_15k_V2_2/0_3/201804041228/380/'
    # file2 = '../res/v2/res/jape/en_fr_15k_V2_2/0_3/201804041226/240/'
    # file3 = '../res/v2/res/mtranse/en_fr_15k_V2_2/0_3/201804041142/270/'
    # voting(file1, file2, file3)

    # file1 = '../res/v2/res/iptranse/en_de_15k_V2_2/0_3/201804041401/370/'
    # file2 = '../res/v2/res/jape/en_de_15k_V2_2/0_3/201804041430/520/'
    # file3 = '../res/v2/res/mtranse/en_de_15k_V2_2/0_3/201804041238/360/'
    # voting(file1, file2, file3)

    # file1 = '../res/v2/res/iptranse/en_de_15k_V1_2/0_3/201804041335/600/'
    # file2 = '../res/v2/res/jape/en_de_15k_V1_2/0_3/201804041341/770/'
    # file3 = '../res/v2/res/mtranse/en_de_15k_V1_2/0_3/201804041217/560/'
    # voting(file1, file2, file3)

    # file1 = '../res/v2/res/iptranse/dbp_wd_15k_V1_2/0_3/201804041102/430/'
    # file2 = '../res/v2/res/jape/dbp_wd_15k_V1_2/0_3/201804041102/400/'
    # file3 = '../res/v2/res/mtranse/dbp_wd_15k_V1_2/0_3/201804041102/340/'
    # voting(file1, file2, file3)

    # file1 = '../res/v2/res/iptranse/dbp_wd_15k_V2_2/0_3/201804041128/390/'
    # file2 = '../res/v2/res/jape/dbp_wd_15k_V2_2/0_3/201804041130/210/'
    # file3 = '../res/v2/res/mtranse/dbp_wd_15k_V2_2/0_3/201804041116/230/'
    # voting(file1, file2, file3)

    file1 = '../res/v2/res/iptranse/dbp_yg_15k_V2_2/0_3/201804041314/320/'
    file2 = '../res/v2/res/jape/dbp_yg_15k_V2_2/0_3/201804041317/210/'
    file3 = '../res/v2/res/mtranse/dbp_yg_15k_V2_2/0_3/201804041207/200/'
    voting(file2, file1, file3)