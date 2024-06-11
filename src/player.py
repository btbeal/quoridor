from collections import deque
import numpy as np
import pygame
import torch
import torch.nn as nn
from src.dqn import DQN, ExperienceReplay


class Player(pygame.sprite.Sprite):

    def __init__(self, index, name, position, color, radius, total_walls=10, is_ai=False):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.index = index
        self.matrix_representation = (index + 1) * 10
        self.name = name
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=position)
        self.initial_position = position
        self.position = position
        self.total_walls = total_walls
        self.starting_walls = total_walls
        self.is_ai = is_ai

    def reset(self):
        self.rect.center = self.initial_position
        self.rect.center = self.initial_position
        self.total_walls = self.starting_walls

    def current_node(self, nodes):
        for node in nodes:
            if node.position == self.rect.center:
                return node

        return None

    def place_wall(self, board, coords):
        validated_wall = next(wall for wall in board.walls if wall.rect.center == coords)
        adjacent_wall = board.get_adjacent_wall(validated_wall)
        proposed_new_wall = pygame.Rect.union(validated_wall.rect, adjacent_wall.rect)
        validated_wall.is_occupied = True
        validated_wall.image = validated_wall.hover_image
        validated_wall.union_walls(adjacent_wall, proposed_new_wall)
        adjacent_wall.kill()
        self.total_walls -= 1

    def move_player(self, board, coords):
        nodes = board.nodes
        new_node = next(node for node in nodes if node.rect.center == coords)
        current_node = self.current_node(nodes)
        current_node.is_occupied = False
        new_node.is_occupied = True
        self.rect.center = new_node.rect.center


class AIPlayer(Player):

    def __init__(
            self,
            index,
            name,
            position,
            color,
            radius,
            gamma=0.75,
            epsilon_greedy=1.0,
            epsilon_min=0.15,
            epsilon_decay=0.995,
            learning_rate=1e-3,
            max_memory_size=2000,
            update_target_every=50,
            policy_model=None,
            target_model=None
    ):
        self.max_memory_size = max_memory_size
        self.memory = ExperienceReplay(max_memory_capacity=max_memory_size)
        self.gamma = gamma
        self.epsilon = epsilon_greedy
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.lr = learning_rate
        self.model_store_path = None
        self.policy_model = policy_model
        self.target_model = target_model
        self.loss_fn = nn.MSELoss()
        self.optimizer = None
        self.update_target_every = update_target_every
        super(AIPlayer, self).__init__(index, name, position, color, radius, is_ai=True)

    def choose_action(self, action_space, state, legal_moves):
        ineligible_indices = []
        eligible_indices = []
        for i, action_item in enumerate(action_space):
            if action_item in legal_moves:
                eligible_indices.append(i)
            else:
                ineligible_indices.append(i)

        if np.random.rand() <= self.epsilon:
            return np.random.choice(eligible_indices)
        with torch.no_grad():
            q_values = self.policy_model(torch.tensor(state, dtype=torch.float32).unsqueeze(0))[0]
            q_values[ineligible_indices] = float('-inf')

        return torch.argmax(q_values).item()

    def learn(self, batch_samples):
        batch_states, batch_targets = [], []
        for transition in batch_samples:
            s, a, next_s, r, done = transition
            with torch.no_grad():
                if done:
                    target = r
                else:
                    pred = self.target_model(torch.tensor(np.array(next_s), dtype=torch.float32).unsqueeze(0))[0]
                    target = r + self.gamma * pred.max()
                target_all = self.policy_model(torch.tensor(np.array(s), dtype=torch.float32).unsqueeze(0))[0]
            target_all[a] = target
            batch_states.append(s.flatten())
            batch_targets.append(target_all)

        self.optimizer.zero_grad()
        pred = self.policy_model(torch.tensor(np.array(batch_states), dtype=torch.float32))
        loss = self.loss_fn(pred, torch.stack(batch_targets))
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def update_target_network(self):
        self.target_model.load_state_dict(self.policy_model.state_dict())

    def adjust_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

