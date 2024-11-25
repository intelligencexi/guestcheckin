from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Guest

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

def upload_csv(request):
    if request.method == "POST":
        csv_file = request.FILES.get('csv_file')
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'success': False, 'message': 'Invalid file format. Upload a .csv file'})

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.splitlines()
        duplicates = []
        success_count = 0

        for index, line in enumerate(lines):
            if index == 0 and "first_name" in line.lower():
                continue  # Skip header row

            fields = line.split(",")
            if len(fields) < 3:
                continue

            first_name = fields[0].strip()
            last_name = fields[1].strip()
            email = fields[2].strip()
            number_of_companions = int(fields[3].strip()) if len(fields) > 3 and fields[3].strip().isdigit() else 0

            try:
                Guest.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    number_of_companions=number_of_companions
                )
                success_count += 1
            except IntegrityError:
                duplicates.append(email)

        return JsonResponse({
            'success': True,
            'message': f"{success_count} guests added successfully.",
            'duplicates': duplicates
        })
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def list_guests(request):
    guests = Guest.objects.all()
    return render(request, 'guests/guest-list.html', {'guests': guests})
