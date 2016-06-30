# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from .base import BaseOneSkyClient


class ProjectClient(BaseOneSkyClient):
    """
    Project Management
    """

    def get_project_detail(self, project_id):
        """
        Detail of Project

        :param project_id (OneSky project id) int
        """
        return self.make_request(url="projects/%s/" % project_id)

    def remove_project(self, project_id):
        """
        Remove project

        :param project_id (OneSky project id) int
        """
        return self.make_request(url="projects/%s/" % project_id,
                                 method="DELETE")

    def update_project(self, project_id, name):
        """
        Update Project

        :param name (New project name) str
        """
        return self.make_request(url="projects/%s/" % project_id,
                                 params={'name': name},
                                 method="PUT")

    def get_project_languages(self, project_id):
        """
        List languages of a project

        :param project_id (OneSky project id) int
        """
        return self.make_request(url="projects/%s/languages" % project_id)

    def get_project_file_list(self, project_id, page=1):
        """
        List of uploaded files for given project.

        :param project_id (OneSky project id) int
        """
        return self.make_request(url="projects/%s/files" % project_id,
                                 params={'page': page})

    def project_file_upload(self, project_id, file_name,
                            file_format="GNU_PO", locale=None,
                            is_keeping_all_strings=None):
        """
        Add or update translations by file

        :param project_id (OneSky project id) int
        :param locale (language_code) str
        :param file_name (path of file) str
        :param file_format (file type like JSON, PO, CSV...)
        :param is_keeping_all_strings (For strings that cannot be found in
            newly uploaded file with same file name, keep those strings
            unchange if set to true) bool
        """
        params = {
            'file_format': file_format,
            'locale': locale,
            'is_keeping_all_strings': is_keeping_all_strings
        }
        with open(file_name, 'rb') as file_stream:
            files = {'file': ((os.path.basename(file_name), file_stream))}
            return self.make_request(url="projects/%s/files" % project_id,
                                     files=files,
                                     method='POST',
                                     params=params)

    def translation_export(self, project_id, locale, source_file_name,
                           export_file_name):
        """
        Download project translation

        :param locale (language_code) str
        :param source_file_name (Specify the name of the source file.) str
        :param export_file_name (
            Specify the name of export file that is the file to be returned.)
        """
        params = {
            "locale": locale,
            "source_file_name": source_file_name,
            "export_file_name": export_file_name
        }
        return self.make_request(url="projects/%s/translations" % project_id,
                                 params=params)
