import torch
from torch import nn
import numpy as np
from kaggle_environments import make

from model import SimpleNet, ResNet, ConvNet
from mcts import mcts
from agents import netAgent, processObservation
from epoch_training import selfplay, net_update
from evaluation import evaluate


model = ConvNet(42, 7, 64)
defaultModel = ConvNet(42, 7, 64)

log = open("log.txt", 'w')
# defaultModel.load_state_dict(torch.load('parameters_simple128.pth'))
optimizer = torch.optim.SGD(model.parameters(), lr = 0.01)
for epoch in range(1000):
    agent = netAgent(model, return_probs=True)
    against = netAgent(defaultModel, incorrect_moves=False)
    
    training_data = selfplay(agent, against, num=10)
    net_update(model, training_data, optimizer)
        
    agent = netAgent(model, incorrect_moves=False, best_move=False)
    against = netAgent(defaultModel, incorrect_moves=False, best_move=False)
    result = evaluate(agent, against, 1000)

    log.write("Epoch " + str(epoch) + " Result: " + str(result) + "\n")
    print("Test result: ", result)
    if (result > 0.65):
        torch.save(model.state_dict(), "parameters_simple128.pth")
        defaultModel.load_state_dict(model.state_dict())
        print("switch")
        log.write("Switch\n")