from torch import tensor
from torch.nn import Sequential, Linear, Module, MSELoss, Tanh, Sigmoid
from torch.optim import SGD


class MultiLayerNetwork(Module):

    def __init__(self, sizes):
        super(MultiLayerNetwork, self).__init__()
        self.total_epochs = 0
        self.tanh = Tanh()

        layer_list = [Linear(l_in, l_out) for l_in, l_out in zip(sizes, sizes[1:])]
        self.layers = Sequential()

        for layer in layer_list[:-1]:
            self.layers.append(layer)
            self.layers.append(Sigmoid())
        self.layers.append(layer_list[-1])

    def forward(self, x):
        x = x.float()
        value = self.layers(x)
        return value

    def play(self, data, learning_rate=0.001):
        self.train()
        loss_func = MSELoss()
        optimizer = SGD(self.parameters(), lr=learning_rate)

        for player_y, ball_x, ball_y, active in data:

            player_y = player_y.float()
            ball_x = ball_x.float()
            ball_y = ball_y.float()
            active = active.bool().item()

            pred = self(tensor([player_y, ball_x, ball_y]))
            loss = loss_func(pred, ball_y)

            if active:
                print(
                    f'({player_y.item():<4.4}, {ball_y.item()}, {pred.item():<4.4}) -> Loss: {loss.item():<7.5}')

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            return pred
