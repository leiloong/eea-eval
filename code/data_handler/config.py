# 只需改变这几个变量
ATTR_NUM = 0
KB_TYPE_1 = "yg"
KB_TYPE_2 = "en"
ENT_LINKS_NUM = 15000
MIN_DEGREE = 5
# 目前无须修改
MAX_DEGREE = 10000
WD_MAX_DEGREE = MAX_DEGREE
# 特殊处理时可删除的度数，此时只删除一个ent
SPECIAL_HANDLE_DEGREE = MIN_DEGREE
# 是否需要生成原始数据，第一次需要生成，以后可以使用中间数据
IS_GENERATE_RAW_DATA = False
# 删除ent时的倍率，默认基数为1000、20、10、1
REMOVE_NUM_RATE = 0.1
# 是否启用随机删除过程
IS_REMOVE_BY_RANDOM = True
RANDOM_REMOVE_RATE = 0.02
# 随机删除的下限个数
RANDOM_DELETE_LIMIT = ENT_LINKS_NUM * 3
# 按照degree删除时，采用排序式删除的上限个数
REMOVE_SORTED_LIMIT = ENT_LINKS_NUM * 1
#
TAIL_IN_HEAD = False

# 0 1
SAMPLE_TYPE = 1

# 是否生成relation 或 attribute
IS_GENERATE_REL = False
IS_GENERATE_ATTR = False

# FOLDER_IN = "F:\data2\\final\\"
FOLDER_IN = "H:\data\\raw\\"
# FOLDER_OUT = "F:\data2\\final\\"+KB_TYPE_1+"_"+KB_TYPE_2+"_"+str(int(ENT_LINKS_NUM/1000))+"k_new\\"
FOLDER_OUT = 'H:/data/ISWC2018/'+KB_TYPE_1+'_'+KB_TYPE_2+'_'+str(int(ENT_LINKS_NUM/1000))+'k_'+str(MIN_DEGREE)+"_V1_2/"
FOLDER_TEMP = "H:\data\ISWC2018\\"+KB_TYPE_1+"_"+KB_TYPE_2+"_"+str(int(ENT_LINKS_NUM/1000))+"k\\temp\\"

# 不变
ENT_LINKS_RAW_PATH = "F:\data2\zqsun\\interlanguage_links_"+KB_TYPE_1+".ttl"

PORP_LINKS_PATH = FOLDER_IN+"prop_links_all_"+KB_TYPE_1+"_"+KB_TYPE_2
PORP_LINKS_PATH_EN_FR = FOLDER_IN+"prop_links_all_en_fr"
PORP_LINKS_PATH_EN_WD = FOLDER_IN+"prop_links_all_en_wd"
PORP_LINKS_PATH_FR_WD = FOLDER_IN+"prop_links_all_fr_wd"

TRIPLES_ATTR_RAW_PATH_1 = FOLDER_IN+"attr_triples_"+KB_TYPE_1
TRIPLES_ATTR_RAW_PATH_2 = FOLDER_IN+"attr_triples_"+KB_TYPE_2
TRIPLES_REL_RAW_PATH_1 = FOLDER_IN+"filter_by_link/rel_triples_"+KB_TYPE_1+"_"+KB_TYPE_2+"_"+KB_TYPE_1
TRIPLES_REL_RAW_PATH_2 = FOLDER_IN+"filter_by_link/rel_triples_"+KB_TYPE_1+"_"+KB_TYPE_2+"_"+KB_TYPE_2

ENT_LINKS_PATH = FOLDER_OUT+"ent_links"
REL_LINKS_OUT_PATH = FOLDER_OUT+"rel_links"

TRIPLES_OUT_PATH_1 = FOLDER_OUT+"triples_1"
TRIPLES_OUT_PATH_2 = FOLDER_OUT+"triples_2"

ATTR_OUT_PATH_1 = FOLDER_OUT+"attr_1"
ATTR_OUT_PATH_2 = FOLDER_OUT+"attr_2"
ATTR_LINKS_OUT_PATH = FOLDER_OUT+"attr_links"
ATTR_TRIPLES_OUT_PATH_1 = FOLDER_OUT+"attr_triples_1"
ATTR_TRIPLES_OUT_PATH_2 = FOLDER_OUT+"attr_triples_2"

TEMP_ATTR_OUT_PATH_1 = FOLDER_TEMP+"temp_attr_1"
TEMP_ATTR_OUT_PATH_2 = FOLDER_TEMP+"temp_attr_2"
TEMP_ATTR_LINKS_OUT_PATH = FOLDER_TEMP+"temp_attr_links"
TEMP_ENTS_1 = FOLDER_TEMP+"temp_ent_1"
TEMP_ENTS_2 = FOLDER_TEMP+"temp_ent_2"
TEMP_ENT_LINKS = FOLDER_TEMP+"temp_ent_links"
