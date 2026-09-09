import torch

from fmdtl.losses import mk_mmd_loss
from fmdtl.models import DomainDiscriminator, PhysicsTeacher


def test_mk_mmd_zero_for_identical_samples():
    x = torch.randn(8, 16)
    loss = mk_mmd_loss(x, x)
    assert abs(float(loss)) < 1e-6


def test_confirmed_macro_architecture_shapes():
    model = PhysicsTeacher(feature_dim=128, num_classes=3)
    x = torch.randn(4, 1, 4096)
    z, logits = model(x)

    assert z.shape == (4, 128)
    assert logits.shape == (4, 3)

    disc = DomainDiscriminator(128)
    assert disc(z).shape == (4,)
