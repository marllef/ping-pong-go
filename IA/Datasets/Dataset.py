import torch.distributions.uniform as urand
from torch.utils.data import Dataset


class AlgebraicDataset(Dataset):
    def __init__(self, f, interval, n_samples):
        samples = urand.Uniform(interval[0], interval[1]).sample([n_samples])
        self.data = [(x, f(x)) for x in samples]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
