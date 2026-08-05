# W05 Project: Grocery Store Receipt
# Author: Julius Conteh
# Creativity Enhancement: Added a "Return by date" notice (30 days from purchase)
# and a coupon message for exceeding $20 subtotal.

import csv
from datetime import datetime, timedelta

# -------------------------------
# Function: read_dictionary
# -------------------------------
def read_dictionary(filename, key_column_index):
    """Read a CSV file into a compound dictionary.
    Args:
        filename (str): name of the CSV file
        key_column_index (int): column index to use as dictionary key
    Returns:
        dict: dictionary with keys from key_column_index and values as row lists
    """
    dictionary = {}
    try:
        with open(filename, "rt") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # skip header row
            for row in reader:
                key = row[key_column_index]
                dictionary[key] = row
    except FileNotFoundError as e:
        print("Error: missing file")
        print(e)
    except PermissionError as e:
        print("Error: permission denied")
        print(e)
    return dictionary


# -------------------------------
# Function: main
# -------------------------------
def main():
    try:
        # 1. Read products into dictionary
        products_dict = read_dictionary("products.csv", 0)

        # 2. Print store name
        print("Inkom Emporium")

        # 3. Open request file
        with open("request.csv", "rt") as request_file:
            reader = csv.reader(request_file)
            next(reader)  # skip header row

            total_items = 0
            subtotal = 0

            # 4. Process each request row
            for row in reader:
                prod_num = row[0]
                quantity = int(row[1])

                try:
                    if prod_num in products_dict:
                        prod_info = products_dict[prod_num]
                        name = prod_info[1]
                        price = float(prod_info[2])

                        print(f"{name}: {quantity} @ {price:.2f}")

                        total_items += quantity
                        subtotal += price * quantity
                    else:
                        raise KeyError(prod_num)

                except KeyError as e:
                    print("Error: unknown product ID in the request.csv file")
                    print(e)

            # 5. Totals
            print(f"Number of items: {total_items}")
            print(f"Subtotal: {subtotal:.2f}")

            sales_tax = subtotal * 0.06
            total = subtotal + sales_tax

            print(f"Sales Tax: {sales_tax:.2f}")
            print(f"Total: {total:.2f}")

            # 6. Thank you message
            print("Thank you for shopping at the Inkom Emporium.")

            # 7. Current date and time
            current_time = datetime.now()
            print(current_time.strftime("%a %b %d %H:%M:%S %Y"))

            # 🎉 Creativity: Return-by date and coupon
            return_date = current_time + timedelta(days=30)
            print(f"Items may be returned until: {return_date.strftime('%a %b %d %Y')}")
            if subtotal > 20:
                print("🎁 Coupon: 10% off your next purchase!")

    except FileNotFoundError as e:
        print("Error: missing file")
        print(e)
    except PermissionError as e:
        print("Error: permission denied")
        print(e)


# -------------------------------
# Run Program
# -------------------------------
if __name__ == "__main__":
    main()

