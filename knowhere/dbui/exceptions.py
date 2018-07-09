

class SchemaOutOfDateError(Exception):

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

    def __str__(self):
        return "The schema of the file you provided is out of date. Please ensure you are using the " \
                            "correct version of the collection software. To see the current schema, look at {0}"\
                            ". This occurred while parsing {1}".format(self.message, self.expression)


class DuplicateDataUploadError(Exception):

    def __init__(self, expression, original_msg):
        self.expression = expression
        self.original_msg = original_msg

    def __str__(self):
        return "The data you've entered appears to already exist. Please ensure you are uploading a file " \
                            "which has NOT already been uploaded. To see what's been uploaded, see knowhere.pison.io/admin"\
                            ". This occurred while parsing {0}. <br>Original message was: {1}"\
            .format(self.expression, self.original_msg)
