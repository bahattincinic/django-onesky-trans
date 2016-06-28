import os

from optparse import make_option
from operator import itemgetter

from django.core import management
from django.core.management.base import CommandError
from django.conf import settings

from requests.exceptions import HTTPError

from django_onesky.client import OneSkyClient
from django_onesky.utils import remove_fuzzy_translations
from django_onesky.conf import app_settings
from django_onesky.status import (HTTP_200_OK, HTTP_204_NO_CONTENT,
                                  HTTP_500_INTERNAL_SERVER_ERROR)

client = OneSkyClient()


def run_makemessages(verbosity=0, locale):
    management.call_command('makemessages', locale=locale,
                            symlinks=True, verbosity=verbosity)
    management.call_command('gmakemessages', locale=locale,
                            symlinks=True, domain='djangojs',
                            ignore_patterns=["node_modules", "bower",
                                             "static", "components"],
                            verbosity=verbosity)


def run_compilemessages(verbosity=0, locale):
    management.call_command('compilemessages', locale=locale,
                            verbosity=verbosity)


class Command(management.BaseCommand):
    help = "Updates .po translation files using makemessages and "\
           "uploads them to OneSky translation service. \n"\
           "Pushes new translation strings"\
           "from OneSky to django app and compiles messages."""

    option_list = management.BaseCommand.option_list + (
        make_option('--locale', '-l', dest='locale', action='append',
                    help='locale(s) to process (e.g. de_AT). Default is to '
                         'process all. Can be used multiple times.'),
    )

    def _get_error_message(self, response):
        return response.get("meta", {}).get("message", "")

    def _pull_translations(self):
        """
        Download Translation files from OneSky
        """
        project = app_settings.PO_TRANSLATE_PROJECT
        status, response = client.get_project_languages(project)
        if status != HTTP_200_OK:
            error_message = self._get_error_message(response)
            raise CommandError("Unable to retrieve project languages "
                               "for #%s. OneSky API status: %s, OneSky API"
                               "message: %s" % (project, status,
                                                error_message))

        project_languages = response.get("data", [])
        status, response = client.get_project_file_list(project)
        if status != HTTP_200_OK:
            error_message = self._get_error_message(response)
            raise CommandError("Unable to retrieve project files "
                               "for #%s. OneSky API status: %s, OneSky API"
                               "message: %s" % (project, status,
                                                error_message))

        file_names = [
            file.get("file_name")
            for file in response.get("data", [])
            if file.get("file_name").endswith(".po")
        ]

        for file_name in file_names:
            for language in project_languages:
                export_file_name = os.path.join(
                    language.get("code", "unknown"),
                    "LC_MESSAGES", file_name)

                if not language.get("is_ready_to_publish"):
                    self.stdout.write("Unable to save translation file "
                                      "%s for #%s. Mark it as ready to "
                                      "publish." % (export_file_name, project))
                    continue

                # Download PO files from OneSky to locale folder.
                status, response = client.translation_export(
                    project, locale=language.get("code"),
                    source_file_name=file_name,
                    export_file_name=export_file_name)

                error_messages = {
                    HTTP_200_OK: 'Saving translation file %(filename)s '
                                 'for #%(project)s.',
                    HTTP_204_NO_CONTENT: 'Unable to download translation '
                                         'file %(export_file_name)s '
                                         'for #%(project)s. File has no '
                                         'content. OneSky API '
                                         'status: %(status)s, OneSky API '
                                         'message: %(message)s"',
                    HTTP_500_INTERNAL_SERVER_ERROR: 'Something went wrong '
                                                    'with downloading '
                                                    'translation file '
                                                    '%(export_file_name)s '
                                                    'for #%(project)s. '
                                                    'OneSky API  status: '
                                                    '%(status)s, OneSky API '
                                                    'message: %(message)s',
                }

                message = error_messages.get(status,
                                             HTTP_500_INTERNAL_SERVER_ERROR)
                self.stdout.write(message % {
                    'export_file_name': export_file_name,
                    'project': project,
                    'status': status,
                    'message': self._get_error_message(response),
                    'file_name': response.get('file_name', '')
                })
        return file_names

    def _push_translations(self, file_names, locale):
        """
        Send Translation Files to OneSky

        :file_names array
        """
        project = app_settings.PO_TRANSLATE_PROJECT
        for language_code in locale:
            for file_name in file_names:
                upload_file_name = os.path.join(client.locale_path,
                                                language_code,
                                                "LC_MESSAGES",
                                                file_name)
                if not os.path.isfile(upload_file_name):
                    continue

                remove_fuzzy_translations(upload_file_name)

                if upload_file_name.endswith(".po"):
                    client.project_file_upload(project, upload_file_name,
                                               file_format="GNU_PO",
                                               locale=language_code,
                                               is_keeping_all_strings=False)

    def handle(self, *args, **options):
        try:
            locale = options.get('locale',
                                 map(itemgetter(0), settings.LANGUAGES))

            if not app_settings.ENABLED:
                output = raw_input("OneSky Disabled in settings. Are you "
                                   "sure you want to continue with "
                                   "this process ? Type 'yes' to continue, or "
                                   "'no' to cancel")
                if output.lower() not in ['y', 'yes']:
                    raise CommandError('Process cancelled.')

            status, response = client.get_project_detail(
                project_id=app_settings.PO_TRANSLATE_PROJECT)
            if status != 200:
                raise CommandError('%s project is invalid. You should '
                                   'check ONESKY_CONFIG' % project_id)

            file_names = self._pull_translations()
            run_makemessages(verbosity=options['verbosity'], locale=locale)

            self._push_translations(file_names, locale)
            run_compilemessages(verbosity=options['verbosity'], locale=locale)
        except HTTPError as exc:
            raise CommandError("[%s] %s [%s]" % (exc.request.method,
                                                 exc.request.url,
                                                 exc.message))
