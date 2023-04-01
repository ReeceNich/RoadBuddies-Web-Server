from gunicorn.glogging import Logger

class CustomLogger(Logger):
    def access(self, resp, req, environ, request_time):
        atoms = self.atoms(resp, req, environ, request_time)
        if resp.status.startswith("200"):
            self.access_log.info(self.cfg.access_log_format % atoms)
        else:
            self.error_log.info(self.cfg.access_log_format % atoms)