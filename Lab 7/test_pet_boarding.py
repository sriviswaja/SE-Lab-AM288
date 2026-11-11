"""Hypothesis fuzz tests for pet_boarding.py (Lab 7)."""
import math

from hypothesis import given, strategies as st
from pet_boarding import parse_booking, stay_average, payable_fee


# ---------- 1. No-crash properties: random text or None ----------

@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"parse_booking crashed with: {e!r}"


@given(st.text() | st.none())
def test_stay_average_no_crash(s):
    try:
        stay_average(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"stay_average crashed with: {e!r}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"payable_fee crashed with: {e!r}"


# ---------- 2. Targeted fuzzing: inputs shaped like real bookings ----------

numbers = st.floats(allow_nan=True, allow_infinity=True).map(str)


@given(st.text(max_size=10), numbers)
def test_parse_booking_shaped_input(pet, days):
    # e.g. "dog:5", ":nan", "cat:-3", " :inf"
    try:
        result = parse_booking(f"{pet}:{days}")
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"parse_booking crashed with: {e!r}"
    if result is not None:
        name, n_days = result
        assert name, "pet name must not be empty"
        assert math.isfinite(n_days), "days must be a finite number"
        assert n_days >= 0, "days cannot be negative"


@given(st.lists(st.integers(min_value=-10, max_value=60), max_size=8))
def test_stay_average_shaped_input(values):
    # e.g. "", "2,5,7", "-3,4"
    text = ",".join(str(v) for v in values)
    try:
        result = stay_average(text)
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"stay_average crashed with: {e!r}"
    if result is not None:
        assert result >= 0, "average stay cannot be negative"


@given(numbers, numbers)
def test_payable_fee_shaped_input(fee, discount):
    # e.g. "1500|100", "nan|0", "1e308|0", "-50|0"
    try:
        result = payable_fee(f"{fee}|{discount}")
    except Exception as e:  # pylint: disable=broad-except
        assert False, f"payable_fee crashed with: {e!r}"
    if result is not None:
        assert math.isfinite(result), "fee must be a finite number"
        assert result >= 0, "fee cannot be negative"


# ---------- 3. Correctness on valid input ----------

def test_valid_examples():
    assert parse_booking("dog:5") == ("Dog", 5.0)
    assert stay_average("2,5,7") == 4.67
    assert payable_fee("1500|100") == 1670.0
