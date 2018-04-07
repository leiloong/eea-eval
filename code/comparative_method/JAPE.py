import sys

from JAPE_attr2vec import learn_vec
from JAPE_ent2vec import ent2vec
# from JAPE_cse_pos_neg import structure_embedding
from JAPE_se_pos_neg_together import structure_embedding

if __name__ == '__main__':
    if len(sys.argv) == 3:
        data_folder = sys.argv[1]
        radio = sys.argv[2]
        structure_embedding(data_folder, radio)
    elif len(sys.argv) == 1:
        structure_embedding("../ISWC2018/dbp_wd_15k_V1/", 0.3)
