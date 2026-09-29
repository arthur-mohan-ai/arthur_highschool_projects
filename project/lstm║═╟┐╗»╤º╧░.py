import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
import random
from collections import deque
import gym
import torch.nn as nn
import torch
from torch.autograd import Variable
import numpy as np
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
from sklearn.metrics import mean_squared_error
import math
if __name__ == '__main__':
    input_dim = 1
    hidden_dim = 50
    num_layers = 2
    output_dim = 1
    epochs = 200
start = datetime(2010, 1, 1)
end = datetime.now()

df = pdr.DataReader("AAPL", 'yahoo', start, end)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df['Close'].values.reshape(-1,1))
def create_dataset(dataset, look_back=60):
    X, Y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        X.append(a)
        Y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(Y)
x, y = create_dataset(scaled_data)
train_size = int(len(x) * 0.8)
test_size = len(x) - train_size
train_x, test_x = x[0:train_size,:], x[train_size:len(x),:]
train_y, test_y = y[0:train_size], y[train_size:len(y)]

class StockLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(StockLSTM, self).__init__()
        self.rnn = nn.LSTM(input_size = input_dim, hidden_size = hidden_dim, num_layers = num_layers)
        self.fc1 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x, hidden):
        out, hidden = self.rnn(x, hidden)
        out = self.fc1(out)
        return out, hidden

class StockLSTM_trainer(object):
    
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, epoch=500):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.output_dim = output_dim
        self.epoch = epoch
        print('input size:', self.input_dim)
        print('hidden size:', self.hidden_dim)
        print('number of layers:', self.num_layers)
        print('output size:', self.output_dim)
        self.model = StockLSTM(self.input_dim, self.hidden_dim, self.num_layers, self.output_dim)
        self.loss_fn = torch.nn.MSELoss()
    
    def input_list_to_batch(self, x):
        new_list = []
        for i in range(len(x)):
            temp = torch.from_numpy(x[i].reshape((1, 1, self.input_dim)))
            new_list.append(temp.float())
        return new_list

    def output_list_to_batch(self, x):
        new_list = []
        for i in range(len(x)):
            temp = torch.from_numpy(x[i].reshape((1, 1, self.output_dim)))
            new_list.append(temp.float())
        return new_list

    def train(self, x, y, init_hidden):
        data_len = len(x)
        optimizer = torch.optim.Adam(self.model.parameters(), lr=5e-3)
        train_x = self.input_list_to_batch(x)
        train_y = self.output_list_to_batch(y)
        for epoch in range(self.epoch):
            loss = 0
            hidden = init_hidden
            for i in range(data_len):
                out, hidden = self.model(train_x[i], hidden)
                loss = loss + self.loss_fn(out, train_y[i])
            print('epoch', epoch, 'loss', loss.data.item())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    def predict(self, x, init_hidden):
        test_x = self.input_list_to_batch(x)
        hidden = init_hidden
        output_list = []
        for i in range(len(test_x)):
            out, hidden = self.model(test_x[i], hidden)
            output_list.append(out.detach().numpy())
        return output_list
        
# Assuming the model is already trained and test_x is prepared

    model.eval()  # Set the model to evaluation mode

    predicted_stock_prices = []

    for i in range(len(test_x)):
        # Reshape test data to (batch_size, sequence_length, input_size)
        test_input = test_x[i].unsqueeze(0)

        # Forward pass to get output/logits
        predicted_price, _ = model(test_input)

        # Convert predictions back to original scale if data was normalized
        predicted_price = scaler.inverse_transform(predicted_price.detach().numpy())
        predicted_stock_prices.append(predicted_price)

    # Convert the list of predictions to a suitable format for further analysis
    predicted_stock_prices = np.array(predicted_stock_prices).squeeze()

if __name__ == '__main__':
    input_dim=3
    hidden_dim=5
    num_layers=4
    output_dim =2
    rnn = StockLSTM_trainer(input_dim, hidden_dim, num_layers, output_dim, epoch=200)
    x = [np.array([0, 0, 1]), np.array([0, 1, 0]), np.array([1, 0, 0])]
    y = [np.array([0, 1]), np.array([1, 0]), np.array([1, 1])]
    h0 = Variable(torch.zeros(num_layers, 1, hidden_dim).float())
    c0 = Variable(torch.zeros(num_layers, 1, hidden_dim).float())
    rnn.train(x, y, (h0, c0))
    print(rnn.predict(x, (h0, c0)))