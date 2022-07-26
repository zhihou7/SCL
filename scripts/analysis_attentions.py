from scripts import get_id_convert_dicts, obtain_config, get_convert_matrix_coco3
from sklearn.metrics import average_precision_score

hico_to_coco_obj = {0: 4, 1: 47, 2: 24, 3: 46, 4: 34, 5: 35, 6: 21, 7: 59, 8: 13, 9: 1, 10: 14, 11: 8, 12: 73, 13: 39,
                    14: 45, 15: 50,
                    16: 5, 17: 55, 18: 2, 19: 51, 20: 15, 21: 67, 22: 56, 23: 74, 24: 57, 25: 19, 26: 41, 27: 60,
                    28: 16, 29: 54,
                    30: 20, 31: 10, 32: 42, 33: 29, 34: 23, 35: 78, 36: 26, 37: 17, 38: 52, 39: 66, 40: 33, 41: 43,
                    42: 63, 43: 68,
                    44: 3, 45: 64, 46: 49, 47: 69, 48: 12, 49: 0, 50: 53, 51: 58, 52: 72, 53: 65, 54: 48, 55: 76,
                    56: 18, 57: 71,
                    58: 36, 59: 30, 60: 31, 61: 44, 62: 32, 63: 11, 64: 28, 65: 37, 66: 77, 67: 38, 68: 27, 69: 70,
                    70: 61, 71: 79,
                    72: 9, 73: 6, 74: 7, 75: 62, 76: 25, 77: 75, 78: 40, 79: 22}

vcoco_29_2_24 = {0: 0, 1: 1, 2: 2, 4: 3, 5: 4, 6: 5, 7: 6,8: 7, 9: 8, 10: 9, 11: 10, 12: 11, 13: 12,
 14: 13, 15: 14, 16: 15, 18: 16, 19: 17, 20: 18, 21: 19, 24: 20, 25: 21, 26: 22,  28: 23}

import numpy as np
tmp = np.zeros([29, 24])
for k, v in vcoco_29_2_24.items():
    tmp[k][v] = 1.
vcoco_29_2_24 = tmp

vcoco_29_2_21 = {0: 0, 1: 1, 2: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6, 9: 7, 10: 8, 11: 9, 12: 10, 13: 11, 14: 12, 15: 13,
                 16: 7, 18: 14, 19: 15, 20: 15, 21: 16, 24: 17, 25: 18, 26: 19, 28: 20}
import numpy as np
tmp = np.zeros([29, 21])
for k, v in vcoco_29_2_21.items():
    tmp[k][v] = 1.
vcoco_29_2_21 = tmp


def get_convert_matrix(verb_class_num=117, obj_class_num=80):
    import os
    DATA_DIR = './'
    import pickle
    import numpy as np
    verb_to_HO_matrix = np.zeros((600, verb_class_num), np.float32)
    hoi_to_vb = pickle.load(open(DATA_DIR + '/hoi_to_vb.pkl', 'rb'))
    for k, v in hoi_to_vb.items():
        verb_to_HO_matrix[k][v] = 1
    verb_to_HO_matrix = np.transpose(verb_to_HO_matrix)


    obj_to_HO_matrix = np.zeros((600, obj_class_num), np.float32)
    hoi_to_obj = pickle.load(open(DATA_DIR + '/hoi_to_obj.pkl', 'rb'))
    for k, v in hoi_to_obj.items():
        obj_to_HO_matrix[k][hico_to_coco_obj[v]] = 1
    obj_to_HO_matrix = np.transpose(obj_to_HO_matrix)

    return verb_to_HO_matrix, obj_to_HO_matrix



def cal_ap(gt_labels, affordance_probs_new, mask):
    """
    remove masks
    :param gt_labels:
    :param affordance_probs_new:
    :param mask:
    :return:
    """
    # ap = average_precision_score(gt_labels.reshape(-1), affordance_stat_tmp1.reshape(-1))
    # print(ap)
    # exit()
    #
    mask = mask.reshape([-1])
    gt_labels = gt_labels.reshape(-1).tolist()
    affordance_probs_new = affordance_probs_new.reshape(-1).tolist()
    assert len(mask) == len(gt_labels) == len(affordance_probs_new), (len(mask), len(gt_labels), len(affordance_probs_new))
    gt_labels = [gt_labels[i] for i in range(len(mask)) if mask[i] == 0]
    affordance_probs_new = [affordance_probs_new[i] for i in range(len(mask)) if mask[i] == 0]

    ap = average_precision_score(gt_labels, affordance_probs_new)
    return ap


def stat_pre_concept_result(item, gt_labels, mask, num_classes=600, verb_class_num=117, obj_class_num=80):
    import numpy as np
    affordance_stat_tmp = np.load(DATA_DIR + '/afford/'+item)
    hico_id_pairs = []
    ap_new = cal_ap(gt_labels, affordance_stat_tmp, mask)

    ap_all = cal_ap(gt_labels, affordance_stat_tmp, np.zeros([verb_class_num, obj_class_num], np.float32))
    affordance_stat_tmp = affordance_stat_tmp.reshape([verb_class_num, obj_class_num])
    max_v = np.max(affordance_stat_tmp)
    # for v, o in hico_id_pairs:
    #     affordance_stat_tmp[v][o] = 100. + max_v
    affordance_stat_tmp_filter_known = affordance_stat_tmp + gt_known_labels * max_v
    ap_all_fix = cal_ap(gt_labels, affordance_stat_tmp_filter_known, np.zeros([verb_class_num, obj_class_num], np.float32))

    gt_labels_known = np.zeros([verb_class_num, obj_class_num], np.float32)
    print(gt_labels_known.shape)
    for v, o in hico_id_pairs:
        gt_labels_known[v][o] = 1.
    ap_all_know = cal_ap(gt_labels_known, affordance_stat_tmp, np.zeros([verb_class_num, obj_class_num], np.float32))

    f = open(DATA_DIR + '/hico_concepts_fixed.txt', 'a')
    file_name_id = item.replace(".npy", "")
    f.write('{} {}\t{:.4}\t{:.4}\t{:.4}\t{:.4}\n'.format('analysis', file_name_id, ap_new, ap_all, ap_all_fix, ap_all_know))
    f.close()
    print(file_name_id, ap_new, ap_all, ap_all_fix, ap_all_know)


def stat_concepts(file_name, gt_labels, mask, verb_to_HO_matrix, obj_to_HO_matrix,
                  num_classes=600, verb_class_num=117, obj_class_num=80):
    model_name = file_name.split('output/')[-1]
    import torch
    models = torch.load(file_name, map_location=torch.device('cpu'))
    file_name_id = file_name + str(models['epoch'])
    if 'affordance_matrix' not in models['model']:
        return
    affordance_stat = models['model']['affordance_matrix']
    affordance_stat = affordance_stat.cpu().numpy()  # 117x81
    if file_name.__contains__('vcoco'):
        convert_24_21 = {0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 12: 11, 13: 12, 14: 13, 15: 7,
                         16: 14, 17: 15, 18: 15, 19: 16, 20: 17, 21: 18, 22: 19, 23: 20}
        convert_m_24_21 = np.zeros([24, 21], np.float32)
        for k in convert_24_21:
            convert_m_24_21[k] = convert_24_21[k]
        convert_m_norm = convert_m_24_21 if verb_class_num == 21 else np.ones([24, 1])
        vcoco_convert_matrix = vcoco_29_2_21 if verb_class_num == 21 else vcoco_29_2_24
        affordance_stat = np.matmul(affordance_stat.transpose(), vcoco_convert_matrix) / convert_m_norm.sum(axis=0)
        affordance_stat = affordance_stat.transpose()
        # import ipdb;ipdb.set_trace()

    affordance_stat = affordance_stat[:, :obj_class_num]
    list_pairs = []
    affordance_stat_tmp = affordance_stat.reshape(-1)

    ap_new = cal_ap(gt_labels, affordance_stat_tmp, mask)
    np.save(DATA_DIR + '/afford/' + model_name.replace('/', '_') + ".npy", affordance_stat_tmp)
    ap_all = cal_ap(gt_labels, affordance_stat_tmp, np.zeros([verb_class_num, obj_class_num], np.float32))
    affordance_stat_tmp = affordance_stat_tmp.reshape([verb_class_num, obj_class_num])
    max_v = np.max(affordance_stat_tmp)
    # for v, o in hico_id_pairs:
    #     affordance_stat_tmp[v][o] = 100. + max_v
    affordance_stat_tmp_filter_known = affordance_stat_tmp + gt_known_labels * max_v
    ap_all_fix = cal_ap(gt_labels, affordance_stat_tmp_filter_known, np.zeros([verb_class_num, obj_class_num], np.float32))

    gt_labels_known = np.zeros([verb_class_num, obj_class_num], np.float32)
    print(gt_labels_known.shape)
    for v, o in hico_id_pairs:
        gt_labels_known[v][o] = 1.
    ap_all_know = cal_ap(gt_labels_known, affordance_stat_tmp, np.zeros([verb_class_num, obj_class_num], np.float32))

    f = open(DATA_DIR + '/hico_concepts.txt', 'a')
    f.write('{} {}\t{:.4}\t{:.4}\t{:.4}\t{:.4}\n'.format('analysis', file_name_id, ap_new, ap_all, ap_all_fix, ap_all_know))
    f.close()
    print(file_name_id, ap_new, ap_all, ap_all_fix, ap_all_know)
# ap_all_know


if __name__ == "__main__":

    import os

    DATA_DIR = 'data'
    import numpy as np
    import sys
    id_vb, id_obj, id_hoi, hoi_to_obj, hoi_to_verbs = get_id_convert_dicts()
    verb_to_HO_matrix, obj_to_HO_matrix = get_convert_matrix(obj_class_num=81)
    hico_id_pairs = []
    zs_id_pairs = []
    for i in range(600):
        hico_id_pairs.append((hoi_to_verbs[i], hico_to_coco_obj[hoi_to_obj[i]]))
    mask = np.zeros([117, 80], np.float32)
    for v, o in hico_id_pairs:
        mask[v][o] = 1.
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    num_classes, verb_class_num, obj_class_num, gt_labels, concept_gt_pairs, gt_known_labels = obtain_config(file_name)
    print(gt_known_labels.shape, gt_labels.shape)
    if file_name.__contains__('npy'):
        import glob

        begin = False
        for item in os.listdir(DATA_DIR + '/afford/'):
            if not (item.__contains__('checkpoint')):
                continue

            num_classes, verb_class_num, obj_class_num, gt_labels, concept_gt_pairs, gt_known_labels = obtain_config(item)
            # print(item, gt_labels.shape)
            try:
                stat_pre_concept_result(item, gt_labels, gt_known_labels, num_classes, verb_class_num, obj_class_num)
            except Exception as e:
                print(item, 'fail', e)
                continue
    elif file_name.__contains__('*'):
        import re
        r = re.compile(file_name)
        import glob
        tmp = glob.glob('output/*')
        tmp.sort(key=os.path.getmtime, reverse=False)
        tmp = [item.split('/')[-1] for item in tmp]
        model_arr = list(filter(r.match, tmp))
        for i, model in enumerate(model_arr):

            for index in list(range(9999, 3000001, 10000)):
                fname = './output/{}/model_{:0>7d}.pth'.format(model, index)
                if os.path.exists(fname):
                    stat_concepts(fname, gt_labels, gt_known_labels, verb_to_HO_matrix, obj_to_HO_matrix,
                                  num_classes=num_classes, verb_class_num=verb_class_num, obj_class_num=obj_class_num)
    else:

        if file_name.__contains__('VCOCO') or file_name.__contains__('vcoco'):
            hoi_to_obj, hoi_to_verbs, verb_to_HO_matrix, obj_to_HO_matrix = get_convert_matrix_coco3(verb_class_num=verb_class_num)
        else:
            id_vb, id_obj, id_hoi, hoi_to_obj, hoi_to_verbs = get_id_convert_dicts()
        hico_id_pairs = []
        zs_id_pairs = []
        for i in range(num_classes):
            hico_id_pairs.append((hoi_to_verbs[i], hoi_to_obj[i]))

        stat_concepts(file_name, gt_labels, gt_known_labels, verb_to_HO_matrix, obj_to_HO_matrix,
                      num_classes=num_classes, verb_class_num=verb_class_num, obj_class_num=obj_class_num)
    # import ipdb;ipdb.set_trace()