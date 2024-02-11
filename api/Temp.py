import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import asyncio
import requests
import json
import secrets


doc_ID = None
user_id_token = None

def add_cohort(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

    if not (user_id_token and doc_ID):
        return JsonResponse({'error': 'Missing required parameters.'}, status=400)

    api_key = os.environ.get('FIREBASE_API_KEY')
    project_id = os.environ.get('FIREBASE_PROJECT_ID')

    if not (api_key and project_id):
        return JsonResponse({'error': 'Firebase credentials not configured.'}, status=500)

    cohort_number = generate_cohort_number()

    # Check if cohort number already exists
    firestore_get_response = requests.get(
        f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/regUser',
        headers={'Content-Type': 'application/json'}
    )

    if not firestore_get_response.ok:
        return JsonResponse({'error': 'Failed to fetch document from Firestore.'}, status=firestore_get_response.status_code)

    user_data = firestore_get_response.json()
    for document in user_data.get('documents', []):
        cohort_numbers = document.get('fields', {}).get('cohort', {}).get('stringValue', '').split(',')
        if cohort_number in cohort_numbers:
            return JsonResponse({'error': 'Cohort number already exists.'}, status=400)

    # Get existing cohort numbers from Firestore
    firestore_get_response = requests.get(
        f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/regUser/{doc_ID}',
        headers={'Content-Type': 'application/json'}
    )

    if not firestore_get_response.ok:
        return JsonResponse({'error': 'Failed to fetch document from Firestore.'}, status=firestore_get_response.status_code)

    existing_cohorts = firestore_get_response.json().get('fields', {}).get('cohort', {}).get('stringValue', '')

    # Append new cohort number after existing ones
    new_cohorts = ','.join([existing_cohorts, cohort_number]) if existing_cohorts else cohort_number

    # Update document in Firestore
    firestore_update_data = {
        "fields": {
            "cohort": {
                "stringValue": new_cohorts
            }
        }
    }

    firestore_update_response = requests.patch(
        f'https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/regUser/{doc_ID}',
        headers={'Content-Type': 'application/json'},
        json=firestore_update_data
    )

    if not firestore_update_response.ok:
        return JsonResponse({'error': 'Failed to update document in Firestore.'}, status=firestore_update_response.status_code)

    return JsonResponse({'message': 'Cohort number added successfully.'})

def generate_cohort_number():
    return ''.join(secrets.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(10))

