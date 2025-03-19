import logging
import coloredlogs


def log_init():
    logging.basicConfig(level=logging.INFO)

    coloredlogs.install(
        level='INFO',
        fmt='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s',
        field_styles={
            'levelname': {
                'color': 'cyan'
            },
            'message': {
                'color': 'green'
            }
        },
        level_styles={
            'info': {
                'color': 'green'
            },
            'warning': {
                'color': 'white'
            },
            'error': {
                'color': 'red'
            },
            'critical': {
                'color': 'magenta'
            },
            'debug': {
                'color': 'white'
            }
        }
    )
