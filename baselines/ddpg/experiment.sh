python3 main.py --save-networks --evaluation --env-id HalfCheetah-v1 --log-dir baseline
python3 main.py --perform --env-id HalfCheetah-v1 --log-dir perform
python3 main.py --use-expert --evaluation --env-id HalfCheetah-v1 --log-dir expert

python3 main.py --save-networks --evaluation --env-id InvertedPendulum-v1 --log-dir baseline
python3 main.py --perform --env-id InvertedPendulum-v1 --log-dir perform
python3 main.py --use-expert --evaluation --env-id InvertedPendulum-v1 --log-dir expert

python3 main.py --save-networks --evaluation --env-id Reacher-v1 --log-dir baseline
python3 main.py --perform --env-id Reacher-v1 --log-dir perform
python3 main.py --use-expert --evaluation --env-id Reacher-v1 --log-dir expert

python3 main.py --save-networks --evaluation --env-id Hopper-v1 --log-dir baseline
python3 main.py --perform --env-id Hopper-v1 --log-dir perform
python3 main.py --use-expert --evaluation --env-id Hopper-v1 --log-dir expert

python3 main.py --save-networks --evaluation --env-id HumanoidStandup-v1 --log-dir baseline
python3 main.py --perform --env-id HumanoidStandup-v1 --log-dir perform
python3 main.py --use-expert --evaluation --env-id HumanoidStandup-v1 --log-dir expert