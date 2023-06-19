'''
Copyright (c) 2023 by Haiming Zhang. All Rights Reserved.

Author: Haiming Zhang
Date: 2023-06-19 14:45:00
Email: haimingzhang@link.cuhk.edu.cn
Description: Convert the checkpoint information from the original checkpoint to the new checkpoint.
'''

import torch
from copy import deepcopy
from collections import OrderedDict


def modify_state_dict(state_dict1, state_dict2):
    ## append the teacher model string to the pre-trained checkpoint dict
    new_state_dict2 = deepcopy(state_dict2)
    for key in list(state_dict2.keys()):
        new_key = "teacher_model." + key
        new_state_dict2[new_key] = new_state_dict2.pop(key)

    ## modify the state_dict1
    keys = ['teacher_model.final_conv.conv.weight',
            'teacher_model.final_conv.conv.bias']
    for key in keys:
        state_dict1[key] = new_state_dict2[key]


def append_prefix(state_dict, prefix="teacher_model."):
    if not prefix.endswith('.'):
        prefix += '.'  # append '.' to the end of prefix if not exist
    
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = prefix + k
        new_state_dict[name] = v
    return new_state_dict


if __name__ == "__main__":
    torch.cuda.empty_cache()

    filename = "work_dirs/bevdet-lidar-occ-voxel-multi-sweeps-24e/epoch_24_ema.pth"
    checkpoint = torch.load(filename, map_location="cpu")
    print(checkpoint.keys())

    new_state_dict = append_prefix(checkpoint['state_dict'])
    checkpoint['state_dict'] = new_state_dict
    torch.save(checkpoint, "bevdet-lidar-occ-voxel-multi-sweeps-24e_teacher_model.pth")
