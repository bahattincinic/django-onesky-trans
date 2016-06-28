import os
import polib
from operator import itemgetter

from django.core import management
from django.core.management.base import CommandError
from django.conf import settings

from requests.exceptions import HTTPError

from gezi.libs.onesky import OneSkyClient


language_codes = map(itemgetter(0), settings.LANGUAGES)
client = OneSkyClient()


def run_makemessages(verbosity=0):
    management.call_command('makemessages', locale=language_codes,
                            symlinks=True, verbosity=verbosity)
    management.call_command('gmakemessages', locale=language_codes,
                            symlinks=True, domain='djangojs',
                            ignore_patterns=["node_modules", "bower",
                                             "static", "components"],
                            verbosity=verbosity)


def run_compilemessages(verbosity=0):
    management.call_command('compilemessages', locale=language_codes,
                            verbosity=verbosity)


def remove_fuzzy_translations(file_name):
    """
    This function removes the fuzzy translation strings + fuzzy flags by
    given translation file.

    :file_name string.
    """
    po_file = polib.pofile(file_name)
    for entry in po_file.fuzzy_entries():
        entry.msgstr = ''
        if entry.msgid_plural and isinstance(entry.msgstr_plural, dict):
            # Some languages (ru) have more than two plural forms.
            entry.msgstr_plural = {
                key: ''
                for key, val in entry.msgstr_plural.iteritems()
            }
        entry.flags.remove('fuzzy')
    po_file.save()


class Command(management.BaseCommand):
    help = "Updates .po translation files using makemessages and "\
           "uploads them to OneSky translation service. \n"\
           "Pushes new translation strings"\
           "from OneSky to django app and compiles messages."""

    def _get_error_message(self, response):
        return response.get("meta", {}).get("message", "")

    def _pull_translations(self):
        """
        Download Translation files from OneSky
        """
        project = settings.ONESKY_CONFIG['PO_TRANSLATE_PROJECT']
        status, response = client.get_project_languages(project)
        if status != 200:
            error_message = self._get_error_message(response)
            raise CommandError("Unable to retrieve project languages "
                               "for #%s. OneSky API status: %s, OneSky API"
                               "message: %s" % (project, status,
                                                error_message))

        project_languages = response.get("data", [])
        status, response = client.get_project_file_list(project)
        if status != 200:
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
                    200: 'Saving translation file %s for #%s.' % (
                        response.get('file_name', ''), project),
                    204: 'Unable to download translation file %s '
                         'for #%s. File has no content. OneSky API '
                         'status: %s, OneSky API message: %s"' % (
                        export_file_name, project, status,
                        self._get_error_message(response)),
                    500: 'Something went wrong with downloading '
                         'translation file %s for #%s. OneSky API '
                         'status: %s, OneSky API message: %s' % (
                        export_file_name, project, status,
                        self._get_error_message(response))
                }
                self.stdout.write(error_messages.get(status, 500))
        return file_names

    def _push_translations(self, file_names):
        """
        Send Translation Files to OneSky

        :file_names array
        """
        project = settings.ONESKY_CONFIG['PO_TRANSLATE_PROJECT']
        for language_code in language_codes:
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
            if not settings.ONESKY_CONFIG['ENABLED']:
                output = raw_input("OneSky Disabled in settings. Are you "
                                   "sure you want to continue with "
                                   "this process ? Type 'yes' to continue, or "
                                   "'no' to cancel")
                if output.lower() not in ['y', 'yes']:
                    raise CommandError('Process cancelled.')

                status, response = client.get_project_detail(
                    project_id=settings.ONESKY_CONFIG['PO_TRANSLATE_PROJECT'])
                if status != 200:
                    raise CommandError('%s project is invalid. You should '
                                       'check ONESKY_CONFIG' % project_id)

            file_names = self._pull_translations()
            run_makemessages(verbosity=options['verbosity'])

            self._push_translations(file_names)
            run_compilemessages(verbosity=options['verbosity'])
        except HTTPError as exc:
            raise CommandError("[%s] %s [%s]" % (exc.request.method,
                                                 exc.request.url,
                                                 exc.message))
