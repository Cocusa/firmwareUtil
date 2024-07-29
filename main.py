import logging
import traceback
from services.logger_configurations import configure_init_log
from ui.app import MainWindow


if __name__ == "__main__":
    configure_init_log()

    try:
        app = MainWindow()
        app.mainloop()
    except Exception as ex:
        logging.error(str(ex) + "\n" + traceback.format_exc())
