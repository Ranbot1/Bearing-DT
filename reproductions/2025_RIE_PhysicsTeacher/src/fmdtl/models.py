"""Neural-network skeleton for the paper reproduction.

The exact layer widths and all hyperparameters must be updated only when they
are confirmed from the paper. This module intentionally provides a small
auditable baseline rather than pretending inferred architecture details are
paper-faithful.
"""

from __future__ import annotations

import torch
from torch import nn


class FeatureExtractor1D(nn.Module):
    def __init__(self, feature_dim: int = 128):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv1d(1, 32, kernel_size=15, stride=2, padding=7),
            nn.BatchNorm1d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool1d(2),
            nn.Conv1d(32, 64, kernel_size=9, stride=2, padding=4),
            nn.BatchNorm1d(64),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool1d(1),
        )
        self.proj = nn.Linear(64, feature_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.proj(self.features(x).squeeze(-1))


class Classifier(nn.Module):
    def __init__(self, feature_dim: int, num_classes: int):
        super().__init__()
        self.net = nn.Linear(feature_dim, num_classes)

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return self.net(z)


class DomainDiscriminator(nn.Module):
    def __init__(self, feature_dim: int):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(feature_dim, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, 2),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return self.net(z)


class PhysicsTeacher(nn.Module):
    def __init__(self, feature_dim: int, num_classes: int):
        super().__init__()
        self.feature_extractor = FeatureExtractor1D(feature_dim)
        self.classifier = Classifier(feature_dim, num_classes)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        z = self.feature_extractor(x)
        return z, self.classifier(z)
