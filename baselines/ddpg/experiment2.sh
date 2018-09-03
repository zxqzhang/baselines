#python3 main.py --evaluation --env-id InvertedPendulum-v2 --log-dir baseline
#python3 main.py --evaluation --env-id Reacher-v2 --log-dir baseline

#python3 main.py --evaluation --env-id InvertedDoublePendulum-v2 --log-dir baseline

#python3 main.py --use-expert --evaluation --env-id InvertedPendulum-v2 --log-dir ppoexpert_new --expert-dir ~/Projects/conda/demonstrations/InvertedPendulum_ppo2/expert.pkl --nb-epochs 50 --pre-epoch 6
#python3 main.py --use-expert --evaluation --env-id InvertedDoublePendulum-v2 --log-dir ppoexpert_new --expert-dir ~/Projects/conda/demonstrations/InvertedDoublePendulum_ppo2/expert.pkl --nb-epochs 50 --pre-epoch 6

#python3 main.py --use-expert --evaluation --env-id InvertedPendulum-v2 --log-dir ppoexpert_sup_new --expert-dir ~/Projects/conda/demonstrations/InvertedPendulum_ppo2/expert.pkl --nb-epochs 50 --pre-epoch 6 --supervise
#python3 main.py --use-expert --evaluation --env-id InvertedDoublePendulum-v2 --log-dir ppoexpert_sup_new --expert-dir ~/Projects/conda/demonstrations/InvertedDoublePendulum_ppo2/expert.pkl --nb-epochs 50 --pre-epoch 6 --supervise


nohup python3 main.py --use-expert --evaluation --env-id Hopper-v2 --log-dir ppoexpert_sup_1_500pre_001 --expert-dir ~/Projects/conda/demonstrations/Hopper_ppo2/expert.pkl --pre-epoch 500 --supervise --seed 1 --actor-lr 0.00001 --critic-lr 0.0001 &
nohup python3 main.py --use-expert --evaluation --env-id Hopper-v2 --log-dir ppoexpert_sup_1_500pre_002 --expert-dir ~/Projects/conda/demonstrations/Hopper_ppo2/expert.pkl --pre-epoch 500 --supervise --seed 2 --actor-lr 0.00001 --critic-lr 0.0001 &
nohup python3 main.py --use-expert --evaluation --env-id Hopper-v2 --log-dir ppoexpert_sup_1_500pre_003 --expert-dir ~/Projects/conda/demonstrations/Hopper_ppo2/expert.pkl --pre-epoch 500 --supervise --seed 3 --actor-lr 0.00001 --critic-lr 0.0001 &
nohup python3 main.py --use-expert --evaluation --env-id Hopper-v2 --log-dir ppoexpert_sup_1_500pre_004 --expert-dir ~/Projects/conda/demonstrations/Hopper_ppo2/expert.pkl --pre-epoch 500 --supervise --seed 4 --actor-lr 0.00001 --critic-lr 0.0001 &
python3 main.py --use-expert --evaluation --env-id Hopper-v2 --log-dir ppoexpert_sup_1_500pre_005 --expert-dir ~/Projects/conda/demonstrations/Hopper_ppo2/expert.pkl --pre-epoch 500 --supervise --seed 5 --actor-lr 0.00001 --critic-lr 0.0001