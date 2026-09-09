"""Loss primitives for staged reproduction."""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F


def classification_loss(logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
    return F.cross_entropy(logits, labels)


def knowledge_feature_loss(
    student_features: torch.Tensor,
    teacher_features: torch.Tensor,
) -> torch.Tensor:
    """Simple feature-MSE placeholder until the paper's exact knowledge loss is confirmed."""
    if student_features.shape != teacher_features.shape:
        raise ValueError("Teacher/student feature shapes must match")
    return F.mse_loss(student_features, teacher_features.detach())


class GradientReversal(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: torch.Tensor, scale: float) -> torch.Tensor:
        ctx.scale = scale
        return x.view_as(x)

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor):
        return -ctx.scale * grad_output, None


def grad_reverse(x: torch.Tensor, scale: float = 1.0) -> torch.Tensor:
    return GradientReversal.apply(x, scale)
