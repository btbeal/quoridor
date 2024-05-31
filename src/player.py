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
        self, index, name, position, color, radius, discount_factor=0.95,
        epsilon_greedy=1.0, epsilon_min=0.01,
        epsilon_decay=0.995, learning_rate=1e-3,
        max_memory_size=2000
    ):
        super().__init__(index, name, position, color, radius, is_ai=True)
        self.memory = deque(maxlen=max_memory_size)
        self.gamma = discount_factor
        self.epsilon = epsilon_greedy
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.lr = learning_rate
        self.model = None

    def remember(self, transition):
        self.memory.append(transition)

    def choose_action(self, action_space, state, legal_moves):
        ineligible_indices = []
        eligible_indices = []
        for i, action_item in enumerate(action_space):
            if action_item in legal_moves:
                eligible_indices.append(i)
            else:
                ineligible_indices.append(i)
        if 0 <= self.epsilon:
        #if np.random.rand() <= self.epsilon:
            return np.random.choice(eligible_indices)
        with torch.no_grad():
            q_values = self.model(torch.tensor(state, dtype=torch.float32))[0]
            q_values[ineligible_indices] = float('-inf')

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


