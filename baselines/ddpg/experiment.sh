# python3 main.py --save-networks --evaluation --env-id HalfCheetah-v1 --log-dir baseline
# python3 main.py --perform --env-id HalfCheetah-v1 --log-dir perform
# python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --log-dir expert

# python3 main.py --save-networks --evaluation --env-id InvertedPendulum-v1 --log-dir baseline
# python3 main.py --perform --env-id InvertedPendulum-v1 --log-dir perform
# python3 main.py --use-expert --evaluation --env-id InvertedPendulum-v1 --log-dir expert

# python3 main.py --save-networks --evaluation --env-id Reacher-v1 --log-dir baseline
# python3 main.py --perform --env-id Reacher-v1 --log-dir perform
# python3 main.py --use-expert --evaluation --env-id Reacher-v1 --log-dir expert

# python3 main.py --save-networks --evaluation --env-id Hopper-v1 --log-dir baseline
# python3 main.py --perform --env-id Hopper-v1 --log-dir perform
# python3 main.py --use-expert --evaluation --env-id Hopper-v1 --log-dir expert

# python3 main.py --save-networks --evaluation --env-id HumanoidStandup-v1 --log-dir baseline
# python3 main.py --save-networks --evaluation --env-id HumanoidStandup-v1 --log-dir baseline
# python3 main.py --save-networks --evaluation --env-id HumanoidStandup-v1 --log-dir baseline
# python3 main.py --save-networks --evaluation --env-id HumanoidStandup-v1 --log-dir baseline
# python3 main.py --perform --env-id HumanoidStandup-v1 --log-dir perform
# mv ./saved_networks/* ./data/humanoid/saved_networks/
# python3 main.py --save-networks --use-expert --evaluation --env-id HumanoidStandup-v1 --log-dir expert
# python3 main.py --save-networks --use-expert --evaluation --env-id HumanoidStandup-v1 --log-dir expert
# python3 main.py --save-networks --use-expert --evaluation --env-id HumanoidStandup-v1 --log-dir expert
# python3 main.py --save-networks --use-expert --evaluation --env-id HumanoidStandup-v1 --log-dir expert

# python3 main.py --save-networks --evaluation --env-id Walker2d-v1 --log-dir baseline
# python3 main.py --perform --env-id Walker2d-v1 --log-dir perform
# mkdir ./data/Walker2d-v1/
# mkdir ./data/Walker2d-v1/saved_networks/
# mv ./saved_networks/* ./data/Walker2d-v1/saved_networks/
# python3 main.py --use-expert --evaluation --env-id Walker2d-v1 --log-dir expert

# python3 main.py --use-expert --evaluation --supervise --env-id HalfCheetah-v1 --log-dir supervise
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --pre-epoch 10 --log-dir 10epoch
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --pre-epoch 20 --log-dir 20epoch
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --pre-epoch 30 --log-dir 30epoch
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --pre-epoch 40 --log-dir 40epoch
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --pre-epoch 50 --log-dir 50epoch
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --pre-epoch 60 --log-dir 60epoch
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --pre-epoch 70 --log-dir 70epoch
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --pre-epoch 80 --log-dir 80epoch
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --pre-epoch 90 --log-dir 90epoch
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --pre-epoch 100 --log-dir 100epoch
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --pre-epoch 110 --log-dir 110epoch
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --pre-epoch 120 --log-dir 120epoch

# not working: humanoidstandup ant
