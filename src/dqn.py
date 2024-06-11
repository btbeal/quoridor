import torch.nn as nn
from collections import namedtuple, deque
import random


class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super().__init__()
        self.linear_relu = nn.Sequential(
            nn.Linear(state_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_size)
        )

    def forward(self, x):
        return self.linear_relu(x)


class ExperienceReplay:
    def __init__(self, max_memory_capacity):
        self.memory = deque([], max_memory_capacity)

    def push_memory(self, *args):
        self.memory.append(Transition(*args))

    def sample_memories(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward', 'done'))


