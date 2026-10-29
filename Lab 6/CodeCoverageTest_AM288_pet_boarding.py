"""Code (line) coverage tests for pet_boarding.py.

Goal: execute every line of pet_boarding.py at least once.
"""
import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# ---------- boarding_fee ----------

def test_within_included_days():
    # dog includes 2 days, so 1 day costs nothing (extra <= 0)
    assert boarding_fee("dog", 1, False) == 0


def test_unknown_pet_type_raises():
    with pytest.raises(ValueError):
        boarding_fee("hamster", 3, False)


def test_negative_days_raises():
    with pytest.raises(ValueError):
        boarding_fee("cat", -1, False)


def test_cat_short_extra_stay():
    # cat: 3 included, 5 days -> 2 extra at rate 20
    assert boarding_fee("cat", 5, False) == 40


def test_premium_dog_long_stay():
    # dog premium: 2 + 1 = 3 included, 20 days -> 17 extra
    # extra > 10 -> rate 30 + 10 + 5 (dog surcharge) = 45
    assert boarding_fee("dog", 20, True) == 17 * 45


# ---------- admission_ok ----------

def test_admission_ok():
    assert admission_ok(4, 2, False) is True


def test_senior_admission():
    assert admission_ok(10, 3, True) is True


def test_too_young_rejected():
    assert admission_ok(0.5, 2, False) is False


# ---------- checkout_status ----------

def test_checkout_open():
    # short stay, weekday -> cutoff 15
    assert checkout_status(20, False, False) == "open"


def test_checkout_late_long_stay_weekend():
    # long stay + weekend -> cutoff 30 + 20 = 50; 40 >= 35 -> late
    assert checkout_status(40, True, True) == "late"


def test_checkout_closed():
    # long stay, weekday -> cutoff 30; 5 < 30 - 15 -> closed
    assert checkout_status(5, True, False) == "closed"
