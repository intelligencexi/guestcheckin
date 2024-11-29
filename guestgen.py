import csv
import random

def generate_guest_list(num_guests, output_file):
    first_names = [
        "Intelligence", "Chichetam", "Confidence", "Ogochukwu", "Uloma",
        "Onyinye", "Jeff", "Michelle", "Fonzy", "Genny",
        "Clark", "Kiliua", "Baki", "Daniel",
    ]
    last_names = [
        "Uchechukwu", "Chukwu", "Mbonu", "Ubani", "Banner",
        "Ibekwe", "Ezemonye", "Nnoli", "Onwuka", "El",
        "Illoh", "Akalonu", "Iwuoha", "Chima", "Okoronta",
    ]
    courts = ["KC1", "KC2", "KC3", "KC4", "KC5", "KC6"]

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(["FirstName", "LastName", "Court", "Row", "NoOfCompanions"])

        for _ in range(num_guests):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            court = random.choice(courts)
            row = random.randint(1, 10)
            no_of_companions = random.randint(0, 5)

            # Write the guest information
            writer.writerow([first_name, last_name, court, row, no_of_companions])

# Generate a guest list with 15,000 entries
generate_guest_list(1000, "guestlist.csv")
