import pytest


def is_vehicle_eligible(
    battery,
    ignition,
    driving
):
    if battery < 60:
        return False

    if ignition:
        return False

    if driving:
        return False

    return True


def test_vehicle_eligible():
    assert is_vehicle_eligible(
        battery=80,
        ignition=False,
        driving=False
    ) is True


def test_low_battery_blocked():
    assert is_vehicle_eligible(
        battery=50,
        ignition=False,
        driving=False
    ) is False


def test_ignition_on_blocked():
    assert is_vehicle_eligible(
        battery=80,
        ignition=True,
        driving=False
    ) is False


def test_vehicle_driving_blocked():
    assert is_vehicle_eligible(
        battery=80,
        ignition=False,
        driving=True
    ) is False