from django.core.management import call_command


class MakeMessagesProcess(object):

    def __call__(self, options):
        locale = options.get('locale')
        verbosity = options.get('verbosity', 0)
        ignore_patterns = options.get('ignore_patterns', [])

        call_command('makemessages', locale=locale,
                     symlinks=True, verbosity=verbosity,
                     ignore_patterns=ignore_patterns)


class CompileMessagesProcess(object):

    def __call__(self, options):
        locale = options.get('locale')
        verbosity = options.get('verbosity', 0)

        call_command('compilemessages', locale=locale, verbosity=verbosity)
