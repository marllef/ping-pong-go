import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import cuda, tensor
from torch.utils.data import DataLoader

from Datasets.Dataset import AlgebraicDataset
from Neural.Network import MultiLayerNetwork

device = "cuda" if cuda.is_available() else "cpu"
print(f"Using {device} device")

target_fn = lambda x: 5 * x * x + 5

train_n_samples = 3000
test_n_samples = 100
predict_n_samples = 1
train_dataset = AlgebraicDataset(target_fn, (-10, 10), train_n_samples)
test_dataset = AlgebraicDataset(target_fn, (-10, 10), test_n_samples)
predict_dataset = AlgebraicDataset(target_fn, (-10, 10), predict_n_samples)

train_dataloader = DataLoader(train_dataset, train_n_samples, shuffle=True)
test_dataloader = DataLoader(test_dataset, test_n_samples, shuffle=True)
predict_dataloader = DataLoader(predict_dataset, predict_n_samples, shuffle=True)


def plot(f, model_net, interval=(-10, 10), n_samples=100, title='Após treino inicial'):
    fig, ax = plt.subplots()
    # fig.suptitle('Treinando Modelo - MultiCamadas')
    manager = plt.get_current_fig_manager()
    manager.set_window_title('Resultados - Redes Neurais')

    ax.grid(True, which='both')
    ax.set_title(title)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    samples = np.linspace(interval[0], interval[1], n_samples)
    model_net.eval()
    arr = []

    with torch.no_grad():
        pred = model_net(tensor(samples).unsqueeze(1).float().to(device))
        arr.append(pred)

    ax.plot(samples, list(map(f, samples)), '--', label='Valor esperado', color='red')
    ax.plot(samples, arr[0].cpu(), label='Valor obtido')

    plt.legend()
    return arr


model = MultiLayerNetwork([1, 30, 1]).to(device)
model.train_model(train_dataloader, epochs=50, learning_rate=0.0005)
plot(target_fn, model, title=f'Após treino inicial | {model.total_epochs} epochs')
for i in range(4):
    print('Treinando novamente... ')
    model.train_model(train_dataloader, epochs=700, learning_rate=0.0005)
    plot(target_fn, model, title=f'Após {i + 1} treinos | {model.total_epochs} epochs')

plt.show()
