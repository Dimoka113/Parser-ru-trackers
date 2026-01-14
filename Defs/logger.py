
class Logger(object):
    """
### A class for displaying my project's logs.

##### Default level logging: 
`logger.level(Logger.types.INFO)`

##### Name Logger: 
Supports different names for different streams; by default, it has no name. 

`Logger(name="Your thread name")`

##### Support levels logging:
    `logger.debug`
    `logger.info`
    `logger.warn`
    `logger.error`
    `logger.crit`
    """
    thread_name = ""

    def __init__(self, name=""):
        self.thread_name = name
        
    class colors():
        green = "\033[32m"
        yellow = "\033[33m"
        red = "\033[31m"
        reset = "\033[0m"
        light_red = "\033[1;31m"


    class types():
        ERROR = ["error", "critical"]
        WARN = ["warn", "error", "critical"]
        INFO = ["info", "warn", "error", "critical"]
        DEBUG = ["debug", "info", "warn", "error", "critical"]

    logging = types.INFO

    def _log(self, tag, text, color, key):
        if key in self.logging:
            prefix = f"[{self.thread_name}]" if self.thread_name else ""
            print(f"{color}[{tag}]{f' {prefix}' if prefix else ''} {' '.join(str(x) for x in text)}{self.colors.reset}")

    @classmethod
    def level(self, log_level): self.logging = log_level

    def debug(self, *text): self._log("DEBUG", text, "", "debug")
    def info(self, *text): self._log("INFO", text, self.colors.green, "info")
    def warn(self, *text): self._log("WARN", text, self.colors.yellow, "warn")
    def error(self, *text): self._log("ERROR", text, self.colors.light_red, "error")
    def crit(self, *text): self._log("CRITICAL", text, self.colors.red, "critical")


