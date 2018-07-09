from django.db import models
import uuid


class Sessions(models.Model):
    id = models.CharField(primary_key=True, max_length=255)


class KeyEvents(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)


class SerialFrames(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)


class TestSubjects(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
