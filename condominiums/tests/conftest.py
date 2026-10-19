import itertools
from datetime import date

import pytest

from condominiums.models import Block, Company, Condominium
from setup.models import Address

_counter = itertools.count(1)


def _valid_cnpj(seed: int) -> str:
    """Build a CNPJ with correct check digits from a numeric seed."""
    base = f"{seed:012d}"
    weights1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    weights2 = (6, *weights1)

    def digit(chars, weights):
        r = sum(int(c) * w for c, w in zip(chars, weights)) % 11
        return 0 if r < 2 else 11 - r

    d1 = digit(base, weights1)
    d2 = digit(base + str(d1), weights2)
    return f"{base}{d1}{d2}"


@pytest.fixture
def make_address(db):
    def _make(**overrides):
        data = {"street": "Rua A", "city": "Porto Alegre", "state": "RS"}
        data.update(overrides)
        return Address.objects.create(**data)

    return _make


@pytest.fixture
def make_company(make_address):
    def _make(**overrides):
        n = next(_counter)
        data = {
            "legal_name": f"Company {n} LTDA",
            "trade_name": f"Company {n}",
            "cnpj": _valid_cnpj(n),
            "email": f"company{n}@example.com",
            "address": make_address(),
        }
        data.update(overrides)
        return Company.objects.create(**data)

    return _make


@pytest.fixture
def make_condominium(make_company, make_address):
    def _make(**overrides):
        n = next(_counter)
        data = {
            "company": make_company(),
            "code": f"{n:04d}",
            "name": f"Condo {n}",
            "type": Condominium.Type.RESIDENTIAL,
            "address": make_address(),
            "administration_start_date": date(2026, 1, 1),
        }
        data.update(overrides)
        return Condominium.objects.create(**data)

    return _make


@pytest.fixture
def make_block(make_condominium):
    def _make(**overrides):
        data = {"condominium": make_condominium(), "name": "Bloco A"}
        data.update(overrides)
        return Block.objects.create(**data)

    return _make
