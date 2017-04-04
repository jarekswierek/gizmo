# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import csv
import settings


class GizmoDB(object):
    """Database tool.
    """
    FILENAME = settings.DATABASE_FILENAME
    SUCCESS_CODE = 1
    FAILURE_CODE = -1
    SUCCESS_RESPONSE = (SUCCESS_CODE, "DATA SAVED")
    FAILURE_RESPONSE = (FAILURE_CODE, "DATA NOT GIVEN")

    def save(self, data):
        """Save data to CSV file.
        """
        file_exists = os.path.isfile(self.FILENAME)
        try:
            with open(self.FILENAME, 'a') as csvfile:
                fieldnames = ['name', 'login', 'password']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(data)
        except Exception:
            response = self.FAILURE_RESPONSE
        else:
            response = self.SUCCESS_RESPONSE
        return response

    def get_accounts(self):
        """Method returns list of saved accounts.
        """
        data = self.load()
        return [row.get('name') for row in data]

    def load(self):
        """Load data from CSV file.
        """
        if os.path.exists(self.FILENAME):
            with open(self.FILENAME) as csvfile:
                reader = csv.DictReader(csvfile)
                data = [row for row in reader]
        else:
            data = []
        return data
