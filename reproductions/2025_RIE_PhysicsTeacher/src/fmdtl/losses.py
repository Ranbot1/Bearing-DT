"""Loss primitives for staged reproduction."""

from __future__ import annotations

import torch
from torch.nn import functional as F


def classification_loss(logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
    return F.cross_entropy(logits, labels)


def _pairwise_sq_dist(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    return torch.cdist(x, y, p=2).pow(2)


def mk_mmd_loss(
    x: torch.Tensor,
    y: torch.Tensor,
    bandwidths: tuple[float, ...] = (0.5, 1.0, 2.0, 4.0, 8.0),
) -> torch.Tensor:
    """Multi-kernel maximum mean discrepancy.

    The paper explicitly uses MK-MMD for the knowledge loss. Kernel bandwidth
    values are not yet confirmed and are therefore configurable/inferred.
    """
    if x.ndim != 2 or y.ndim != 2:
        raise ValueError("MK-MMD expects [batch, feature] tensors")

    d_xx = _pairwise_sq_dist(x, x)
    d_yy = _pairwise_sq_dist(y, y)
    d_xy = _pairwise_sq_dist(x, y)

    k_xx = 0.0
    k_yy = 0.0
    k_xy = 0.0
    for bw in bandwidths:
        gamma = 1.0 / (2.0 * bw * bw)
        k_xx = k_xx + torch.exp(-gamma * d_xx)
        k_yy = k_yy + torch.exp(-gamma * d_yy)
        k_xy = k_xy + torch.exp(-gamma * d_xy)

    return k_xx.mean() + k_yy.mean() - 2.0 * k_xy.mean()


def knowledge_mk_mmd_loss(
    student_response: torch.Tensor,
    teacher_response: torch.Tensor,
    bandwidths: tuple[float, ...] = (0.5, 1.0, 2.0, 4.0, 8.0),
) -> torch.Tensor:
    """Paper-aligned knowledge loss primitive using teacher outputs as an anchor."""
    return mk_mmd_loss(student_response, teacher_response.detach(), bandwidths)


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
