import pickle
import tensorflow as tf
import numpy as np
from baselines.ddpg.memory import Memory
from baselines.ddpg.ddpg import normalize, denormalize
from baselines.ddpg.models import Discriminator


class Expert:
    def __init__(self, limit, env):
        self.limit = limit
        self.env = env
        self.memory = Memory(limit=self.limit,
                             action_shape=self.env.action_space.shape,
                             observation_shape=self.env.observation_space.shape)
        self.file_dir = None

    def load_file(self, file_dir):
        self.file_dir = file_dir
        expert_file = open(self.file_dir, 'rb')
        expert_data = pickle.load(expert_file)
        expert_file.close()
        k = 0
        for episode_sample in expert_data:
            for step_sample in episode_sample:
                k = k+1
                if k <= self.limit:
                    self.memory.append(step_sample[0], step_sample[1], step_sample[2], step_sample[3], step_sample[4])
                else:
                    return

    def load_file_trpo(self, file_dir):
        self.file_dir = file_dir
        traj_data = np.load(file_dir)
        if self.limit is None:
            obs = traj_data["obs"][:]
            acs = traj_data["acs"][:]
        else:
            obs = traj_data["obs"][:self.limit]
            acs = traj_data["acs"][:self.limit]
        episode_num = len(acs)
        '''
        step_num = 0
        for i in range(episode_num):
            step_num += len(acs[i])
        print("Total Step is:", step_num, "\nTotal_Episode is:", episode_num)
        '''
        for i in range(episode_num):
            episode_len = len(acs[i])
            for j in range(episode_len):
                done = True if (j == episode_len - 1) else False
                self.memory.append(obs[i][j], acs[i][j], 0., 0., done)

    def sample(self, batch_size):
        return self.memory.sample(batch_size)

    def set_tf(self, actor, critic, obs0, actions, obs_rms, ret_rms, observation_range, return_range, supervise=False, critic_only=False,
               actor_only=False, both_ours_sup = False, gail = False, pofd = False):
        self.expert_state = tf.placeholder(tf.float32, shape=(None,) + self.env.observation_space.shape,
                                           name='expert_state')
        self.expert_action = tf.placeholder(tf.float32, shape=(None,) + self.env.action_space.shape,
                                            name='expert_action')
        normalized_state = tf.clip_by_value(normalize(self.expert_state, obs_rms),
                                            observation_range[0], observation_range[1])
        expert_actor = actor(normalized_state, reuse=True)
        normalized_q_with_expert_data = critic(normalized_state, self.expert_action, reuse=True)
        normalized_q_with_expert_actor = critic(normalized_state, expert_actor, reuse=True)
        self.Q_with_expert_data = denormalize(
            tf.clip_by_value(normalized_q_with_expert_data, return_range[0], return_range[1]), ret_rms)
        self.Q_with_expert_actor = denormalize(
            tf.clip_by_value(normalized_q_with_expert_actor, return_range[0], return_range[1]), ret_rms)
        if supervise:
            self.actor_loss = tf.nn.l2_loss(self.expert_action-expert_actor)
            self.critic_loss = 0
        else:
            self.critic_loss = tf.reduce_mean(tf.nn.relu(self.Q_with_expert_actor - self.Q_with_expert_data))
            self.actor_loss = -tf.reduce_mean(self.Q_with_expert_actor)
            if critic_only:
                self.actor_loss = 0
            if actor_only:
                self.critic_loss = 0
        #self.dist = tf.reduce_mean(self.Q_with_expert_data - self.Q_with_expert_actor)
        if both_ours_sup:
            self.actor_loss = tf.nn.l2_loss(self.expert_action-expert_actor) - tf.reduce_mean(self.Q_with_expert_actor)
            self.critic_loss = tf.reduce_mean(tf.nn.relu(self.Q_with_expert_actor - self.Q_with_expert_data))
            
        if gail or pofd:
            discriminator = Discriminator()
            d_with_expert_data = discriminator(normalized_state, self.expert_action)
            d_with_gen_data = discriminator(obs0, actions, reuse=True)
            self.discriminator_loss = tf.reduce_mean(tf.log(d_with_gen_data))+tf.reduce_mean(tf.log(1-d_with_expert_data))
            self.actor_loss = tf.reduce_mean(tf.log(d_with_gen_data))
