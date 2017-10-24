# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import time
import os
import hashlib

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from django.conf import settings

from django_onesky.conf import app_settings


class BaseOneSkyClient(object):
    """
    Simple python client around the OneSky API for managing translations.

    Documentation:
    https://github.com/onesky/api-documentation-platform
    """

    def __init__(self, locale_path=None):
        self.locale_path = locale_path or settings.LOCALE_PATHS[0]

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
        dev_hash.update(timestamp.encode('utf-8'))
        dev_hash.update(app_settings.PRIVATE_KEY.encode('utf-8'))

        return {
            'timestamp': timestamp,
            'dev_hash': dev_hash.hexdigest(),
            'api_key': app_settings.PUBLIC_KEY
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

            # in some cases the locale of One Sky does not match the locale of django.
            # example: fy-NL => fy
            if app_settings.REPLACE_LOCALES is not None and len(app_settings.REPLACE_LOCALES) > 0:
                for one_sky_locale, django_locale in app_settings.REPLACE_LOCALES:
                    if one_sky_locale in short_filename:
                        short_filename = short_filename.replace(one_sky_locale, django_locale)

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
        base_url = app_settings.BASE_URL

        # Send auth credentials for every request.
        params = kwargs.pop('params', {})
        params.update(self._get_authentication_params())

        response = requests.request(url=urljoin(base_url, url),
                                    method=method,
                                    params=params,
                                    **kwargs)
        return response.status_code, self._normalize_response(response)
