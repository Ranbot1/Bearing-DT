"""Neural-network components for the paper reproduction.

Confirmed from the paper:
- shared Feature Extractor with 4 convolutional layers;
- Batch Normalization and CBAM attention;
- Leaky ReLU in convolutional feature extraction;
- 128-d feature before the classifier/discriminators;
- label predictor: 128 -> num_classes;
- domain discriminators: 128 -> 64 -> 1.

Still unresolved:
- exact convolution kernel/channel dimensions in Fig. 7/Fig. 9;
- whether the paper's final implementation consumes raw 1-D vibration or a
  2-D representation at every stage.

Therefore this file implements a transparent 1-D reconstruction while
marking the unresolved dimensional details as INFERRED.
"""

from __future__ import annotations

import torch
from torch import nn


class ChannelAttention1D(nn.Module):
    def __init__(self, channels: int, reduction: int = 8):
        super().__init__()
        hidden = max(channels // reduction, 1)
        self.mlp = nn.Sequential(
            nn.Conv1d(channels, hidden, kernel_size=1, bias=False),
            nn.ReLU(inplace=True),
            nn.Conv1d(hidden, channels, kernel_size=1, bias=False),
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        avg = torch.mean(x, dim=-1, keepdim=True)
        mx = torch.amax(x, dim=-1, keepdim=True)
        gate = self.sigmoid(self.mlp(avg) + self.mlp(mx))
        return x * gate


class SpatialAttention1D(nn.Module):
    def __init__(self, kernel_size: int = 7):
        super().__init__()
        padding = kernel_size // 2
        self.conv = nn.Conv1d(2, 1, kernel_size=kernel_size, padding=padding, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        avg = torch.mean(x, dim=1, keepdim=True)
        mx = torch.amax(x, dim=1, keepdim=True)
        gate = self.sigmoid(self.conv(torch.cat([avg, mx], dim=1)))
        return x * gate


class CBAM1D(nn.Module):
    def __init__(self, channels: int):
        super().__init__()
        self.channel = ChannelAttention1D(channels)
        self.spatial = SpatialAttention1D()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.spatial(self.channel(x))


class ConvCBAMBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int):
        super().__init__()
        padding = kernel_size // 2
        self.net = nn.Sequential(
            nn.Conv1d(in_channels, out_channels, kernel_size, stride=2, padding=padding),
            nn.BatchNorm1d(out_channels),
            nn.LeakyReLU(negative_slope=0.2, inplace=True),
            CBAM1D(out_channels),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class FeatureExtractor1D(nn.Module):
    """INFERRED 1-D reconstruction of the confirmed four-layer CNN+BN+CBAM design."""

    def __init__(self, feature_dim: int = 128):
        super().__init__()
        self.features = nn.Sequential(
            ConvCBAMBlock(1, 16, 15),
            ConvCBAMBlock(16, 32, 9),
            ConvCBAMBlock(32, 64, 7),
            ConvCBAMBlock(64, 128, 5),
            nn.AdaptiveAvgPool1d(1),
        )
        self.proj = nn.Identity() if feature_dim == 128 else nn.Linear(128, feature_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        z = self.features(x).squeeze(-1)
        return self.proj(z)


class Classifier(nn.Module):
    def __init__(self, feature_dim: int, num_classes: int):
        super().__init__()
        self.net = nn.Linear(feature_dim, num_classes)

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return self.net(z)


class DomainDiscriminator(nn.Module):
    """Confirmed 128 -> 64 -> 1 discriminator topology when feature_dim=128."""

    def __init__(self, feature_dim: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(feature_dim, 64),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(64, 1),
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return self.net(z).squeeze(-1)


class PhysicsTeacher(nn.Module):
    def __init__(self, feature_dim: int, num_classes: int):
        super().__init__()
        self.feature_extractor = FeatureExtractor1D(feature_dim)
        self.classifier = Classifier(feature_dim, num_classes)

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        z = self.feature_extractor(x)
        return z, self.classifier(z)
