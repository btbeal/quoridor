import os
import pygame
from pygame.sprite import Group
from src.board import Board
from src.constants import (
    DEFAULT_FONT_SIZE,
    SCREEN_SIZE_X,
    SCREEN_SIZE_Y,
    GAME_SIZE,
    CELL,
    HALF_DISTANCE,
    TERMINAL_NODE_Y,
    WALL_EDGE_COORD,
)
from src.directions import Direction
from src.dqn import DQN
from src.player import AIPlayer
from src.render_mixin import RenderMixin
from src.rules_mixin import QuoridorRulesMixin
import time
import torch
import warnings


class Quoridor(RenderMixin, QuoridorRulesMixin):
    def __init__(self, players=None, font_size=DEFAULT_FONT_SIZE):
        # Set up game infrastructure.
        pygame.init()
        pygame.display.set_caption("Quoridor")
        self.screen = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
        self.font_size = font_size
        self.font = pygame.font.SysFont('Arial', font_size)

        # Set up players and board.
        self.players = players if players else self.default_players()
        self.board = Board()
        self.action_space = self.default_action_space()
        self.player_group = Group()
        self.player_group.add(self.players)

    @staticmethod
    def default_players():
        return [
            AIPlayer(
                index=0,
                name="Orange",
                color=pygame.Color("coral"),
                position=(GAME_SIZE * 0.5, HALF_DISTANCE),
                radius=0.5 * CELL,
            ),
            AIPlayer(
                index=1,
                name="Blue",
                color=pygame.Color("blue"),
                position=(GAME_SIZE * 0.5, GAME_SIZE - HALF_DISTANCE),
                radius=0.5 * CELL,
            ),
        ]

    def default_action_space(
            self,
            eligible_movements=(
                    (Direction.UP, Direction.UP),
                    (Direction.UP, Direction.RIGHT),
                    (Direction.UP, Direction.LEFT),
                    (Direction.DOWN, Direction.DOWN),
                    (Direction.DOWN, Direction.RIGHT),
                    (Direction.DOWN, Direction.LEFT),
                    (Direction.RIGHT, Direction.DOWN),
                    (Direction.RIGHT, Direction.UP),
                    (Direction.RIGHT, Direction.UP),
                    (Direction.LEFT, Direction.DOWN),
                    (Direction.LEFT, Direction.RIGHT),
                    (Direction.LEFT, Direction.LEFT),
                    Direction.UP,
                    Direction.DOWN,
                    Direction.RIGHT,
                    Direction.LEFT
            )
    ):
        wall_actions = [wall.rect.center for wall in self.board.walls if WALL_EDGE_COORD not in wall.rect.center]
        pawn_actions = [direction_tuple for direction_tuple in eligible_movements]
        action_list = wall_actions + pawn_actions
        return action_list

    def run_game(self):
        current_player_index = 0
        while True:
            current_player = self.players[current_player_index]
            if current_player.is_ai:
                success = False
                while not success:
                    board = self.board
                    state = board.get_state(self.players)
                    legal_move_dict = self._get_legal_moves(current_player)
                    legal_wall_cords = legal_move_dict['place_wall']
                    legal_pawn_moves = list(legal_move_dict['move_pawn'].keys())
                    legal_moves = legal_wall_cords + legal_pawn_moves
                    action_index = current_player.choose_action(self.action_space, state, legal_moves)
                    action = self.action_space[action_index]
                    if action in legal_wall_cords:
                        current_player.place_wall(board, action)
                    else:
                        node = legal_move_dict['move_pawn'].get(action)
                        current_player.move_player(board, node.rect.center)

                    success = True

                time.sleep(0.1)
                current_player_index = (current_player_index + 1) % len(self.players)
                self._render(current_player)

            else:
                success = False
                while not success:
                    events = pygame.event.get()
                    pos = pygame.mouse.get_pos()
                    for event in events:
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            wall_to_place = next(
                                (wall for wall in self.board.walls if wall.rect.collidepoint(pos))
                                , None
                            )
                            if not wall_to_place:
                                success = False
                                continue

                            if self._wall_is_legal(wall_to_place) and current_player.total_walls > 0:
                                current_player.place_wall(self.board, wall_to_place.rect.center)
                                success = True
                        elif event.type == pygame.KEYDOWN:
                            pressed_keys = pygame.key.get_pressed()
                            key_list = [key for key in iter(Direction) if pressed_keys[key]]
                            total_keys_pressed = sum(pressed_keys)

                            if pressed_keys[pygame.K_a] and key_list and total_keys_pressed <= 2:
                                adjacent_movement = key_list[0]
                                legal_adjacent_moves = self._get_legal_adjacent_moves(current_player)
                                if adjacent_movement in legal_adjacent_moves:
                                    new_node = legal_adjacent_moves[adjacent_movement]
                                    current_player.move_player(self.board, new_node.rect.center)
                                    success = True

                            elif key_list:
                                movement = key_list[0]
                                legal_lateral_moves = self._get_legal_lateral_moves(current_player)
                                if movement in legal_lateral_moves:
                                    new_node = legal_lateral_moves[movement]
                                    current_player.move_player(self.board, new_node.rect.center)
                                    success = True

                    self._render(current_player)
                current_player_index = (current_player_index + 1) % len(self.players)

    @staticmethod
    def _is_winner(current_player):
        return TERMINAL_NODE_Y[current_player.index] == current_player.rect.center[1]


class QuoridorGym(Quoridor):
    def __init__(
            self,
            games_to_sim=1000,
            update_target_every=50,
            model_filenames=None
    ):
        super().__init__()
        self.update_target_every = update_target_every
        self.games_to_sim = games_to_sim
        self.model_filenames = model_filenames

    def give_players_a_brain(self):
        state_size = len(self.board.get_state(self.players))
        action_size = len(self.action_space)
        for player in self.players:
            player.policy_model = DQN(action_size=action_size, state_size=state_size)
            player.target_model = DQN(action_size=action_size, state_size=state_size)
            player.optimizer = torch.optim.Adam(player.policy_model.parameters(), player.lr)

        if self.model_filenames:
            if len(self.model_filenames) != len(self.players):
                raise ValueError(f"The number of players must be equivalent to the number of paths if paths are specified")

            for player in self.players:
                filename = self.model_filenames[player.index]
                if os.path.exists(filename):
                    self.load_checkpoints(player.policy_model, player.target_model, player.optimizer, filename)
                else:
                    warnings.warn('Model filenames were given but none were found; base models will be used for the remainder of the training')

    def run_training_session(self):
        self.give_players_a_brain()
        losses = []
        batch_size = 1000
        current_player_index = 0
        total_loops = 0
        current_player = self.players[current_player_index]
        while len(current_player.memory) < batch_size:
            print(len(current_player.memory))
            current_player = self.players[current_player_index]
            state, action_index, next_state, reward, done = self._step(current_player)
            current_player.memory.push_memory(state, action_index, next_state, reward, done)
            total_loops += 1
            if done:
                self._reset_env()
            current_player_index = (current_player_index + 1) % len(self.players)

        start_time = 0
        end_time = 0
        for episode in range(2):
            print(f"Episode #{episode}; time elapsed between last episode: {end_time - start_time}")
            start_time = time.time()
            done = False
            next_player_index = 0
            while not done:
                current_player_index = next_player_index
                current_player = self.players[current_player_index]
                state, action_index, next_state, reward, done = self._step(current_player)
                current_player.memory.push_memory(state, action_index, next_state, reward, done)
                self._render(current_player)
                if done:
                    self._reset_env()
                batch_samples = current_player.memory.sample_memories(batch_size)
                loss = current_player.learn(batch_samples)
                losses.append(loss)
                total_loops += 1
                next_player_index = (current_player_index + 1) % len(self.players)
                if episode % self.update_target_every == 0:
                    current_player.update_target_network()
                    self.players[current_player_index].update_target_network()

            end_time = time.time()
            current_player.adjust_epsilon()

            print(losses[-1])

        for player in self.players:
            filename = self.model_filenames[player.index]
            self.save_checkpoints(player.policy_model, player.optimizer, filename)

    def _reset_env(self):
        for player in self.players:
            player.reset()
        self.board = Board()
        self.player_group = Group()
        self.player_group.add(self.players)

    def _step(self, current_player):
        board = self.board
        state = board.get_state(self.players)
        legal_move_dict = self._get_legal_moves(current_player)
        legal_wall_cords = legal_move_dict['place_wall']
        legal_pawn_moves = list(legal_move_dict['move_pawn'].keys())
        legal_moves = legal_wall_cords + legal_pawn_moves
        action_index = current_player.choose_action(self.action_space, state, legal_moves)
        action = self.action_space[action_index]
        if action in legal_wall_cords:
            current_player.place_wall(board, action)
        else:
            node = legal_move_dict['move_pawn'].get(action)
            current_player.move_player(board, node.rect.center)

        next_state = board.get_state(self.players)
        done = self._is_winner(current_player)
        reward = self._assign_reward(current_player, done)
        return state, action_index, next_state, reward, done

    def _assign_reward(self, current_player, done):
        if done:
            max_distance = SCREEN_SIZE_Y - HALF_DISTANCE
            next_player_index = (current_player.index + 1) % len(self.players)
            y_distance = current_player.rect.centery - self.players[next_player_index].rect.centery
            reward = 10*(1 - abs(y_distance/max_distance))
            print(reward)
            return reward

        print(-0.1)
        return -0.1

    @staticmethod
    def save_checkpoints(model, optimizer, filename):
        checkpoint = {
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict()
        }
        torch.save(checkpoint, filename)

    @staticmethod
    def load_checkpoints(policy_model, target_model, optimizer, filename):
        checkpoint = torch.load(filename)
        policy_model.load_state_dict(checkpoint['model_state_dict'])
        target_model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])