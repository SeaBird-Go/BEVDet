
config="configs/bevdet_occ/bevdet-occ-r50-4d-stereo-24e.py"

checkpoint="work_dirs/pretrained_models/bevdet-occ-r50-4d-stereo-24e.pth"

checkpoint="work_dirs/bevdet-occ-r50-4d-stereo-24e/latest.pth"

num_gpu=8
set -x
bash ./tools/dist_test.sh ${config} ${checkpoint} ${num_gpu} --eval mAP

## single gpu
# python tools/test.py $config $checkpoint --eval mAP --gpu-id 7