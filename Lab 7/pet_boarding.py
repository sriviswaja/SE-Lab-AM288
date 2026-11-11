"""Pet boarding helpers, hardened against invalid input found by fuzzing.

Each function returns None instead of crashing when the input is invalid.
"""
import math


def _to_number(text):
    """Convert text to a finite float, or return None."""
    try:
        value = float(text)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(value):  # rejects nan, inf, -inf
        return None
    return value


def parse_booking(text):
    """Parse 'pet:days' into (Pet, days). Return None if invalid."""
    if not isinstance(text, str) or text.count(":") != 1:
        return None
    pet, days = text.split(":")
    pet = pet.strip()
    days = _to_number(days)
    if not pet or days is None or days < 0:
        return None
    return pet.title(), days


def stay_average(days_csv):
    """Return the average of comma-separated stay lengths. None if invalid."""
    if not isinstance(days_csv, str):
        return None
    values = []
    for part in days_csv.split(","):
        try:
            value = int(part)
        except ValueError:
            return None
        if value < 0:
            return None
        values.append(value)
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def payable_fee(text):
    """Return fee + 18% GST minus discount, floored at 0. None if invalid."""
    if not isinstance(text, str) or text.count("|") != 1:
        return None
    fee, discount = (_to_number(part) for part in text.split("|"))
    if fee is None or discount is None or fee < 0 or discount < 0:
        return None
    total = fee * 1.18 - discount
    if not math.isfinite(total):  # e.g. fee = 1e308 overflows to inf
        return None
    return round(max(total, 0), 2)


def run_step(title, prompt, func, label):
    """Ask for one input, run func on it and print the result or an error."""
    print(f"==== Running {title} ====")
    result = func(input(prompt))
    if result is None:
        print("Invalid input, please check the format.")
    else:
        print(f"{label}:", result)


def main():
    """Run the three helpers interactively."""
    run_step("parse_booking", "Enter pet:days (e.g. dog:5): ",
             parse_booking, "Pet and Days")
    print()
    run_step("stay_average",
             "Enter stay lengths in days as CSV (e.g. 2,5,7): ",
             stay_average, "Average Stay")
    print()
    run_step("payable_fee", "Enter fee|discount (e.g. 1500|100): ",
             payable_fee, "Payable Fee")


if __name__ == "__main__":
    main()
