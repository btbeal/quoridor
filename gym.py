from src.quoridor import QuoridorGym


if __name__ == "__main__":
    gym = QuoridorGym(model_filenames={0: 'agent_0.pth', 1: 'agent_1.pth'})
    gym.run_training_session()
