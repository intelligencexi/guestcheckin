import csv
import random

def generate_guest_list(num_guests, output_file):
    first_names = [
        "Intelligence",
        "Chichetam",
        "Confidence",
        "Ogochukwu",
        "Uloma",
        "Onyinye",
        "Jeff",
        "Michelle",
        "Fonzy",
        "Genny",
        "Clark",
        "Kiliua",
        "Baki",
        "Daniel",
    ]
    last_names = [
        "Uchechukwu",
        "Chukwu",
        "Mbonu",
        "Ubani",
        "Banner",
        "Ibekwe",
        "Ezemonye",
        "Nnoli",
        "Onwuka",
        "El",
        "Illoh",
        "Akalonu",
        "Iwuoha",
        "Chima",
        "Okoronta",
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["FirstName", "LastName", "Email"])

        for guest_id in range(1, num_guests + 1):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{guest_id}@example.com"

            writer.writerow([first_name, last_name, email])

generate_guest_list(15000, "guestlist.csv")
