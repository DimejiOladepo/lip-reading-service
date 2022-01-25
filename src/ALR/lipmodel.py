import torch
import torch.nn as nn
from torch.nn.modules.pooling import MaxPool2d

placeholder = 'some value'

class Lipmodel(nn.Module):

    def __init__(self):
        super(Lipmodel, self).__init__()
        self.Layer1 = nn.Sequential(
            nn.Conv2d(in_channels=placeholder, out_channels=100, kernel_size=3, stride=1, ),
            nn.BatchNorm2d(32),
            nn.ReLU()
        )

        self.Layer2 = nn.Sequential(
            nn.Conv2d(in_channels=100, out_channels=60, kernel_size=3, stride=1),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(3)
        )

        self.Layer3 = nn.Sequential(
            nn.MaxPool2d(kernel_size=3, stride=2),
            nn.ELU()
        )

        self.Layer4 = nn.Sequential(
            nn.Conv2d(in_channels=60, out_channels=40, kernel_size=3),
            nn.BatchNorm2d(128),
            nn.MaxPool2d(3)
        )

        self.Layer5 = nn.Sequential(
        nn.MaxPool2d(kernel_size=3, stride=2),
        nn.ELU()
        )

        self.fc1 = nn.Sequential(
            nn.Linear(in_features=placeholder, out_features=300),
            nn.ReLU(),
            nn.Dropout2d(0.55)
            )
        self.fc2 = nn.Sequential(
            nn.Linear(in_features=300, out_features=240),
            nn.ReLU(),
            nn.Dropout2d(0.55)
            )


    def forward(self, x):
        out = self.Layer1(x)
        out = self.Layer2(out)
        out = self.Layer3(out)
        out = self.Layer4(out)
        out = self.Layer5(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc1(out)
        out = self.fc2(out)
        return out