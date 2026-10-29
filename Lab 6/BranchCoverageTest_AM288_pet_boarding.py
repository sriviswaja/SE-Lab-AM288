"""Branch coverage tests for pet_boarding.py.

Goal: make every decision (if / elif / else) evaluate to BOTH True and
False at least once, including boundary values.
"""
import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# ---------- boarding_fee ----------

def test_unknown_pet_type_raises():
    with pytest.raises(ValueError):
        boarding_fee("hamster", 3, False)


def test_negative_days_raises():
    with pytest.raises(ValueError):
        boarding_fee("cat", -1, False)


def test_zero_days_is_valid():
    # boundary: days == 0 is NOT < 0
    assert boarding_fee("cat", 0, False) == 0


def test_within_included_days():
    assert boarding_fee("dog", 1, False) == 0


def test_exactly_included_days_is_free():
    # boundary: extra == 0 -> still free
    assert boarding_fee("dog", 2, False) == 0


def test_premium_adds_free_day_for_dog():
    # premium dog: 3 included, so 3 days is free
    assert boarding_fee("dog", 3, True) == 0


def test_premium_ignored_for_rabbit():
    # premium True but pet is rabbit -> condition False, still 4 included
    assert boarding_fee("rabbit", 6, True) == 2 * 20


def test_dog_short_extra_stay():
    # dog rate 30, extra 3 (<= 10)
    assert boarding_fee("dog", 5, False) == 3 * 30


def test_cat_short_extra_stay():
    # non-dog rate 20, extra 2
    assert boarding_fee("cat", 5, False) == 2 * 20


def test_extra_exactly_ten_no_surcharge():
    # boundary: extra == 10 is NOT > 10
    assert boarding_fee("cat", 13, False) == 10 * 20


def test_cat_long_stay_surcharge():
    # extra 11 > 10, non-dog -> rate 20 + 10 = 30 (no dog add-on)
    assert boarding_fee("cat", 14, False) == 11 * 30


def test_dog_long_stay_surcharge():
    # premium dog: 3 included, 20 days -> 17 extra; rate 30 + 10 + 5 = 45
    assert boarding_fee("dog", 20, True) == 17 * 45


# ---------- admission_ok ----------

def test_senior_admitted():
    assert admission_ok(10, 3, True) is True


def test_senior_rejected_low_vaccinations():
    assert admission_ok(10, 2, True) is False


def test_too_young_rejected():
    assert admission_ok(0.5, 2, False) is False


def test_exactly_one_year_admitted():
    # boundary: age == 1 is NOT < 1
    assert admission_ok(1, 2, False) is True


def test_adult_admitted():
    assert admission_ok(4, 2, False) is True


def test_adult_rejected_low_vaccinations():
    assert admission_ok(4, 1, False) is False


# ---------- checkout_status ----------

def test_open_short_stay_weekday():
    assert checkout_status(20, False, False) == "open"


def test_open_at_exact_cutoff():
    # boundary: minutes == cutoff -> open
    assert checkout_status(15, False, False) == "open"


def test_late_short_stay_weekday():
    # cutoff 15; 10 >= 0 -> late
    assert checkout_status(10, False, False) == "late"


def test_late_long_stay_weekend():
    # cutoff 30 + 20 = 50; 40 >= 35 -> late
    assert checkout_status(40, True, True) == "late"


def test_open_long_stay_weekend():
    assert checkout_status(50, True, True) == "open"


def test_open_short_stay_weekend():
    # cutoff 15 + 20 = 35
    assert checkout_status(35, False, True) == "open"


def test_closed_long_stay_weekday():
    # cutoff 30; 5 < 15 -> closed
    assert checkout_status(5, True, False) == "closed"


def test_closed_short_stay_weekend():
    # cutoff 35; 10 < 20 -> closed
    assert checkout_status(10, False, True) == "closed"
