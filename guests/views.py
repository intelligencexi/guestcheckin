from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Guest
from django.core.paginator import Paginator
import logging
import re
import csv
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
#logger = logging.getLogger(__name__)
logger = logging.getLogger('guests.upload_csv')


import os
import csv
import logging
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Guest

logger = logging.getLogger('guests.upload_csv')  # Matches 'guests.upload_csv' in LOGGING config

def upload_csv(request):
    logger.info("Starting CSV upload process...")
    
    if request.method == "POST":
        csv_file = request.FILES.get('csv_file')
        if not csv_file or not csv_file.name.endswith('.csv'):
            logger.error("Invalid file format or missing file.")
            return JsonResponse({'success': False, 'message': 'Invalid file format. Upload a .csv file.'})
        
        try:
            # Read and decode the file content
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.splitlines()

            # Initialize tracking variables
            duplicates = []
            success_count = 0
            success_entries = []

            logger.info(f"Processing {len(lines) - 1} potential guests (excluding header).")
            
            for index, line in enumerate(lines):
                if index == 0 and "first_name" in line.lower():  # Skip header row
                    logger.debug(f"Skipping header row: {line}")
                    continue

                fields = line.split(",")
                if len(fields) < 3:
                    logger.warning(f"Skipping line {index + 1}: Insufficient fields.")
                    continue

                first_name = fields[0].strip()
                last_name = fields[1].strip()
                email = fields[2].strip()

                # Populate defaults for missing fields
                number_of_companions = (
                    int(fields[3].strip()) if len(fields) > 3 and fields[3].strip().isdigit() else 0
                )
                has_arrived = False  # Default value
                
                # Validate and check for duplicates
                if Guest.objects.filter(first_name__iexact=first_name, last_name__iexact=last_name).exists():
                    duplicates.append(f"{first_name} {last_name}")
                    logger.info(f"Duplicate guest detected: {first_name} {last_name}.")
                    continue

                try:
                    # Create guest with default values
                    Guest.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        number_of_companions=number_of_companions,
                        has_arrived=has_arrived
                    )
                    success_count += 1
                    success_entries.append(f"{first_name} {last_name} ({email})")
                    logger.info(f"Successfully added guest: {first_name} {last_name}.")
                except IntegrityError as e:
                    duplicates.append(f"{first_name} {last_name}")
                    logger.error(f"IntegrityError for guest {first_name} {last_name}: {str(e)}")

            logger.info(f"Upload summary: {success_count} successful, {len(duplicates)} duplicates.")
            
            # Save duplicates to CSV
            duplicate_csv_path = os.path.join(os.path.dirname(__file__), 'duplicates.csv')
            with open(duplicate_csv_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Duplicate Guests"])
                for duplicate in duplicates:
                    csv_writer.writerow([duplicate])
            
            logger.info(f"Duplicates saved to {duplicate_csv_path}")

            # Store success message in session and return response
            success_message = (
                f"Successfully added {success_count} guests. "
                f"Duplicates detected: {len(duplicates)}."
            )
            request.session['upload_message'] = success_message

            return JsonResponse({
                'success': True,
                'message': success_message,
                'total_success': success_count,
                'total_duplicates': len(duplicates),
                'successful_entries': success_entries,
                'duplicate_entries': duplicates,
                'duplicates_csv': duplicate_csv_path,
            })

        except Exception as e:
            logger.exception("An error occurred during the CSV upload process.")
            return JsonResponse({'success': False, 'message': 'An error occurred while processing the file.'})

    logger.warning("Invalid request method.")
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})




class GuestUpdateView(UpdateView):
    model = Guest
    fields = ['first_name', 'last_name', 'email', 'number_of_companions', 'has_arrived']
    template_name = 'guests/guest_edit.html'
    success_url = reverse_lazy('list_guests')  # Redirect to the guest list after saving

    def form_valid(self, form):
        # Add custom logic here if needed (e.g., logging changes)
        response = super().form_valid(form)
        self.request.session['upload_message'] = f"Guest '{self.object.first_name} {self.object.last_name}' was updated successfully!"
        return response













































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
