ENVIRONMENT = '%ENVIRONMENT%'

# folder locations, connection properties etc
settings = dict(
    process_prefix='Synergy',   # global prefix that is added to every process name started for synergy-data
    process_cwd='/mnt/tmp',     # daemonized process working directory, where it can create .cache and other folders

    log_directory='/mnt/log/synergy-data/', 
    pid_directory='/mnt/log/synergy-data/',

    perf_ticker_interval=30,                        # seconds between performance ticker messages
    debug=False,                                    # if True - logger is given additional "console" adapter
    under_test=False
)

# For now just two level... we can have configs for all deployments
# Need to have a better way for switching these
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
    'tests.test_time_helper',
    'tests.test_repeat_timer',
    'tests.test_process_starter',
]


def enable_test_mode():
    test_settings = dict(
        debug=True,
        under_test=True,
    )
    settings.update(test_settings)
