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

python3 main.py --use-expert --evaluation --env-id Hopper-v1 --log-dir expert

# not working: humanoidstandup ant