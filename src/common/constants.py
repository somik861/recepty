from enum import StrEnum, auto


class Spice(StrEnum):
    pažitka = auto()
    pepř = auto()
    solčanka = auto()
    sůl = auto()


class RawMaterial(StrEnum):
    cibule = auto()
    vejce = auto()
    voda = auto()
