import requests
import time
import os
import hashlib

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from django_onesky.conf import package_settings


class OneSkyClient(object):
    """
    Simple python client around the OneSky API for managing translations.

    Documentation:
    https://github.com/onesky/api-documentation-platform
    """

    def __init__(self, locale_path=None):
        self.locale_path = locale_path or package_settings.DEFAULT_LOCALE_PATH

    def _get_authentication_params(self):
        """
        OneSky Token based Authentication

        Auth Params:
        - api_key string  Your own API key
        - timestamp   integer Current unix timestamp (GMT+0)
        - dev_hash    string  Calculate with timestamp and api_secret
        Formula: md5(concatenate(<timestamp>, <api_secret>))
        """
        timestamp = str(int(time.time()))
        dev_hash = hashlib.md5()
        dev_hash.update(timestamp)
        dev_hash.update(package_settings.PRIVATE_KEY)

        return {
            'timestamp': timestamp,
            'dev_hash': dev_hash.hexdigest(),
            'api_key': package_settings.PUBLIC_KEY
        }

    def _normalize_response(self, response):
        # a json response is requested.  some requests (such as
        # project_group_delete) don't return anything, so we'll just return
        # an empty dictionary.
        try:
            content = response.json()
        except ValueError:
            content = {}

        if (response.headers.get('content-disposition', '').
                startswith('attachment;')):
            # the response body is the contents of a file.  We save to a file
            # here and return 'filename' in the response dictionary.
            # the filename is in the 'content-disposition' header, in the form
            # "attachment; filename=hi-IN.po".  simplest to just split on = to
            # find it.
            short_filename = (
                response.headers['content-disposition'].split('=')[1]
            )

            absolute_filename = os.path.join(self.locale_path, short_filename)
            with open(absolute_filename, 'wb') as f:
                for chunk in response.iter_content():
                    f.write(chunk)

            content.update({'downloaded_filename': absolute_filename})
        return content

    def make_request(self, url, method='GET', **kwargs):
        """
        Make OneSky Request

        :url endpoint
        :method GET|POST...
        """
        base_url = package_settings.BASE_URL

        # Send auth credentials for every request.
        params = kwargs.pop('params', {})
        params.update(self._get_authentication_params())

        response = requests.request(url=urljoin(base_url, url),
                                    method=method,
                                    params=params,
                                    **kwargs)
        return response.status_code, self._normalize_response(response)

    def get_project_detail(self, project_id):
        """
        Detail of Project

        :param project_id (OneSky project id) int
        """
        return self.make_request(url="projects/%s/" % project_id)

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
