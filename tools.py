import csv
import os
import random
import shutil
import tempfile
import time
from dotenv import load_dotenv

load_dotenv()


def _update_order_in_csv(order_id: str, new_status: str) -> bool:
    file_path = "orders.csv"
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        return False

    updated = False
    rows = []

    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == order_id:
                row[3] = new_status
                updated = True
            rows.append(row)

    if updated:
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
            f.flush()

    return updated


def greetings(name: str = None) -> str:
    """Main greeting of a company"""
    message = f"Hi, {name} - company VoronCo greet you" if name else "Hello, company VoronCo greet you"
    return message


def calculate_shipping(weight: float, city: str) -> str:
    """Calculate the shipping cost of a company"""
    additional_cost = {
        "Kyiv": 50,
        "lviv": 50,
        "Odesa": 30,
        "Kharkiv": 20
    }
    shipping_cost = weight * 10 + additional_cost.get(city.capitalize(), 0)
    return (f"The cost of delivering cargo weighing {weight}kg "
            f"to the city {city} is {shipping_cost} UAH")


def confirm_delivery(name: str) -> str:
    """Confirm user's delivery, return confirmation bill number"""
    unix_timestamp_int = int(time.time())
    eight_digit_number = random.randint(10000000, 99999999)
    order_id = f"{unix_timestamp_int}-{eight_digit_number}"
    payment_details = os.getenv("PAYMENT_DETAILS")

    with open("orders.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([order_id, unix_timestamp_int, name, "pending"])
        f.flush()
        os.fsync((f.fileno()))

    return (f"Your order #{eight_digit_number} is confirmed by {payment_details}"
            f"Order ID: {order_id}, recipient: {name})")


def successful_payment(order_id: str) -> str:
    """Successful payment of a company"""
    if _update_order_in_csv(order_id, "paid"):
        return f"Payment for order {order_id} confirmed."
    return f"Order {order_id} not found."


def successful_delivery(order_id: str) -> str:
    """Successful order of a company"""
    if _update_order_in_csv(order_id, "finished"):
        return f"Order {order_id} is successful delivered."
    return f"Order {order_id} not found."


def cancel_order(order_id: str) -> str:
    """Cancel order by order_id"""
    if _update_order_in_csv(order_id, "cancelled"):
        return f"Order {order_id} has been successfully cancelled."
    return f"Could not find order {order_id} to cancel."


def check_order_status(order_id: str) -> str:
    """Check the status of a order"""
    if not os.path.exists("orders.csv"):
        return "Orders database is empty."

    with open("orders.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == order_id:
                return f"Order {order_id} status is: {row[3].upper()}"
    return f"Order {order_id} not found."


names_to_functions = {
    "greetings": greetings,
    "calculate_shipping": calculate_shipping,
    "confirm_delivery": confirm_delivery,
    "successful_payment": successful_payment,
    "successful_delivery": successful_delivery,
    "cancel_order": cancel_order,
    "check_order_status": check_order_status
}