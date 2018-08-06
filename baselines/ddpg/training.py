import os
import time
from collections import deque
import pickle

from baselines.ddpg.ddpg import DDPG
from baselines.ddpg.util import mpi_mean, mpi_std, mpi_max, mpi_sum
import baselines.common.tf_util as U

from baselines import logger
import numpy as np
import tensorflow as tf
from mpi4py import MPI


def train(env, nb_epochs, nb_epoch_cycles, render_eval, reward_scale, render, param_noise, actor, critic,
    normalize_returns, normalize_observations, critic_l2_reg, actor_lr, critic_lr, action_noise,
    popart, gamma, clip_norm, nb_train_steps, nb_rollout_steps, nb_eval_steps, batch_size, memory,
    tau=0.01, eval_env=None, param_noise_adaption_interval=50, perform=False, expert=None, save_networks=False, supervise=False, pre_epoch=60, actor_only=False, critic_only=False):
    rank = MPI.COMM_WORLD.Get_rank()

    assert (np.abs(env.action_space.low) == env.action_space.high).all()  # we assume symmetric actions.
    max_action = env.action_space.high
    logger.info('scaling actions by {} before executing in env'.format(max_action))
    agent = DDPG(actor, critic, memory, env.observation_space.shape, env.action_space.shape,
        gamma=gamma, tau=tau, normalize_returns=normalize_returns, normalize_observations=normalize_observations,
        batch_size=batch_size, action_noise=action_noise, param_noise=param_noise, critic_l2_reg=critic_l2_reg,
        actor_lr=actor_lr, critic_lr=critic_lr, enable_popart=popart, clip_norm=clip_norm,
        reward_scale=reward_scale, expert=expert, save_networks=save_networks, supervise=supervise, actor_only=actor_only, critic_only=critic_only)
    logger.info('Using agent with the following configuration:')
    logger.info(str(agent.__dict__.items()))

    # Set up logging stuff only for a single worker.
    if rank == 0:
        saver = tf.train.Saver()
    else:
        saver = None

    step = 0
    episode = 0
    eval_episode_rewards_history = deque(maxlen=100)
    episode_rewards_history = deque(maxlen=100)
    with U.single_threaded_session() as sess:
        # Prepare everything.
        network_saving_dir = os.path.join('./saved_networks', env.env.spec.id)+'/'
        if not os.path.exists(network_saving_dir):
            os.makedirs(network_saving_dir)
        agent.initialize(sess, saver, network_saving_dir, 10000, 30000)
        sess.graph.finalize()

        agent.reset()
        obs = env.reset()
        if eval_env is not None:
            eval_obs = eval_env.reset()
        if expert is None:
            pretrain = False
        else:
            pretrain = True
        done = False
        episode_reward = 0.
        episode_step = 0
        episodes = 0
        t = 0

        epoch = 0
        start_time = time.time()

        epoch_episode_rewards = []
        epoch_episode_steps = []
        epoch_episode_eval_rewards = []
        epoch_episode_eval_steps = []
        epoch_start_time = time.time()
        epoch_actions = []
        epoch_qs = []
        epoch_episodes = 0
        small_buffer = []
        big_buffer = []
        for epoch in range(nb_epochs):
            for cycle in range(nb_epoch_cycles):
                if not perform:
                    # Perform rollouts.
                    for t_rollout in range(nb_rollout_steps):
                        # Predict next action.
                        action, q = agent.pi(obs, apply_noise=True, compute_Q=True)
                        assert action.shape == env.action_space.shape

                        # Execute next action.
                        if rank == 0 and render:
                            env.render()
                        assert max_action.shape == action.shape
                        new_obs, r, done, info = env.step(max_action * action)  # scale for execution in env (as far as DDPG is concerned, every action is in [-1, 1])

                        t += 1
                        if rank == 0 and render:
                            env.render()
                        episode_reward += r
                        episode_step += 1

                        # Book-keeping.
                        epoch_actions.append(action)
                        epoch_qs.append(q)
                        agent.store_transition(obs, action, r, new_obs, done)
                        obs = new_obs

                        if done:
                            # Episode done.
                            epoch_episode_rewards.append(episode_reward)
                            episode_rewards_history.append(episode_reward)
                            epoch_episode_steps.append(episode_step)
                            episode_reward = 0.
                            episode_step = 0
                            epoch_episodes += 1
                            episodes += 1

                            agent.reset()
                            obs = env.reset()

                    # Train.
                    epoch_actor_losses = []
                    epoch_critic_losses = []
                    epoch_dists = []
                    epoch_adaptive_distances = []
                    for t_train in range(nb_train_steps):
                        # Adapt param noise, if necessary.
                        if memory.nb_entries >= batch_size and t % param_noise_adaption_interval == 0:
                            distance = agent.adapt_param_noise()
                            epoch_adaptive_distances.append(distance)

                        cl, al, d = agent.train(pretrain)
                        epoch_critic_losses.append(cl)
                        epoch_actor_losses.append(al)
                        epoch_dists.append(d)
                        agent.update_target_net()

                # Evaluate.
                eval_episode_rewards = []
                eval_qs = []
                if eval_env is not None:
                    eval_episode_reward = 0.
                    for t_rollout in range(nb_eval_steps):
                        old_eval_obs = eval_obs
                        eval_action, eval_q = agent.pi(eval_obs, apply_noise=False, compute_Q=True)
                        eval_obs, eval_r, eval_done, eval_info = eval_env.step(max_action * eval_action)  # scale for execution in env (as far as DDPG is concerned, every action is in [-1, 1])

                        if perform:
                            small_buffer.append([old_eval_obs, eval_action, eval_r, eval_obs, eval_done])

                        if render_eval:
                            eval_env.render()
                        eval_episode_reward += eval_r

                        eval_qs.append(eval_q)
                        if eval_done:
                            eval_obs = eval_env.reset()
                            eval_episode_rewards.append(eval_episode_reward)
                            eval_episode_rewards_history.append(eval_episode_reward)
                            eval_episode_reward = 0.

                            if perform and len(small_buffer) > 0:
                                big_buffer.append(small_buffer)
                                small_buffer = []
                                if len(big_buffer) > 0 and len(big_buffer) % 1000 == 0:
                                    expert_dir = os.path.join('./expert', env.env.spec.id) + '/'
                                    if not os.path.exists(expert_dir):
                                        os.makedirs(expert_dir)
                                    pwritefile = open(os.path.join(expert_dir, 'expert.pkl'), 'wb')
                                    pickle.dump(big_buffer, pwritefile, -1)
                                    pwritefile.close()
                                    logger.info('Expert data saved!')
                                    return

            # Log stats.
            epoch_train_duration = time.time() - epoch_start_time
            duration = time.time() - start_time
            combined_stats = {}
            if not perform:
                stats = agent.get_stats()
                for key in sorted(stats.keys()):
                    combined_stats[key] = mpi_mean(stats[key])

            # Rollout statistics.
            if not perform:
                epoch_ave_dist = mpi_mean(epoch_dists)
                # if epoch_ave_dist < 0.01 and pretrain:
                if epoch >= pre_epoch and pretrain:
                    pretrain = False
                    logger.info('Stoped pretrain at epoch {}'.format(epoch))

                combined_stats['rollout/return'] = mpi_mean(epoch_episode_rewards)
                combined_stats['rollout/return_history'] = mpi_mean(np.mean(episode_rewards_history))
                combined_stats['rollout/episode_steps'] = mpi_mean(epoch_episode_steps)
                combined_stats['rollout/episodes'] = mpi_sum(epoch_episodes)
                combined_stats['rollout/actions_mean'] = mpi_mean(epoch_actions)
                combined_stats['rollout/actions_std'] = mpi_std(epoch_actions)
                combined_stats['rollout/Q_mean'] = mpi_mean(epoch_qs)

                # Train statistics.
                combined_stats['train/loss_actor'] = mpi_mean(epoch_actor_losses)
                combined_stats['train/loss_critic'] = mpi_mean(epoch_critic_losses)
                combined_stats['train/dist'] = epoch_ave_dist
                combined_stats['train/param_noise_distance'] = mpi_mean(epoch_adaptive_distances)

            # Evaluation statistics.
            if eval_env is not None:
                combined_stats['eval/return'] = mpi_mean(eval_episode_rewards)
                combined_stats['eval/return_history'] = mpi_mean(np.mean(eval_episode_rewards_history))
                combined_stats['eval/Q'] = mpi_mean(eval_qs)
                combined_stats['eval/episodes'] = mpi_mean(len(eval_episode_rewards))
            if not perform:
                # Total statistics.
                combined_stats['total/duration'] = mpi_mean(duration)
                combined_stats['total/steps_per_second'] = mpi_mean(float(t) / float(duration))
                combined_stats['total/episodes'] = mpi_mean(episodes)
                combined_stats['total/epochs'] = epoch + 1
                combined_stats['total/steps'] = t

            for key in sorted(combined_stats.keys()):
                logger.record_tabular(key, combined_stats[key])
            logger.dump_tabular()
            logger.info('')
            logdir = logger.get_dir()
            if rank == 0 and logdir:
                if hasattr(env, 'get_state'):
                    with open(os.path.join(logdir, 'env_state.pkl'), 'wb') as f:
                        pickle.dump(env.get_state(), f)
                if eval_env and hasattr(eval_env, 'get_state'):
                    with open(os.path.join(logdir, 'eval_env_state.pkl'), 'wb') as f:
                        pickle.dump(eval_env.get_state(), f)
