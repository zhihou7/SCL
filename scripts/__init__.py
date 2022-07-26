HICO_NO_INTERACTION_IDS =[item-1 for item in [10, 24, 31, 46, 54, 65, 76, 86, 92, 96, 107, 111, 129, 146, 160, 170, 174, 186, 194, 198, 208, 214,
                                              224, 232, 235, 239, 243, 247, 252, 257, 264, 273, 283, 290, 295, 305, 313, 325, 330, 336, 342, 348,
                                              352, 356, 363, 368, 376, 383, 389, 393, 397, 407, 414, 418, 429, 434, 438, 445, 449, 453, 463, 474,
                                              483, 488, 502, 506, 516, 528, 533, 538, 546, 550, 558, 562, 567, 576, 584, 588, 595, 600]]
DATA_DIR = 'data'
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


def get_id_dicts():
    fobj = open(DATA_DIR + '/hico_list_obj.txt')
    fhoi = open(DATA_DIR + '/hico_list_hoi.txt')
    fvb = open(DATA_DIR + '/hico_list_vb.txt')
    id_obj = {}
    hoi_to_obj = {}
    hoi_to_verbs = {}
    obj_id = {}
    id_hoi = {}
    vb_id = {}
    obj_to_hoi = {}
    id_vb = {}
    for line in fobj.readlines()[2:]:
        line = line.strip()
        # print(line.split(' '), [item for item in line.split(' ') if item != ''])

        cid, obj = [item for item in line.split(' ') if item != '']
        obj_id[obj] = hico_to_coco_obj[int(cid) - 1]
        id_obj[hico_to_coco_obj[int(cid) - 1]] = obj
        # print(coco_annos_map[coco_obj], obj, cid)

    for line in fvb.readlines()[2:]:
        line = line.strip()
        # print(line.split(' '), [item for item in line.split(' ') if item != ''])

        cid, vb = [item for item in line.split(' ') if item != '']
        vb_id[vb] = int(cid) - 1
        id_vb[int(cid) - 1] = vb

    for line in fhoi.readlines()[2:]:
        line = line.strip()
        # print(line.split(' '), [item for item in line.split(' ') if item != ''])

        cid, obj, vb = [item for item in line.split(' ') if item != '']
        hoi_to_obj[int(cid) - 1] = obj_id[obj]
        id_hoi[int(cid) - 1] = obj + ' ' + vb
        hoi_to_verbs[int(cid) - 1] = vb_id[vb]
        if obj_id[obj] in obj_to_hoi:
            obj_to_hoi[obj_id[obj]].append(int(cid) - 1)
        else:
            obj_to_hoi[obj_id[obj]] = [int(cid) - 1]

    return id_vb, id_obj, id_hoi


def get_convert_matrix_coco3(verb_class_num=24, obj_class_num=80):
    if verb_class_num == 24:
        set_list = [(0, 38), (1, 31), (1, 32), (2, 43), (2, 44), (2, 77), (3, 1), (3, 19), (3, 28), (3, 46), (3, 47),
                    (3, 48), (3, 49), (3, 51), (3, 52), (3, 54), (3, 55), (3, 56), (4, 2), (4, 3), (4, 4), (4, 6), (4, 7),
                    (4, 8), (4, 9), (4, 18), (4, 21), (5, 68), (6, 33), (7, 64), (8, 47), (8, 48), (8, 49), (8, 50),
                    (8, 51), (8, 52), (8, 53), (8, 54), (8, 55), (8, 56), (9, 2), (9, 4), (9, 14), (9, 18), (9, 21),
                    (9, 25), (9, 27), (9, 29), (9, 57), (9, 58), (9, 60), (9, 61), (9, 62), (9, 64), (10, 31), (10, 32),
                    (10, 37), (10, 38), (11, 14), (11, 57), (11, 58), (11, 60), (11, 61), (12, 40), (12, 41), (12, 42),
                    (12, 46), (13, 1), (13, 25), (13, 26), (13, 27), (13, 29), (13, 30), (13, 31), (13, 32), (13, 33),
                    (13, 34), (13, 35), (13, 37), (13, 38), (13, 39), (13, 40), (13, 41), (13, 42), (13, 47), (13, 50),
                    (13, 68), (13, 74), (13, 75), (13, 78), (14, 30), (14, 33), (15, 43), (15, 44), (15, 45), (16, 1),
                    (16, 2), (16, 3), (16, 4), (16, 5), (16, 6), (16, 7), (16, 8), (16, 11), (16, 14), (16, 15), (16, 16),
                    (16, 17), (16, 18), (16, 19), (16, 20), (16, 21), (16, 24), (16, 25), (16, 26), (16, 27), (16, 28),
                    (16, 29), (16, 30), (16, 31), (16, 32), (16, 33), (16, 34), (16, 35), (16, 36), (16, 37), (16, 38),
                    (16, 39), (16, 40), (16, 41), (16, 42), (16, 43), (16, 44), (16, 45), (16, 46), (16, 47), (16, 48),
                    (16, 49), (16, 51), (16, 53), (16, 54), (16, 55), (16, 56), (16, 57), (16, 61), (16, 62), (16, 63),
                    (16, 64), (16, 65), (16, 66), (16, 67), (16, 68), (16, 73), (16, 74), (16, 75), (16, 77), (17, 35),
                    (17, 39), (18, 33), (19, 31), (19, 32), (20, 74), (21, 1), (21, 2), (21, 4), (21, 8), (21, 9), (21, 14),
                    (21, 15), (21, 16), (21, 17), (21, 18), (21, 19), (21, 21), (21, 25), (21, 26), (21, 27), (21, 28),
                    (21, 29), (21, 30), (21, 31), (21, 32), (21, 33), (21, 34), (21, 35), (21, 36), (21, 37), (21, 38),
                    (21, 39), (21, 40), (21, 41), (21, 42), (21, 43), (21, 44), (21, 45), (21, 46), (21, 47), (21, 48),
                    (21, 49), (21, 50), (21, 51), (21, 52), (21, 53), (21, 54), (21, 55), (21, 56), (21, 57), (21, 64),
                    (21, 65), (21, 66), (21, 67), (21, 68), (21, 73), (21, 74), (21, 77), (21, 78), (21, 79), (21, 80),
                    (22, 32), (22, 37), (23, 30), (23, 33)]
    elif verb_class_num == 21:
        set_list = [(0, 38), (1, 31), (1, 32), (2, 1), (2, 19), (2, 28), (2, 43), (2, 44), (2, 46), (2, 47), (2, 48),
                    (2, 49),
                    (2, 51), (2, 52), (2, 54), (2, 55), (2, 56), (2, 77), (3, 2), (3, 3), (3, 4), (3, 6), (3, 7),
                    (3, 8),
                    (3, 9), (3, 18), (3, 21), (4, 68), (5, 33), (6, 64), (7, 43), (7, 44), (7, 45), (7, 47), (7, 48),
                    (7, 49),
                    (7, 50), (7, 51), (7, 52), (7, 53), (7, 54), (7, 55), (7, 56), (8, 2), (8, 4), (8, 14), (8, 18),
                    (8, 21),
                    (8, 25), (8, 27), (8, 29), (8, 57), (8, 58), (8, 60), (8, 61), (8, 62), (8, 64), (9, 31), (9, 32),
                    (9, 37),
                    (9, 38), (10, 14), (10, 57), (10, 58), (10, 60), (10, 61), (11, 40), (11, 41), (11, 42), (11, 46),
                    (12, 1),
                    (12, 25), (12, 26), (12, 27), (12, 29), (12, 30), (12, 31), (12, 32), (12, 33), (12, 34), (12, 35),
                    (12, 37), (12, 38), (12, 39), (12, 40), (12, 41), (12, 42), (12, 47), (12, 50), (12, 68), (12, 74),
                    (12, 75), (12, 78), (13, 30), (13, 33), (14, 1), (14, 2), (14, 3), (14, 4), (14, 5), (14, 6),
                    (14, 7),
                    (14, 8), (14, 11), (14, 14), (14, 15), (14, 16), (14, 17), (14, 18), (14, 19), (14, 20), (14, 21),
                    (14, 24),
                    (14, 25), (14, 26), (14, 27), (14, 28), (14, 29), (14, 30), (14, 31), (14, 32), (14, 33), (14, 34),
                    (14, 35), (14, 36), (14, 37), (14, 38), (14, 39), (14, 40), (14, 41), (14, 42), (14, 43), (14, 44),
                    (14, 45), (14, 46), (14, 47), (14, 48), (14, 49), (14, 51), (14, 53), (14, 54), (14, 55), (14, 56),
                    (14, 57), (14, 61), (14, 62), (14, 63), (14, 64), (14, 65), (14, 66), (14, 67), (14, 68), (14, 73),
                    (14, 74), (14, 75), (14, 77), (15, 33), (15, 35), (15, 39), (16, 31), (16, 32), (17, 74), (18, 1),
                    (18, 2),
                    (18, 4), (18, 8), (18, 9), (18, 14), (18, 15), (18, 16), (18, 17), (18, 18), (18, 19), (18, 21),
                    (18, 25),
                    (18, 26), (18, 27), (18, 28), (18, 29), (18, 30), (18, 31), (18, 32), (18, 33), (18, 34), (18, 35),
                    (18, 36), (18, 37), (18, 38), (18, 39), (18, 40), (18, 41), (18, 42), (18, 43), (18, 44), (18, 45),
                    (18, 46), (18, 47), (18, 48), (18, 49), (18, 50), (18, 51), (18, 52), (18, 53), (18, 54), (18, 55),
                    (18, 56), (18, 57), (18, 64), (18, 65), (18, 66), (18, 67), (18, 68), (18, 73), (18, 74), (18, 77),
                    (18, 78), (18, 79), (18, 80), (19, 32), (19, 37), (20, 30), (20, 33)]
    else:
        return
    import pickle
    import numpy as np
    hoi_to_obj = {}
    hoi_to_verbs = {}
    verb_to_HO_matrix = np.zeros((len(set_list), verb_class_num))

    for i in range(len(set_list)):
        item = set_list[i]
        verb_to_HO_matrix[i][item[0]] = 1
        hoi_to_verbs[i] = item[0]

    verb_to_HO_matrix = np.transpose(verb_to_HO_matrix)

    obj_to_HO_matrix = np.zeros((len(set_list), obj_class_num))
    for i in range(len(set_list)):
        item = set_list[i]
        obj_to_HO_matrix[i][item[1] - 1] = 1
        hoi_to_obj[i] = item[1] -1
    obj_to_HO_matrix = np.transpose(obj_to_HO_matrix)
    return hoi_to_obj, hoi_to_verbs, verb_to_HO_matrix, obj_to_HO_matrix


def obtain_config(file_name):
    verb_classes = ['hold_obj', 'stand', 'sit_instr', 'ride_instr', 'walk', 'look_obj', 'hit_instr', 'hit_obj',
                    'eat_obj', 'eat_instr', 'jump_instr', 'lay_instr', 'talk_on_phone_instr', 'carry_obj',
                    'throw_obj', 'catch_obj', 'cut_instr', 'cut_obj', 'run', 'work_on_computer_instr',
                    'ski_instr', 'surf_instr', 'skateboard_instr', 'smile', 'drink_instr', 'kick_obj',
                    'point_instr', 'read_obj', 'snowboard_instr']
    thesis_map_indices = [0, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 24, 25, 27, 28]
    if file_name.__contains__('VCOCO') and file_name.__contains__('CL_24'):

        num_classes = 222
        verb_class_num = 24
        obj_class_num = 80

        gt_label_file = open(DATA_DIR + 'vcoco_concepts_24.csv')
        import numpy as np

        gt_labels = np.zeros([verb_class_num, obj_class_num], np.float)
        gt_known_labels = np.zeros([verb_class_num, obj_class_num], np.float)
        concept_gt_pairs = []
        for line in gt_label_file.readlines():
            arrs = line.split(' ')
            v = arrs[1]
            o = arrs[2]
            verb_name = arrs[3]
            qpic_vcoco_vid = thesis_map_indices.index(verb_classes.index(verb_name))
            v = qpic_vcoco_vid
            gt_labels[int(v)][int(o)] = 1.

            concept_gt_pairs.append((int(v), int(o)))
            if line.startswith('yes'):
                gt_known_labels[int(v)][int(o)] = 1.
    elif file_name.__contains__('VCOCO') and file_name.__contains__('CL_21') or file_name.__contains__('vcoco'):
        convert_24_21 = {0: 0, 1: 1, 2: 2, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 12: 11, 13: 12, 14: 13, 15: 7,
                         16: 14, 17: 15, 18: 15, 19: 16, 20: 17, 21: 18, 22: 19, 23: 20}
        num_classes = 222
        verb_class_num = 21
        obj_class_num = 80

        gt_label_file = open(DATA_DIR + 'vcoco_concepts_24.csv')
        import numpy as np

        gt_labels = np.zeros([verb_class_num, obj_class_num], np.float)
        gt_known_labels = np.zeros([verb_class_num, obj_class_num], np.float)
        concept_gt_pairs = []
        for line in gt_label_file.readlines():
            arrs = line.split(' ')
            v = arrs[1]
            o = arrs[2]
            verb_name = arrs[3]
            qpic_vcoco_vid = thesis_map_indices.index(verb_classes.index(verb_name))
            v = qpic_vcoco_vid
            gt_labels[convert_24_21[int(v)]][int(o)] = 1.
            if line.startswith('yes'): gt_known_labels[convert_24_21[int(v)]][int(o)] = 1.
            concept_gt_pairs.append((convert_24_21[int(v)], int(o)))
    else:
        num_classes = 600
        verb_class_num = 117
        obj_class_num = 80

        gt_label_file = open(DATA_DIR + 'label_hoi_concept_new.csv')
        import numpy as np

        gt_labels = np.zeros([verb_class_num, obj_class_num], np.float)
        gt_known_labels = np.zeros([verb_class_num, obj_class_num], np.float)
        concept_gt_pairs = []
        hoi_to_obj, hoi_to_verbs, obj_to_hoi, coco_to_hico_obj, coco80_to_hico_obj, \
        hico_to_coco_obj, id_vb, id_obj, id_hoi = get_hoi_convert_dicts()
        for line in gt_label_file.readlines():
            arrs = line.split(' ')
            v = arrs[1]
            o = arrs[2]
            gt_labels[int(v)][hico_to_coco_obj[int(o)]] = 1.
            concept_gt_pairs.append((int(v), hico_to_coco_obj[int(o)]))
            if line.startswith('yes'):
                gt_known_labels[int(v)][hico_to_coco_obj[int(o)]] = 1.
    return num_classes, verb_class_num, obj_class_num, gt_labels, concept_gt_pairs, gt_known_labels


def get_zero_shot_type(model_name):
    zero_shot_type = 0
    if model_name.__contains__('_zs_'):
        zero_shot_type = 1
    elif model_name.__contains__('_zs3_'):
        zero_shot_type = 3
    elif model_name.__contains__('_zs4_'):
        zero_shot_type = 4
    elif model_name.__contains__('_zs6_'):
        zero_shot_type = 6
    elif model_name.__contains__('_zs7_'):
        zero_shot_type = 7
    return zero_shot_type


def get_unseen_index(zero_shot_type):
    unseen_idx = None
    if zero_shot_type == 2:
        unseen_idx = [516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 538, 539, 540, 541, 542, 543, 544,
                      545, 546, 547, 548, 549, 558, 559, 560, 561, 576, 577, 578, 579, 580, 581, 582, 583, 76, 77, 78,
                      79, 80, 81, 82, 83, 84, 85, 107, 108, 109, 110, 194, 195, 196, 197, 208, 209, 210, 211, 212, 213,
                      235, 236, 237, 238, 239, 240, 241, 242, 325, 326, 327, 328, 329, 342, 343, 344, 345, 346, 347,
                      376, 377, 378, 379, 380, 381, 382, 393, 394, 395, 396, 414, 415, 416, 417, 429, 430, 431, 432,
                      433, 434, 435, 436, 437, 449, 450, 451, 452, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473]
    elif zero_shot_type == 8:
        unseen_idx = [366, 143, 314, 115, 459, 415, 313, 387, 117, 131, 457, 241, 455, 226, 156, 271, 264, 577, 518, 385, 266, 347, 78, 476, 479]
    elif zero_shot_type == 9:
        unseen_idx = [366, 143, 314, 115, 459, 415, 313, 387, 117, 131, 457, 241, 455, 226, 156, 271, 264, 577, 518, 385, 266, 347, 78, 476, 479]


    elif zero_shot_type == 11:
        unseen_idx = [111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                      126, 127, 128, 224, 225, 226, 227, 228, 229, 230, 231, 290, 291, 292, 293,
                      294, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 336, 337,
                      338, 339, 340, 341, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428,
                      429, 430, 431, 432, 433, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462,
                      463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 533, 534, 535, 536,
                      537, 558, 559, 560, 561, 595, 596, 597, 598, 599]
        #  miss [ 5, 6, 28, 56, 88] verbs 006  break    007  brush_with 029  flip  057  move  089  slide
    elif zero_shot_type == 17:
        unseen_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 24, 25, 26, 27, 28, 29, 30, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
                      78, 79, 80, 81, 82, 83, 84, 85, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 170, 171, 172, 173, 186,
                      187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 232,
                      233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263,
                      273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 290, 291, 292, 293, 294, 325, 326, 327, 328, 329, 330, 331,
                      332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 348, 349, 350, 351, 352, 353, 354, 355, 389, 390, 391, 392,
                      393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 434, 435, 436, 437, 483, 484, 485, 486,
                      487, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522,
                      523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 546, 547, 548, 549, 550, 551, 552,
                      553, 554, 555, 556, 557, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 584, 585, 586,
                      587, 595, 596, 597, 598, 599]
    elif zero_shot_type == 12:
        unseen_idx = [
            0, 1, 10, 29, 30, 41, 48, 50, 56, 57, 69, 72, 80, 81, 92, 93, 96, 109,
            110, 114, 127, 134, 139, 161, 170, 177, 183, 189, 191, 197, 198, 201,
            208, 209, 221, 227, 229, 232, 233, 235, 239, 242, 245, 247, 250, 252,
            260, 263, 270, 271, 280, 286, 288, 290, 299, 301, 308, 316, 325, 334,
            336, 343, 344, 352, 355, 356, 357, 363, 375, 376, 380, 384, 387, 389,
            395, 396, 397, 404, 408, 413, 414, 417, 422, 425, 433, 434, 436, 444,
            448, 452, 454, 455, 463, 480, 484, 488, 498, 503, 505, 507, 513, 516,
            527, 530, 532, 536, 537, 540, 546, 547, 550, 555, 561, 562, 566, 567,
            572, 581, 587, 598
        ]
    elif zero_shot_type == 13:
        unseen_idx = [
            0, 3, 22, 29, 32, 52, 58, 63, 72, 73, 78, 89, 91, 92, 105, 106, 107,
            113, 137, 148, 163, 165, 172, 178, 179, 194, 196, 207, 209, 210, 214,
            215, 229, 231, 233, 234, 236, 240, 241, 243, 245, 247, 252, 254, 260,
            262, 269, 272, 282, 286, 289, 292, 296, 302, 310, 315, 322, 326, 333,
            335, 338, 340, 343, 347, 350, 351, 353, 354, 358, 362, 367, 368, 376,
            380, 388, 389, 393, 395, 397, 399, 410, 412, 416, 417, 419, 420, 429,
            434, 439, 441, 445, 449, 454, 467, 476, 483, 495, 503, 507, 511, 519,
            528, 529, 535, 537, 539, 547, 548, 556, 557, 561, 563, 565, 569, 579,
            587, 589, 591, 595, 597
        ]
    elif zero_shot_type == 14:
        unseen_idx = [
            9, 25, 30, 49, 51, 61, 71, 74, 77, 82, 94, 108, 110, 116, 126, 131,
            143, 164, 168, 177, 185, 200, 201, 208, 212, 229, 232, 234, 239, 241,
            243, 244, 248, 255, 256, 258, 259, 266, 272, 279, 281, 287, 288, 290,
            294, 295, 301, 305, 308, 319, 322, 325, 328, 330, 332, 337, 344, 347,
            349, 350, 356, 359, 366, 367, 370, 375, 378, 380, 386, 387, 390, 391,
            400, 406, 409, 411, 416, 419, 428, 429, 431, 436, 439, 443, 445, 447,
            449, 451, 454, 457, 466, 468, 477, 479, 485, 486, 491, 497, 504, 508,
            510, 516, 527, 529, 531, 533, 536, 544, 545, 546, 549, 550, 552, 558,
            561, 568, 589, 594, 596, 599
        ]
    elif zero_shot_type == 15:
        unseen_idx = [
            4, 14, 26, 27, 41, 45, 51, 53, 62, 69, 74, 80, 88, 91, 92, 93, 100,
            107, 110, 125, 127, 130, 136, 152, 153, 163, 167, 170, 177, 183, 186,
            188, 196, 200, 207, 210, 217, 220, 225, 232, 237, 242, 243, 246, 248,
            252, 253, 263, 267, 270, 280, 285, 289, 291, 292, 302, 312, 316, 325,
            335, 341, 343, 348, 355, 356, 362, 363, 368, 378, 382, 384, 385, 390,
            394, 396, 404, 406, 407, 415, 416, 426, 428, 429, 431, 435, 441, 443,
            448, 450, 452, 454, 460, 467, 469, 479, 480, 483, 498, 503, 505, 509,
            518, 524, 532, 533, 541, 549, 551, 560, 561, 566, 572, 573, 579, 580,
            585, 587, 594, 595, 599
        ]
    elif zero_shot_type == 16:
        unseen_idx = [
            0, 4, 28, 29, 42, 43, 49, 53, 55, 56, 66, 72, 80, 81, 87, 90, 92, 94,
            100, 103, 109, 110, 129, 137, 149, 159, 166, 167, 170, 171, 179, 182,
            189, 193, 194, 195, 201, 206, 236, 237, 244, 245, 248, 249, 254, 255,
            257, 258, 266, 270, 290, 292, 300, 303, 316, 317, 326, 327, 331, 333,
            339, 340, 345, 347, 349, 350, 352, 353, 357, 362, 365, 366, 375, 380,
            381, 383, 385, 395, 396, 425, 426, 446, 448, 450, 451, 458, 466, 470,
            474, 476, 485, 487, 494, 495, 504, 505, 509, 515, 516, 525, 528, 529,
            536, 537, 539, 541, 546, 548, 556, 557, 568, 572, 578, 582, 585, 586,
            590, 593, 595, 597
        ]
    elif zero_shot_type == 3:
        # rare
        unseen_idx = [509, 279, 280, 402, 504, 286, 499, 498, 289, 485, 303, 311, 325, 439, 351, 358, 66, 427, 379, 418, 70, 416,
                      389, 90, 395, 76, 397, 84, 135, 262, 401, 592, 560, 586, 548, 593, 526, 181, 257, 539, 535, 260, 596, 345, 189,
                      205, 206, 429, 179, 350, 405, 522, 449, 261, 255, 546, 547, 44, 22, 334, 599, 239, 315, 317, 229, 158, 195,
                      238, 364, 222, 281, 149, 399, 83, 127, 254, 398, 403, 555, 552, 520, 531, 440, 436, 482, 274, 8, 188, 216, 597,
                      77, 407, 556, 469, 474, 107, 390, 410, 27, 381, 463, 99, 184, 100, 292, 517, 80, 333, 62, 354, 104, 55, 50,
                      198, 168, 391, 192, 595, 136, 581]
    elif zero_shot_type == 4:
        # non rare
        unseen_idx = [38, 41, 20, 18, 245, 11, 19, 154, 459, 42, 155, 139, 60, 461, 577, 153, 582, 89, 141, 576, 75, 212, 472, 61,
                      457, 146, 208, 94, 471, 131, 248, 544, 515, 566, 370, 481, 226, 250, 470, 323, 169, 480, 479, 230, 385, 73,
                      159, 190, 377, 176, 249, 371, 284, 48, 583, 53, 162, 140, 185, 106, 294, 56, 320, 152, 374, 338, 29, 594, 346,
                      456, 589, 45, 23, 67, 478, 223, 493, 228, 240, 215, 91, 115, 337, 559, 7, 218, 518, 297, 191, 266, 304, 6, 572,
                      529, 312, 9, 308, 417, 197, 193, 163, 455, 25, 54, 575, 446, 387, 483, 534, 340, 508, 110, 329, 246, 173, 506,
                      383, 93, 516, 64]
        # 25729, 93041
    elif zero_shot_type == 5:
        # 61 rare
        unseen_idx = [509, 402, 18, 286, 11, 498, 154, 485, 42, 311, 139, 439, 461, 358, 153, 66, 89, 379, 576, 70, 212, 389, 61,
                      395, 146, 397, 94, 135, 131, 401, 544, 560, 370, 586, 226, 593, 470, 181, 169, 539, 479, 260, 385, 345, 159,
                      205, 190, 429, 176, 350, 371, 522, 48, 112, 53, 255, 140, 547, 106, 549, 56, 334, 152, 239, 338, 317, 158, 346,
                      238, 589, 222, 23, 149, 67, 83, 223, 254, 228, 403, 215, 552, 115, 531, 436, 7, 274, 518, 188, 191, 216, 266,
                      77, 6, 529, 469, 9, 107, 417, 390, 193, 27, 455, 463, 25, 184, 575, 292, 387, 80, 483, 340, 354, 110, 55, 329,
                      550, 246, 168, 383, 595]
    elif zero_shot_type == 6:
        # 24 rare
        unseen_idx = [371, 75, 532, 358, 419, 541, 195, 483, 277, 114, 210, 133, 373, 590, 85, 511, 128, 518, 579, 553, 394, 35, 547,
                      14, 77, 64, 468, 132, 22, 301, 487, 544, 139, 576, 271, 258, 556, 444, 257, 162, 23, 407, 46, 259, 273, 104,
                      593, 84, 473, 457, 32, 171, 583, 125, 329, 344, 79, 11, 307, 31, 283, 96, 545, 265, 19, 475, 460, 98, 448, 538,
                      34, 151, 91, 582, 324, 370, 198, 93, 341, 393, 146, 26, 530, 390, 447, 51, 164, 474, 466, 218, 571, 107, 144,
                      361, 326, 185, 50, 179, 517, 261, 202, 522, 256, 235, 355, 546, 103, 278, 392, 246, 254, 13, 596, 381, 21, 337,
                      178, 318, 321, 193]
    elif zero_shot_type == 7:
        # 24 rare merge of zs3 & zs4
        unseen_idx = [509, 279, 280, 402, 504, 286, 499, 498, 289, 485, 303, 311, 325, 439, 351, 358, 66, 427, 379, 418, 70, 416, 389,
                      90, 38, 41, 20, 18, 245, 11, 19, 154, 459, 42, 155, 139, 60, 461, 577, 153, 582, 89, 141, 576, 75, 212, 472, 61,
                      457, 146, 208, 94, 471, 131, 248, 544, 515, 566, 370, 481, 226, 250, 470, 323, 169, 480, 479, 230, 385, 73, 159,
                      190, 377, 176, 249, 371, 284, 48, 583, 53, 162, 140, 185, 106, 294, 56, 320, 152, 374, 338, 29, 594, 346, 456, 589,
                      45, 23, 67, 478, 223, 493, 228, 240, 215, 91, 115, 337, 559, 7, 218, 518, 297, 191, 266, 304, 6, 572, 529, 312,
                      9]
        # 22529, 14830, 22493, 17411, 21912,
    elif zero_shot_type == 0:
        unseen_idx = []
    return unseen_idx


def get_id_convert_dicts():
    fobj = open(DATA_DIR + '/Data/hico_list_obj.txt')
    fhoi = open(DATA_DIR + '/Data/hico_list_hoi.txt')
    fvb = open(DATA_DIR + '/Data/hico_list_vb.txt')
    id_obj = {}
    hoi_to_obj = {}
    hoi_to_verbs = {}
    obj_id = {}
    id_hoi = {}
    vb_id = {}
    obj_to_hoi = {}
    id_vb = {}
    for line in fobj.readlines()[2:]:
        line = line.strip()
        # print(line.split(' '), [item for item in line.split(' ') if item != ''])

        cid, obj = [item for item in line.split(' ') if item != '']
        obj_id[obj] = hico_to_coco_obj[int(cid) - 1]
        id_obj[hico_to_coco_obj[int(cid) - 1]] = obj
        # print(coco_annos_map[coco_obj], obj, cid)

    for line in fvb.readlines()[2:]:
        line = line.strip()
        # print(line.split(' '), [item for item in line.split(' ') if item != ''])

        cid, vb = [item for item in line.split(' ') if item != '']
        vb_id[vb] = int(cid) - 1
        id_vb[int(cid) - 1] = vb

    for line in fhoi.readlines()[2:]:
        line = line.strip()
        # print(line.split(' '), [item for item in line.split(' ') if item != ''])

        cid, obj, vb = [item for item in line.split(' ') if item != '']
        hoi_to_obj[int(cid) - 1] = obj_id[obj]
        id_hoi[int(cid) - 1] = obj + ' ' + vb
        hoi_to_verbs[int(cid) - 1] = vb_id[vb]
        if obj_id[obj] in obj_to_hoi:
            obj_to_hoi[obj_id[obj]].append(int(cid) - 1)
        else:
            obj_to_hoi[obj_id[obj]] = [int(cid) - 1]

    return id_vb, id_obj, id_hoi, hoi_to_obj, hoi_to_verbs


def get_hoi_convert_dicts():
    # from pycocotools.coco import COCO
    #
    # coco_annotation_path = DATA_DIR + 'Data/v-coco/coco/annotations/instances_train2014.json'
    # coco_annotation_path = DATA_DIR + '/dataset/coco/annotations/instances_val2017.json'
    # coco = COCO(coco_annotation_path)
    # cats = coco.loadCats(coco.getCatIds())
    # coco_annos_map = {}
    # for item in cats:
    #     coco_annos_map[item['name']] = item['id']
    coco_annos_map = {'person': 1, 'bicycle': 2, 'car': 3, 'motorcycle': 4, 'airplane': 5, 'bus': 6, 'train': 7,
                      'truck': 8, 'boat': 9, 'traffic light': 10, 'fire hydrant': 11, 'stop sign': 13,
                      'parking meter': 14, 'bench': 15, 'bird': 16, 'cat': 17, 'dog': 18, 'horse': 19, 'sheep': 20,
                      'cow': 21, 'elephant': 22, 'bear': 23, 'zebra': 24, 'giraffe': 25, 'backpack': 27, 'umbrella': 28,
                      'handbag': 31, 'tie': 32, 'suitcase': 33, 'frisbee': 34, 'skis': 35, 'snowboard': 36,
                      'sports ball': 37, 'kite': 38, 'baseball bat': 39, 'baseball glove': 40, 'skateboard': 41,
                      'surfboard': 42, 'tennis racket': 43, 'bottle': 44, 'wine glass': 46, 'cup': 47, 'fork': 48,
                      'knife': 49, 'spoon': 50, 'bowl': 51, 'banana': 52, 'apple': 53, 'sandwich': 54, 'orange': 55,
                      'broccoli': 56, 'carrot': 57, 'hot dog': 58, 'pizza': 59, 'donut': 60, 'cake': 61, 'chair': 62,
                      'couch': 63, 'potted plant': 64, 'bed': 65, 'dining table': 67, 'toilet': 70, 'tv': 72,
                      'laptop': 73, 'mouse': 74, 'remote': 75, 'keyboard': 76, 'cell phone': 77, 'microwave': 78,
                      'oven': 79, 'toaster': 80, 'sink': 81, 'refrigerator': 82, 'book': 84, 'clock': 85, 'vase': 86,
                      'scissors': 87, 'teddy bear': 88, 'hair drier': 89, 'toothbrush': 90}

    # print(cats);exit()
    # [{'id': 224, 'name': 'scale'}, {'id': 220, 'name': 'tape'}, {'id': 217, 'name': 'chicken'}, {'id': 244, 'name': 'hurdle'}, {'id': 354, 'name': 'game board'}, {'id': 334, 'name': 'baozi'}, {'id': 360, 'name': 'target'}, {'id': 26, 'name': 'plants pot/vase'}, {'id': 209, 'name': 'toothbrush'}, {'id': 190, 'name': 'projector'}, {'id': 300, 'name': 'cheese'}, {'id': 166, 'name': 'candy'}, {'id': 352, 'name': 'durian'}, {'id': 279, 'name': 'dumbbell'}, {'id': 136, 'name': 'gas stove'}, {'id': 335, 'name': 'lion'}, {'id': 251, 'name': 'french fries'}, {'id': 27, 'name': 'bench'}, {'id': 83, 'name': 'power outlet'}, {'id': 58, 'name': 'faucet'}, {'id': 25, 'name': 'storage box'}, {'id': 330, 'name': 'crab'}, {'id': 237, 'name': 'helicopter'}, {'id': 362, 'name': 'chainsaw'}, {'id': 288, 'name': 'antelope'}, {'id': 280, 'name': 'hamimelon'}, {'id': 294, 'name': 'jellyfish'}, {'id': 200, 'name': 'kettle'}, {'id': 215, 'name': 'marker'}, {'id': 204, 'name': 'clutch'}, {'id': 283, 'name': 'lettuce'}, {'id': 138, 'name': 'toilet'}, {'id': 115, 'name': 'oven'}, {'id': 170, 'name': 'baseball'}, {'id': 85, 'name': 'drum'}, {'id': 88, 'name': 'hanger'}, {'id': 236, 'name': 'toaster'}, {'id': 22, 'name': 'bracelet'}, {'id': 261, 'name': 'cherry'}, {'id': 159, 'name': 'tissue '}, {'id': 225, 'name': 'watermelon'}, {'id': 183, 'name': 'basketball'}, {'id': 128, 'name': 'cleaning products'}, {'id': 123, 'name': 'tent'}, {'id': 188, 'name': 'fire hydrant'}, {'id': 81, 'name': 'truck'}, {'id': 304, 'name': 'rice cooker'}, {'id': 331, 'name': 'microscope'}, {'id': 262, 'name': 'tablet'}, {'id': 73, 'name': 'stuffed animal'}, {'id': 228, 'name': 'golf ball'}, {'id': 247, 'name': 'CD'}, {'id': 273, 'name': 'eggplant'}, {'id': 44, 'name': 'bowl'}, {'id': 12, 'name': 'desk'}, {'id': 351, 'name': 'eagle'}, {'id': 43, 'name': 'slippers'}, {'id': 252, 'name': 'horn'}, {'id': 40, 'name': 'carpet'}, {'id': 234, 'name': 'notepaper'}, {'id': 232, 'name': 'peach'}, {'id': 346, 'name': 'saw'}, {'id': 144, 'name': 'surfboard'}, {'id': 210, 'name': 'facial cleanser'}, {'id': 265, 'name': 'corn'}, {'id': 169, 'name': 'folder'}, {'id': 214, 'name': 'violin'}, {'id': 64, 'name': 'watch'}, {'id': 10, 'name': 'glasses'}, {'id': 124, 'name': 'shampoo/shower gel'}, {'id': 131, 'name': 'pizza'}, {'id': 357, 'name': 'asparagus'}, {'id': 295, 'name': 'mushroom'}, {'id': 322, 'name': 'steak'}, {'id': 178, 'name': 'suitcase'}, {'id': 347, 'name': 'table tennis  paddle'}, {'id': 211, 'name': 'mango'}, {'id': 29, 'name': 'boots'}, {'id': 56, 'name': 'necklace'}, {'id': 327, 'name': 'noodles'}, {'id': 272, 'name': 'volleyball'}, {'id': 141, 'name': 'baseball bat'}, {'id': 264, 'name': 'nuts'}, {'id': 139, 'name': 'stroller'}, {'id': 155, 'name': 'pumpkin'}, {'id': 171, 'name': 'strawberry'}, {'id': 181, 'name': 'pear'}, {'id': 111, 'name': 'luggage'}, {'id': 54, 'name': 'sandals'}, {'id': 150, 'name': 'liquid soap'}, {'id': 13, 'name': 'handbag'}, {'id': 365, 'name': 'flashlight'}, {'id': 291, 'name': 'trombone'}, {'id': 116, 'name': 'remote'}, {'id': 140, 'name': 'shovel'}, {'id': 180, 'name': 'ladder'}, {'id': 74, 'name': 'cake'}, {'id': 292, 'name': 'pomegranate'}, {'id': 84, 'name': 'clock'}, {'id': 162, 'name': 'vent'}, {'id': 104, 'name': 'cymbal'}, {'id': 364, 'name': 'iron'}, {'id': 348, 'name': 'okra'}, {'id': 359, 'name': 'pasta'}, {'id': 126, 'name': 'lantern'}, {'id': 269, 'name': 'broom'}, {'id': 192, 'name': 'fire extinguisher'}, {'id': 177, 'name': 'snowboard'}, {'id': 277, 'name': 'rice'}, {'id': 245, 'name': 'swing'}, {'id': 82, 'name': 'cow'}, {'id': 63, 'name': 'van'}, {'id': 305, 'name': 'tuba'}, {'id': 15, 'name': 'book'}, {'id': 249, 'name': 'swan'}, {'id': 5, 'name': 'lamp'}, {'id': 303, 'name': 'race car'}, {'id': 213, 'name': 'egg'}, {'id': 253, 'name': 'avocado'}, {'id': 92, 'name': 'guitar'}, {'id': 246, 'name': 'radio'}, {'id': 2, 'name': 'sneakers'}, {'id': 342, 'name': 'eraser'}, {'id': 320, 'name': 'measuring cup'}, {'id': 312, 'name': 'sushi'}, {'id': 212, 'name': 'deer'}, {'id': 318, 'name': 'parrot'}, {'id': 168, 'name': 'scissors'}, {'id': 102, 'name': 'balloon'}, {'id': 317, 'name': 'tortoise/turtle'}, {'id': 285, 'name': 'meat balls'}, {'id': 148, 'name': 'cat'}, {'id': 315, 'name': 'electric drill'}, {'id': 341, 'name': 'comb'}, {'id': 191, 'name': 'sausage'}, {'id': 223, 'name': 'bar soap'}, {'id': 201, 'name': 'hamburger'}, {'id': 174, 'name': 'pepper'}, {'id': 227, 'name': 'router/modem'}, {'id': 316, 'name': 'spring rolls'}, {'id': 182, 'name': 'american football'}, {'id': 299, 'name': 'egg tart'}, {'id': 278, 'name': 'tape measure/ruler'}, {'id': 109, 'name': 'banana'}, {'id': 146, 'name': 'gun'}, {'id': 187, 'name': 'billiards'}, {'id': 11, 'name': 'picture/frame'}, {'id': 118, 'name': 'paper towel'}, {'id': 87, 'name': 'bus'}, {'id': 284, 'name': 'goldfish'}, {'id': 133, 'name': 'computer box'}, {'id': 21, 'name': 'potted plant'}, {'id': 216, 'name': 'ship'}, {'id': 356, 'name': 'ambulance'}, {'id': 99, 'name': 'dog'}, {'id': 286, 'name': 'medal'}, {'id': 298, 'name': 'butterfly'}, {'id': 308, 'name': 'hair dryer'}, {'id': 268, 'name': 'globe'}, {'id': 355, 'name': 'french horn'}, {'id': 275, 'name': 'board eraser'}, {'id': 94, 'name': 'tea pot'}, {'id': 106, 'name': 'telephone'}, {'id': 328, 'name': 'mop'}, {'id': 137, 'name': 'broccoli'}, {'id': 311, 'name': 'dolphin'}, {'id': 3, 'name': 'chair'}, {'id': 4, 'name': 'hat'}, {'id': 96, 'name': 'tripod'}, {'id': 51, 'name': 'traffic light'}, {'id': 208, 'name': 'hot dog'}, {'id': 90, 'name': 'pot/pan'}, {'id': 9, 'name': 'car'}, {'id': 30, 'name': 'dining table'}, {'id': 306, 'name': 'crosswalk sign'}, {'id': 121, 'name': 'tomato'}, {'id': 45, 'name': 'barrel/bucket'}, {'id': 161, 'name': 'washing machine'}, {'id': 337, 'name': 'polar bear'}, {'id': 49, 'name': 'tie'}, {'id': 350, 'name': 'monkey'}, {'id': 238, 'name': 'green beans'}, {'id': 203, 'name': 'cucumber'}, {'id': 163, 'name': 'cookies'}, {'id': 47, 'name': 'suv'}, {'id': 239, 'name': 'brush'}, {'id': 160, 'name': 'carrot'}, {'id': 165, 'name': 'tennis racket'}, {'id': 17, 'name': 'helmet'}, {'id': 66, 'name': 'sink'}, {'id': 36, 'name': 'stool'}, {'id': 23, 'name': 'flower'}, {'id': 157, 'name': 'radiator'}, {'id': 260, 'name': 'fishing rod'}, {'id': 147, 'name': 'Life saver'}, {'id': 338, 'name': 'lighter'}, {'id': 60, 'name': 'bread'}, {'id': 326, 'name': 'radish'}, {'id': 1, 'name': 'human'}, {'id': 93, 'name': 'traffic cone'}, {'id': 78, 'name': 'knife'}, {'id': 179, 'name': 'grapes'}, {'id': 79, 'name': 'cellphone'}, {'id': 274, 'name': 'trophy'}, {'id': 313, 'name': 'urinal'}, {'id': 8, 'name': 'cup'}, {'id': 185, 'name': 'paint brush'}, {'id': 105, 'name': 'mouse'}, {'id': 113, 'name': 'soccer'}, {'id': 164, 'name': 'cutting/chopping board'}, {'id': 221, 'name': 'wheelchair'}, {'id': 156, 'name': 'Accordion/keyboard/piano'}, {'id': 189, 'name': 'goose'}, {'id': 336, 'name': 'red cabbage'}, {'id': 16, 'name': 'plate'}, {'id': 254, 'name': 'saxophone'}, {'id': 77, 'name': 'laptop'}, {'id': 194, 'name': 'facial mask'}, {'id': 218, 'name': 'onion'}, {'id': 75, 'name': 'motorbike/motorcycle'}, {'id': 55, 'name': 'canned'}, {'id': 363, 'name': 'lobster'}, {'id': 135, 'name': 'toiletries'}, {'id': 242, 'name': 'earphone'}, {'id': 33, 'name': 'flag'}, {'id': 333, 'name': 'Bread/bun'}, {'id': 255, 'name': 'trumpet'}, {'id': 248, 'name': 'parking meter'}, {'id': 250, 'name': 'garlic'}, {'id': 143, 'name': 'skateboard'}, {'id': 198, 'name': 'pie'}, {'id': 332, 'name': 'barbell'}, {'id': 329, 'name': 'yak'}, {'id': 281, 'name': 'stapler'}, {'id': 130, 'name': 'tangerine'}, {'id': 151, 'name': 'zebra'}, {'id': 70, 'name': 'traffic sign'}, {'id': 6, 'name': 'bottle'}, {'id': 361, 'name': 'hotair balloon'}, {'id': 129, 'name': 'sailboat'}, {'id': 325, 'name': 'llama'}, {'id': 101, 'name': 'blackboard/whiteboard'}, {'id': 175, 'name': 'coffee machine'}, {'id': 319, 'name': 'flute'}, {'id': 345, 'name': 'pencil case'}, {'id': 219, 'name': 'ice cream'}, {'id': 65, 'name': 'combine with bowl'}, {'id': 132, 'name': 'kite'}, {'id': 53, 'name': 'microphone'}, {'id': 86, 'name': 'fork'}, {'id': 358, 'name': 'hoverboard'}, {'id': 205, 'name': 'blender'}, {'id': 167, 'name': 'skating and skiing shoes'}, {'id': 89, 'name': 'nightstand'}, {'id': 287, 'name': 'toothpaste'}, {'id': 323, 'name': 'poker card'}, {'id': 98, 'name': 'fan'}, {'id': 108, 'name': 'orange'}, {'id': 196, 'name': 'chopsticks'}, {'id': 302, 'name': 'pig'}, {'id': 176, 'name': 'bathtub'}, {'id': 20, 'name': 'glove'}, {'id': 202, 'name': 'golf club'}, {'id': 119, 'name': 'refrigerator'}, {'id': 290, 'name': 'rickshaw'}, {'id': 72, 'name': 'candle'}, {'id': 57, 'name': 'mirror'}, {'id': 142, 'name': 'microwave'}, {'id': 158, 'name': 'converter'}, {'id': 110, 'name': 'airplane'}, {'id': 149, 'name': 'lemon'}, {'id': 125, 'name': 'head phone'}, {'id': 235, 'name': 'tricycle'}, {'id': 259, 'name': 'bear'}, {'id': 37, 'name': 'backpack'}, {'id': 69, 'name': 'apple'}, {'id': 114, 'name': 'trolley'}, {'id': 206, 'name': 'tong'}, {'id': 307, 'name': 'papaya'}, {'id': 233, 'name': 'cello'}, {'id': 282, 'name': 'camel'}, {'id': 324, 'name': 'binoculars'}, {'id': 226, 'name': 'cabbage'}, {'id': 31, 'name': 'umbrella'}, {'id': 241, 'name': 'cigar'}, {'id': 301, 'name': 'pomelo'}, {'id': 7, 'name': 'cabinet/shelf'}, {'id': 95, 'name': 'keyboard'}, {'id': 67, 'name': 'horse'}, {'id': 152, 'name': 'duck'}, {'id': 117, 'name': 'combine with glove'}, {'id': 229, 'name': 'pine apple'}, {'id': 184, 'name': 'potato'}, {'id': 103, 'name': 'air conditioner'}, {'id': 270, 'name': 'pliers'}, {'id': 231, 'name': 'fire truck'}, {'id': 97, 'name': 'hockey stick'}, {'id': 134, 'name': 'elephant'}, {'id': 153, 'name': 'sports car'}, {'id': 48, 'name': 'toy'}, {'id': 339, 'name': 'mangosteen'}, {'id': 353, 'name': 'rabbit'}, {'id': 59, 'name': 'bicycle'}, {'id': 154, 'name': 'giraffe'}, {'id': 267, 'name': 'screwdriver'}, {'id': 100, 'name': 'spoon'}, {'id': 91, 'name': 'sheep'}, {'id': 266, 'name': 'key'}, {'id': 28, 'name': 'wine glass'}, {'id': 297, 'name': 'treadmill'}, {'id': 193, 'name': 'extension cord'}, {'id': 289, 'name': 'shrimp'}, {'id': 62, 'name': 'ring'}, {'id': 32, 'name': 'boat'}, {'id': 263, 'name': 'green vegetables'}, {'id': 46, 'name': 'coffee table'}, {'id': 343, 'name': 'pitaya'}, {'id': 321, 'name': 'shark'}, {'id': 41, 'name': 'basket'}, {'id': 76, 'name': 'wild bird'}, {'id': 240, 'name': 'carriage'}, {'id': 207, 'name': 'slide'}, {'id': 68, 'name': 'fish'}, {'id': 199, 'name': 'frisbee'}, {'id': 271, 'name': 'hammer'}, {'id': 186, 'name': 'printer'}, {'id': 222, 'name': 'plum'}, {'id': 42, 'name': 'towel/napkin'}, {'id': 71, 'name': 'camera'}, {'id': 34, 'name': 'speaker'}, {'id': 107, 'name': 'pickup truck'}, {'id': 61, 'name': 'high heels'}, {'id': 172, 'name': 'bow tie'}, {'id': 173, 'name': 'pigeon'}, {'id': 293, 'name': 'coconut'}, {'id': 122, 'name': 'machinery vehicle'}, {'id': 38, 'name': 'sofa'}, {'id': 50, 'name': 'bed'}, {'id': 195, 'name': 'tennis ball'}, {'id': 276, 'name': 'dates'}, {'id': 14, 'name': 'street lights'}, {'id': 80, 'name': 'paddle'}, {'id': 296, 'name': 'calculator'}, {'id': 349, 'name': 'starfish'}, {'id': 310, 'name': 'chips'}, {'id': 120, 'name': 'train'}, {'id': 258, 'name': 'kiwi fruit'}, {'id': 39, 'name': 'belt'}, {'id': 24, 'name': 'monitor'}, {'id': 112, 'name': 'skis'}, {'id': 18, 'name': 'leather shoes'}, {'id': 256, 'name': 'sandwich'}, {'id': 197, 'name': 'Electronic stove and gas stove'}, {'id': 243, 'name': 'penguin'}, {'id': 145, 'name': 'surveillance camera'}, {'id': 257, 'name': 'cue'}, {'id': 344, 'name': 'scallop'}, {'id': 309, 'name': 'green onion'}, {'id': 340, 'name': 'seal'}, {'id': 230, 'name': 'crane'}, {'id': 314, 'name': 'donkey'}, {'id': 52, 'name': 'pen/pencil'}, {'id': 127, 'name': 'donut'}, {'id': 19, 'name': 'pillow'}, {'id': 35, 'name': 'trash bin/can'}]
    # [{'supercategory': 'person', 'id': 1, 'name': 'person'},
    # {'supercategory': 'vehicle', 'id': 2, 'name': 'bicycle'},
    # {'supercategory': 'vehicle', 'id': 3, 'name': 'car'},
    # {'supercategory': 'vehicle', 'id': 4, 'name': 'motorcycle'},
    # {'supercategory': 'vehicle', 'id': 5, 'name': 'airplane'}, {'supercategory': 'vehicle', 'id': 6, 'name': 'bus'},
    # {'supercategory': 'vehicle', 'id': 7, 'name': 'train'}, {'supercategory': 'vehicle', 'id': 8, 'name': 'truck'}, {'supercategory': 'vehicle', 'id': 9, 'name': 'boat'}, {'supercategory': 'outdoor', 'id': 10, 'name': 'traffic light'}, {'supercategory': 'outdoor', 'id': 11, 'name': 'fire hydrant'}, {'supercategory': 'outdoor', 'id': 13, 'name': 'stop sign'}, {'supercategory': 'outdoor', 'id': 14, 'name': 'parking meter'}, {'supercategory': 'outdoor', 'id': 15, 'name': 'bench'}, {'supercategory': 'animal', 'id': 16, 'name': 'bird'}, {'supercategory': 'animal', 'id': 17, 'name': 'cat'}, {'supercategory': 'animal', 'id': 18, 'name': 'dog'}, {'supercategory': 'animal', 'id': 19, 'name': 'horse'}, {'supercategory': 'animal', 'id': 20, 'name': 'sheep'}, {'supercategory': 'animal', 'id': 21, 'name': 'cow'}, {'supercategory': 'animal', 'id': 22, 'name': 'elephant'}, {'supercategory': 'animal', 'id': 23, 'name': 'bear'}, {'supercategory': 'animal', 'id': 24, 'name': 'zebra'}, {'supercategory': 'animal', 'id': 25, 'name': 'giraffe'}, {'supercategory': 'accessory', 'id': 27, 'name': 'backpack'}, {'supercategory': 'accessory', 'id': 28, 'name': 'umbrella'}, {'supercategory': 'accessory', 'id': 31, 'name': 'handbag'}, {'supercategory': 'accessory', 'id': 32, 'name': 'tie'}, {'supercategory': 'accessory', 'id': 33, 'name': 'suitcase'}, {'supercategory': 'sports', 'id': 34, 'name': 'frisbee'}, {'supercategory': 'sports', 'id': 35, 'name': 'skis'}, {'supercategory': 'sports', 'id': 36, 'name': 'snowboard'}, {'supercategory': 'sports', 'id': 37, 'name': 'sports ball'}, {'supercategory': 'sports', 'id': 38, 'name': 'kite'}, {'supercategory': 'sports', 'id': 39, 'name': 'baseball bat'}, {'supercategory': 'sports', 'id': 40, 'name': 'baseball glove'}, {'supercategory': 'sports', 'id': 41, 'name': 'skateboard'}, {'supercategory': 'sports', 'id': 42, 'name': 'surfboard'}, {'supercategory': 'sports', 'id': 43, 'name': 'tennis racket'}, {'supercategory': 'kitchen', 'id': 44, 'name': 'bottle'}, {'supercategory': 'kitchen', 'id': 46, 'name': 'wine glass'}, {'supercategory': 'kitchen', 'id': 47, 'name': 'cup'}, {'supercategory': 'kitchen', 'id': 48, 'name': 'fork'}, {'supercategory': 'kitchen', 'id': 49, 'name': 'knife'}, {'supercategory': 'kitchen', 'id': 50, 'name': 'spoon'}, {'supercategory': 'kitchen', 'id': 51, 'name': 'bowl'}, {'supercategory': 'food', 'id': 52, 'name': 'banana'}, {'supercategory': 'food', 'id': 53, 'name': 'apple'}, {'supercategory': 'food', 'id': 54, 'name': 'sandwich'}, {'supercategory': 'food', 'id': 55, 'name': 'orange'}, {'supercategory': 'food', 'id': 56, 'name': 'broccoli'}, {'supercategory': 'food', 'id': 57, 'name': 'carrot'}, {'supercategory': 'food', 'id': 58, 'name': 'hot dog'}, {'supercategory': 'food', 'id': 59, 'name': 'pizza'}, {'supercategory': 'food', 'id': 60, 'name': 'donut'}, {'supercategory': 'food', 'id': 61, 'name': 'cake'}, {'supercategory': 'furniture', 'id': 62, 'name': 'chair'}, {'supercategory': 'furniture', 'id': 63, 'name': 'couch'}, {'supercategory': 'furniture', 'id': 64, 'name': 'potted plant'}, {'supercategory': 'furniture', 'id': 65, 'name': 'bed'}, {'supercategory': 'furniture', 'id': 67, 'name': 'dining table'}, {'supercategory': 'furniture', 'id': 70, 'name': 'toilet'}, {'supercategory': 'electronic', 'id': 72, 'name': 'tv'}, {'supercategory': 'electronic', 'id': 73, 'name': 'laptop'}, {'supercategory': 'electronic', 'id': 74, 'name': 'mouse'}, {'supercategory': 'electronic', 'id': 75, 'name': 'remote'}, {'supercategory': 'electronic', 'id': 76, 'name': 'keyboard'}, {'supercategory': 'electronic', 'id': 77, 'name': 'cell phone'}, {'supercategory': 'appliance', 'id': 78, 'name': 'microwave'}, {'supercategory': 'appliance', 'id': 79, 'name': 'oven'}, {'supercategory': 'appliance', 'id': 80, 'name': 'toaster'}, {'supercategory': 'appliance', 'id': 81, 'name': 'sink'}, {'supercategory': 'appliance', 'id': 82, 'name': 'refrigerator'}, {'supercategory': 'indoor', 'id': 84, 'name': 'book'}, {'supercategory': 'indoor', 'id': 85, 'name': 'clock'}, {'supercategory': 'indoor', 'id': 86, 'name': 'vase'}, {'supercategory': 'indoor', 'id': 87, 'name': 'scissors'}, {'supercategory': 'indoor', 'id': 88, 'name': 'teddy bear'}, {'supercategory': 'indoor', 'id': 89, 'name': 'hair drier'}, {'supercategory': 'indoor', 'id': 90, 'name': 'toothbrush'}]
    # coco is sequence (0-79)

    coco_id_map_90_2_80 = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 10, 13: 11, 14: 12, 15: 13,
                           16: 14, 17: 15, 18: 16, 19: 17, 20: 18, 21: 19, 22: 20, 23: 21, 24: 22, 25: 23, 27:
                               24, 28: 25, 31: 26, 32: 27, 33: 28, 34: 29, 35: 30, 36: 31, 37: 32, 38: 33, 39: 34,
                           40: 35, 41: 36, 42: 37, 43: 38, 44: 39, 46: 40, 47: 41, 48: 42, 49: 43, 50: 44, 51: 45,
                           52: 46
        , 53: 47, 54: 48, 55: 49, 56: 50, 57: 51, 58: 52, 59: 53, 60: 54, 61: 55, 62: 56, 63: 57, 64: 58, 65: 59,
                           67: 60, 70: 61, 72: 62, 73: 63, 74: 64, 75: 65, 76: 66, 77: 67, 78: 68,
                           79: 69, 80: 70, 81: 71, 82: 72, 84: 73, 85: 74, 86: 75, 87: 76, 88: 77, 89: 78, 90: 79}

    fobj = open(DATA_DIR + '/Data/hico_list_obj.txt')
    fhoi = open(DATA_DIR + '/Data/hico_list_hoi.txt')
    fvb = open(DATA_DIR + '/Data/hico_list_vb.txt')
    id_obj = {}
    hoi_to_obj = {}
    hoi_to_verbs = {}
    obj_id = {}
    id_hoi = {}
    vb_id = {}
    obj_to_hoi = {}
    id_vb = {}
    coco_to_hico_obj = {}
    coco80_to_hico_obj = {}
    hico_to_coco_obj = {}
    for line in fobj.readlines()[2:]:
        line = line.strip()
        # print(line.split(' '), [item for item in line.split(' ') if item != ''])

        cid, obj = [item for item in line.split(' ') if item != '']
        obj_id[obj] = int(cid) - 1
        id_obj[int(cid) - 1] = obj
        coco_obj = obj.replace('_', ' ')
        coco_to_hico_obj[coco_annos_map[coco_obj]] = int(cid) - 1
        coco80_to_hico_obj[coco_id_map_90_2_80[coco_annos_map[coco_obj]] + 1] = int(cid) - 1
        hico_to_coco_obj[int(cid) - 1] = coco_id_map_90_2_80[coco_annos_map[coco_obj]]
        # print(coco_annos_map[coco_obj], obj, cid)

    for line in fvb.readlines()[2:]:
        line = line.strip()
        # print(line.split(' '), [item for item in line.split(' ') if item != ''])

        cid, vb = [item for item in line.split(' ') if item != '']
        vb_id[vb] = int(cid) - 1
        id_vb[int(cid) - 1] = vb

    for line in fhoi.readlines()[2:]:
        line = line.strip()
        # print(line.split(' '), [item for item in line.split(' ') if item != ''])

        cid, obj, vb = [item for item in line.split(' ') if item != '']
        hoi_to_obj[int(cid) - 1] = obj_id[obj]
        id_hoi[int(cid) - 1] = obj + ' ' + vb
        hoi_to_verbs[int(cid) - 1] = vb_id[vb]
        if obj_id[obj] in obj_to_hoi:
            obj_to_hoi[obj_id[obj]].append(int(cid) - 1)
        else:
            obj_to_hoi[obj_id[obj]] = [int(cid) - 1]
    return hoi_to_obj, hoi_to_verbs, obj_to_hoi, coco_to_hico_obj, coco80_to_hico_obj, hico_to_coco_obj, id_vb, id_obj, id_hoi