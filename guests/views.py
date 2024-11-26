from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Guest
from django.core.paginator import Paginator
import logging
import re
import csv
from django.conf import settings
#logger = logging.getLogger(__name__)
logger = logging.getLogger('guests.upload_csv')


def upload_csv(request):
    if request.method == "POST":
        # Get the uploaded file
        csv_file = request.FILES.get('csv_file')
        if not csv_file or not csv_file.name.endswith('.csv'):
            return JsonResponse({'success': False, 'message': 'Invalid file format. Upload a .csv file.'})

        # Read and decode the file content
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.splitlines()

        # Initialize tracking variables
        duplicates = []
        success_count = 0
        success_entries = []

        # Iterate over each line in the CSV (skip header)
        for index, line in enumerate(lines):
            # Skip the header row (assuming first row contains column names)
            if index == 0 and "first_name" in line.lower():
                logger.info(f"Skipping header row: {line}")
                continue

            fields = line.split(",")
            if len(fields) < 3:
                logger.warning(f"Skipping line {index + 1}: Insufficient fields.")
                continue

            first_name = fields[0].strip()
            last_name = fields[1].strip()
            email = fields[2].strip()

            # Validate first_name and last_name to only contain letters
            if not first_name.isalpha() or not last_name.isalpha():
                logger.warning(f"Skipping line {index + 1}: Invalid name format. Name should only contain letters (no numbers).")
                continue

            # Validate email format (check if it matches standard format)
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                logger.warning(f"Skipping line {index + 1}: Invalid email format. Email should be a valid email address.")
                continue

            number_of_companions = (
                int(fields[3].strip()) if len(fields) > 3 and fields[3].strip().isdigit() else 0
            )

            # Check for duplicates based on first_name and last_name
            if Guest.objects.filter(first_name__iexact=first_name, last_name__iexact=last_name).exists():
                duplicates.append([first_name, last_name, email])  # Add duplicates as a list of fields
                logger.info(f"Duplicate guest detected: {first_name} {last_name}.")
                continue

            try:
                # Create guest without phone field, using only model-defined fields
                Guest.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    number_of_companions=number_of_companions
                )
                success_count += 1
                success_entries.append(f"{first_name} {last_name} ({email})")
                logger.info(f"Successfully added guest: {first_name} {last_name}.")
            except IntegrityError as e:
                duplicates.append([first_name, last_name, email])  # Add duplicates as a list of fields
                logger.error(f"IntegrityError for guest {first_name} {last_name}: {str(e)}")

        # Log summary of upload
        logger.info(f"Uploaded {success_count} guests. Duplicates: {len(duplicates)}")
        logger.info(f"Successful entries: {success_entries}")

        # Write duplicates to CSV file
        duplicate_csv_path = settings.BASE_DIR / 'duplicate.csv'
        with open(duplicate_csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['first_name', 'last_name', 'email'])  # Write header
            writer.writerows(duplicates)  # Write duplicate entries

        # Store success message in session and redirect with success popup
        success_message = (
            f"Successfully added {success_count} guests. "
            f"Duplicates detected: {len(duplicates)}."
        )
        request.session['upload_message'] = success_message

        # Return response with details
        return JsonResponse({
            'success': True,
            'message': success_message,
            'total_success': success_count,
            'total_duplicates': len(duplicates),
            'successful_entries': success_entries,
            'duplicate_entries': duplicates,
        })

    # Handle invalid request method
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def home(request):
    return render(request, 'guests/home.html')

def add_guest(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        number_of_companions = int(request.POST.get('number_of_companions', 0))

        try:
            Guest.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                number_of_companions=number_of_companions
            )
            return JsonResponse({'success': True})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Duplicate email detected'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def list_guests(request):
    # Retrieve and remove the success message from the session, if any
    success_message = request.session.pop('upload_message', None)

    # Fetch all guests from the database
    guests = Guest.objects.all()

    # Get the desired number of guests per page (default to 20)
    per_page = request.GET.get('per_page', 20)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 20  # Fallback to default if invalid

    # Set up pagination
    paginator = Paginator(guests, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'guests/guest_list.html', {
        'page_obj': page_obj,  # Pass paginated guest objects
        'success_message': success_message,
        'per_page': per_page,  # Pass the current per_page value
    })
