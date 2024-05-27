from collections import deque
import numpy as np
import pygame
import torch
import torch.nn as nn


class Player(pygame.sprite.Sprite):
    total_walls = 10

    def __init__(self, index, name, position, color, radius, is_ai=False):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.index = index
        self.matrix_representation = (index + 1) * 10
        self.name = name
        self.radius = radius
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=position)
        self.position = position
        self.is_ai = is_ai

    def current_node(self, nodes):
        for node in nodes:
            if node.position == self.rect.center:
                return node

        return None

    def place_wall(self, board, validated_wall):
        adjacent_wall = board.get_adjacent_wall(validated_wall)
        proposed_new_wall = pygame.Rect.union(validated_wall.rect, adjacent_wall.rect)
        validated_wall.is_occupied = True
        validated_wall.image = validated_wall.hover_image
        validated_wall.union_walls(adjacent_wall, proposed_new_wall)
        adjacent_wall.kill()
        self.total_walls -= 1

    def move_player(self, new_node, all_nodes):
        current_node = self.current_node(all_nodes)
        current_node.is_occupied = False
        new_node.is_occupied = True
        self.rect.center = new_node.rect.center


class AIPlayer(Player):

    def __init__(
        self, env, discount_factor=0.95,
        epsilon_greedy=1.0, epsilon_min=0.01,
        epsilon_decay=0.995, learning_rate=1e-3,
        max_memory_size=2000
    ):
        self.env = env
        self.state_size = env.observation_space.shape[0]
        self.action_size = env.action_space.n
        self.memory = deque(maxlen=max_memory_size)
        self.gamma = discount_factor
        self.epsilon = epsilon_greedy
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.lr = learning_rate
        self._build_nn_model()

    def _build_nn_model(self):
        self.model = nn.Sequential(nn.Linear(self.state_size, 256),
                                   nn.ReLU(),
                                   nn.Linear(256, 128),
                                   nn.ReLU(),
                                   nn.Linear(128, 64),
                                   nn.ReLU(),
                                   nn.Linear(64, self.action_size))
        self.loss_fn = nn.MSELoss()
        self.optimizer = torch.optim.Adam(
            self.model.parameters(), self.lr)

    def remember(self, transition):
        self.memory.append(transition)

    def choose_action(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        with torch.no_grad():
            q_values = self.model(torch.tensor(state, dtype=torch.float32))[0]
        return torch.argmax(q_values).item()

    def _learn(self, batch_samples):
        batch_states, batch_targets = [], []
        for transition in batch_samples:
            s, a, r, next_s, done = transition
            with torch.no_grad():
                if done:
                    target = r
                else:
                    pred = self.model(torch.tensor(next_s, dtype=torch.float32))[0]
                    target = r + self.gamma * pred.max()
            target_all = self.model(torch.tensor(s, dtype=torch.float32))[0]
            target_all[a] = target
            batch_states.append(s.flatten())
            batch_targets.append(target_all)
            self._adjust_epsilon()
            self.optimizer.zero_grad()
            pred = self.model(torch.tensor(batch_states,
                                           dtype=torch.float32))
            loss = self.loss_fn(pred, torch.stack(batch_targets))
            loss.backward()
            self.optimizer.step()

        return loss.item()

    def _adjust_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def replay(self, batch_size):
        samples = np.random.sample(self.memory, batch_size)
        return self._learn(samples)


