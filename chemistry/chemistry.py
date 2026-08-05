# chemistry.py

# Step 1: Create the periodic table dictionary
def make_periodic_table():
    periodic_table_dict = {
        "Ac": ["Actinium", 227],
        "Ag": ["Silver", 107.8682],
        "Al": ["Aluminum", 26.9815386],
        "Ar": ["Argon", 39.948],
        "As": ["Arsenic", 74.9216],
        "At": ["Astatine", 210],
        "Au": ["Gold", 196.966569],
        "B": ["Boron", 10.811],
        "Ba": ["Barium", 137.327],
        "Be": ["Beryllium", 9.012182],
        "Bi": ["Bismuth", 208.9804],
        "Br": ["Bromine", 79.904],
        "C": ["Carbon", 12.0107],
        "Ca": ["Calcium", 40.078],
        "Cd": ["Cadmium", 112.411],
        "Ce": ["Cerium", 140.116],
        "Cl": ["Chlorine", 35.453],
        "Co": ["Cobalt", 58.933195],
        "Cr": ["Chromium", 51.9961],
        "Cs": ["Cesium", 132.9054519],
        "Cu": ["Copper", 63.546],
        "Dy": ["Dysprosium", 162.5],
        "Er": ["Erbium", 167.259],
        "Eu": ["Europium", 151.964],
        "F": ["Fluorine", 18.9984032],
        "Fr": ["Francium", 223],
        "Ga": ["Gallium", 69.723],
        "Gd": ["Gadolinium", 157.25],
        "Ge": ["Germanium", 72.64],
        "H": ["Hydrogen", 1.00794],
    }
    return periodic_table_dict


# Step 2: Compute molar mass
def compute_molar_mass(symbol_quantity_list, periodic_table_dict):
    total_mass = 0
    for symbol, quantity in symbol_quantity_list:
        atomic_mass = periodic_table_dict[symbol][1]
        total_mass += atomic_mass * quantity
    return total_mass


# Step 3: Main program
def main():
    # Ask user for chemical formula and sample mass
    formula = input("Enter the chemical formula: ")
    sample_mass = float(input("Enter the sample mass in grams: "))

    # Build periodic table
    periodic_table_dict = make_periodic_table()

    # Use parse_formula from formula.py (already provided)
    from formula import parse_formula
    symbol_quantity_list = parse_formula(formula)

    # Compute molar mass
    molar_mass = compute_molar_mass(symbol_quantity_list, periodic_table_dict)

    # Compute number of moles
    moles = sample_mass / molar_mass

    # Display results
    print(f"Molar mass of {formula}: {molar_mass:.4f} g/mol")
    print(f"Number of moles in {sample_mass} g: {moles:.4f} mol")


# Run program
if __name__ == "__main__":
    main()
