from datetime import datetime

settings = dict(
    process_cwd = '/tmp',   # daemonized process working directory, where it can create .cache and other folders

    log_directory='/var/log/synergy-data/',
    pid_directory='/var/log/synergy-data/',
    perf_ticker_interval=10,                                            # seconds between performance ticker messages
    synergy_start_timestamp=datetime.utcnow().strftime('%Y%m%d%H'),    # precision is process dependent
    debug=True
)
