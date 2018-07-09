from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core import serializers
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UploadFileForm
from .models import Sessions, KeyEvents, SerialFrames, TestSubjects
from .tasks import async_process_file
from .exceptions import SchemaOutOfDateError, DuplicateDataUploadError
import os
import time


def is_data_viewer(user):
    return user.groups.filter(name='data_viewers').exists() or user.is_staff or user.is_superuser


def is_data_editor(user):
    return user.groups.filter(name='data_editors').exists() or user.is_staff or user.is_superuser


def not_authorized(request):
    return render(request, 'registration/not_authorized.html')


@login_required()
def index(request):
    sessions = Sessions.objects.all()
    return render(request, 'dbui/index.html', {'sessions': sessions})


@login_required()
@user_passes_test(is_data_viewer, login_url='../accounts/not_authorized', redirect_field_name=None)
def chronos(request, session_id=None):
    sessions = Sessions.objects.all()
    return render(request, 'dbui/chronos.html', {'sessions': sessions, 'selected_session': session_id})


@login_required()
@user_passes_test(is_data_viewer, login_url='../accounts/not_authorized', redirect_field_name=None)
def get_sessions(request):
    sessions = Sessions.objects.all()
    sessions_json = serializers.serialize('json', sessions)
    return HttpResponse(sessions_json, content_type='application/json')


@login_required()
@user_passes_test(is_data_viewer, login_url='../accounts/not_authorized', redirect_field_name=None)
def get_frames_by_session(request, session_id):
    frames = SerialFrames.objects.filter(session_id=session_id)
    frames_json = serializers.serialize('json', frames)
    return HttpResponse(frames_json, content_type='application/json')


@login_required()
@user_passes_test(is_data_editor, login_url='../accounts/not_authorized', redirect_field_name=None)
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return process_and_import_files_async(request)
    else:
        form = UploadFileForm()

    return render(request, 'dbui/uploader.html', {'form': form})


def process_and_import_files_async(request):
    result = "Uploaded files: "
    for file in request.FILES.getlist('files'):
        try:
            file_path = download_file(file)
            task = async_process_file.delay(file_path)
            if len(request.FILES.getlist('files')) == 1:
                result += file.name
            else:
                result += ', ' + file.name
        except SchemaOutOfDateError as schema_error:
            return HttpResponse(schema_error)
        except DuplicateDataUploadError as duplicate_data_error:
            return HttpResponse(duplicate_data_error)
    return HttpResponse(result)
    # return render(request, 'dbui/display_progress.html', context={'task_id': task.task_id})


def download_file(file):
    start = time.time()
    file_path = os.path.join(os.getcwd(), file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    end = time.time()
    print("time to download file was {0} seconds".format(end-start))
    return file_path


