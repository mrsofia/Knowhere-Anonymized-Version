from __future__ import absolute_import, unicode_literals
from django.db import transaction, IntegrityError
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from .models import Sessions, KeyEvents, SerialFrames, TestSubjects
from .exceptions import SchemaOutOfDateError, DuplicateDataUploadError
import sqlite3
import uuid
import time


@shared_task
def async_process_file(file):

    with transaction.atomic():
        progress_recorder = ProgressRecorder(async_process_file)

        start = time.time()

        with sqlite3.connect(file) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            num_items_to_complete = 0
            cursor.execute("select * from table1")
            num_items_to_complete += len(cursor.fetchall())
            cursor.execute("select * from table2")
            num_items_to_complete += len(cursor.fetchall())
            cursor.execute("select * from table3")
            num_items_to_complete += len(cursor.fetchall())
            cursor.execute("select * from table4")
            num_items_to_complete += len(cursor.fetchall())

            items_completed = 0

            cursor.execute("select * from table1")
            ss = []
            for row in cursor:
                s = Sessions()
                s.id = row['id']
                ss.append(s)
                items_completed += 1
                if items_completed % 2000 == 0:
                    progress_recorder.set_progress(items_completed, num_items_to_complete)

            Sessions.objects.bulk_create(ss)

            cursor.execute("select * from table2")
            sfs = []
            for row in cursor:
                sf = SerialFrames()
                sf.id = uuid.uuid4()

                sfs.append(sf)
                items_completed += 1
                if items_completed % 2000 == 0:
                    progress_recorder.set_progress(items_completed, num_items_to_complete)

            SerialFrames.objects.bulk_create(sfs)

            cursor.execute("select * from table3")
            kes = []
            for row in cursor:
                k = KeyEvents()
                k.id = uuid.uuid4()

                kes.append(k)
                items_completed += 1
                if items_completed % 2000 == 0:
                    progress_recorder.set_progress(items_completed, num_items_to_complete)
            KeyEvents.objects.bulk_create(kes)

            cursor.execute("select * from table4")
            tss = []
            for row in cursor:
                t = TestSubjects()
                t.id = uuid.uuid4()

                tss.append(t)
                items_completed += 1
                if items_completed % 2000 == 0:
                    progress_recorder.set_progress(items_completed, num_items_to_complete)

            TestSubjects.objects.bulk_create(tss)

        end = time.time()
        print("time to complete db transaction was {0} seconds".format(end-start))
        print('done processing')


