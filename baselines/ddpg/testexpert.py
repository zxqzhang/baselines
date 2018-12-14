from baselines.ddpg.expert import Expert
import gym
from baselines import logger, bench
env = gym.make('Humanoid-v2')
env = bench.Monitor(env, logger.get_dir() and os.path.join(logger.get_dir(), str(1)))
expert_dir = '/home/zhangxiaoqin/Projects/conda/demonstrations/Humanoid_ppo2_1m/expert.pkl'
expert = Expert(limit=int(1e6), env=env)
expert.load_file(expert_dir,True)