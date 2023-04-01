from gunicorn.glogging import Logger

class CustomLogger(Logger):
    def access(self, resp, req, environ, request_time):
        atoms = self.atoms(resp, req, environ, request_time)
        if resp.status.startswith("200"):
            self.access_log.info(self.cfg.access_log_format % atoms)
        else:
            self.error_log.info(self.cfg.access_log_format % atoms)

logconfig_dict = {
    "version": 1,
    "handlers": {
        "access_200_file": {
            "class": "logging.FileHandler",
            "filename": "access_200.log",
            "formatter": "generic",
        },
        "access_other_file": {
            "class": "logging.FileHandler",
            "filename": "access_other.log",
            "formatter": "generic",
        },
    },
    "loggers": {
        "gunicorn.access": {
            "handlers": ["access_200_file"],
            "level": "INFO",
        },
        "gunicorn.error": {
            "handlers": ["access_other_file"],
            "level": "INFO",
        },
    },
}