import argparse
import codecs
import contextlib
import io
import os
import os.path as osp
import sys
import traceback
import warnings
from pathlib import Path
from typing import AnyStr

import yaml
from loguru import logger
# Aggiunto QtCore, QtGui e QtWidgets negli import
from PyQt5 import QtCore, QtGui, QtWidgets

from labelme import __appname__
from labelme import __version__
from labelme.app import MainWindow
from labelme.config import get_user_config_file
from labelme.utils import newIcon


class _LoggerIO(io.StringIO):
    def write(self, s: AnyStr) -> int:
        assert isinstance(s, str)
        if stripped_s := s.strip():
            logger.debug(stripped_s)
        return len(s)

    def flush(self) -> None:
        pass

    def writable(self) -> bool:
        return True

    def readable(self) -> bool:
        return False

    def seekable(self) -> bool:
        return False

    @property
    def closed(self) -> bool:
        return False


def _setup_loguru(logger_level: str) -> None:
    try:
        logger.remove(handler_id=0)
    except ValueError:
        pass

    if sys.stderr:
        logger.add(sys.stderr, level=logger_level)

    cache_dir: str
    if os.name == "nt":
        cache_dir = os.path.join(os.environ["LOCALAPPDATA"], "labelme")
    else:
        cache_dir = os.path.expanduser("~/.cache/labelme")

    os.makedirs(cache_dir, exist_ok=True)

    log_file = os.path.join(cache_dir, "labelme.log")
    logger.add(
        log_file,
        colorize=True,
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="gz",
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )


def _handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        sys.exit(0)

    traceback_str: str = "".join(
        traceback.format_exception(exc_type, exc_value, exc_traceback)
    )
    logger.critical(traceback_str)

    traceback_html: str = traceback_str.replace("\n", "<br/>").replace(" ", "&nbsp;")
    QtWidgets.QMessageBox.critical(
        None,
        "Error",
        f"An unexpected error occurred. The application will close.<br/><br/>{traceback_html}",
    )

    if app := QtWidgets.QApplication.instance():
        app.quit()
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", "-V", action="store_true", help="show version")
    parser.add_argument("--reset-config", action="store_true", help="reset qt config")
    parser.add_argument(
        "--logger-level",
        default="debug",
        choices=["debug", "info", "warning", "fatal", "error"],
        help="logger level",
    )
    parser.add_argument("path", nargs="?", help="image file, label file, or directory")
    parser.add_argument(
        "--output",
        help="output directory for saving annotation JSON files",
    )
    default_config_file = get_user_config_file()
    parser.add_argument(
        "--config",
        dest="config",
        help=f"config file or yaml-format string (default: {default_config_file})",
        default=default_config_file,
    )
    
    # ... (gli altri argomenti del parser rimangono invariati)
    parser.add_argument("--with-image-data", dest="with_image_data", action="store_true", default=argparse.SUPPRESS)
    parser.add_argument("--no-auto-save", dest="auto_save", action="store_false", default=argparse.SUPPRESS)
    parser.add_argument("--flags", help="flags", default=argparse.SUPPRESS)
    parser.add_argument("--labels", help="labels", default=argparse.SUPPRESS)
    parser.add_argument("--epsilon", type=float, help="epsilon", default=argparse.SUPPRESS)
    
    args = parser.parse_args()

    if args.version:
        print(f"{__appname__} {__version__}")
        sys.exit(0)

    _setup_loguru(logger_level=args.logger_level.upper())
    sys.excepthook = _handle_exception

    # Configurazione logica caricamento config
    config_from_args = args.__dict__
    config_from_args.pop("version")
    reset_config = config_from_args.pop("reset_config")
    filename = config_from_args.pop("path")
    output = config_from_args.pop("output")

    config_str: str = config_from_args.pop("config")
    if isinstance(config_loaded := yaml.safe_load(config_str), dict):
        config_overrides = config_loaded
        config_file = None
    else:
        config_overrides = {}
        config_file = Path(config_str)
        if not config_file.is_file():
            sys.exit(1)
    
    config_overrides.update(config_from_args)
    output_dir = output

    # Inizializzazione Applicazione
    app = QtWidgets.QApplication(sys.argv)
    
    # --- INIZIO AGGIUNTA SPLASH SCREEN ---
    # Recuperiamo l'icona usando la funzione helper di labelme
    icon_obj = newIcon("splash.png")
    
    if icon_obj.isNull():
        # Fallback: se l'icona non esiste, crea un rettangolo bianco
        splash_pix = QtGui.QPixmap(600, 400)
        splash_pix.fill(QtGui.QColor("white"))
    else:
        # Trasformiamo la QIcon in QPixmap (es. 500x500)
        splash_pix = icon_obj.pixmap(500, 500)

    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    
    splash.showMessage(
        "Caricamento  vvLabeler...", 
        QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, 
        QtCore.Qt.black
    )
    
    app.processEvents() 
    # --- FINE AGGIUNTA SPLASH SCREEN ---

    app.setStyle("Fusion")
    app.setPalette(QtWidgets.QStyleFactory.create("Fusion").standardPalette())
    app.setApplicationName(__appname__)
    app.setWindowIcon(newIcon("icona_vici.jpg"))

    # Creazione della finestra principale
    win = MainWindow(
        config_file=config_file,
        config_overrides=config_overrides,
        filename=filename,
        output_dir=output_dir,
    )

    if reset_config:
        win.settings.clear()
        sys.exit(0)

    with contextlib.redirect_stderr(new_target=_LoggerIO()):
        win.show()
        win.raise_()
        
        # Chiude lo splash screen quando la finestra principale è pronta
        splash.finish(win)
        
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
