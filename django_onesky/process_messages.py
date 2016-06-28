from django.core.management import call_command


class MakeMessagesProcess(object):

    def __call__(self, options):
        locale = options.get('locale')
        verbosity = options.get('verbosity')
        ignore = options.get('ignore')

        call_command('makemessages', locale=locale,
                     symlinks=True, verbosity=verbosity, ignore=ignore)


class CompileMessagesProcess(object):

    def __call__(self, options):
        locale = options.get('locale')
        verbosity = options.get('verbosity')

        management.call_command('compilemessages', locale=locale,
                                verbosity=verbosity)
