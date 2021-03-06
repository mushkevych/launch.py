ENVIRONMENT = '%ENVIRONMENT%'

# folder locations, connection properties etc
settings = dict(
    process_prefix='Synergy',   # global prefix that is added to every process name started by launch.py
    process_cwd='/mnt/tmp',     # daemonized process working directory, where it can create .cache and other folders

    log_directory='/mnt/logs/launchpy/',
    pid_directory='/mnt/logs/launchpy/',

    perf_ticker_interval=60,    # seconds between performance tracker ticks

    debug=False,                # if True, logger.setLevel is set to DEBUG. Otherwise to INFO

    under_test=False            # marks execution of the Unit Tests
                                # if True, a console handler for STDOUT and STDERR are appended to the logger.
                                # Otherwise STDOUT and STDERR are redirected to .log files
)

# Update current dict with the environment-specific settings
try:
    overrides = __import__('settings_' + ENVIRONMENT)
except:
    overrides = __import__('settings_dev')
settings.update(overrides.settings)


# Modules to test and verify (pylint/pep8)
testable_modules = [
    'system',
    'workers',
]

test_cases = [
    'tests.test_repeat_timer',
    'tests.test_process_starter',
]


def enable_test_mode():
    if settings['under_test']:
        # test mode is already enabled
        return

    test_settings = dict(
        debug=True,
        under_test=True,
    )
    settings.update(test_settings)

    from tests.ut_process_context import register_unit_test_context
    register_unit_test_context()
