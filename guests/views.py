from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Guest
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import UpdateView
from django.db.models import Q
import logging
import os
import csv

#logger = logging.getLogger(__name__)
logger = logging.getLogger('guests.upload_csv')



# def upload_csv(request):
#     logger.info("Starting CSV upload process...")

#     if request.method == "POST":
#         csv_file = request.FILES.get("csv_file")
#         if not csv_file or not csv_file.name.endswith(".csv"):
#             logger.error("Invalid file format or missing file.")
#             return JsonResponse({
#                 "success": False,
#                 "message": "Invalid file format. Upload a .csv file."
#             })

#         try:
#             # Read and decode the file content
#             file_data = csv_file.read().decode("utf-8")
#             lines = file_data.splitlines()

#             # Initialize tracking variables
#             duplicates = []
#             success_count = 0
#             success_entries = []

#             logger.info(f"Processing {len(lines) - 1} potential guests (excluding header).")

#             for index, line in enumerate(lines):
#                 if index == 0 and "FirstName" in line:  # Skip header row
#                     logger.debug(f"Skipping header row: {line}")
#                     continue

#                 fields = line.split(",")
#                 if len(fields) < 5:  # Ensure all required fields are present
#                     logger.warning(f"Skipping line {index + 1}: Insufficient fields.")
#                     continue

#                 first_name = fields[0].strip()
#                 last_name = fields[1].strip()
#                 court = fields[2].strip()
#                 row = int(fields[3].strip()) if fields[3].strip().isdigit() else 0
#                 number_of_companions = (
#                     int(fields[4].strip()) if fields[4].strip().isdigit() else 0
#                 )

#                 # Validate and check for duplicates
#                 if Guest.objects.filter(
#                     first_name__iexact=first_name, last_name__iexact=last_name
#                 ).exists():
#                     duplicates.append(f"{first_name} {last_name}")
#                     logger.info(f"Duplicate guest detected: {first_name} {last_name}.")
#                     continue

#                 try:
#                     # Create guest entry
#                     Guest.objects.create(
#                         first_name=first_name,
#                         last_name=last_name,
#                         court=court,
#                         row=row,
#                         number_of_companions=number_of_companions,
#                     )
#                     success_count += 1
#                     success_entries.append(f"{first_name} {last_name}")
#                     logger.info(f"Successfully added guest: {first_name} {last_name}.")
#                 except IntegrityError as e:
#                     duplicates.append(f"{first_name} {last_name}")
#                     logger.error(f"IntegrityError for guest {first_name} {last_name}: {str(e)}")

#             logger.info(f"Upload summary: {success_count} successful, {len(duplicates)} duplicates.")

#             # Save duplicates to CSV
#             duplicate_csv_path = os.path.join(os.path.dirname(__file__), "duplicates.csv")
#             with open(duplicate_csv_path, "w", newline="") as csvfile:
#                 csv_writer = csv.writer(csvfile)
#                 csv_writer.writerow(["Duplicate Guests"])
#                 for duplicate in duplicates:
#                     csv_writer.writerow([duplicate])

#             logger.info(f"Duplicates saved to {duplicate_csv_path}")

#             # Store success message in session and return response
#             success_message = (
#                 f"Successfully added {success_count} guests. "
#                 f"Duplicates detected: {len(duplicates)}."
#             )
#             request.session["upload_message"] = success_message

#             return JsonResponse({
#                 "success": True,
#                 "message": success_message,
#                 "total_success": success_count,
#                 "total_duplicates": len(duplicates),
#                 "successful_entries": success_entries,
#                 "duplicate_entries": duplicates,
#                 "duplicates_csv": duplicate_csv_path,
#             })

#         except Exception as e:
#             logger.exception("An error occurred during the CSV upload process.")
#             return JsonResponse({
#                 "success": False,
#                 "message": "An error occurred while processing the file."
#             })

#     logger.warning("Invalid request method.")
#     return JsonResponse({"success": False, "message": "Invalid request method."})



def upload_csv(request):
    logger.info("Starting CSV upload process...")

    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")
        if not csv_file or not csv_file.name.endswith(".csv"):
            logger.error("Invalid file format or missing file.")
            response_data = {
                "success": False,
                "message": "Invalid file format. Upload a .csv file.",
            }
            if "redirect" in request.GET:
                request.session["upload_message"] = response_data["message"]
                return redirect(reverse("guest-list"))
            return JsonResponse(response_data)

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
                if index == 0 and "FirstName" in line:  # Skip header row
                    logger.debug(f"Skipping header row: {line}")
                    continue

                fields = line.split(",")
                if len(fields) < 5:  # Ensure all required fields are present
                    logger.warning(f"Skipping line {index + 1}: Insufficient fields.")
                    continue

                first_name = fields[0].strip()
                last_name = fields[1].strip()
                court = fields[2].strip()
                row = int(fields[3].strip()) if fields[3].strip().isdigit() else 0
                number_of_companions = (
                    int(fields[4].strip()) if fields[4].strip().isdigit() else 0
                )

                # Validate and check for duplicates
                if Guest.objects.filter(
                    first_name__iexact=first_name, last_name__iexact=last_name
                ).exists():
                    duplicates.append(f"{first_name} {last_name}")
                    logger.info(f"Duplicate guest detected: {first_name} {last_name}.")
                    continue

                try:
                    # Create guest entry
                    Guest.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        court=court,
                        row=row,
                        number_of_companions=number_of_companions,
                    )
                    success_count += 1
                    success_entries.append(f"{first_name} {last_name}")
                    logger.info(f"Successfully added guest: {first_name} {last_name}.")
                except IntegrityError as e:
                    duplicates.append(f"{first_name} {last_name}")
                    logger.error(f"IntegrityError for guest {first_name} {last_name}: {str(e)}")

            logger.info(f"Upload summary: {success_count} successful, {len(duplicates)} duplicates.")

            # Save duplicates to CSV
            duplicate_csv_path = os.path.join(os.path.dirname(__file__), "duplicates.csv")
            with open(duplicate_csv_path, "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Duplicate Guests"])
                for duplicate in duplicates:
                    csv_writer.writerow([duplicate])

            logger.info(f"Duplicates saved to {duplicate_csv_path}")

            # Prepare response data
            success_message = (
                f"Successfully added {success_count} guests. "
                f"Duplicates detected: {len(duplicates)}."
            )
            response_data = {
                "success": True,
                "message": success_message,
                "total_success": success_count,
                "total_duplicates": len(duplicates),
                "successful_entries": success_entries,
                "duplicate_entries": duplicates,
                "duplicates_csv": duplicate_csv_path,
            }

            # Redirect or return JSON based on request
            if "redirect" in request.GET:
                request.session["upload_message"] = response_data["message"]
                return redirect(reverse("list_guests"))

            return JsonResponse(response_data)

        except Exception as e:
            logger.exception("An error occurred during the CSV upload process.")
            response_data = {
                "success": False,
                "message": "An error occurred while processing the file.",
            }
            if "redirect" in request.GET:
                request.session["upload_message"] = response_data["message"]
                return redirect(reverse("list_guests"))
            return JsonResponse(response_data)

    logger.warning("Invalid request method.")
    response_data = {"success": False, "message": "Invalid request method."}
    if "redirect" in request.GET:
        request.session["upload_message"] = response_data["message"]
        return redirect(reverse("list_guests"))
    return JsonResponse(response_data)


def search(request):
    q = request.GET.get('q', '')
    print(q)

    if q:
        results = Guest.objects.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(court__icontains=q)
            
            ).order_by( 'first_name', 'last_name',)[0:50] if q else []
    else:
        results = []
    
    return render(request, 'guests/results.html', {'results': results})


class GuestUpdateView(UpdateView):
    model = Guest
    fields = ['first_name', 'last_name', 'number_of_companions', 'has_arrived', 'court', 'row']
    template_name = 'guests/guest_edit.html'
    success_url = reverse_lazy('list_guests')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Add success message to the session
        if self.object:
            self.request.session['upload_message'] = f"Guest '{self.object.first_name} {self.object.last_name}' was updated successfully!"
        return response


def home(request):
    return render(request, 'guests/home.html')

def add_guest(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        number_of_companions = int(request.POST.get('number_of_companions', 0))
        court = request.POST.get('court')
        row = request.POST.get('row')

        try:
            Guest.objects.create(
                first_name=first_name,
                last_name=last_name,
                court=court,
                row=row,
                number_of_companions=number_of_companions
            )
            return JsonResponse({'success': True})
        except IntegrityError:
            return JsonResponse({'success': False, 'message': 'Duplicate guest detected'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})



def list_guests(request):
    success_message = request.session.pop('upload_message', None)
    guests = Guest.objects.all()

    # Handle pagination
    per_page = request.GET.get('per_page', 20)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 20

    paginator = Paginator(guests, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Check if a guest needs to be highlighted
    highlight_id = request.GET.get('highlight')
    highlighted_guest = None
    if highlight_id:
        try:
            highlighted_guest = int(highlight_id)
        except ValueError:
            pass

    return render(request, 'guests/guest_list.html', {
        'page_obj': page_obj,
        'success_message': success_message,
        'per_page': per_page,
        'highlighted_guest': highlighted_guest,
    })