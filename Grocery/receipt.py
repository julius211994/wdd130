import csv

def read_dictionary(filename, key_column_index):
    dictionary = {}
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            key = row[key_column_index]
            dictionary[key] = row
    return dictionary

import datetime

def main():
    try:
        products_dict = read_dictionary("products.csv", 0)
        with open("request.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)
            subtotal = 0
            total_items = 0
            print("\n=== Julius Grocery Store Receipt ===")
            for row in reader:
                product_number, quantity = row
                quantity = int(quantity)
                product = products_dict[product_number]
                name = product[1]
                price = float(product[2])
                print(f"{name}: {quantity} @ ${price:.2f}")
                subtotal += price * quantity
                total_items += quantity
            sales_tax = subtotal * 0.06
            total = subtotal + sales_tax
            print("\nItems:", total_items)
            print("Subtotal:", f"${subtotal:.2f}")
            print("Sales Tax:", f"${sales_tax:.2f}")
            print("Total:", f"${total:.2f}")
            print("Thank you for shopping with us!")
            print("Date:", datetime.datetime.now())
    except FileNotFoundError:
        print("Error: File not found.")
    except PermissionError:
        print("Error: Permission denied.")
    except KeyError as e:
        print(f"Error: Product {e} not found in catalog.")

if __name__ == "__main__":
    main()
