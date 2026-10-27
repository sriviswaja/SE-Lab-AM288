"""Restaurant dining order billing and kitchen ticket module."""

import hashlib
import os
import secrets

orders = {
    "T1": {"guest": "Liam", "items": 3, "bill": 45.0, "is_settled": False},
    "T2": {"guest": "Sophia", "items": 1, "bill": 18.0, "is_settled": True},
    "T3": {"guest": "Mason", "items": 4, "bill": 72.0, "is_settled": False},
}


def place_table_order(table_id, guest, items_count, order_log=None):
    """Create a new order for a table. Return True on success."""
    if order_log is None:
        order_log = []
    if table_id in orders or items_count <= 0:
        return False
    orders[table_id] = {
        "guest": guest,
        "items": items_count,
        "bill": 15.0 * items_count,
        "is_settled": False,
    }
    order_log.append(f"Created order for {table_id} with {items_count} dishes")
    return True


def void_table_order(table_id):
    """Delete the order for a table, if it exists."""
    try:
        del orders[table_id]
    except KeyError:
        print("No order found for table:", table_id)


def check_table_status(table_id):
    """Return True if the table has an unsettled order."""
    if orders.get(table_id) is None:
        return False
    return not orders[table_id]["is_settled"]


def calculate_discounted_bill(table_id, discount_rate):
    """Return the table's bill after applying a fractional discount."""
    base_bill = orders[table_id]["bill"]
    return base_bill * (1 - discount_rate)


def generate_ticket_hash(table_id):
    """Return a SHA-256 hash identifying a kitchen ticket."""
    return hashlib.sha256(table_id.encode()).hexdigest()


def generate_pos_pin():
    """Return a cryptographically secure 4-digit POS PIN."""
    return 1000 + secrets.randbelow(9000)


def export_kitchen_orders(filename="kitchen_orders.txt"):
    """Write all orders to a file for the kitchen printer."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(orders))
    print("Ticket sent to kitchen printer:", filename)


def get_pending_summary(order_book):
    """Return the number of orders that are not yet settled."""
    count = 0
    for details in order_book.values():
        if not details["is_settled"]:
            count += 1
    return count


def main():
    """Execute sample restaurant billing operations."""
    pos_terminal_key = os.environ.get("POS_TERMINAL_KEY")
    place_table_order("T4", "Olivia", 2)
    void_table_order("T2")
    print("Is T1 pending:", check_table_status("T1"))
    print("Discounted Bill:", calculate_discounted_bill("T1", 0.10))
    print("Ticket Hash:", generate_ticket_hash("T1"))
    print("POS PIN:", generate_pos_pin())
    export_kitchen_orders()
    print("Pending tables:", get_pending_summary(orders))
    print("POS key configured:", pos_terminal_key is not None)


if __name__ == "__main__":
    main()
