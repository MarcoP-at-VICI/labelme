# from __future__ import annotations

# import enum
# import functools
# import html
# import math
# import os
# import os.path as osp
# import platform
# import re
# import subprocess
# import time
# import webbrowser
# from collections.abc import Callable
# from pathlib import Path
# from typing import Literal
# from typing import NamedTuple
# import math
        

# import imgviz
# import natsort
# import numpy as np
# import osam
# from loguru import logger
# from numpy.typing import NDArray
# from PyQt5 import QtCore
# from PyQt5 import QtGui
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QMessageBox
# import cv2
# import numpy as np
# from qtpy import QtCore

# from labelme import __appname__
# from labelme import __version__
# from labelme._automation import bbox_from_text
# from labelme._automation._osam_session import OsamSession
# from labelme._label_file import LabelFile
# from labelme._label_file import LabelFileError
# from labelme._label_file import ShapeDict
# from labelme.config import load_config
# from labelme.shape import Shape
# from labelme.widgets import AiAssistedAnnotationWidget
# from labelme.widgets import AiTextToAnnotationWidget
# from labelme.widgets import BrightnessContrastDialog
# from labelme.widgets import Canvas
# from labelme.widgets import FileDialogPreview
# from labelme.widgets import LabelDialog
# from labelme.widgets import LabelListWidget
# from labelme.widgets import LabelListWidgetItem
# from labelme.widgets import StatusStats
# from labelme.widgets import ToolBar
# from labelme.widgets import UniqueLabelQListWidget
# from labelme.widgets import ZoomWidget
# from labelme.widgets import download_ai_model

# from . import utils

# # handle high-dpi scaling issue
# # https://leomoon.com/journal/python/high-dpi-scaling-in-pyqt5
# if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
#     QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
#     QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


# LABEL_COLORMAP: NDArray[np.uint8] = imgviz.label_colormap()


# class _ZoomMode(enum.Enum):
#     FIT_WINDOW = enum.auto()
#     FIT_WIDTH = enum.auto()
#     MANUAL_ZOOM = enum.auto()


# _AI_TEXT_TO_ANNOTATION_CREATE_MODE_TO_SHAPE_TYPE: dict[
#     str, Literal["mask", "polygon", "rectangle"]
# ] = {
#     "ai_mask": "mask",
#     "ai_polygon": "polygon",
#     "polygon": "polygon",
#     "rectangle": "rectangle",
# }


# class _StatusBarWidgets(NamedTuple):
#     message: QtWidgets.QLabel
#     stats: StatusStats


# class _CanvasWidgets(NamedTuple):
#     canvas: Canvas
#     zoom_widget: ZoomWidget
#     scroll_bars: dict[Qt.Orientation, QtWidgets.QScrollBar]


# class _DockWidgets(NamedTuple):
#     flag_dock: QtWidgets.QDockWidget
#     flag_list: QtWidgets.QListWidget
#     shape_dock: QtWidgets.QDockWidget
#     label_list: LabelListWidget
#     label_dock: QtWidgets.QDockWidget
#     unique_label_list: UniqueLabelQListWidget
#     file_dock: QtWidgets.QDockWidget
#     file_search: QtWidgets.QLineEdit
#     file_list: QtWidgets.QListWidget


# class _Actions(NamedTuple):
#     about: QtWidgets.QAction
#     save: QtWidgets.QAction
#     save_as: QtWidgets.QAction
#     save_auto: QtWidgets.QAction
#     save_with_image_data: QtWidgets.QAction
#     change_output_dir: QtWidgets.QAction
#     open: QtWidgets.QAction
#     close: QtWidgets.QAction
#     delete_file: QtWidgets.QAction
#     toggle_keep_prev_mode: QtWidgets.QAction
#     toggle_keep_prev_brightness_contrast: QtWidgets.QAction
#     delete: QtWidgets.QAction
#     edit: QtWidgets.QAction
#     duplicate: QtWidgets.QAction
#     copy: QtWidgets.QAction
#     paste: QtWidgets.QAction
#     undo_last_point: QtWidgets.QAction
#     undo: QtWidgets.QAction
#     remove_point: QtWidgets.QAction
#     create_mode: QtWidgets.QAction
#     edit_mode: QtWidgets.QAction
#     create_rectangle_mode: QtWidgets.QAction
#     create_circle_mode: QtWidgets.QAction
#     create_line_mode: QtWidgets.QAction
#     create_point_mode: QtWidgets.QAction
#     create_line_strip_mode: QtWidgets.QAction
#     create_ai_polygon_mode: QtWidgets.QAction
#     create_ai_mask_mode: QtWidgets.QAction
#     open_next_img: QtWidgets.QAction
#     open_prev_img: QtWidgets.QAction
#     keep_prev_scale: QtWidgets.QAction
#     fit_window: QtWidgets.QAction
#     fit_width: QtWidgets.QAction
#     brightness_contrast: QtWidgets.QAction
#     zoom_in: QtWidgets.QAction
#     zoom_out: QtWidgets.QAction
#     zoom_org: QtWidgets.QAction
#     reset_layout: QtWidgets.QAction
#     fill_drawing: QtWidgets.QAction
#     hide_all: QtWidgets.QAction
#     show_all: QtWidgets.QAction
#     toggle_all: QtWidgets.QAction
#     open_dir: QtWidgets.QAction
#     zoom_widget_action: QtWidgets.QWidgetAction
#     draw: list[tuple[str, QtWidgets.QAction]]
#     zoom: tuple[ZoomWidget | QtWidgets.QAction, ...]
#     on_load_active: tuple[QtWidgets.QAction, ...]
#     on_shapes_present: tuple[QtWidgets.QAction, ...]
#     context_menu: tuple[QtWidgets.QAction, ...]
#     edit_menu: tuple[QtWidgets.QAction | None, ...]


# class _Menus(NamedTuple):
#     file: QtWidgets.QMenu
#     edit: QtWidgets.QMenu
#     view: QtWidgets.QMenu
#     help: QtWidgets.QMenu
#     recent_files: QtWidgets.QMenu
#     label_list: QtWidgets.QMenu


# class MainWindow(QtWidgets.QMainWindow):
#     _config_file: Path | None
#     _config: dict

#     _text_osam_session: OsamSession | None = None
#     _is_changed: bool = False
#     _copied_shapes: list[Shape]
#     _zoom_mode: _ZoomMode
#     _prev_opened_dir: str | None
#     _canvas_widgets: _CanvasWidgets
#     _status_bar: _StatusBarWidgets
#     _docks: _DockWidgets
#     _actions: _Actions
#     _menus: _Menus
#     _scalers: dict[_ZoomMode, Callable[[], float]]
#     _label_dialog: LabelDialog
#     _ai_annotation: AiAssistedAnnotationWidget
#     _ai_text: AiTextToAnnotationWidget

#     _output_dir: str | None
#     _filename: str | None
#     _image: QtGui.QImage
#     _label_file: LabelFile | None
#     _image_path: str | None
#     _recent_files: list[str]
#     _max_recent: int
#     _other_data: dict | None
#     _zoom_values: dict[str, tuple[_ZoomMode, int]]
#     _brightness_contrast_values: dict[str, tuple[int | None, int | None]]
#     _scroll_values: dict[Qt.Orientation, dict[str, float]]
#     _default_state: QtCore.QByteArray

#     def __init__(
#         self,
#         config_file: Path | None = None,
#         config_overrides: dict | None = None,
#         filename: str | None = None,
#         output_dir: str | None = None,
#     ) -> None:
#         super().__init__()
#         self.setWindowTitle(__appname__)
        

#         self._config_file, self._config = self._load_config(
#             config_file=config_file, config_overrides=config_overrides
#         )

#         # set default shape colors
#         Shape.line_color = QtGui.QColor(*self._config["shape"]["line_color"])
#         Shape.fill_color = QtGui.QColor(*self._config["shape"]["fill_color"])
#         Shape.select_line_color = QtGui.QColor(
#             *self._config["shape"]["select_line_color"]
#         )
#         Shape.select_fill_color = QtGui.QColor(
#             *self._config["shape"]["select_fill_color"]
#         )
#         Shape.vertex_fill_color = QtGui.QColor(
#             *self._config["shape"]["vertex_fill_color"]
#         )
#         Shape.hvertex_fill_color = QtGui.QColor(
#             *self._config["shape"]["hvertex_fill_color"]
#         )

#         # Set point size from config file
#         Shape.point_size = self._config["shape"]["point_size"]

#         self._copied_shapes = []

#         self._label_dialog = LabelDialog(
#             parent=self,
#             labels=self._config["labels"],
#             sort_labels=self._config["sort_labels"],
#             show_text_field=self._config["show_label_text_field"],
#             completion=self._config["label_completion"],
#             fit_to_content=self._config["fit_to_content"],
#             flags=self._config["label_flags"],
#         )

#         self._prev_opened_dir = None
#         self._docks = self._setup_dock_widgets()

#         self.setAcceptDrops(True)
#         self._canvas_widgets = self._setup_canvas()
#         self._canvas_widgets.canvas.selectionChanged.connect(self.sync_selection_to_list) #attiva la selezione delle linee automatiche
#         self._actions = self._setup_actions()
#         self._scalers = {
#             _ZoomMode.FIT_WINDOW: self.scaleFitWindow,
#             _ZoomMode.FIT_WIDTH: self.scaleFitWidth,
#             _ZoomMode.MANUAL_ZOOM: lambda: 1,
#         }
#         self._menus = self._setup_menus()

#         self._ai_annotation = AiAssistedAnnotationWidget(
#             default_model=self._config["ai"]["default"],
#             on_model_changed=self._canvas_widgets.canvas.set_ai_model_name,
#             parent=self,
#         )
#         self._ai_annotation.setEnabled(False)

#         self._ai_text = AiTextToAnnotationWidget(
#             on_submit=self._submit_ai_prompt, parent=self
#         )
#         self._ai_text.setEnabled(False)

#         self._setup_toolbars()

#         self._status_bar = self._setup_status_bar()

#         self._setup_app_state(output_dir=output_dir, filename=filename)

#         self.updateFileMenu()

#         self._canvas_widgets.zoom_widget.valueChanged.connect(self._paint_canvas)

#         self.populateModeActions()

#     def _setup_actions(self) -> _Actions:
#         action = functools.partial(utils.newAction, self)
#         shortcuts = self._config["shortcuts"]

#         about = action(
#             text=f"&About {__appname__}",
#             slot=functools.partial(
#                 QMessageBox.about,
#                 self,
#                 f"About {__appname__}",
#                 f"""
# <h3>{__appname__}</h3>
# <p>Image Polygonal Annotation with Python</p>
# <p>Version: {__version__}</p>
# <p>Author: Kentaro Wada</p>
# <p>
#     <a href="https://labelme.io">Homepage</a> |
#     <a href="https://labelme.io/docs">Documentation</a> |
#     <a href="https://labelme.io/docs/troubleshoot">Troubleshooting</a>
# </p>
# <p>
#     <a href="https://github.com/wkentaro/labelme">GitHub</a> |
#     <a href="https://x.com/labelmeai">Twitter/X</a>
# </p>
# """,
#             ),
#         )
#         save = action(
#             text=self.tr("&Save\n"),
#             slot=self.saveFile,
#             shortcut=shortcuts["save"],
#             icon="floppy-disk.svg",
#             tip=self.tr("Save labels to file"),
#             enabled=False,
#         )
#         save_as = action(
#             text=self.tr("&Save As"),
#             slot=self.saveFileAs,
#             shortcut=shortcuts["save_as"],
#             icon="floppy-disk.svg",
#             tip=self.tr("Save labels to a different file"),
#             enabled=False,
#         )
#         save_auto = action(
#             text=self.tr("Save &Automatically"),
#             tip=self.tr("Save automatically"),
#             checkable=True,
#             enabled=True,
#         )
#         save_auto.setChecked(self._config["auto_save"])
#         save_with_image_data = action(
#             text=self.tr("Save With Image Data"),
#             slot=self.enableSaveImageWithData,
#             tip=self.tr("Save image data in label file"),
#             checkable=True,
#             checked=self._config["with_image_data"],
#         )
#         change_output_dir = action(
#             text=self.tr("&Change Output Dir"),
#             slot=self.changeOutputDirDialog,
#             shortcut=shortcuts["save_to"],
#             icon="folders.svg",
#             tip=self.tr("Change where annotations are loaded/saved"),
#         )
#         open_ = action(
#             text=self.tr("&Open\n"),
#             slot=self._open_file_with_dialog,
#             shortcut=shortcuts["open"],
#             icon="folder-open.svg",
#             tip=self.tr("Open image or label file"),
#         )
#         open_dir = action(
#             text=self.tr("Open Dir"),
#             slot=self._open_dir_with_dialog,
#             shortcut=shortcuts["open_dir"],
#             icon="folder-open.svg",
#             tip=self.tr("Open Dir"),
#         )
#         close = action(
#             text=self.tr("&Close"),
#             slot=self.closeFile,
#             shortcut=shortcuts["close"],
#             icon="x-circle.svg",
#             tip=self.tr("Close current file"),
#         )
#         delete_file = action(
#             text=self.tr("&Delete File"),
#             slot=self.deleteFile,
#             shortcut=shortcuts["delete_file"],
#             icon="file-x.svg",
#             tip=self.tr("Delete current label file"),
#             enabled=False,
#         )
#         toggle_keep_prev_mode = action(
#             text=self.tr("Keep Previous Annotation"),
#             slot=self.toggleKeepPrevMode,
#             shortcut=shortcuts["toggle_keep_prev_mode"],
#             icon=None,
#             tip=self.tr('Toggle "keep previous annotation" mode'),
#             checkable=True,
#         )
#         toggle_keep_prev_mode.setChecked(self._config["keep_prev"])
#         toggle_keep_prev_brightness_contrast = action(
#             text=self.tr("Keep Previous Brightness/Contrast"),
#             slot=lambda: self._config.__setitem__(
#                 "keep_prev_brightness_contrast",
#                 not self._config["keep_prev_brightness_contrast"],
#             ),
#             checkable=True,
#             checked=self._config["keep_prev_brightness_contrast"],
#         )
#         delete = action(
#             self.tr("Delete Shapes"),
#             self.deleteSelectedShape,
#             shortcuts["delete_shape"],
#             icon="trash.svg",
#             tip=self.tr("Delete the selected shapes"),
#             enabled=False,
#         )
#         edit = action(
#             self.tr("&Edit Label"),
#             self._edit_label,
#             shortcuts["edit_label"],
#             icon="note-pencil.svg",
#             tip=self.tr("Modify the label of the selected shape"),
#             enabled=False,
#         )
#         duplicate = action(
#             self.tr("Duplicate Shapes"),
#             self.duplicateSelectedShape,
#             shortcuts["duplicate_shape"],
#             icon="copy.svg",
#             tip=self.tr("Create a duplicate of the selected shapes"),
#             enabled=False,
#         )
#         copy = action(
#             self.tr("Copy Shapes"),
#             self.copySelectedShape,
#             shortcuts["copy_shape"],
#             "copy_clipboard",
#             self.tr("Copy selected shapes to clipboard"),
#             enabled=False,
#         )
#         paste = action(
#             self.tr("Paste Shapes"),
#             self.pasteSelectedShape,
#             shortcuts["paste_shape"],
#             "paste",
#             self.tr("Paste copied shapes"),
#             enabled=False,
#         )
#         undo_last_point = action(
#             self.tr("Undo last point"),
#             self._canvas_widgets.canvas.undoLastPoint,
#             shortcuts["undo_last_point"],
#             icon="arrow-u-up-left.svg",
#             tip=self.tr("Undo last drawn point"),
#             enabled=False,
#         )
#         undo = action(
#             self.tr("Undo\n"),
#             self.undoShapeEdit,
#             shortcuts["undo"],
#             icon="arrow-u-up-left.svg",
#             tip=self.tr("Undo last add and edit of shape"),
#             enabled=False,
#         )
#         remove_point = action(
#             text=self.tr("Remove Selected Point"),
#             slot=self.removeSelectedPoint,
#             shortcut=shortcuts["remove_selected_point"],
#             icon="trash.svg",
#             tip=self.tr("Remove selected point from polygon"),
#             enabled=False,
#         )
#         create_mode = action(
#             text=self.tr("Create Polygons"),
#             slot=lambda: self._switch_canvas_mode(edit=False, createMode="polygon"),
#             shortcut=shortcuts["create_polygon"],
#             icon="polygon.svg",
#             tip=self.tr("Start drawing polygons"),
#             enabled=False,
#         )
#         edit_mode = action(
#             self.tr("Edit Shapes"),
#             lambda: self._switch_canvas_mode(edit=True),
#             shortcuts["edit_shape"],
#             icon="note-pencil.svg",
#             tip=self.tr("Move and edit the selected shapes"),
#             enabled=False,
#         )
#         create_rectangle_mode = action(
#             text=self.tr("Create Rectangle"),
#             slot=lambda: self._switch_canvas_mode(edit=False, createMode="rectangle"),
#             shortcut=shortcuts["create_rectangle"],
#             icon="rectangle.svg",
#             tip=self.tr("Start drawing rectangles"),
#             enabled=False,
#         )
#         create_circle_mode = action(
#             text=self.tr("Create Circle"),
#             slot=lambda: self._switch_canvas_mode(edit=False, createMode="circle"),
#             shortcut=shortcuts["create_circle"],
#             icon="circle.svg",
#             tip=self.tr("Start drawing circles"),
#             enabled=False,
#         )
#         create_line_mode = action(
#             text=self.tr("Create Line"),
#             slot=lambda: self._switch_canvas_mode(edit=False, createMode="line"),
#             shortcut=shortcuts["create_line"],
#             icon="line-segment.svg",
#             tip=self.tr("Start drawing lines"),
#             enabled=False,
#         )
#         create_point_mode = action(
#             text=self.tr("Create Point"),
#             slot=lambda: self._switch_canvas_mode(edit=False, createMode="point"),
#             shortcut=shortcuts["create_point"],
#             icon="circles-four.svg",
#             tip=self.tr("Start drawing points"),
#             enabled=False,
#         )
#         create_line_strip_mode = action(
#             text=self.tr("Create LineStrip"),
#             slot=lambda: self._switch_canvas_mode(edit=False, createMode="linestrip"),
#             shortcut=shortcuts["create_linestrip"],
#             icon="line-segments.svg",
#             tip=self.tr("Start drawing linestrip. Ctrl+LeftClick ends creation."),
#             enabled=False,
#         )
#         create_ai_polygon_mode = action(
#             self.tr("Create AI-Polygon"),
#             lambda: self._switch_canvas_mode(edit=False, createMode="ai_polygon"),
#             None,
#             "ai-polygon.svg",
#             self.tr("Start drawing ai_polygon. Ctrl+LeftClick ends creation."),
#             enabled=False,
#         )
#         create_ai_mask_mode = action(
#             self.tr("Create AI-Mask"),
#             lambda: self._switch_canvas_mode(edit=False, createMode="ai_mask"),
#             None,
#             "ai-mask.svg",
#             self.tr("Start drawing ai_mask. Ctrl+LeftClick ends creation."),
#             enabled=False,
#         )
#         # --- YOUR CUSTOM ACTION ---
#         actionAutoDetect = action(
#             text=self.tr("Auto-Detect Linee"),
#             slot=self.auto_detect_lines, # Ensure you've defined this method in the class!
#             shortcut="Ctrl+Shift+X",
#             icon="magic.svg", # Using a default icon available in LabelMe
#             tip=self.tr("Rileva automaticamente le linee nella vista corrente"),
#             enabled=False, # It starts disabled until an image is actually loaded
#         )

#         actionProjectlines = action(
#             text=self.tr("Projections Lines"),
#             slot=self.project_lines_preview, # Ensure you've defined this method in the class!
#             shortcut="Ctrl+Shift+P",
#             icon="Projection_and_rejection.svg", # Using a default icon available in LabelMe
#             tip=self.tr("Proietta le linee fino all'intersezione con i bordi dell'immagine"),
#             enabled=False, # It starts disabled until an image is actually loaded
#         )

#         actionProjectlines2txt = action(
#             text=self.tr("Save Projected Lines"),
#             slot=self.export_segments_to_txt, # Ensure you've defined this method in the class!
#             shortcut="Ctrl+Shift+K", 
#             tip=self.tr("Salva le linee proiettate in txt"),
#             enabled=False, # It starts disabled until an image is actually loaded
#         )

#         actionMergeLines = action(
#             text = self.tr("Merge Lines"),
#             slot = self.merge_parallel_lines,
#             shortcut="Ctrl+Shift+M", 
#             icon="merging.svg", # Using a default icon available in LabelMe
#             tip=self.tr("Fonde le linee parallele entro un certo epsilon"),
#             enabled=False
#         )
#         ######################################################
        
#         open_next_img = action(
#             text=self.tr("&Next Image"),
#             slot=self._open_next_image,
#             shortcut=shortcuts["open_next"],
#             icon="arrow-fat-right.svg",
#             tip=self.tr("Open next (hold Ctl+Shift to copy labels)"),
#             enabled=False,
#         )
#         open_prev_img = action(
#             text=self.tr("&Prev Image"),
#             slot=self._open_prev_image,
#             shortcut=shortcuts["open_prev"],
#             icon="arrow-fat-left.svg",
#             tip=self.tr("Open prev (hold Ctl+Shift to copy labels)"),
#             enabled=False,
#         )
#         keep_prev_scale = action(
#             self.tr("&Keep Previous Scale"),
#             self.enableKeepPrevScale,
#             tip=self.tr("Keep previous zoom scale"),
#             checkable=True,
#             checked=self._config["keep_prev_scale"],
#             enabled=True,
#         )
#         fit_window = action(
#             self.tr("&Fit Window"),
#             self.setFitWindow,
#             shortcuts["fit_window"],
#             icon="frame-corners.svg",
#             tip=self.tr("Zoom follows window size"),
#             checkable=True,
#             enabled=False,
#         )
#         fit_width = action(
#             self.tr("Fit &Width"),
#             self.setFitWidth,
#             shortcuts["fit_width"],
#             icon="frame-arrows-horizontal.svg",
#             tip=self.tr("Zoom follows window width"),
#             checkable=True,
#             enabled=False,
#         )
#         brightness_contrast = action(
#             self.tr("&Brightness Contrast"),
#             self.brightnessContrast,
#             None,
#             "brightness-contrast.svg",
#             self.tr("Adjust brightness and contrast"),
#             enabled=False,
#         )
#         zoom_in = action(
#             self.tr("Zoom &In"),
#             lambda _: self._add_zoom(increment=1.1),
#             shortcuts["zoom_in"],
#             icon="magnifying-glass-minus.svg",
#             tip=self.tr("Increase zoom level"),
#             enabled=False,
#         )
#         zoom_out = action(
#             self.tr("&Zoom Out"),
#             lambda _: self._add_zoom(increment=0.9),
#             shortcuts["zoom_out"],
#             icon="magnifying-glass-plus.svg",
#             tip=self.tr("Decrease zoom level"),
#             enabled=False,
#         )
#         zoom_org = action(
#             self.tr("&Original size"),
#             self._set_zoom_to_original,
#             shortcuts["zoom_to_original"],
#             icon="image-square.svg",
#             tip=self.tr("Zoom to original size"),
#             enabled=False,
#         )
#         reset_layout = action(
#             text=self.tr("Reset Layout"),
#             slot=self._reset_layout,
#             icon="layout-duotone.svg",
#         )
#         fill_drawing = action(
#             self.tr("Fill Drawing Polygon"),
#             self._canvas_widgets.canvas.setFillDrawing,
#             None,
#             icon="paint-bucket.svg",
#             tip=self.tr("Fill polygon while drawing"),
#             checkable=True,
#             enabled=True,
#         )
#         if self._config["canvas"]["fill_drawing"]:
#             fill_drawing.trigger()
#         hide_all = action(
#             self.tr("&Hide\nShapes"),
#             functools.partial(self.toggleShapes, False),
#             shortcuts["hide_all_shapes"],
#             icon="eye.svg",
#             tip=self.tr("Hide all shapes"),
#             enabled=False,
#         )
#         show_all = action(
#             self.tr("&Show\nShapes"),
#             functools.partial(self.toggleShapes, True),
#             shortcuts["show_all_shapes"],
#             icon="eye.svg",
#             tip=self.tr("Show all shapes"),
#             enabled=False,
#         )
#         toggle_all = action(
#             self.tr("&Toggle\nShapes"),
#             functools.partial(self.toggleShapes, None),
#             shortcuts["toggle_all_shapes"],
#             icon="eye.svg",
#             tip=self.tr("Toggle all shapes"),
#             enabled=False,
#         )

#         zoom_widget_action = QtWidgets.QWidgetAction(self)
#         zoom_box_layout = QtWidgets.QVBoxLayout()
#         zoom_label = QtWidgets.QLabel(self.tr("Zoom"))
#         zoom_label.setAlignment(Qt.AlignCenter)
#         zoom_box_layout.addWidget(zoom_label)
#         zoom_box_layout.addWidget(self._canvas_widgets.zoom_widget)
#         zoom_widget_action.setDefaultWidget(QtWidgets.QWidget())
#         zoom_widget_action.defaultWidget().setLayout(zoom_box_layout)
#         self._canvas_widgets.zoom_widget.setWhatsThis(
#             str(
#                 self.tr(
#                     "Zoom in or out of the image. Also accessible with "
#                     "{} and {} from the canvas."
#                 )
#             ).format(
#                 utils.fmtShortcut(f"{shortcuts['zoom_in']},{shortcuts['zoom_out']}"),
#                 utils.fmtShortcut(self.tr("Ctrl+Wheel")),
#             )
#         )
#         self._canvas_widgets.zoom_widget.setEnabled(False)

#         self._zoom_mode = _ZoomMode.FIT_WINDOW
#         fit_window.setChecked(Qt.Checked)

#         self._canvas_widgets.canvas.vertexSelected.connect(remove_point.setEnabled)

#         draw = [
#             ("polygon", create_mode),
#             ("rectangle", create_rectangle_mode),
#             ("circle", create_circle_mode),
#             ("point", create_point_mode),
#             ("line", create_line_mode),
#             ("linestrip", create_line_strip_mode),
#             ("ai_polygon", create_ai_polygon_mode),
#             ("ai_mask", create_ai_mask_mode),
#             ("Auto-Detect Linee", actionAutoDetect),
#             ("Projections Lines",actionProjectlines),
#             ("Save Projected Lines", actionProjectlines2txt),
#             ("Merge Lines", actionMergeLines)
#         ]
#         zoom = (
#             self._canvas_widgets.zoom_widget,
#             zoom_in,
#             zoom_out,
#             zoom_org,
#             fit_window,
#             fit_width,
#         )
#         on_load_active = (
#             close,
#             create_mode,
#             create_rectangle_mode,
#             create_circle_mode,
#             create_line_mode,
#             create_point_mode,
#             create_line_strip_mode,
#             create_ai_polygon_mode,
#             create_ai_mask_mode,
#             brightness_contrast,
#             actionAutoDetect,
#             actionProjectlines,
#             actionProjectlines2txt,
#             actionMergeLines,
#         )
#         on_shapes_present = (save_as, hide_all, show_all, toggle_all)
#         context_menu = (
#             *[draw_action for _, draw_action in draw],
#             actionAutoDetect,
#             actionProjectlines,
#             actionProjectlines2txt,
#             actionMergeLines,
#             edit_mode,
#             edit,
#             duplicate,
#             copy,
#             paste,
#             delete,
#             undo,
#             undo_last_point,
#             remove_point,
#         )
#         edit_menu = (
#             edit,
#             duplicate,
#             copy,
#             paste,
#             delete,
#             None,
#             undo,
#             undo_last_point,
#             None,
#             remove_point,
#             None,
#             toggle_keep_prev_mode,
#         )
    

        
#         return _Actions(
#             about=about,
#             save=save,
#             save_as=save_as,
#             save_auto=save_auto,
#             save_with_image_data=save_with_image_data,
#             change_output_dir=change_output_dir,
#             open=open_,
#             close=close,
#             delete_file=delete_file,
#             toggle_keep_prev_mode=toggle_keep_prev_mode,
#             toggle_keep_prev_brightness_contrast=toggle_keep_prev_brightness_contrast,
#             delete=delete,
#             edit=edit,
#             duplicate=duplicate,
#             copy=copy,
#             paste=paste,
#             undo_last_point=undo_last_point,
#             undo=undo,
#             remove_point=remove_point,
#             create_mode=create_mode,
#             edit_mode=edit_mode,
#             create_rectangle_mode=create_rectangle_mode,
#             create_circle_mode=create_circle_mode,
#             create_line_mode=create_line_mode,
#             create_point_mode=create_point_mode,
#             create_line_strip_mode=create_line_strip_mode,
#             create_ai_polygon_mode=create_ai_polygon_mode,
#             create_ai_mask_mode=create_ai_mask_mode,
#             open_next_img=open_next_img,
#             open_prev_img=open_prev_img,
#             keep_prev_scale=keep_prev_scale,
#             fit_window=fit_window,
#             fit_width=fit_width,
#             brightness_contrast=brightness_contrast,
#             zoom_in=zoom_in,
#             zoom_out=zoom_out,
#             zoom_org=zoom_org,
#             reset_layout=reset_layout,
#             fill_drawing=fill_drawing,
#             hide_all=hide_all,
#             show_all=show_all,
#             toggle_all=toggle_all,
#             open_dir=open_dir,
#             zoom_widget_action=zoom_widget_action,
#             draw=draw,
#             zoom=zoom,
#             on_load_active=on_load_active,
#             on_shapes_present=on_shapes_present,
#             context_menu=context_menu,
#             edit_menu=edit_menu,
#         )
#     # def auto_detect_lines(self):
#     #     """Estrae i segmenti LSD leggendo l'immagine dal disco (ricerca dinamica del path)."""
#     #     import math
#     #     import os
#     #     import numpy as np
#     #     import cv2
#     #     from qtpy import QtCore
#     #     from labelme.shape import Shape
        
#     #     print("DEBUG: Avvio auto-detect...") 

#     #     # 1. Cacciatore di variabili: cerchiamo in tutti i nomi usati storicamente da LabelMe
#     #     file_path = None
#     #     possibili_variabili = [
#     #         'imagePath', 'image_path', '_image_path', 
#     #         'filename', '_filename', 'filePath', '_image_file'
#     #     ]
        
#     #     for var_name in possibili_variabili:
#     #         val = getattr(self, var_name, None)
#     #         # Se la variabile è una stringa e corrisponde a un file reale sul disco
#     #         if isinstance(val, str) and os.path.exists(val):
#     #             file_path = val
#     #             print(f"DEBUG: Percorso trovato nella variabile 'self.{var_name}': {file_path}")
#     #             break

#     #     if not file_path:
#     #         print("DEBUG: Impossibile trovare il file fisico in nessuna variabile nota.")
#     #         self.statusBar().showMessage("Errore: Percorso file non trovato in memoria.")
#     #         return
            
#     #     print(f"DEBUG: Lettura OpenCV dal disco confermata.")

#     #     # 2. Lettura robusta (Windows-safe) e decodifica
#     #     img_arr = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        
#     #     if img_arr is None:
#     #         print("DEBUG: Fallimento decodifica immagine da OpenCV.")
#     #         return

#     #     gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
        
#     #     # 3. Rilevamento LSD
#     #     lsd = cv2.createLineSegmentDetector(0)
#     #     lines = lsd.detect(gray)[0]
        
#     #     if lines is None:
#     #         print("DEBUG: Nessun segmento rilevato.")
#     #         return
            
#     #     # 4. Filtraggio euclideo per rimuovere il rumore
#     #     min_length = 30.0 
#     #     filtered_lines = []
#     #     for line in lines:
#     #         x1, y1, x2, y2 = line[0]
#     #         length = math.hypot(x2 - x1, y2 - y1)
#     #         if length >= min_length:
#     #             filtered_lines.append((length, line[0]))
                
#     #     # 5. Protezione interfaccia PyQt5
#     #     max_gui_lines = 800
#     #     if len(filtered_lines) > max_gui_lines:
#     #         filtered_lines.sort(key=lambda x: x[0], reverse=True)
#     #         filtered_lines = filtered_lines[:max_gui_lines]

#     #     # 6. Iniezione nel Canvas (Adattato alla nuova architettura)
#     #     # Puntiamo alla nuova variabile che contiene il canvas
#     #     target_canvas = self._canvas_widgets.canvas
        
#     #     target_canvas.deSelectShape()
        
#     #     for length, line_coords in filtered_lines:
#     #         x1, y1, x2, y2 = line_coords
#     #         # shape = Shape(label="Linea", shape_type="line")
#     #         shape = Shape(label="Linea", shape_type="polygon") # cambiamo shape_type da "line" a "polygon". Un polygin può avere un numero variabile di punti (da 2 a infiniti).
#     #         shape.addPoint(QtCore.QPointF(x1, y1))
#     #         shape.addPoint(QtCore.QPointF(x2, y2))
           

#     #         # --- ATTRIBUTI FONDAMENTALI PER IL SALVATAGGIO JSON ---
#     #         shape.group_id = None
#     #         shape.description = ""
#     #         shape.flags = {}
#     #         # ------------------------------------------------------
#     #         shape.close() 
#     #         # Aggiunge al canvas
#     #         target_canvas.shapes.append(shape)
            
#     #         # Aggiunge alla lista laterale (con un controllo di sicurezza 
#     #         # nel caso anche labelList sia stata incapsulata)
#     #         # Usa il metodo nativo della finestra per registrare l'annotazione
#     #         if hasattr(self, 'addLabel'):
#     #             self.addLabel(shape)
#     #         elif hasattr(self, 'labelList'):
#     #             self.labelList.addShape(shape)
        
#     #     # --- SINCRONIZZAZIONE STATO INTERNO ---
#     #     # FONDAMENTALE: Salva le forme nel sistema Undo/Redo per evitare IndexError
#     #     if hasattr(target_canvas, 'storeShapes'):
#     #         target_canvas.storeShapes()       
            
#     #     target_canvas.update()
#     #     self.setDirty() 
#     #     msg = f"Iniettati {len(filtered_lines)} segmenti validi. Pronti per il salvataggio."
#     #     self.statusBar().showMessage(msg)
#     #     print(f"DEBUG: {msg}")
        
#     def get_next_label(self, prefix="L_"):
#         """Trova il numero più alto tra le etichette esistenti e suggerisce il successivo."""
#         max_id = -1
#         target_canvas = self._canvas_widgets.canvas
        
#         # Scansiona tutte le forme già presenti per trovare l'indice massimo
#         for shape in target_canvas.shapes:
#             if shape.label and shape.label.startswith(prefix):
#                 try:
#                     # Estrae la parte numerica (es. da "L_005" prende "005")
#                     num_str = shape.label.replace(prefix, "")
#                     num = int(num_str)
#                     if num > max_id:
#                         max_id = num
#                 except ValueError:
#                     continue
        
#         # Restituisce il prossimo ID formattato con tre cifre (es. L_011)
#         return f"{prefix}{max_id + 1:03d}"



        
#     def auto_detect_lines(self):
#         """Estrae i segmenti LSD, esegue lo Snap dei vertici contigui e li inietta nel Canvas."""
        
        
#         print("DEBUG: Avvio auto-detect con Snap...") 

#         # 1. Ricerca del file path (Invariato)
#         file_path = None
#         possibili_variabili = ['imagePath', 'image_path', '_image_path', 'filename', '_filename', 'filePath', '_image_file']
#         for var_name in possibili_variabili:
#             val = getattr(self, var_name, None)
#             if isinstance(val, str) and os.path.exists(val):
#                 file_path = val
#                 break

#         if not file_path:
#             self.statusBar().showMessage("Errore: Percorso file non trovato.")
#             return

#         # 2. Lettura e conversione (Invariato)
#         img_arr = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
#         if img_arr is None: return
#         gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
        
#         # 3. Rilevamento LSD
#         lsd = cv2.createLineSegmentDetector(0)
#         lines = lsd.detect(gray)[0]
#         if lines is None: return
            
#         # 4. Filtraggio e preparazione lista coordinate
#         min_length = 30.0 
#         raw_coords = []
#         for line in lines:
#             x1, y1, x2, y2 = line[0]
#             length = math.hypot(x2 - x1, y2 - y1)
#             if length >= min_length:
#                 raw_coords.append([x1, y1, x2, y2])
        
#         # --- [INIZIO LOGICA SNAP] ---
#         # Uniamo gli estremi che sono molto vicini (Epsilon pixel)
        
#         snap_epsilon = 5.0 
#         for i in range(len(raw_coords)):
#             for j in range(i + 1, len(raw_coords)):
#                 # Indici degli estremi: P1=(0,1), P2=(2,3)
#                 for idx_i in [(0,1), (2,3)]:
#                     for idx_j in [(0,1), (2,3)]:
#                         dist = math.hypot(raw_coords[i][idx_i[0]] - raw_coords[j][idx_j[0]], 
#                                           raw_coords[i][idx_i[1]] - raw_coords[j][idx_j[1]])
#                         if dist < snap_epsilon:
#                             # Il punto del segmento j "salta" esattamente sulle coordinate del segmento i
#                             raw_coords[j][idx_j[0]] = raw_coords[i][idx_i[0]]
#                             raw_coords[j][idx_j[1]] = raw_coords[i][idx_i[1]]
                        
#         #                 if dist < snap_epsilon:
#         #                     # Eseguiamo lo Snap: il punto del segmento j 
#         #                     # assume le coordinate esatte del segmento i
#         #                     raw_coords[j][idx_j[0]] = raw_coords[i][idx_i[0]]
#         #                     raw_coords[j][idx_j[1]] = raw_coords[i][idx_i[1]]
#         # # --- [FINE LOGICA SNAP] ---

#         # 5. Iniezione nel Canvas
#         # target_canvas = self._canvas_widgets.canvas
#         # target_canvas.deSelectShape()
#             # 4. Iniezione nel Canvas e sincronizzazione LabelList
#         target_canvas = self._canvas_widgets.canvas
#         # target_canvas.shapes = [] # Pulisce per evitare sovrapposizioni
            
#         # --- FIX ATTRIBUTE ERROR: Svuota la lista usando il nome corretto ---
#         # label_widget = getattr(self, 'labelList', getattr(self, 'label_list', None))
#         # if label_widget:
#         #     label_widget.clear()
        
#         # Limite per performance GUI
#         raw_coords = raw_coords[:800]

#         for idx, coords in enumerate(raw_coords):
#             x1_raw, y1_raw, x2_raw, y2_raw = coords
#             # --- CHIAMATA ALLO SNAP ---
#             # Applichiamo la "calamita" sia al punto d'inizio che a quello di fine
#             x1, y1 = self._apply_snap(x1_raw, y1_raw)
#             x2, y2 = self._apply_snap(x2_raw, y2_raw)
#             # --------------------------
            
#             # 2. GENERAZIONE ETICHETTA UNICA (Richiamo funzione)
#             # Questo garantisce che non ci siano conflitti nel file TXT/JSON
#             unique_label = self.get_next_label(prefix="L_")
                
#             shape = Shape(label=unique_label, shape_type="polygon")
#             shape.addPoint(QtCore.QPointF(x1, y1))
#             shape.addPoint(QtCore.QPointF(x2, y2))

#             shape.group_id = None
#             shape.description = ""
#             shape.flags = {}
#             shape.close() 

#             target_canvas.shapes.append(shape)
            
#             if hasattr(self, 'addLabel'):
#                 self.addLabel(shape)
#             elif hasattr(self, 'labelList'):
#                 self.labelList.addShape(shape)
        
#         # 6. Sincronizzazione Selezione (Punto 2 della tua richiesta)
#         # Colleghiamo il segnale del canvas per evidenziare la riga corrispondente
#         try:
#             target_canvas.selectionChanged.connect(self.sync_selection_to_list)
#         except:
#             pass # Evita errori se già connesso

#         if hasattr(target_canvas, 'storeShapes'):
#             target_canvas.storeShapes()       
            
#         target_canvas.update()
#         self.setDirty() 
#         self.statusBar().showMessage(f"Rilevati {len(raw_coords)} segmenti con Snap attivo.")
            
#     def sync_selection_to_list(self):
#         """Sincronizza click su linea e lista laterale senza crash."""
#         try:
#             canvas = self._canvas_widgets.canvas
#             # Accesso diretto alla lista etichette
#             label_list = getattr(self, 'labelList', None)
            
#             if not canvas.selectedShapes or label_list is None:
#                 return

#             shape = canvas.selectedShapes[-1]
#             # Accediamo alla view interna della lista etichette
#             label_list_widget = self._docks.label_list
#             label_list_widget.clearSelection()
        
#             for i in range(label_list_widget.count()):
#                 item = label_list_widget.item(i)
#                 # LabelMe memorizza la shape nei dati dell'item (Qt.UserRole)
#                 if item.data(QtCore.Qt.UserRole) == target_shape:
#                     item.setSelected(True)
#                     label_list_widget.scrollToItem(item)
#                     break
#         except Exception as e:
#             # Chiudendo il blocco try con except, il SyntaxError sparisce
#             print(f"Errore sincronizzazione: {e}")
#     # def sync_selection_to_list(self):
#     #     """Sincronizza il click sulla linea con la lista laterale."""
#     #     canvas = self._canvas_widgets.canvas
#     #     # Cerchiamo la vera QListWidget dentro il dock
#     #     label_list_dock = self._docks.label_list
        
#     #     # In LabelMe, la vera lista QListWidget è accessibile così:
#     #     inner_list = getattr(label_list_dock, 'labelList', None) or \
#     #                  getattr(label_list_dock, 'list_widget', None) or \
#     #                  label_list_dock # Fallback
        
#     #     if not canvas.selectedShapes or not hasattr(inner_list, 'count'):
#     #         return

#     #     shape = canvas.selectedShapes[-1]
#     #     inner_list.clearSelection()
        
#     #     # Ora .count() funzionerà perché siamo sulla QListWidget corretta
#     #     for i in range(inner_list.count()):
#     #         item = inner_list.item(i)
#     #         if getattr(item, 'shape', None) == shape:
#     #             item.setSelected(True)
#     #             inner_list.scrollToItem(item)
#     #             break

   
        
#     # def sync_selection_to_list(self):
#     #     """Sincronizza il Canvas con la lista laterale (Annotation List)."""
#     #     target_canvas = self._canvas_widgets.canvas
#     #     label_widget = getattr(self, 'labelList', getattr(self, 'label_list', None))
        
#     #     if not label_widget:
#     #         return

#     #     # Recuperiamo le forme selezionate sul canvas
#     #     selected_shapes = target_canvas.selectedShapes[-1]
        
#     #     # Puliamo la selezione precedente nella lista
#     #     label_widget.clearSelection()
        
#     #     if selected_shapes:
#     #         # Prendiamo l'ultima forma cliccata
#     #         shape = selected_shapes[-1]
#     #         for i in range(label_widget.count()):
#     #             item = label_widget.item(i)
#     #             # Verifichiamo il riferimento alla shape
#     #             if getattr(item, 'shape', None) == shape or item.data(QtCore.Qt.UserRole) == shape:
#     #                 item.setSelected(True)
#     #                 label_widget.scrollToItem(item)
#     #                 break

#     def _apply_snap(self, x, y, epsilon=10.0):
#         """Cerca un vertice vicino nel raggio epsilon e ne restituisce le coordinate precise."""
#         target_canvas = self._canvas_widgets.canvas
#         for shape in target_canvas.shapes:
#             for p in shape.points:
#                 dist = math.hypot(x - p.x(), y - p.y())
#                 if dist < epsilon:
#                     return p.x(), p.y()
#         return x, y
            
#     def project_lines_preview(self):
#         """Proietta ESCLUSIVAMENTE i segmenti adiacenti (P_i -> P_i+1) ai bordi."""
#         target_canvas = self._canvas_widgets.canvas
#         if not target_canvas.pixmap:
#             return
            
#         img_w = target_canvas.pixmap.width()
#         img_h = target_canvas.pixmap.height()
        
#         # Usiamo una lista temporanea per non modificare la lista mentre la cicliamo
#         original_shapes = list(target_canvas.shapes)
#         new_projected_shapes = []

#         for shape in original_shapes:
#             if len(shape.points) < 2:
#                 continue
            
#             # Iteriamo SOLO sulle coppie di punti adiacenti originali
#             for i in range(len(shape.points) - 1):
#                 p1 = shape.points[i]
#                 p2 = shape.points[i+1]
                
#                 x1, y1 = p1.x(), p1.y()
#                 x2, y2 = p2.x(), p2.y()

#                 dx, dy = x2 - x1, y2 - y1
#                 if abs(dx) < 1e-6 and abs(dy) < 1e-6: 
#                     continue

#                 # Calcolo geometrico della retta passante per i due punti consecutivi
#                 t_candidates = []
#                 if abs(dx) > 1e-10:
#                     t_candidates.extend([-x1 / dx, (img_w - x1) / dx])
#                 if abs(dy) > 1e-10:
#                     t_candidates.extend([-y1 / dy, (img_h - y1) / dy])

#                 valid_pts = []
#                 for t in t_candidates:
#                     ix, iy = x1 + t * dx, y1 + t * dy
#                     # Verifichiamo l'intersezione effettiva con il perimetro dell'immagine
#                     if -0.5 <= ix <= img_w + 0.5 and -0.5 <= iy <= img_h + 0.5:
#                         valid_pts.append((ix, iy))
                
#                 if len(valid_pts) >= 2:
#                     # Troviamo i due punti di uscita dai bordi per quel segmento specifico
#                     valid_pts.sort(key=lambda p: (p[0], p[1]))
#                     ps, pe = valid_pts[0], valid_pts[-1]
                    
#                     # Creiamo la proiezione come entità separata
#                     new_shape = Shape(label=shape.label, shape_type="line")
#                     new_shape.addPoint(QtCore.QPointF(ps[0], ps[1]))
#                     new_shape.addPoint(QtCore.QPointF(pe[0], pe[1]))
                    
#                     # Manteniamo i metadati per la ricerca
#                     new_shape.group_id = shape.group_id
#                     new_shape.close()
#                     new_projected_shapes.append(new_shape)

#         # SOSTITUZIONE: Rimuoviamo le polilinee "corte" e mettiamo i segmenti "lunghi"
#         # Questo evita che ri-premendo il tasto si creino proiezioni incrociate
#         target_canvas.shapes = new_projected_shapes
#         target_canvas.update()
#         self.setDirty() 
#         self.statusBar().showMessage(f"Proiettati {len(new_projected_shapes)} segmenti adiacenti.")

#     # def export_projected_to_txt(self):
#     #     """Salva le linee attualmente visibili (estese) in formato TXT."""
#     #     #1. SALVATAGGIO NATIVO (JSON)
#     #     # Chiamiamo la funzione nativa di LabelMe per assicurarci che lo stato sia salvato
#     #     try:
#     #         self.saveFile()
#     #     except Exception as e:
#     #         print(f"Nota: Salvataggio JSON saltato o fallito: {e}") # Apre la finestra di salvataggio standard o salva se già impostato
#     #     # 2. PREPARAZIONE DATI PER TXT
#     #     lines_output = [] # Inizializzazione fondamentale per evitare NameError
        
#     #     try:
#     #         # Recuperiamo le forme dal canvas
#     #         canvas = self._canvas_widgets.canvas
#     #         if not canvas or not hasattr(canvas, 'shapes'):
#     #             self.statusBar().showMessage("Errore: Canvas non accessibile.")
#     #             return

#     #         for shape in canvas.shapes:
#     #             if len(shape.points) >= 2:
#     #                 p1 = shape.points[0]
#     #                 p2 = shape.points[-1]
#     #                 # Formato x1 y1 x2 y2 con 2 decimali
#     #                 line_str = f"{p1.x():.2f} {p1.y():.2f} {p2.x():.2f} {p2.y():.2f}"
#     #                 lines_output.append(line_str)

#     #         if not lines_output:
#     #             self.statusBar().showMessage("Nessuna linea valida da esportare.")
#     #             return

#     #         # 3. DIALOGO DI SALVATAGGIO
#     #         save_path, _ = QtWidgets.QFileDialog.getSaveFileName(
#     #             self, "Esporta coordinate estese (TXT)", "", "TXT (*.txt)"
#     #         )
            
#     #         if save_path:
#     #             with open(save_path, 'w', encoding='utf-8') as f:
#     #                 f.write("\n".join(lines_output))
#     #             self.statusBar().showMessage(f"Esportate {len(lines_output)} linee in TXT.")
            
#     #     except Exception as e:
#     #         # Messaggio di errore dettagliato per il debugging
#     #         QtWidgets.QMessageBox.critical(self, "Errore", f"Errore nel salvataggio TXT: {str(e)}")
#     #         print(f"DEBUG ERROR: {e}")
#     def export_segments_to_txt(self):
#         """Salva JSON e TXT (x1, x2, y1, y2, H, W) in un colpo solo."""
#         import os
#         # Recupero dinamico del percorso file
#         img_path = getattr(self, 'imagePath', None) or getattr(self, '_image_path', None)
#         if not img_path:
#             # Ultima spiaggia: recupero dal caricatore di file
#             img_path = self.filename if hasattr(self, 'filename') else None

#         if not img_path or not os.path.exists(img_path):
#             self.statusBar().showMessage("Errore: Percorso immagine non trovato.")
#             return

#         # 1. SALVATAGGIO JSON (Metodo robusto)
#         json_path = os.path.splitext(img_path)[0] + ".json"
#         try:
#             # Usiamo il metodo di salvataggio diretto delle labels
#             self.saveLabels(json_path)
#         except Exception as e:
#             print(f"Errore salvataggio JSON: {e}")

#         # 2. GENERAZIONE TXT
#         canvas = self._canvas_widgets.canvas
#         img_w, img_h = canvas.pixmap.width(), canvas.pixmap.height()
        
#         lines_output = []
#         for shape in canvas.shapes:
#             # Scomponiamo ogni polilinea in segmenti reali
#             for i in range(len(shape.points) - 1):
#                 p1, p2 = shape.points[i], shape.points[i+1]
#                 # Formato richiesto: x1, x2, y1, y2, H, W
#                 lines_output.append(f"{p1.x():.2f}, {p2.x():.2f}, {p1.y():.2f}, {p2.y():.2f}, {img_h}, {img_w}")

#         txt_path = os.path.splitext(img_path)[0] + ".txt"
#         with open(txt_path, 'w', encoding='utf-8') as f:
#             f.write("\n".join(lines_output))
        
#         self.setDirty()
#         self.statusBar().showMessage(f"Dataset salvato: {len(lines_output)} segmenti.")      
#     # def export_segments_to_txt(self):
#     #     """Salva i segmenti reali nel formato (x1, x2, y1, y2, H, W)."""
#     #     target_canvas = self._canvas_widgets.canvas
#     #     if not target_canvas or not target_canvas.pixmap:
#     #         self.statusBar().showMessage("Errore: Immagine non caricata.")
#     #         return
            
#     #     # 1. Recupero dimensioni immagine (H, W)
#     #     img_w = target_canvas.pixmap.width()
#     #     img_h = target_canvas.pixmap.height()
        
#     #     lines_output = []

#     #     try:
#     #         for shape in target_canvas.shapes:
#     #             num_points = len(shape.points)
#     #             if num_points < 2:
#     #                 continue

#     #             # Gestione polilinee: salviamo ogni segmento consecutivo separatamente
#     #             # Se è un poligono chiuso, colleghiamo l'ultimo al primo
#     #             is_closed = shape.shape_type == "polygon" and getattr(shape, 'is_closed', True)
#     #             range_limit = num_points if is_closed else num_points - 1

#     #             for i in range(range_limit):
#     #                 p1 = shape.points[i]
#     #                 p2 = shape.points[(i + 1) % num_points]
                    
#     #                 # Coordinate reali (senza proiezioni ai bordi)
#     #                 x1, y1 = p1.x(), p1.y()
#     #                 x2, y2 = p2.x(), p2.y()

#     #                 # 2. Formattazione richiesta: (x1, x2, y1, y2, altezza, larghezza)
#     #                 # Usiamo i nomi delle variabili per chiarezza nel file o solo i numeri? 
#     #                 # Qui metto il formato numerico pulito per il parsing della tua rete neurale:
#     #                 line_str = f"{x1:.2f}, {x2:.2f}, {y1:.2f}, {y2:.2f}, {img_h}, {img_w}"
#     #                 lines_output.append(line_str)

#     #         if not lines_output:
#     #             self.statusBar().showMessage("Nessun segmento da esportare.")
#     #             return

            
#     #         # 3. Dialogo di salvataggio
#     #         base_path = os.path.splitext(self.imagePath)[0] if hasattr(self, 'imagePath') else ""
#     #         save_path, _ = QtWidgets.QFileDialog.getSaveFileName(
#     #             self, "Esporta Dataset Reale", "", "TXT (*.txt)"
#     #         )
            
#     #         if save_path:
#     #             with open(save_path, 'w', encoding='utf-8') as f:
#     #                 # Scriviamo ogni segmento su una nuova riga
#     #                 f.write("\n".join(lines_output))
#     #             self.statusBar().showMessage(f"Salvato: {len(lines_output)} segmenti in formato (x1,x2,y1,y2,H,W).")
            
#     #     except Exception as e:
#     #         QtWidgets.QMessageBox.critical(self, "Errore Export", f"Errore: {str(e)}")

#     # def merge_parallel_lines(self):
#     #     """Fonde segmenti paralleli e vicini (utilissimo per pulire l'output LSD)."""
#     #     import numpy as np
#     #     canvas = self._canvas_widgets.canvas
#     #     if not canvas.shapes: return

#     #     # Parametri di tolleranza per la tua ricerca
#     #     DIST_EPSILON = 15.0      # Pixel di distanza massima tra i segmenti
#     #     ANGLE_EPSILON = 2.0      # Gradi di differenza massima per il parallelismo

#     #     shapes = list(canvas.shapes)
#     #     merged_list = []
#     #     used = [False] * len(shapes)

#     #     for i in range(len(shapes)):
#     #         # Questa riga deve avere 1 tab (o 4 spazi) di rientro
#     #         if used[i] or len(shapes[i].points) < 2: 
#     #             continue
            
#     #         group = [shapes[i]]
#     #         used[i] = True
            
#     #         # Parametri linea i
#     #         p1, p2 = shapes[i].points[0], shapes[i].points[1]
#     #         vec_i = np.array([p2.x() - p1.x(), p2.y() - p1.y()])
#     #         angle_i = np.arctan2(vec_i[1], vec_i[0]) % np.pi

#     #         for j in range(i + 1, len(shapes)):
#     #             # Questo blocco deve avere 2 tab (o 8 spazi)
#     #             if used[j] or len(shapes[j].points) < 2: 
#     #                 continue
                
#     #             p3, p4 = shapes[j].points[0], shapes[j].points[1]
#     #             vec_j = np.array([p4.x() - p3.x(), p4.y() - p3.y()])
#     #             angle_j = np.arctan2(vec_j[1], vec_j[0]) % np.pi

#     #             # Verifica parallelismo
#     #             diff_angle = abs(angle_i - angle_j)
#     #             diff_angle = min(diff_angle, np.pi - diff_angle)

#     #             if diff_angle < np.radians(ANGLE_EPSILON):
#     #                 # Verifica distanza ortogonale
#     #                 mid_j = np.array([(p3.x() + p4.x())/2, (p3.y() + p4.y())/2])
#     #                 dist = self._dist_point_to_line(mid_j, p1, p2)
                    
#     #                 if dist < DIST_EPSILON:
#     #                     group.append(shapes[j])
#     #                     used[j] = True
            
#     #         # Parametri linea i
#     #         p1, p2 = shapes[i].points[0], shapes[i].points[1]
#     #         vec_i = np.array([p2.x() - p1.x(), p2.y() - p1.y()])
#     #         angle_i = np.arctan2(vec_i[1], vec_i[0]) % np.pi

#     #         for j in range(i + 1, len(shapes)):
#     #             if used[j] or len(shapes[j].points) < 2: continue
                
#     #             p3, p4 = shapes[j].points[0], shapes[j].points[1]
#     #             vec_j = np.array([p4.x() - p3.x(), p4.y() - p3.y()])
#     #             angle_j = np.arctan2(vec_j[1], vec_j[0]) % np.pi

#     #             # Verifica parallelismo
#     #             diff_angle = abs(angle_i - angle_j)
#     #             diff_angle = min(diff_angle, np.pi - diff_angle)

#     #             if diff_angle < np.radians(ANGLE_EPSILON):
#     #                 # Verifica distanza tra le rette (proiezione ortogonale)
#     #                 mid_j = np.array([(p3.x() + p4.x())/2, (p3.y() + p4.y())/2])
#     #                 dist = self._dist_point_to_line(mid_j, p1, p2)
                    
#     #                 if dist < DIST_EPSILON:
#     #                     group.append(shapes[j])
#     #                     used[j] = True

#     #         # Creazione della LINEA MEDIA
#     #         if len(group) > 1:
#     #             new_shape = self._create_average_line(group)
#     #             merged_list.append(new_shape)
#     #         else:
#     #             merged_list.append(shapes[i])
    
#     #     # Aggiornamento UI (Safe Mode)
        
#     #     # canvas.shapes = merged_list
#     #     # label_widget = getattr(self, 'labelList', getattr(self, 'label_list', None))
#     #     # if label_widget:
#     #     #     label_widget.clear()
#     #     #     for s in merged_list:
#     #     #         self.addLabel(s)
        
#     #     # canvas.update()
#     #     # self.setDirty()
#     #     # self.statusBar().showMessage(f"Merge: {len(merged_list)} linee risultanti.")


#     #     # # --- PARTE FINALE CORRETTA ---
#     #     # # 1. Pulizia totale sincronizzata
#     #     # canvas.shapes = []
#     #     # label_widget = getattr(self, 'labelList', getattr(self, 'label_list', None))
#     #     # if label_widget:
#     #     #         label_widget.clear()

#     #     # # 2. Re-inserimento tramite addLabel
#     #     # # Questo risolve il crash ValueError: list.remove(x) perché registra la shape
#     #     # for s in merged_list:
#     #     #         # Se la linea è nuova, diamogli un ID progressivo invece di "Linea_Merged"
#     #     #         if s.label == "Linea_Merged":
#     #     #             s.label = self.get_next_label(prefix="L_")
            
#     #     #         self.addLabel(s) # Registra l'item nella lista e lo lega alla shape
#     #     #         canvas.shapes.append(s) # Aggiunge la shape al canvas ufficialmente
#     #     # self.setEditMode() 
#     #     # canvas.setEditing(True) #Aggiunta
#     #     # canvas.update() #Aggiutna
#     #     # self.setDirty()
#     #     # self._actions.save.setEnabled(True)
#     #     # self.statusBar().showMessage(f"Merge completato: {len(merged_list)} linee.")
         
         
#     #     # 1. Pulizia "profonda": scolleghiamo i vecchi riferimenti
#     #     self._canvas_widgets.canvas.shapes = []
        
#     #     # Cerchiamo di pulire la lista in modo sicuro
#     #     # Proviamo i due nomi comuni che LabelMe usa per il widget lista
#     #     l_widget = getattr(self, 'labelList', None) or getattr(self, 'label_list', None)
#     #     if l_widget is not None:
#     #         try:
#     #             l_widget.clear()
#     #         except AttributeError:
#     #             # Se è un oggetto complesso, cerchiamo la view interna
#     #             if hasattr(l_widget, 'view'):
#     #                 l_widget.view.clear()
        
#     #     # 2. Re-iniezione controllata con registrazione ufficiale
#     #     for s in merged_list:
#     #         # Assegnazione ID progressivo
#     #         if s.label == "Linea_Merged" or not s.label:
#     #             s.label = self.get_next_label(prefix="L_")
            
#     #         # REGISTRAZIONE UFFICIALE: Questo lega la Shape alla MainWindow
#     #         # Impedisce il crash "ValueError: x not in list" durante la cancellazione
#     #         self.addLabel(s) 
            
#     #         # AGGIUNTA AL DISEGNO
#     #         if s not in self._canvas_widgets.canvas.shapes:
#     #             self._canvas_widgets.canvas.shapes.append(s)

#     #     # 3. Ripristino Interfaccia e Modalità Selezione
#     #     self.setEditMode() 
#     #     self._canvas_widgets.canvas.setEditing(True)
        
#     #     # 4. Stato Finale e Update Grafico
#     #     self.dirty = True 
#     #     self._actions.save.setEnabled(True)
#     #     self._canvas_widgets.canvas.update()
        
#     #     self.statusBar().showMessage(f"Dataset sincronizzato: {len(merged_list)} linee.")
            
          
         
        



#     def merge_parallel_lines(self):
#         """Fonde segmenti paralleli e vicini (ottimizzato per la tua MainWindow)."""
#         import numpy as np
#         canvas = self._canvas_widgets.canvas
#         if not canvas.shapes: 
#             return

#         DIST_EPSILON = 15.0
#         ANGLE_EPSILON = 2.0

#         shapes = list(canvas.shapes)
#         merged_list = []
#         used = [False] * len(shapes)

#         for i in range(len(shapes)):
#             if used[i] or len(shapes[i].points) < 2: 
#                 continue
            
#             group = [shapes[i]]
#             used[i] = True
            
#             p1, p2 = shapes[i].points[0], shapes[i].points[1]
#             vec_i = np.array([p2.x() - p1.x(), p2.y() - p1.y()])
#             angle_i = np.arctan2(vec_i[1], vec_i[0]) % np.pi

#             for j in range(i + 1, len(shapes)):
#                 if used[j] or len(shapes[j].points) < 2: 
#                     continue
                
#                 p3, p4 = shapes[j].points[0], shapes[j].points[1]
#                 vec_j = np.array([p4.x() - p3.x(), p4.y() - p3.y()])
#                 angle_j = np.arctan2(vec_j[1], vec_j[0]) % np.pi

#                 diff_angle = abs(angle_i - angle_j)
#                 diff_angle = min(diff_angle, np.pi - diff_angle)

#                 if diff_angle < np.radians(ANGLE_EPSILON):
#                     mid_j = np.array([(p3.x() + p4.x())/2, (p3.y() + p4.y())/2])
#                     dist = self._dist_point_to_line(mid_j, p1, p2)
                    
#                     if dist < DIST_EPSILON:
#                         group.append(shapes[j])
#                         used[j] = True

#             if len(group) > 1:
#                 new_shape = self._create_average_line(group)
#                 merged_list.append(new_shape)
#             else:
#                 merged_list.append(shapes[i])

#         # --- SINCRONIZZAZIONE BLINDATA PER LA TUA STRUTTURA ---
        
#         # 1. Pulizia corretta usando self._docks
#         canvas.shapes = []
#         canvas.selectedShapes = []
#         # Accediamo alla lista reale dentro il dock
#         if hasattr(self._docks, 'label_list'):
#             self._docks.label_list.clear()

#         # 2. Re-inserimento Ufficiale
#         for s in merged_list:
#             if s.label == "Linea_Merged" or not s.label:
#                 # Usa il tuo metodo per ottenere il prossimo ID (es. L_001)
#                 s.label = self.get_next_label(prefix="L_")
            
#             # addLabel() collegherà correttamente la shape al widget nel dock
#             self.addLabel(s) 

#         # 3. Ripristino Interfaccia
#         self.setEditMode()
#         canvas.setEditing(True)
#         canvas.update()
        
#         self.setDirty() # Usa il metodo standard di LabelMe
#         self.statusBar().showMessage(f"Merge completato: {len(canvas.shapes)} linee.")    
        
#     def _dist_point_to_line(self, p, l1, l2):
#         """Calcola la distanza minima tra un punto P e la retta passante per l1-l2."""
#         import numpy as np
#         p1 = np.array([l1.x(), l1.y()])
#         p2 = np.array([l2.x(), l2.y()])
#         return np.abs(np.cross(p2-p1, p1-p)) / np.linalg.norm(p2-p1)

#     def _create_average_line(self, group):
#         """Genera una retta media basata sui punti del gruppo."""

#         all_pts = []
#         for s in group:
#             for p in s.points:
#                 all_pts.append([p.x(), p.y()])
#         all_pts = np.array(all_pts)

#         # Usiamo la PCA (SVD) per trovare la direzione principale della nuvola di punti
#         centroid = np.mean(all_pts, axis=0)
#         _, _, vh = np.linalg.svd(all_pts - centroid)
#         direction = vh[0] # Vettore direzione principale

#         # Proiettiamo i punti sulla direzione per trovare gli estremi
#         projections = (all_pts - centroid) @ direction
#         p_min = centroid + np.min(projections) * direction
#         p_max = centroid + np.max(projections) * direction

#         # --- APPLICAZIONE SNAP SUI NUOVI ESTREMI ---
#         # Questo assicura che se la retta media finisce vicino a un vertice 
#         # di una linea NON mergiata, vi si agganci.
#         x1, y1 = self._apply_snap(p_min[0], p_min[1])
#         x2, y2 = self._apply_snap(p_max[0], p_max[1])

#         new_s = Shape(label="Linea_Merged", shape_type="polygon")
#         new_s.addPoint(QtCore.QPointF(x1, y1))
#         new_s.addPoint(QtCore.QPointF(x2, y2))
#         new_s.close()
#         return new_s
#         #     for j in range(i + 1, len(shapes)):
#         #         if used[j]: continue
#         #         s2 = shapes[j]
                
#         #         # Calcolo parametri retta 2
#         #         p3, p4 = s2.points[0], s2.points[1]
#         #         vec2 = np.array([p4.x() - p3.x(), p4.y() - p3.y()])
#         #         ang2 = np.arctan2(vec2[1], vec2[0]) % np.pi
#         #         center2 = np.array([(p3.x() + p4.x())/2, (p3.y() + p4.y())/2])

#         #         # Verifica parallelismo e vicinanza
#         #         ang_diff = abs(ang1 - ang2)
#         #         ang_diff = min(ang_diff, np.pi - ang_diff)
#         #         dist = np.linalg.norm(center1 - center2)

#         #         if ang_diff < np.radians(ANGLE_EPSILON) and dist < DIST_EPSILON:
#         #             group.append(s2)
#         #             used[j] = True

#         #     # Se ho trovato linee simili, creo la "linea media"
#         #     if len(group) > 1:
#         #         avg_p1_x = sum(s.points[0].x() for s in group) / len(group)
#         #         avg_p1_y = sum(s.points[0].y() for s in group) / len(group)
#         #         avg_p2_x = sum(s.points[1].x() for s in group) / len(group)
#         #         avg_p2_y = sum(s.points[1].y() for s in group) / len(group)
                
#         #         new_s = Shape(label="linea_merged", shape_type="line")
#         #         new_s.addPoint(QtCore.QPointF(avg_p1_x, avg_p1_y))
#         #         new_s.addPoint(QtCore.QPointF(avg_p2_x, avg_p2_y))
#         #         merged_list.append(new_s)
#         #     else:
#         #         merged_list.append(s1)

#         # # Aggiorna il Canvas e la lista etichette
#         # canvas.shapes = merged_list
#         # # In LabelMe il widget della lista etichette è solitamente self.labelList
#         # # ma dobbiamo assicurarci di svuotarlo e riempirlo correttamente
#         # if hasattr(self, 'labelList'):
#         #     self.labelList.clear()
#         #     for s in merged_list:
#         #         # addLabel è il metodo standard di MainWindow per sincronizzare UI e Canvas
#         #         self.addLabel(s)
#         # elif hasattr(self, 'label_list'): # Backup per versioni alternative
#         #     self.label_list.clear()
#         #     for s in merged_list:
#         #         self.addLabel(s)
        
#         # canvas.update()
#         # self.setDirty() # Indica che il file è stato modificato e va salvato
#         # self.statusBar().showMessage(f"Merge completato: ridotte a {len(merged_list)} linee.")
 
    
#     def _setup_menus(self) -> _Menus:
#         action = functools.partial(utils.newAction, self)
#         shortcuts = self._config["shortcuts"]

#         quit_ = action(
#             text=self.tr("&Quit"),
#             slot=self.close,
#             shortcut=shortcuts["quit"],
#             icon=None,
#             tip=self.tr("Quit application"),
#         )
#         open_config = action(
#             text=self.tr("Preferences…"),
#             slot=self._open_config_file,
#             shortcut="Ctrl+," if platform.system() == "Darwin" else "Ctrl+Shift+,",
#             icon=None,
#             tip=self.tr("Open config file in text editor"),
#         )
#         open_config.setMenuRole(QtWidgets.QAction.PreferencesRole)
#         help_ = action(
#             self.tr("&Tutorial"),
#             self.tutorial,
#             icon="question.svg",
#             tip=self.tr("Show tutorial page"),
#         )

#         file_menu = self.menu(self.tr("&File"))
#         edit_menu = self.menu(self.tr("&Edit"))
#         view_menu = self.menu(self.tr("&View"))
#         help_menu = self.menu(self.tr("&Help"))
#         recent_files = QtWidgets.QMenu(self.tr("Open &Recent"))

#         label_menu = QtWidgets.QMenu()
#         utils.addActions(label_menu, (self._actions.edit, self._actions.delete))
#         self._docks.label_list.setContextMenuPolicy(Qt.CustomContextMenu)
#         self._docks.label_list.customContextMenuRequested.connect(self.popLabelListMenu)

#         utils.addActions(
#             file_menu,
#             (
#                 self._actions.open,
#                 self._actions.open_next_img,
#                 self._actions.open_prev_img,
#                 self._actions.open_dir,
#                 recent_files,
#                 self._actions.save,
#                 self._actions.save_as,
#                 self._actions.save_auto,
#                 self._actions.change_output_dir,
#                 self._actions.save_with_image_data,
#                 self._actions.close,
#                 self._actions.delete_file,
#                 None,
#                 open_config,
#                 None,
#                 quit_,
#             ),
#         )
#         utils.addActions(help_menu, (help_, self._actions.about))
#         utils.addActions(
#             view_menu,
#             (
#                 self._docks.flag_dock.toggleViewAction(),
#                 self._docks.label_dock.toggleViewAction(),
#                 self._docks.shape_dock.toggleViewAction(),
#                 self._docks.file_dock.toggleViewAction(),
#                 None,
#                 self._actions.reset_layout,
#                 None,
#                 self._actions.fill_drawing,
#                 None,
#                 self._actions.hide_all,
#                 self._actions.show_all,
#                 self._actions.toggle_all,
#                 None,
#                 self._actions.zoom_in,
#                 self._actions.zoom_out,
#                 self._actions.zoom_org,
#                 self._actions.keep_prev_scale,
#                 None,
#                 self._actions.fit_window,
#                 self._actions.fit_width,
#                 None,
#                 self._actions.brightness_contrast,
#                 self._actions.toggle_keep_prev_brightness_contrast,
#             ),
#         )

#         file_menu.aboutToShow.connect(self.updateFileMenu)

#         utils.addActions(
#             self._canvas_widgets.canvas.menus[0], self._actions.context_menu
#         )
#         utils.addActions(
#             self._canvas_widgets.canvas.menus[1],
#             (
#                 action("&Copy here", self.copyShape),
#                 action("&Move here", self.moveShape),
#             ),
#         )

#         return _Menus(
#             file=file_menu,
#             edit=edit_menu,
#             view=view_menu,
#             help=help_menu,
#             recent_files=recent_files,
#             label_list=label_menu,
#         )

#     def _setup_toolbars(self) -> None:
#         select_ai_model = QtWidgets.QWidgetAction(self)
#         select_ai_model.setDefaultWidget(self._ai_annotation)

#         ai_prompt_action = QtWidgets.QWidgetAction(self)
#         ai_prompt_action.setDefaultWidget(self._ai_text)

#         self.addToolBar(
#             Qt.TopToolBarArea,
#             ToolBar(
#                 title="Tools",
#                 actions=[
#                     self._actions.open,
#                     self._actions.open_dir,
#                     self._actions.open_prev_img,
#                     self._actions.open_next_img,
#                     self._actions.save,
#                     self._actions.delete_file,
#                     None,
#                     self._actions.edit_mode,
#                     self._actions.duplicate,
#                     self._actions.delete,
#                     self._actions.undo,
#                     self._actions.brightness_contrast,
#                     None,
#                     self._actions.fit_window,
#                     self._actions.zoom_widget_action,
#                     None,
#                     select_ai_model,
#                     None,
#                     ai_prompt_action,
#                 ],
#                 font_base=self.font(),
#             ),
#         )
#         self.addToolBar(
#             Qt.LeftToolBarArea,
#             ToolBar(
#                 title="CreateShapeTools",
#                 actions=[a for _, a in self._actions.draw],
#                 orientation=Qt.Vertical,
#                 button_style=Qt.ToolButtonTextUnderIcon,
#                 font_base=self.font(),
#             ),
#         )

#     def _setup_app_state(
#         self,
#         *,
#         output_dir: str | None,
#         filename: str | None,
#     ) -> None:
#         self._output_dir = output_dir

#         self._image = QtGui.QImage()
#         self._label_file = None
#         self._image_path = None
#         self._max_recent = 7
#         self._other_data = None
#         self._zoom_values = {}
#         self._brightness_contrast_values = {}
#         self._scroll_values = {
#             Qt.Horizontal: {},
#             Qt.Vertical: {},
#         }

#         if self._config["file_search"]:
#             self._docks.file_search.setText(self._config["file_search"])

#         self._default_state = self.saveState()
#         #
#         # XXX: Could be completely declarative.
#         # Restore application settings.
#         self.settings = QtCore.QSettings("labelme", "labelme")
#         #
#         # Bump this when dock/toolbar layout changes to reset window state
#         # for users upgrading from an older version.
#         SETTINGS_VERSION: int = 1
#         if self.settings.value("settingsVersion", 0, type=int) != SETTINGS_VERSION:
#             self._reset_layout()
#             self.settings.setValue("settingsVersion", SETTINGS_VERSION)
#         #
#         self._recent_files = self.settings.value("recentFiles", []) or []
#         self.resize(self.settings.value("window/size", QtCore.QSize(900, 500)))
#         self.move(self.settings.value("window/position", QtCore.QPoint(0, 0)))
#         self.restoreState(self.settings.value("window/state", QtCore.QByteArray()))
#         # Recover window position when the saved screen is no longer connected.
#         if not any(
#             s.availableGeometry().intersects(self.frameGeometry())
#             for s in QtWidgets.QApplication.screens()
#         ) and (primary_screen := QtWidgets.QApplication.primaryScreen()):
#             self.move(primary_screen.availableGeometry().topLeft())

#         if filename:
#             if osp.isdir(filename):
#                 self._import_images_from_dir(
#                     root_dir=filename, pattern=self._docks.file_search.text()
#                 )
#                 self._open_next_image()
#             else:
#                 self._load_file(filename=filename)
#         else:
#             self._filename = None

#     def _setup_status_bar(self) -> _StatusBarWidgets:
#         message = QtWidgets.QLabel(self.tr("%s started.") % __appname__)
#         stats = StatusStats()
#         self.statusBar().addWidget(message, 1)
#         self.statusBar().addWidget(stats, 0)
#         self.statusBar().show()
#         return _StatusBarWidgets(message=message, stats=stats)

#     def _setup_canvas(self) -> _CanvasWidgets:
#         zoom_widget = ZoomWidget()

#         canvas = Canvas(
#             epsilon=self._config["epsilon"],
#             double_click=self._config["canvas"]["double_click"],
#             num_backups=self._config["canvas"]["num_backups"],
#             crosshair=self._config["canvas"]["crosshair"],
#         )
#         canvas.zoomRequest.connect(self._zoom_requested)
#         canvas.mouseMoved.connect(self._update_status_stats)
#         canvas.statusUpdated.connect(
#             lambda text: self._status_bar.message.setText(text)
#         )

#         scroll_area = QtWidgets.QScrollArea()
#         scroll_area.setWidget(canvas)
#         scroll_area.setWidgetResizable(True)
#         scroll_bars = {
#             Qt.Vertical: scroll_area.verticalScrollBar(),
#             Qt.Horizontal: scroll_area.horizontalScrollBar(),
#         }
#         canvas.scrollRequest.connect(self.scrollRequest)

#         canvas.newShape.connect(self.newShape)
#         canvas.shapeMoved.connect(self.setDirty)
#         canvas.selectionChanged.connect(self.shapeSelectionChanged)
#         canvas.drawingPolygon.connect(self.toggleDrawingSensitive)

#         self.setCentralWidget(scroll_area)

#         return _CanvasWidgets(
#             canvas=canvas,
#             zoom_widget=zoom_widget,
#             scroll_bars=scroll_bars,
#         )

#     def _setup_dock_widgets(self) -> _DockWidgets:
#         flag_list = QtWidgets.QListWidget()
#         flag = QtWidgets.QDockWidget(self.tr("Flags"), self)
#         flag.setObjectName("Flags")
#         if self._config["flags"]:
#             self._load_flags(
#                 flags={k: False for k in self._config["flags"]},
#                 widget=flag_list,
#             )
#         flag.setWidget(flag_list)
#         flag_list.itemChanged.connect(self.setDirty)

#         label_list = LabelListWidget()
#         label_list.itemSelectionChanged.connect(self._label_selection_changed)
#         label_list.itemDoubleClicked.connect(self._edit_label)
#         label_list.itemChanged.connect(self.labelItemChanged)
#         label_list.itemDropped.connect(self.labelOrderChanged)
#         shape = QtWidgets.QDockWidget(self.tr("Annotation List"), self)
#         shape.setObjectName("Labels")
#         shape.setWidget(label_list)

#         unique_label_list = UniqueLabelQListWidget()
#         unique_label_list.setToolTip(
#             self.tr("Select label to start annotating for it. Press 'Esc' to deselect.")
#         )
#         if self._config["labels"]:
#             for lbl in self._config["labels"]:
#                 unique_label_list.add_label_item(
#                     label=lbl,
#                     color=self._get_rgb_by_label(
#                         label=lbl, unique_label_list=unique_label_list
#                     ),
#                 )
#         label = QtWidgets.QDockWidget(self.tr("Label List"), self)
#         label.setObjectName("Label List")
#         label.setWidget(unique_label_list)

#         file_search = QtWidgets.QLineEdit()
#         file_search.setPlaceholderText(self.tr("Search Filename"))
#         file_search.textChanged.connect(self.fileSearchChanged)
#         file_list = QtWidgets.QListWidget()
#         file_list.itemSelectionChanged.connect(self.fileSelectionChanged)
#         file_list_layout = QtWidgets.QVBoxLayout()
#         file_list_layout.setContentsMargins(0, 0, 0, 0)
#         file_list_layout.setSpacing(0)
#         file_list_layout.addWidget(file_search)
#         file_list_layout.addWidget(file_list)
#         file = QtWidgets.QDockWidget(self.tr("File List"), self)
#         file.setObjectName("Files")
#         file_list_container = QtWidgets.QWidget()
#         file_list_container.setLayout(file_list_layout)
#         file.setWidget(file_list_container)

#         for config_key, dock_widget in [
#             ("flag_dock", flag),
#             ("label_dock", label),
#             ("shape_dock", shape),
#             ("file_dock", file),
#         ]:
#             features = QtWidgets.QDockWidget.DockWidgetFeatures()
#             if self._config[config_key]["closable"]:
#                 features = features | QtWidgets.QDockWidget.DockWidgetClosable
#             if self._config[config_key]["floatable"]:
#                 features = features | QtWidgets.QDockWidget.DockWidgetFloatable
#             if self._config[config_key]["movable"]:
#                 features = features | QtWidgets.QDockWidget.DockWidgetMovable
#             dock_widget.setFeatures(features)
#             if self._config[config_key]["show"] is False:
#                 dock_widget.setVisible(False)
#             self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)

#         return _DockWidgets(
#             flag_dock=flag,
#             flag_list=flag_list,
#             shape_dock=shape,
#             label_list=label_list,
#             label_dock=label,
#             unique_label_list=unique_label_list,
#             file_dock=file,
#             file_search=file_search,
#             file_list=file_list,
#         )

#     def _load_config(
#         self, config_file: Path | None, config_overrides: dict | None
#     ) -> tuple[Path | None, dict]:
#         try:
#             config = load_config(
#                 config_file=config_file, config_overrides=config_overrides or {}
#             )
#         except ValueError as e:
#             msg_box = QMessageBox(self)
#             msg_box.setIcon(QMessageBox.Warning)
#             msg_box.setWindowTitle(self.tr("Configuration Errors"))
#             msg_box.setText(
#                 self.tr(
#                     "Errors were found while loading the configuration. "
#                     "Please review the errors below and reload your configuration or "
#                     "ignore the erroneous lines."
#                 )
#             )
#             msg_box.setInformativeText(str(e))
#             msg_box.setStandardButtons(QMessageBox.Ignore)
#             msg_box.setModal(False)
#             msg_box.show()

#             config_file = None
#             config_overrides = {}
#             config = load_config(
#                 config_file=config_file, config_overrides=config_overrides
#             )
#         return config_file, config

#     def menu(self, title, actions=None):
#         menu = self.menuBar().addMenu(title)
#         if actions:
#             utils.addActions(menu, actions)
#         return menu

#     # Support Functions

#     def noShapes(self) -> bool:
#         return not len(self._docks.label_list)

#     def populateModeActions(self) -> None:
#         self._canvas_widgets.canvas.menus[0].clear()
#         utils.addActions(
#             self._canvas_widgets.canvas.menus[0], self._actions.context_menu
#         )
#         self._menus.edit.clear()
#         actions = (
#             *[draw_action for _, draw_action in self._actions.draw],
#             self._actions.edit_mode,
#             *self._actions.edit_menu,
#         )
#         utils.addActions(self._menus.edit, actions)

#     def _get_window_title(self, dirty: bool) -> str:
#         window_title: str = __appname__
#         if self._image_path:
#             window_title = f"{window_title} - {self._image_path}"
#             if self._docks.file_list.count() and self._docks.file_list.currentItem():
#                 window_title = (
#                     f"{window_title} "
#                     f"[{self._docks.file_list.currentRow() + 1}"
#                     f"/{self._docks.file_list.count()}]"
#                 )
#         if dirty:
#             window_title = f"{window_title}*"
#         return window_title

#     def setDirty(self) -> None:
#         # Even if we autosave the file, we keep the ability to undo
#         self._actions.undo.setEnabled(self._canvas_widgets.canvas.isShapeRestorable)

#         if self._config["auto_save"] or self._actions.save_auto.isChecked():
#             assert self._image_path
#             label_file = f"{osp.splitext(self._image_path)[0]}.json"
#             if self._output_dir:
#                 label_file_without_path = osp.basename(label_file)
#                 label_file = osp.join(self._output_dir, label_file_without_path)
#             self.saveLabels(label_file)
#             return
#         self._is_changed = True
#         self._actions.save.setEnabled(True)
#         self.setWindowTitle(self._get_window_title(dirty=True))

#     def setClean(self) -> None:
#         self._is_changed = False
#         self._actions.save.setEnabled(False)
#         for _, action in self._actions.draw:
#             action.setEnabled(True)
#         self.setWindowTitle(self._get_window_title(dirty=False))

#         if self.hasLabelFile():
#             self._actions.delete_file.setEnabled(True)
#         else:
#             self._actions.delete_file.setEnabled(False)

#     def toggleActions(self, value: bool = True) -> None:
#         """Enable/Disable widgets which depend on an opened image."""
#         for z in self._actions.zoom:
#             z.setEnabled(value)
#         for action in self._actions.on_load_active:
#             action.setEnabled(value)

#     def queueEvent(self, function: Callable[[], None]) -> None:
#         QtCore.QTimer.singleShot(0, function)

#     def show_status_message(self, message: str, delay: int = 500) -> None:
#         self.statusBar().showMessage(message, delay)

#     def _submit_ai_prompt(self, _) -> None:
#         if (
#             self._canvas_widgets.canvas.createMode
#             not in _AI_TEXT_TO_ANNOTATION_CREATE_MODE_TO_SHAPE_TYPE
#         ):
#             logger.warning(
#                 "Unsupported createMode={!r}", self._canvas_widgets.canvas.createMode
#             )
#             return
#         shape_type: Literal["rectangle", "polygon", "mask"] = (
#             _AI_TEXT_TO_ANNOTATION_CREATE_MODE_TO_SHAPE_TYPE[
#                 self._canvas_widgets.canvas.createMode
#             ]
#         )

#         texts = self._ai_text.get_text_prompt().split(",")

#         model_name: str = self._ai_text.get_model_name()
#         model_type = osam.apis.get_model_type_by_name(model_name)
#         if not (_is_already_downloaded := model_type.get_size() is not None):
#             if not download_ai_model(model_name=model_name, parent=self):
#                 return
#         if (
#             self._text_osam_session is None
#             or self._text_osam_session.model_name != model_name
#         ):
#             self._text_osam_session = OsamSession(model_name=model_name)

#         boxes, scores, labels, masks = bbox_from_text.get_bboxes_from_texts(
#             session=self._text_osam_session,
#             image=utils.img_qt_to_arr(self._image)[:, :, :3],
#             image_id=str(hash(self._image_path)),
#             texts=texts,
#         )

#         SCORE_FOR_EXISTING_SHAPE: float = 1.01
#         for shape in self._canvas_widgets.canvas.shapes:
#             if shape.shape_type != shape_type or shape.label not in texts:
#                 continue
#             points: NDArray[np.float64] = np.array(
#                 [[p.x(), p.y()] for p in shape.points]
#             )
#             xmin, ymin = points.min(axis=0)
#             xmax, ymax = points.max(axis=0)
#             box = np.array([xmin, ymin, xmax, ymax], dtype=np.float32)
#             boxes = np.r_[boxes, [box]]
#             scores = np.r_[scores, [SCORE_FOR_EXISTING_SHAPE]]
#             labels = np.r_[labels, [texts.index(shape.label)]]

#         boxes, scores, labels, indices = bbox_from_text.nms_bboxes(
#             boxes=boxes,
#             scores=scores,
#             labels=labels,
#             iou_threshold=self._ai_text.get_iou_threshold(),
#             score_threshold=self._ai_text.get_score_threshold(),
#             max_num_detections=100,
#         )

#         is_new = scores != SCORE_FOR_EXISTING_SHAPE
#         boxes = boxes[is_new]
#         scores = scores[is_new]
#         labels = labels[is_new]
#         indices = indices[is_new]

#         if masks is not None:
#             masks = masks[indices]
#         del indices

#         shapes: list[Shape] = bbox_from_text.get_shapes_from_bboxes(
#             boxes=boxes,
#             scores=scores,
#             labels=labels,
#             texts=texts,
#             masks=masks,
#             shape_type=shape_type,
#         )

#         self._canvas_widgets.canvas.storeShapes()
#         self._load_shapes(shapes, replace=False)
#         self.setDirty()

#     def resetState(self) -> None:
#         self._docks.label_list.clear()
#         self._filename = None
#         self._image_path = None
#         self.imageData = None
#         self._label_file = None
#         self._other_data = None
#         self._canvas_widgets.canvas.resetState()

#     def currentItem(self) -> LabelListWidgetItem | None:
#         items = self._docks.label_list.selectedItems()
#         if items:
#             return items[0]
#         return None

#     def addRecentFile(self, filename: str) -> None:
#         if filename in self._recent_files:
#             self._recent_files.remove(filename)
#         elif len(self._recent_files) >= self._max_recent:
#             self._recent_files.pop()
#         self._recent_files.insert(0, filename)

#     # Callbacks

#     def undoShapeEdit(self) -> None:
#         self._canvas_widgets.canvas.restoreShape()
#         self._docks.label_list.clear()
#         self._load_shapes(self._canvas_widgets.canvas.shapes)
#         self._actions.undo.setEnabled(self._canvas_widgets.canvas.isShapeRestorable)

#     def tutorial(self):
#         url = "https://github.com/labelmeai/labelme/tree/main/examples/tutorial"  # NOQA
#         webbrowser.open(url)

#     def toggleDrawingSensitive(self, drawing=True):
#         """Toggle drawing sensitive.

#         In the middle of drawing, toggling between modes should be disabled.
#         """
#         self._actions.edit_mode.setEnabled(not drawing)
#         self._actions.undo_last_point.setEnabled(drawing)
#         self._actions.undo.setEnabled(not drawing)
#         self._actions.delete.setEnabled(not drawing)

#     def _switch_canvas_mode(
#         self, edit: bool = True, createMode: str | None = None
#     ) -> None:
#         self._canvas_widgets.canvas.setEditing(edit)
#         if createMode is not None:
#             self._canvas_widgets.canvas.createMode = createMode
#         if edit:
#             for _, draw_action in self._actions.draw:
#                 draw_action.setEnabled(True)
#         else:
#             for draw_mode, draw_action in self._actions.draw:
#                 draw_action.setEnabled(createMode != draw_mode)
#         self._actions.edit_mode.setEnabled(not edit)
#         self._ai_text.setEnabled(
#             not edit and createMode in _AI_TEXT_TO_ANNOTATION_CREATE_MODE_TO_SHAPE_TYPE
#         )
#         self._ai_annotation.setEnabled(
#             not edit and createMode in ("ai_polygon", "ai_mask")
#         )

#     def updateFileMenu(self):
#         current = self._filename

#         def exists(filename):
#             return osp.exists(str(filename))

#         menu = self._menus.recent_files
#         menu.clear()
#         files = [f for f in self._recent_files if f != current and exists(f)]
#         for i, f in enumerate(files):
#             icon = utils.newIcon("labels")
#             action = QtWidgets.QAction(
#                 icon, f"&{i + 1} {QtCore.QFileInfo(f).fileName()}", self
#             )
#             action.triggered.connect(functools.partial(self.loadRecent, f))
#             menu.addAction(action)

#     def popLabelListMenu(self, point: QtCore.QPoint) -> None:
#         self._menus.label_list.exec(self._docks.label_list.mapToGlobal(point))  # type: ignore[invalid-argument-type]

#     def validateLabel(self, label):
#         # no validation
#         if self._config["validate_label"] is None:
#             return True

#         for i in range(self._docks.unique_label_list.count()):
#             label_i = self._docks.unique_label_list.item(i).data(Qt.UserRole)  # type: ignore[attr-defined,union-attr]
#             if self._config["validate_label"] in ["exact"]:
#                 if label_i == label:
#                     return True
#         return False

#     def _edit_label(self, value=None):
#         items = self._docks.label_list.selectedItems()
#         if not items:
#             logger.warning("No label is selected, so cannot edit label.")
#             return

#         shape = items[0].shape()

#         if len(items) == 1:
#             edit_text = True
#             edit_flags = True
#             edit_group_id = True
#             edit_description = True
#         else:
#             edit_text = all(item.shape().label == shape.label for item in items[1:])
#             edit_flags = all(item.shape().flags == shape.flags for item in items[1:])
#             edit_group_id = all(
#                 item.shape().group_id == shape.group_id for item in items[1:]
#             )
#             edit_description = all(
#                 item.shape().description == shape.description for item in items[1:]
#             )

#         if not edit_text:
#             self._label_dialog.edit.setDisabled(True)
#             self._label_dialog.labelList.setDisabled(True)
#         if not edit_group_id:
#             self._label_dialog.edit_group_id.setDisabled(True)
#         if not edit_description:
#             self._label_dialog.editDescription.setDisabled(True)

#         text, flags, group_id, description = self._label_dialog.popUp(
#             text=shape.label if edit_text else "",
#             flags=shape.flags if edit_flags else None,
#             group_id=shape.group_id if edit_group_id else None,
#             description=shape.description if edit_description else None,
#             flags_disabled=not edit_flags,
#         )

#         if not edit_text:
#             self._label_dialog.edit.setDisabled(False)
#             self._label_dialog.labelList.setDisabled(False)
#         if not edit_group_id:
#             self._label_dialog.edit_group_id.setDisabled(False)
#         if not edit_description:
#             self._label_dialog.editDescription.setDisabled(False)

#         if text is None:
#             assert flags is None
#             assert group_id is None
#             assert description is None
#             return

#         if not self.validateLabel(text):
#             self.errorMessage(
#                 self.tr("Invalid label"),
#                 self.tr("Invalid label '{}' with validation type '{}'").format(
#                     text, self._config["validate_label"]
#                 ),
#             )
#             return

#         self._canvas_widgets.canvas.storeShapes()
#         for item in items:
#             shape: Shape = item.shape()  # type: ignore[no-redef]

#             if edit_text:
#                 shape.label = text
#             if edit_flags:
#                 shape.flags = flags
#             if edit_group_id:
#                 shape.group_id = group_id
#             if edit_description:
#                 shape.description = description

#             self._update_shape_color(shape)
#             if shape.group_id is None:
#                 r, g, b = shape.fill_color.getRgb()[:3]
#                 item.setText(
#                     f"{html.escape(shape.label)} "
#                     f'<font color="#{r:02x}{g:02x}{b:02x}">●</font>'
#                 )
#             else:
#                 item.setText(f"{shape.label} ({shape.group_id})")
#             self.setDirty()
#             if self._docks.unique_label_list.find_label_item(shape.label) is None:
#                 self._docks.unique_label_list.add_label_item(
#                     label=shape.label,
#                     color=self._get_rgb_by_label(
#                         label=shape.label,
#                         unique_label_list=self._docks.unique_label_list,
#                     ),
#                 )

#     def fileSearchChanged(self):
#         self._import_images_from_dir(
#             root_dir=self._prev_opened_dir, pattern=self._docks.file_search.text()
#         )

#     def fileSelectionChanged(self) -> None:
#         items = self._docks.file_list.selectedItems()
#         if not items:
#             return
#         item = items[0]

#         if not self._can_continue():
#             return

#         curr_index = self.imageList.index(str(item.text()))
#         if curr_index < len(self.imageList):
#             filename = self.imageList[curr_index]
#             if filename:
#                 self._load_file(filename)

#     # React to canvas signals.
#     def shapeSelectionChanged(self, selected_shapes: list[Shape]) -> None:
#         self._docks.label_list.itemSelectionChanged.disconnect(
#             self._label_selection_changed
#         )
#         for shape in self._canvas_widgets.canvas.selectedShapes:
#             shape.selected = False
#         self._docks.label_list.clearSelection()
#         self._canvas_widgets.canvas.selectedShapes = selected_shapes
#         for shape in self._canvas_widgets.canvas.selectedShapes:
#             shape.selected = True
#             item = self._docks.label_list.findItemByShape(shape)
#             self._docks.label_list.selectItem(item)
#             self._docks.label_list.scrollToItem(item)
#         self._docks.label_list.itemSelectionChanged.connect(
#             self._label_selection_changed
#         )
#         n_selected = len(selected_shapes) > 0
#         self._actions.delete.setEnabled(n_selected)
#         self._actions.duplicate.setEnabled(n_selected)
#         self._actions.copy.setEnabled(n_selected)
#         self._actions.edit.setEnabled(n_selected)

#     def addLabel(self, shape: Shape) -> None:
#         assert shape.label is not None
#         if shape.group_id is None:
#             text = shape.label
#         else:
#             text = f"{shape.label} ({shape.group_id})"
#         label_list_item = LabelListWidgetItem(text, shape)
#         self._docks.label_list.addItem(label_list_item)
#         if self._docks.unique_label_list.find_label_item(shape.label) is None:
#             self._docks.unique_label_list.add_label_item(
#                 label=shape.label,
#                 color=self._get_rgb_by_label(
#                     label=shape.label,
#                     unique_label_list=self._docks.unique_label_list,
#                 ),
#             )
#         self._label_dialog.addLabelHistory(shape.label)
#         for action in self._actions.on_shapes_present:
#             action.setEnabled(True)

#         self._update_shape_color(shape)
#         r, g, b = shape.fill_color.getRgb()[:3]
#         label_list_item.setText(
#             f'{html.escape(text)} <font color="#{r:02x}{g:02x}{b:02x}">●</font>'
#         )

#     def _update_shape_color(self, shape: Shape) -> None:
#         assert shape.label is not None
#         r, g, b = self._get_rgb_by_label(
#             shape.label, unique_label_list=self._docks.unique_label_list
#         )
#         shape.line_color = QtGui.QColor(r, g, b)
#         shape.vertex_fill_color = QtGui.QColor(r, g, b)
#         shape.hvertex_fill_color = QtGui.QColor(255, 255, 255)
#         shape.fill_color = QtGui.QColor(r, g, b, 128)
#         shape.select_line_color = QtGui.QColor(255, 255, 255)
#         shape.select_fill_color = QtGui.QColor(r, g, b, 155)

#     def _get_rgb_by_label(
#         self,
#         label: str,
#         unique_label_list: UniqueLabelQListWidget,
#     ) -> tuple[int, int, int]:
#         if self._config["shape_color"] == "auto":
#             item = unique_label_list.find_label_item(label)
#             item_index: int = (
#                 unique_label_list.indexFromItem(item).row()
#                 if item
#                 else unique_label_list.count()
#             )
#             label_id: int = (
#                 1  # skip black color by default
#                 + item_index
#                 + self._config["shift_auto_shape_color"]
#             )
#             rgb: tuple[int, int, int] = tuple(
#                 LABEL_COLORMAP[label_id % len(LABEL_COLORMAP)].tolist()
#             )
#             return rgb
#         elif (
#             self._config["shape_color"] == "manual"
#             and self._config["label_colors"]
#             and label in self._config["label_colors"]
#         ):
#             if not (
#                 len(self._config["label_colors"][label]) == 3
#                 and all(0 <= c <= 255 for c in self._config["label_colors"][label])
#             ):
#                 raise ValueError(
#                     "Color for label must be 0-255 RGB tuple, but got: "
#                     f"{self._config['label_colors'][label]}"
#                 )
#             return tuple(self._config["label_colors"][label])
#         elif self._config["default_shape_color"]:
#             return self._config["default_shape_color"]
#         return (0, 255, 0)

#     def remLabels(self, shapes: list[Shape]) -> None:
#         for shape in shapes:
#             item = self._docks.label_list.findItemByShape(shape)
#             self._docks.label_list.removeItem(item)

#     def _load_shapes(self, shapes: list[Shape], replace: bool = True) -> None:
#         self._docks.label_list.itemSelectionChanged.disconnect(
#             self._label_selection_changed
#         )
#         shape: Shape
#         for shape in shapes:
#             self.addLabel(shape)
#         self._docks.label_list.clearSelection()
#         self._docks.label_list.itemSelectionChanged.connect(
#             self._label_selection_changed
#         )
#         self._canvas_widgets.canvas.loadShapes(shapes=shapes, replace=replace)

#     def _load_shape_dicts(self, shape_dicts: list[ShapeDict]) -> None:
#         shapes: list[Shape] = []
#         shape_dict: ShapeDict
#         for shape_dict in shape_dicts:
#             shape: Shape = Shape(
#                 label=shape_dict["label"],
#                 shape_type=shape_dict["shape_type"],
#                 group_id=shape_dict["group_id"],
#                 description=shape_dict["description"],
#                 mask=shape_dict["mask"],
#             )
#             for x, y in shape_dict["points"]:
#                 shape.addPoint(QtCore.QPointF(x, y))
#             shape.close()

#             default_flags = {}
#             if self._config["label_flags"]:
#                 for pattern, keys in self._config["label_flags"].items():
#                     if not isinstance(shape.label, str):
#                         logger.warning("shape.label is not str: {}", shape.label)
#                         continue
#                     if re.match(pattern, shape.label):
#                         for key in keys:
#                             default_flags[key] = False
#             shape.flags = default_flags
#             shape.flags.update(shape_dict["flags"])
#             shape.other_data = shape_dict["other_data"]

#             shapes.append(shape)
#         self._load_shapes(shapes=shapes)

#     def _load_flags(
#         self,
#         flags: dict[str, bool],
#         widget: QtWidgets.QListWidget,
#     ) -> None:
#         widget.clear()
#         key: str
#         flag: bool
#         for key, flag in flags.items():
#             item: QtWidgets.QListWidgetItem = QtWidgets.QListWidgetItem(key)
#             item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
#             item.setCheckState(Qt.Checked if flag else Qt.Unchecked)
#             widget.addItem(item)

#     def saveLabels(self, filename):
#         lf = LabelFile()

#         def format_shape(s):
#             data = s.other_data.copy()
#             data.update(
#                 dict(
#                     label=s.label,
#                     points=[(p.x(), p.y()) for p in s.points],
#                     group_id=s.group_id,
#                     description=s.description,
#                     shape_type=s.shape_type,
#                     flags=s.flags,
#                     mask=None
#                     if s.mask is None
#                     else utils.img_arr_to_b64(s.mask.astype(np.uint8)),
#                 )
#             )
#             return data

#         shapes = [format_shape(item.shape()) for item in self._docks.label_list]
#         flags = {}
#         for i in range(self._docks.flag_list.count()):
#             item = self._docks.flag_list.item(i)
#             assert item
#             key = item.text()
#             flag = item.checkState() == Qt.Checked
#             flags[key] = flag
#         try:
#             assert self._image_path
#             imagePath = osp.relpath(self._image_path, osp.dirname(filename))
#             imageData = self.imageData if self._config["with_image_data"] else None
#             if osp.dirname(filename) and not osp.exists(osp.dirname(filename)):
#                 os.makedirs(osp.dirname(filename))
#             lf.save(
#                 filename=filename,
#                 shapes=shapes,
#                 imagePath=imagePath,
#                 imageData=imageData,
#                 imageHeight=self._image.height(),
#                 imageWidth=self._image.width(),
#                 otherData=self._other_data,
#                 flags=flags,
#             )
#             self._label_file = lf
#             items = self._docks.file_list.findItems(self._image_path, Qt.MatchExactly)
#             if len(items) > 0:
#                 if len(items) != 1:
#                     raise RuntimeError("There are duplicate files.")
#                 items[0].setCheckState(Qt.Checked)
#             # disable allows next and previous image to proceed
#             # self._filename = filename
#             return True
#         except LabelFileError as e:
#             self.errorMessage(
#                 self.tr("Error saving label data"), self.tr("<b>%s</b>") % e
#             )
#             return False

#     def duplicateSelectedShape(self) -> None:
#         self.copySelectedShape()
#         self.pasteSelectedShape()

#     def pasteSelectedShape(self) -> None:
#         self._load_shapes(shapes=self._copied_shapes, replace=False)
#         self._canvas_widgets.canvas.selectShapes(self._copied_shapes)
#         self.setDirty()

#     def copySelectedShape(self) -> None:
#         self._copied_shapes = [
#             s.copy() for s in self._canvas_widgets.canvas.selectedShapes
#         ]
#         self._actions.paste.setEnabled(len(self._copied_shapes) > 0)

#     def _label_selection_changed(self) -> None:
#         selected_shapes: list[Shape] = []
#         for item in self._docks.label_list.selectedItems():
#             selected_shapes.append(item.shape())
#         if selected_shapes:
#             self._canvas_widgets.canvas.selectShapes(selected_shapes)
#         else:
#             if self._canvas_widgets.canvas.deSelectShape():
#                 self._canvas_widgets.canvas.update()

#     def labelItemChanged(self, item: LabelListWidgetItem) -> None:
#         shape = item.shape()
#         self._canvas_widgets.canvas.setShapeVisible(
#             shape, item.checkState() == Qt.Checked
#         )

#     def labelOrderChanged(self) -> None:
#         self.setDirty()
#         self._canvas_widgets.canvas.loadShapes(
#             [item.shape() for item in self._docks.label_list]
#         )

        
#     def newShape(self) -> None:
#         """Pop-up con suggerimento automatico dell'etichetta e focus sull'editor."""
#         items = self._docks.unique_label_list.selectedItems()
#         text = None
        
#         # 1. Recupero suggerimento automatico
#         # Se non c'è un'etichetta selezionata nella lista 'unique', usiamo il contatore
#         if items:
#             text = items[0].data(Qt.UserRole)
#         else:
#             text = self.get_next_label(prefix="L_") # Chiama la funzione di conteggio

#         flags = {}
#         group_id = None
#         description = ""
        
#         if self._config["display_label_popup"] or not text:
#             # Impostiamo il testo suggerito nel campo di edit prima del popUp
#             self._label_dialog.edit.setText(text)
            
#             # Mostra il dialogo
#             res = self._label_dialog.popUp(text)
#             if res is not None:
#                 text, flags, group_id, description = res
#             else:
#                 text = None # Utente ha premuto Cancel

#         if text and not self.validateLabel(text):
#             self.errorMessage(
#                 self.tr("Invalid label"),
#                 self.tr("Invalid label '{}'").format(text)
#             )
#             text = ""

#         if text:
#             self._docks.label_list.clearSelection()
#             # Imposta l'etichetta sul canvas
#             shape = self._canvas_widgets.canvas.setLastLabel(text, flags)
#             shape.group_id = group_id
#             shape.description = description
            
#             # 2. Registrazione ufficiale (Fondamentale per il salvataggio JSON)
#             self.addLabel(shape)
            
#             self._actions.edit_mode.setEnabled(True)
#             self._actions.undo_last_point.setEnabled(False)
#             self._actions.undo.setEnabled(True)
            
#             # 3. Stato Dirty (Abilita il tasto Save)
#             self.setDirty()
#         else:
#             self._canvas_widgets.canvas.undoLastLine()
#             if self._canvas_widgets.canvas.shapesBackups:
#                 self._canvas_widgets.canvas.shapesBackups.pop()
#     # Callback functions:

#     # def newShape(self) -> None:
#     #     """Pop-up and give focus to the label editor.

#     #     position MUST be in global coordinates.
#     #     """
#     #     items = self._docks.unique_label_list.selectedItems()
#     #     text = None
#     #     if items:
#     #         text = items[0].data(Qt.UserRole)
#     #     flags = {}
#     #     group_id = None
#     #     description = ""
#     #     if self._config["display_label_popup"] or not text:
#     #         previous_text = self._label_dialog.edit.text()
#     #         text, flags, group_id, description = self._label_dialog.popUp(text)
#     #         if not text:
#     #             self._label_dialog.edit.setText(previous_text)

#     #     if text and not self.validateLabel(text):
#     #         self.errorMessage(
#     #             self.tr("Invalid label"),
#     #             self.tr("Invalid label '{}' with validation type '{}'").format(
#     #                 text, self._config["validate_label"]
#     #             ),
#     #         )
#     #         text = ""
#     #     if text:
#     #         self._docks.label_list.clearSelection()
#     #         shape = self._canvas_widgets.canvas.setLastLabel(text, flags)
#     #         shape.group_id = group_id
#     #         shape.description = description
#     #         self.addLabel(shape)
#     #         self._actions.edit_mode.setEnabled(True)
#     #         self._actions.undo_last_point.setEnabled(False)
#     #         self._actions.undo.setEnabled(True)
#     #         self.setDirty()
#     #     else:
#     #         self._canvas_widgets.canvas.undoLastLine()
#     #         self._canvas_widgets.canvas.shapesBackups.pop()

#     def scrollRequest(self, delta: int, orientation: Qt.Orientation) -> None:
#         units = -delta * 0.1  # natural scroll
#         bar = self._canvas_widgets.scroll_bars[orientation]
#         value = bar.value() + bar.singleStep() * units
#         self.setScroll(orientation, value)

#     def setScroll(self, orientation: Qt.Orientation, value: float) -> None:
#         self._canvas_widgets.scroll_bars[orientation].setValue(int(value))
#         if self._filename is not None:
#             self._scroll_values[orientation][self._filename] = value

#     def _set_zoom(self, value: int, pos: QtCore.QPointF | None = None) -> None:
#         if self._filename is None:
#             logger.warning("filename is None, cannot set zoom")
#             return

#         if pos is None:
#             pos = QtCore.QPointF(
#                 self._canvas_widgets.canvas.visibleRegion().boundingRect().center()
#             )
#         canvas_width_old: int = self._canvas_widgets.canvas.width()

#         self._actions.fit_width.setChecked(self._zoom_mode == _ZoomMode.FIT_WIDTH)
#         self._actions.fit_window.setChecked(self._zoom_mode == _ZoomMode.FIT_WINDOW)
#         self._canvas_widgets.canvas.enableDragging(
#             enabled=value > int(self._scalers[_ZoomMode.FIT_WINDOW]() * 100)
#         )
#         self._canvas_widgets.zoom_widget.setValue(value)  # triggers self._paint_canvas
#         self._zoom_values[self._filename] = (self._zoom_mode, value)

#         canvas_width_new: int = self._canvas_widgets.canvas.width()
#         if canvas_width_old == canvas_width_new:
#             return
#         canvas_scale_factor = canvas_width_new / canvas_width_old
#         x_shift: float = pos.x() * canvas_scale_factor - pos.x()
#         y_shift: float = pos.y() * canvas_scale_factor - pos.y()
#         self.setScroll(
#             Qt.Horizontal,
#             self._canvas_widgets.scroll_bars[Qt.Horizontal].value() + x_shift,
#         )
#         self.setScroll(
#             Qt.Vertical,
#             self._canvas_widgets.scroll_bars[Qt.Vertical].value() + y_shift,
#         )

#     def _set_zoom_to_original(self):
#         self._zoom_mode = _ZoomMode.MANUAL_ZOOM
#         self._set_zoom(value=100)

#     def _add_zoom(self, increment: float, pos: QtCore.QPointF | None = None) -> None:
#         zoom_value: int
#         if increment > 1:
#             zoom_value = math.ceil(self._canvas_widgets.zoom_widget.value() * increment)
#         else:
#             zoom_value = math.floor(
#                 self._canvas_widgets.zoom_widget.value() * increment
#             )
#         self._zoom_mode = _ZoomMode.MANUAL_ZOOM
#         self._set_zoom(value=zoom_value, pos=pos)

#     def _zoom_requested(self, delta: int, pos: QtCore.QPointF) -> None:
#         self._add_zoom(increment=1.1 if delta > 0 else 0.9, pos=pos)

#     def setFitWindow(self, value=True):
#         if value:
#             self._actions.fit_width.setChecked(False)
#         self._zoom_mode = _ZoomMode.FIT_WINDOW if value else _ZoomMode.MANUAL_ZOOM
#         self._adjust_scale()

#     def setFitWidth(self, value=True):
#         if value:
#             self._actions.fit_window.setChecked(False)
#         self._zoom_mode = _ZoomMode.FIT_WIDTH if value else _ZoomMode.MANUAL_ZOOM
#         self._adjust_scale()

#     def enableKeepPrevScale(self, enabled):
#         self._config["keep_prev_scale"] = enabled
#         self._actions.keep_prev_scale.setChecked(enabled)

#     def onNewBrightnessContrast(self, qimage):
#         self._canvas_widgets.canvas.loadPixmap(
#             QtGui.QPixmap.fromImage(qimage), clear_shapes=False
#         )

#     def brightnessContrast(self, value: bool, is_initial_load: bool = False):
#         if self._filename is None:
#             logger.warning("filename is None, cannot set brightness/contrast")
#             return

#         brightness: int | None
#         contrast: int | None
#         brightness, contrast = self._brightness_contrast_values.get(
#             self._filename, (None, None)
#         )
#         if is_initial_load:
#             prev_filename: str = self._recent_files[0] if self._recent_files else ""
#             if self._config["keep_prev_brightness_contrast"] and prev_filename:
#                 brightness, contrast = self._brightness_contrast_values.get(
#                     prev_filename, (None, None)
#                 )
#             if brightness is None and contrast is None:
#                 return

#         logger.debug(
#             "Opening brightness/contrast dialog with brightness={}, contrast={}",
#             brightness,
#             contrast,
#         )
#         dialog = BrightnessContrastDialog(
#             utils.img_data_to_pil(self.imageData),
#             self.onNewBrightnessContrast,
#             parent=self,
#         )

#         if brightness is not None:
#             dialog.slider_brightness.setValue(brightness)
#         if contrast is not None:
#             dialog.slider_contrast.setValue(contrast)

#         if is_initial_load:
#             dialog.onNewValue(None)
#         else:
#             dialog.exec_()
#             brightness = dialog.slider_brightness.value()
#             contrast = dialog.slider_contrast.value()

#         self._brightness_contrast_values[self._filename] = (brightness, contrast)
#         logger.debug(
#             "Updated states for {}: brightness={}, contrast={}",
#             self._filename,
#             brightness,
#             contrast,
#         )

#     def toggleShapes(self, value):
#         flag = value
#         for item in self._docks.label_list:
#             if value is None:
#                 flag = item.checkState() == Qt.Unchecked
#             item.setCheckState(Qt.Checked if flag else Qt.Unchecked)

#     def _load_file(self, filename=None):
#         """Load the specified file, or the last opened file if None."""
#         # changing fileListWidget loads file
#         if filename in self.imageList and (
#             self._docks.file_list.currentRow() != self.imageList.index(filename)
#         ):
#             self._docks.file_list.setCurrentRow(self.imageList.index(filename))
#             self._docks.file_list.repaint()
#             return

#         prev_shapes: list[Shape] = (
#             self._canvas_widgets.canvas.shapes
#             if self._config["keep_prev"]
#             or QtWidgets.QApplication.keyboardModifiers()
#             == (Qt.ControlModifier | Qt.ShiftModifier)
#             else []
#         )
#         self.resetState()
#         self._canvas_widgets.canvas.setEnabled(False)
#         if filename is None:
#             filename = self.settings.value("filename", "")
#         filename = str(filename)
#         if not QtCore.QFile.exists(filename):
#             self.errorMessage(
#                 self.tr("Error opening file"),
#                 self.tr("No such file: <b>%s</b>") % filename,
#             )
#             return False
#         # assumes same name, but json extension
#         self.show_status_message(self.tr("Loading %s...") % osp.basename(str(filename)))
#         t0_load_file = time.time()
#         label_file = f"{osp.splitext(filename)[0]}.json"
#         if self._output_dir:
#             label_file_without_path = osp.basename(label_file)
#             label_file = osp.join(self._output_dir, label_file_without_path)
#         if QtCore.QFile.exists(label_file) and LabelFile.is_label_file(label_file):
#             try:
#                 self._label_file = LabelFile(label_file)
#             except LabelFileError as e:
#                 self.errorMessage(
#                     self.tr("Error opening file"),
#                     self.tr(
#                         "<p><b>%s</b></p>"
#                         "<p>Make sure <i>%s</i> is a valid label file.</p>"
#                     )
#                     % (e, label_file),
#                 )
#                 self.show_status_message(self.tr("Error reading %s") % label_file)
#                 return False
#             assert self._label_file is not None
#             self.imageData = self._label_file.imageData
#             assert self._label_file.imagePath
#             self._image_path = osp.join(
#                 osp.dirname(label_file),
#                 self._label_file.imagePath,
#             )
#             self._other_data = self._label_file.otherData
#         else:
#             try:
#                 self.imageData = LabelFile.load_image_file(filename)
#             except OSError as e:
#                 self.errorMessage(
#                     self.tr("Error opening file"),
#                     self.tr(
#                         "<p><b>%s</b></p>"
#                         "<p>Make sure <i>%s</i> is a valid image file.</p>"
#                     )
#                     % (e, filename),
#                 )
#                 self.show_status_message(self.tr("Error reading %s") % filename)
#                 return False
#             if self.imageData:
#                 self._image_path = filename
#             self._label_file = None
#         assert self.imageData is not None
#         t0 = time.time()
#         image = QtGui.QImage.fromData(self.imageData)
#         logger.debug("Created QImage in {:.0f}ms", (time.time() - t0) * 1000)

#         if image.isNull():
#             formats = [
#                 f"*.{fmt.data().decode()}"
#                 for fmt in QtGui.QImageReader.supportedImageFormats()
#             ]
#             self.errorMessage(
#                 self.tr("Error opening file"),
#                 self.tr(
#                     "<p>Make sure <i>{0}</i> is a valid image file.<br/>"
#                     "Supported image formats: {1}</p>"
#                 ).format(filename, ",".join(formats)),
#             )
#             self.show_status_message(self.tr("Error reading %s") % filename)
#             return False
#         self._image = image
#         self._filename = filename
#         t0 = time.time()
#         self._canvas_widgets.canvas.loadPixmap(QtGui.QPixmap.fromImage(image))
#         logger.debug("Loaded pixmap in {:.0f}ms", (time.time() - t0) * 1000)
#         flags = {k: False for k in self._config["flags"] or []}
#         if self._label_file:
#             self._load_shape_dicts(shape_dicts=self._label_file.shapes)
#             if self._label_file.flags is not None:
#                 flags.update(self._label_file.flags)
#         self._load_flags(flags=flags, widget=self._docks.flag_list)
#         if prev_shapes and self.noShapes():
#             self._load_shapes(shapes=prev_shapes, replace=False)
#             self.setDirty()
#         else:
#             self.setClean()
#         self._canvas_widgets.canvas.setEnabled(True)
#         # set zoom values
#         is_initial_load = not self._zoom_values
#         if self._filename in self._zoom_values:
#             self._zoom_mode = self._zoom_values[self._filename][0]
#             self._set_zoom(self._zoom_values[self._filename][1])
#         elif is_initial_load or not self._config["keep_prev_scale"]:
#             self._zoom_mode = _ZoomMode.FIT_WINDOW
#             self._adjust_scale()
#         # set scroll values
#         for orientation in self._scroll_values:
#             if self._filename in self._scroll_values[orientation]:
#                 self.setScroll(
#                     orientation, self._scroll_values[orientation][self._filename]
#                 )
#         self.brightnessContrast(value=False, is_initial_load=True)
#         self._paint_canvas()
#         self.addRecentFile(self._filename)
#         self.toggleActions(True)
#         self._canvas_widgets.canvas.setFocus()
#         self.show_status_message(self.tr("Loaded %s") % osp.basename(filename))
#         logger.info(
#             "Loaded file: {!r} in {:.0f}ms",
#             filename,
#             (time.time() - t0_load_file) * 1000,
#         )
#         return True

#     def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
#         if (
#             self._canvas_widgets.canvas
#             and not self._image.isNull()
#             and self._zoom_mode != _ZoomMode.MANUAL_ZOOM
#         ):
#             self._adjust_scale()
#         super().resizeEvent(a0)

#     def _paint_canvas(self) -> None:
#         if self._image.isNull():
#             logger.warning("image is null, cannot paint canvas")
#             return
#         self._canvas_widgets.canvas.scale = (
#             0.01 * self._canvas_widgets.zoom_widget.value()
#         )
#         self._canvas_widgets.canvas.adjustSize()
#         self._canvas_widgets.canvas.update()

#     def _adjust_scale(self) -> None:
#         self._set_zoom(value=int(self._scalers[self._zoom_mode]() * 100))

#     def scaleFitWindow(self) -> float:
#         EPSILON_TO_HIDE_SCROLLBAR: float = 2.0
#         w1: float = self.centralWidget().width() - EPSILON_TO_HIDE_SCROLLBAR
#         h1: float = self.centralWidget().height() - EPSILON_TO_HIDE_SCROLLBAR
#         a1: float = w1 / h1

#         w2: float = self._canvas_widgets.canvas.pixmap.width()
#         h2: float = self._canvas_widgets.canvas.pixmap.height()
#         a2: float = w2 / h2

#         return w1 / w2 if a2 >= a1 else h1 / h2

#     def scaleFitWidth(self):
#         EPSILON_TO_HIDE_SCROLLBAR: float = 15.0
#         w = self.centralWidget().width() - EPSILON_TO_HIDE_SCROLLBAR
#         return w / self._canvas_widgets.canvas.pixmap.width()

#     def enableSaveImageWithData(self, enabled):
#         self._config["with_image_data"] = enabled
#         self._actions.save_with_image_data.setChecked(enabled)

#     def _reset_layout(self):
#         self.settings.remove("window/state")
#         self.restoreState(self._default_state)

#     def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
#         if not self._can_continue():
#             a0.ignore()
#         self.settings.setValue("filename", self._filename if self._filename else "")
#         self.settings.setValue("window/size", self.size())
#         self.settings.setValue("window/position", self.pos())
#         self.settings.setValue("window/state", self.saveState())
#         self.settings.setValue("recentFiles", self._recent_files)

#     def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
#         extensions = [
#             f".{fmt.data().decode().lower()}"
#             for fmt in QtGui.QImageReader.supportedImageFormats()
#         ]
#         if a0.mimeData().hasUrls():
#             items = [i.toLocalFile() for i in a0.mimeData().urls()]
#             if any([i.lower().endswith(tuple(extensions)) for i in items]):
#                 a0.accept()
#         else:
#             a0.ignore()

#     def dropEvent(self, a0: QtGui.QDropEvent) -> None:
#         if not self._can_continue():
#             a0.ignore()
#             return
#         items = [i.toLocalFile() for i in a0.mimeData().urls()]
#         self.importDroppedImageFiles(items)

#     # User Dialogs #

#     def loadRecent(self, filename):
#         if self._can_continue():
#             self._load_file(filename)

#     def _open_prev_image(self, _value=False) -> None:
#         row_prev: int = self._docks.file_list.currentRow() - 1
#         if row_prev < 0:
#             logger.debug("there is no prev image")
#             return

#         logger.debug("setting current row to {:d}", row_prev)
#         self._docks.file_list.setCurrentRow(row_prev)
#         self._docks.file_list.repaint()

#     def _open_next_image(self, _value=False) -> None:
#         row_next: int = self._docks.file_list.currentRow() + 1
#         if row_next >= self._docks.file_list.count():
#             logger.debug("there is no next image")
#             return

#         logger.debug("setting current row to {:d}", row_next)
#         self._docks.file_list.setCurrentRow(row_next)
#         self._docks.file_list.repaint()

#     def _open_file_with_dialog(self, _value: bool = False) -> None:
#         if not self._can_continue():
#             return
#         path = osp.dirname(str(self._filename)) if self._filename else "."
#         formats = [
#             f"*.{fmt.data().decode()}"
#             for fmt in QtGui.QImageReader.supportedImageFormats()
#         ]
#         filters = self.tr("Image & Label files (%s)") % " ".join(
#             formats + [f"*{LabelFile.suffix}"]
#         )
#         fileDialog = FileDialogPreview(self)
#         fileDialog.setFileMode(FileDialogPreview.ExistingFile)
#         fileDialog.setNameFilter(filters)
#         fileDialog.setWindowTitle(
#             self.tr("%s - Choose Image or Label file") % __appname__,
#         )
        
#         fileDialog.setWindowFilePath(path)
#         fileDialog.setViewMode(FileDialogPreview.Detail)
#         if fileDialog.exec_():
#             fileName = fileDialog.selectedFiles()[0]
#             if fileName:
#                 self._load_file(fileName)

#     def changeOutputDirDialog(self, _value=False):
#         default_output_dir = self._output_dir
#         if default_output_dir is None and self._filename:
#             default_output_dir = osp.dirname(self._filename)
#         if default_output_dir is None:
#             default_output_dir = self.currentPath()

#         output_dir = QtWidgets.QFileDialog.getExistingDirectory(
#             self,
#             self.tr("%s - Save/Load Annotations in Directory") % __appname__,
#             default_output_dir,
#             QtWidgets.QFileDialog.ShowDirsOnly
#             | QtWidgets.QFileDialog.DontResolveSymlinks,
#         )
#         output_dir = str(output_dir)

#         if not output_dir:
#             return

#         self._output_dir = output_dir

#         self.statusBar().showMessage(
#             self.tr("%s . Annotations will be saved/loaded in %s")
#             % ("Change Annotations Dir", self._output_dir)
#         )
#         self.statusBar().show()

#         current_filename = self._filename
#         self._import_images_from_dir(root_dir=self._prev_opened_dir)

#         if current_filename in self.imageList:
#             # retain currently selected file
#             self._docks.file_list.setCurrentRow(self.imageList.index(current_filename))
#             self._docks.file_list.repaint()

#     def saveFile(self, _value: bool = False) -> None:
#         assert not self._image.isNull(), "cannot save empty image"
#         if self._label_file:
#             self._saveFile(self._label_file.filename)
#         else:
#             self._saveFile(self.saveFileDialog())

#     def saveFileAs(self, _value: bool = False) -> None:
#         assert not self._image.isNull(), "cannot save empty image"
#         self._saveFile(self.saveFileDialog())

#     def saveFileDialog(self) -> str:
#         assert self._filename is not None
#         caption = self.tr("%s - Choose File") % __appname__
#         filters = self.tr("Label files (*%s)") % LabelFile.suffix
#         start_dir = self._output_dir if self._output_dir else self.currentPath()
#         dlg = QtWidgets.QFileDialog(self, caption, start_dir, filters)
#         dlg.setDefaultSuffix(LabelFile.suffix[1:])
#         dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
#         dlg.setOption(QtWidgets.QFileDialog.DontConfirmOverwrite, False)
#         dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, False)
#         basename = osp.basename(osp.splitext(self._filename)[0])
#         if self._output_dir:
#             default_labelfile_name = osp.join(
#                 self._output_dir, basename + LabelFile.suffix
#             )
#         else:
#             default_labelfile_name = osp.join(
#                 self.currentPath(), basename + LabelFile.suffix
#             )
#         filename = dlg.getSaveFileName(
#             self,
#             self.tr("Choose File"),
#             default_labelfile_name,
#             self.tr("Label files (*%s)") % LabelFile.suffix,
#         )
#         if isinstance(filename, tuple):
#             return filename[0]
#         return filename

#     def _saveFile(self, filename: str | None) -> None:
#         if filename and self.saveLabels(filename):
#             self.addRecentFile(filename)
#             self.setClean()

#     def closeFile(self, _value: bool = False) -> None:
#         if not self._can_continue():
#             return
#         self.resetState()
#         self.setClean()
#         self.toggleActions(False)
#         self._canvas_widgets.canvas.setEnabled(False)
#         self._docks.file_list.setFocus()
#         self._actions.save_as.setEnabled(False)

#     def getLabelFile(self) -> str:
#         assert self._filename is not None
#         if self._filename.lower().endswith(".json"):
#             return self._filename
#         return f"{osp.splitext(self._filename)[0]}.json"

#     def deleteFile(self) -> None:
#         mb = QtWidgets.QMessageBox
#         msg = self.tr(
#             "You are about to permanently delete this label file, proceed anyway?"
#         )
#         answer = mb.warning(self, self.tr("Attention"), msg, mb.Yes | mb.No)
#         if answer != mb.Yes:
#             return

#         label_file = self.getLabelFile()
#         if osp.exists(label_file):
#             os.remove(label_file)
#             logger.info(f"Label file is removed: {label_file}")

#             item = self._docks.file_list.currentItem()
#             if item:
#                 item.setCheckState(Qt.Unchecked)

#             self.resetState()

#     def _open_config_file(self) -> None:
#         if self._config_file is None:
#             QtWidgets.QMessageBox.information(
#                 self,
#                 self.tr("No Config File"),
#                 self.tr(
#                     "Configuration was provided as a YAML expression via "
#                     "command line.\n\n"
#                     "To use the preferences editor, start Labelme with a config file:\n"
#                     "  labelme --config ~/.labelmerc"
#                 ),
#             )
#             return
#         config_file: Path = self._config_file

#         system: str = platform.system()
#         if system == "Darwin":
#             subprocess.Popen(["open", "-t", config_file])
#         elif system == "Windows":
#             os.startfile(config_file)  # type: ignore[attr-defined]
#         else:
#             subprocess.Popen(["xdg-open", config_file])

#     # Message Dialogs. #
#     def hasLabels(self) -> bool:
#         if self.noShapes():
#             self.errorMessage(
#                 "No objects labeled",
#                 "You must label at least one object to save the file.",
#             )
#             return False
#         return True

#     def hasLabelFile(self) -> bool:
#         if self._filename is None:
#             return False

#         label_file = self.getLabelFile()
#         return osp.exists(label_file)

#     def _can_continue(self) -> bool:
#         if not self._is_changed:
#             return True
#         mb = QtWidgets.QMessageBox
#         msg = self.tr('Save annotations to "{}" before closing?').format(self._filename)
#         answer = mb.question(
#             self,
#             self.tr("Save annotations?"),
#             msg,
#             mb.Save | mb.Discard | mb.Cancel,
#             mb.Save,
#         )
#         if answer == mb.Discard:
#             return True
#         elif answer == mb.Save:
#             self.saveFile()
#             return True
#         else:  # answer == mb.Cancel
#             return False

#     def errorMessage(self, title: str, message: str) -> int:
#         return QtWidgets.QMessageBox.critical(
#             self, title, f"<p><b>{title}</b></p>{message}"
#         )

#     def currentPath(self) -> str:
#         return osp.dirname(str(self._filename)) if self._filename else "."

#     def toggleKeepPrevMode(self) -> None:
#         self._config["keep_prev"] = not self._config["keep_prev"]

#     def removeSelectedPoint(self) -> None:
#         self._canvas_widgets.canvas.removeSelectedPoint()
#         self._canvas_widgets.canvas.update()
#         if (
#             self._canvas_widgets.canvas.hShape
#             and not self._canvas_widgets.canvas.hShape.points
#         ):
#             self._canvas_widgets.canvas.deleteShape(self._canvas_widgets.canvas.hShape)
#             self.remLabels([self._canvas_widgets.canvas.hShape])
#             if self.noShapes():
#                 for action in self._actions.on_shapes_present:
#                     action.setEnabled(False)
#         self.setDirty()

#     def deleteSelectedShape(self) -> None:
#         yes, no = QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No
#         msg = self.tr(
#             "You are about to permanently delete {} shapes, proceed anyway?"
#         ).format(len(self._canvas_widgets.canvas.selectedShapes))
#         if yes == QtWidgets.QMessageBox.warning(
#             self, self.tr("Attention"), msg, yes | no, yes
#         ):
#             self.remLabels(self._canvas_widgets.canvas.deleteSelected())
#             self.setDirty()
#             if self.noShapes():
#                 for action in self._actions.on_shapes_present:
#                     action.setEnabled(False)

#     def copyShape(self) -> None:
#         self._canvas_widgets.canvas.endMove(copy=True)
#         for shape in self._canvas_widgets.canvas.selectedShapes:
#             self.addLabel(shape)
#         self._docks.label_list.clearSelection()
#         self.setDirty()

#     def moveShape(self) -> None:
#         self._canvas_widgets.canvas.endMove(copy=False)
#         self.setDirty()

#     def _open_dir_with_dialog(self, _value: bool = False) -> None:
#         if not self._can_continue():
#             return

#         defaultOpenDirPath: str
#         if self._prev_opened_dir and osp.exists(self._prev_opened_dir):
#             defaultOpenDirPath = self._prev_opened_dir
#         else:
#             defaultOpenDirPath = osp.dirname(self._filename) if self._filename else "."

#         targetDirPath = str(
#             QtWidgets.QFileDialog.getExistingDirectory(
#                 self,
#                 self.tr("%s - Open Directory") % __appname__,
#                 defaultOpenDirPath,
#                 QtWidgets.QFileDialog.ShowDirsOnly
#                 | QtWidgets.QFileDialog.DontResolveSymlinks,
#             )
#         )
#         self._import_images_from_dir(root_dir=targetDirPath)
#         self._open_next_image()

#     @property
#     def imageList(self) -> list[str]:
#         lst = []
#         for i in range(self._docks.file_list.count()):
#             item = self._docks.file_list.item(i)
#             assert item
#             lst.append(item.text())
#         return lst

#     def importDroppedImageFiles(self, imageFiles):
#         extensions = [
#             f".{fmt.data().decode().lower()}"
#             for fmt in QtGui.QImageReader.supportedImageFormats()
#         ]

#         self._filename = None
#         for file in imageFiles:
#             if file in self.imageList or not file.lower().endswith(tuple(extensions)):
#                 continue
#             label_file = f"{osp.splitext(file)[0]}.json"
#             if self._output_dir:
#                 label_file_without_path = osp.basename(label_file)
#                 label_file = osp.join(self._output_dir, label_file_without_path)
#             item = QtWidgets.QListWidgetItem(file)
#             item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
#             if QtCore.QFile.exists(label_file) and LabelFile.is_label_file(label_file):
#                 item.setCheckState(Qt.Checked)
#             else:
#                 item.setCheckState(Qt.Unchecked)
#             self._docks.file_list.addItem(item)

#         if len(self.imageList) > 1:
#             self._actions.open_next_img.setEnabled(True)
#             self._actions.open_prev_img.setEnabled(True)

#         self._open_next_image()

#     def _import_images_from_dir(
#         self, root_dir: str | None, pattern: str | None = None
#     ) -> None:
#         self._actions.open_next_img.setEnabled(True)
#         self._actions.open_prev_img.setEnabled(True)

#         if not self._can_continue() or not root_dir:
#             return

#         self._prev_opened_dir = root_dir
#         self._filename = None
#         self._docks.file_list.clear()

#         filenames = _scan_image_files(root_dir=root_dir)
#         if pattern:
#             try:
#                 filenames = [f for f in filenames if re.search(pattern, f)]
#             except re.error:
#                 pass
#         for filename in filenames:
#             label_file = f"{osp.splitext(filename)[0]}.json"
#             if self._output_dir:
#                 label_file_without_path = osp.basename(label_file)
#                 label_file = osp.join(self._output_dir, label_file_without_path)
#             item = QtWidgets.QListWidgetItem(filename)
#             item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
#             if QtCore.QFile.exists(label_file) and LabelFile.is_label_file(label_file):
#                 item.setCheckState(Qt.Checked)
#             else:
#                 item.setCheckState(Qt.Unchecked)
#             self._docks.file_list.addItem(item)

#     def _update_status_stats(self, mouse_pos: QtCore.QPointF) -> None:
#         stats: list[str] = []
#         stats.append(f"mode={self._canvas_widgets.canvas.mode.name}")
#         stats.append(f"x={mouse_pos.x():6.1f}, y={mouse_pos.y():6.1f}")
#         self._status_bar.stats.setText(" | ".join(stats))


# def _scan_image_files(root_dir: str) -> list[str]:
#     extensions: list[str] = [
#         f".{fmt.data().decode().lower()}"
#         for fmt in QtGui.QImageReader.supportedImageFormats()
#     ]

#     images: list[str] = []
#     for root, dirs, files in os.walk(root_dir):
#         for file in files:
#             if file.lower().endswith(tuple(extensions)):
#                 relativePath = os.path.normpath(osp.join(root, file))
#                 images.append(relativePath)

#     logger.debug("found {:d} images in {!r}", len(images), root_dir)
#     return natsort.os_sorted(images)


from __future__ import annotations

import enum
import functools
import html
import math
import os
import os.path as osp
import platform
import re
import subprocess
import time
import webbrowser
from collections.abc import Callable
from pathlib import Path
from typing import Literal
from typing import NamedTuple

import imgviz
import natsort
import numpy as np
import osam
from loguru import logger
from numpy.typing import NDArray
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import cv2
from qtpy import QtCore

from labelme import __appname__
from labelme import __version__
from labelme._automation import bbox_from_text
from labelme._automation._osam_session import OsamSession
from labelme._label_file import LabelFile
from labelme._label_file import LabelFileError
from labelme._label_file import ShapeDict
from labelme.config import load_config
from labelme.shape import Shape
from labelme.widgets import AiAssistedAnnotationWidget
from labelme.widgets import AiTextToAnnotationWidget
from labelme.widgets import BrightnessContrastDialog
from labelme.widgets import Canvas
from labelme.widgets import FileDialogPreview
from labelme.widgets import LabelDialog
from labelme.widgets import LabelListWidget
from labelme.widgets import LabelListWidgetItem
from labelme.widgets import StatusStats
from labelme.widgets import ToolBar
from labelme.widgets import UniqueLabelQListWidget
from labelme.widgets import ZoomWidget
from labelme.widgets import download_ai_model

from . import utils

# handle high-dpi scaling issue
# https://leomoon.com/journal/python/high-dpi-scaling-in-pyqt5
if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


LABEL_COLORMAP: NDArray[np.uint8] = imgviz.label_colormap()


class _ZoomMode(enum.Enum):
    FIT_WINDOW = enum.auto()
    FIT_WIDTH = enum.auto()
    MANUAL_ZOOM = enum.auto()


_AI_TEXT_TO_ANNOTATION_CREATE_MODE_TO_SHAPE_TYPE: dict[
    str, Literal["mask", "polygon", "rectangle"]
] = {
    "ai_mask": "mask",
    "ai_polygon": "polygon",
    "polygon": "polygon",
    "rectangle": "rectangle",
}


class _StatusBarWidgets(NamedTuple):
    message: QtWidgets.QLabel
    stats: StatusStats


class _CanvasWidgets(NamedTuple):
    canvas: Canvas
    zoom_widget: ZoomWidget
    scroll_bars: dict[Qt.Orientation, QtWidgets.QScrollBar]


class _DockWidgets(NamedTuple):
    flag_dock: QtWidgets.QDockWidget
    flag_list: QtWidgets.QListWidget
    shape_dock: QtWidgets.QDockWidget
    label_list: LabelListWidget
    label_dock: QtWidgets.QDockWidget
    unique_label_list: UniqueLabelQListWidget
    file_dock: QtWidgets.QDockWidget
    file_search: QtWidgets.QLineEdit
    file_list: QtWidgets.QListWidget


class _Actions(NamedTuple):
    about: QtWidgets.QAction
    save: QtWidgets.QAction
    save_as: QtWidgets.QAction
    save_auto: QtWidgets.QAction
    save_with_image_data: QtWidgets.QAction
    change_output_dir: QtWidgets.QAction
    open: QtWidgets.QAction
    close: QtWidgets.QAction
    delete_file: QtWidgets.QAction
    toggle_keep_prev_mode: QtWidgets.QAction
    toggle_keep_prev_brightness_contrast: QtWidgets.QAction
    delete: QtWidgets.QAction
    edit: QtWidgets.QAction
    duplicate: QtWidgets.QAction
    copy: QtWidgets.QAction
    paste: QtWidgets.QAction
    undo_last_point: QtWidgets.QAction
    undo: QtWidgets.QAction
    remove_point: QtWidgets.QAction
    create_mode: QtWidgets.QAction
    edit_mode: QtWidgets.QAction
    create_rectangle_mode: QtWidgets.QAction
    create_circle_mode: QtWidgets.QAction
    create_line_mode: QtWidgets.QAction
    create_point_mode: QtWidgets.QAction
    create_line_strip_mode: QtWidgets.QAction
    create_ai_polygon_mode: QtWidgets.QAction
    create_ai_mask_mode: QtWidgets.QAction
    open_next_img: QtWidgets.QAction
    open_prev_img: QtWidgets.QAction
    keep_prev_scale: QtWidgets.QAction
    fit_window: QtWidgets.QAction
    fit_width: QtWidgets.QAction
    brightness_contrast: QtWidgets.QAction
    zoom_in: QtWidgets.QAction
    zoom_out: QtWidgets.QAction
    zoom_org: QtWidgets.QAction
    reset_layout: QtWidgets.QAction
    fill_drawing: QtWidgets.QAction
    hide_all: QtWidgets.QAction
    show_all: QtWidgets.QAction
    toggle_all: QtWidgets.QAction
    open_dir: QtWidgets.QAction
    zoom_widget_action: QtWidgets.QWidgetAction
    draw: list[tuple[str, QtWidgets.QAction]]
    zoom: tuple[ZoomWidget | QtWidgets.QAction, ...]
    on_load_active: tuple[QtWidgets.QAction, ...]
    on_shapes_present: tuple[QtWidgets.QAction, ...]
    context_menu: tuple[QtWidgets.QAction, ...]
    edit_menu: tuple[QtWidgets.QAction | None, ...]


class _Menus(NamedTuple):
    file: QtWidgets.QMenu
    edit: QtWidgets.QMenu
    view: QtWidgets.QMenu
    help: QtWidgets.QMenu
    recent_files: QtWidgets.QMenu
    label_list: QtWidgets.QMenu


class MainWindow(QtWidgets.QMainWindow):
    _config_file: Path | None
    _config: dict

    _text_osam_session: OsamSession | None = None
    _is_changed: bool = False
    _copied_shapes: list[Shape]
    _zoom_mode: _ZoomMode
    _prev_opened_dir: str | None
    _canvas_widgets: _CanvasWidgets
    _status_bar: _StatusBarWidgets
    _docks: _DockWidgets
    _actions: _Actions
    _menus: _Menus
    _scalers: dict[_ZoomMode, Callable[[], float]]
    _label_dialog: LabelDialog
    _ai_annotation: AiAssistedAnnotationWidget
    _ai_text: AiTextToAnnotationWidget

    _output_dir: str | None
    _filename: str | None
    _image: QtGui.QImage
    _label_file: LabelFile | None
    _image_path: str | None
    _recent_files: list[str]
    _max_recent: int
    _other_data: dict | None
    _zoom_values: dict[str, tuple[_ZoomMode, int]]
    _brightness_contrast_values: dict[str, tuple[int | None, int | None]]
    _scroll_values: dict[Qt.Orientation, dict[str, float]]
    _default_state: QtCore.QByteArray

    def __init__(
        self,
        config_file: Path | None = None,
        config_overrides: dict | None = None,
        filename: str | None = None,
        output_dir: str | None = None,
    ) -> None:
        super().__init__()
        self.setWindowTitle(__appname__)
        

        self._config_file, self._config = self._load_config(
            config_file=config_file, config_overrides=config_overrides
        )

        # set default shape colors
        Shape.line_color = QtGui.QColor(*self._config["shape"]["line_color"])
        Shape.fill_color = QtGui.QColor(*self._config["shape"]["fill_color"])
        Shape.select_line_color = QtGui.QColor(
            *self._config["shape"]["select_line_color"]
        )
        Shape.select_fill_color = QtGui.QColor(
            *self._config["shape"]["select_fill_color"]
        )
        Shape.vertex_fill_color = QtGui.QColor(
            *self._config["shape"]["vertex_fill_color"]
        )
        Shape.hvertex_fill_color = QtGui.QColor(
            *self._config["shape"]["hvertex_fill_color"]
        )

        # Set point size from config file
        Shape.point_size = self._config["shape"]["point_size"]

        self._copied_shapes = []

        self._label_dialog = LabelDialog(
            parent=self,
            labels=self._config["labels"],
            sort_labels=self._config["sort_labels"],
            show_text_field=self._config["show_label_text_field"],
            completion=self._config["label_completion"],
            fit_to_content=self._config["fit_to_content"],
            flags=self._config["label_flags"],
        )

        self._prev_opened_dir = None
        self._docks = self._setup_dock_widgets()

        self.setAcceptDrops(True)
        self._canvas_widgets = self._setup_canvas()
        self._canvas_widgets.canvas.selectionChanged.connect(self.sync_selection_to_list) #attiva la selezione delle linee automatiche
        self._actions = self._setup_actions()
        self._scalers = {
            _ZoomMode.FIT_WINDOW: self.scaleFitWindow,
            _ZoomMode.FIT_WIDTH: self.scaleFitWidth,
            _ZoomMode.MANUAL_ZOOM: lambda: 1,
        }
        self._menus = self._setup_menus()

        self._ai_annotation = AiAssistedAnnotationWidget(
            default_model=self._config["ai"]["default"],
            on_model_changed=self._canvas_widgets.canvas.set_ai_model_name,
            parent=self,
        )
        self._ai_annotation.setEnabled(False)

        self._ai_text = AiTextToAnnotationWidget(
            on_submit=self._submit_ai_prompt, parent=self
        )
        self._ai_text.setEnabled(False)

        self._setup_toolbars()

        self._status_bar = self._setup_status_bar()

        self._setup_app_state(output_dir=output_dir, filename=filename)

        self.updateFileMenu()

        self._canvas_widgets.zoom_widget.valueChanged.connect(self._paint_canvas)

        self.populateModeActions()

    def _setup_actions(self) -> _Actions:
        action = functools.partial(utils.newAction, self)
        shortcuts = self._config["shortcuts"]

        about = action(
            text=f"&About {__appname__}",
            slot=functools.partial(
                QMessageBox.about,
                self,
                f"About {__appname__}",
                f"""
<h3>{__appname__}</h3>
<p>Image Polygonal Annotation with Python</p>
<p>Version: {__version__}</p>
<p>Author: Kentaro Wada</p>
<p>
    <a href="https://labelme.io">Homepage</a> |
    <a href="https://labelme.io/docs">Documentation</a> |
    <a href="https://labelme.io/docs/troubleshoot">Troubleshooting</a>
</p>
<p>
    <a href="https://github.com/wkentaro/labelme">GitHub</a> |
    <a href="https://x.com/labelmeai">Twitter/X</a>
</p>
""",
            ),
        )
        save = action(
            text=self.tr("&Save\n"),
            slot=self.saveFile,
            shortcut=shortcuts["save"],
            icon="floppy-disk.svg",
            tip=self.tr("Save labels to file"),
            enabled=False,
        )
        save_as = action(
            text=self.tr("&Save As"),
            slot=self.saveFileAs,
            shortcut=shortcuts["save_as"],
            icon="floppy-disk.svg",
            tip=self.tr("Save labels to a different file"),
            enabled=False,
        )
        save_auto = action(
            text=self.tr("Save &Automatically"),
            tip=self.tr("Save automatically"),
            checkable=True,
            enabled=True,
        )
        save_auto.setChecked(self._config["auto_save"])
        save_with_image_data = action(
            text=self.tr("Save With Image Data"),
            slot=self.enableSaveImageWithData,
            tip=self.tr("Save image data in label file"),
            checkable=True,
            checked=self._config["with_image_data"],
        )
        change_output_dir = action(
            text=self.tr("&Change Output Dir"),
            slot=self.changeOutputDirDialog,
            shortcut=shortcuts["save_to"],
            icon="folders.svg",
            tip=self.tr("Change where annotations are loaded/saved"),
        )
        open_ = action(
            text=self.tr("&Open\n"),
            slot=self._open_file_with_dialog,
            shortcut=shortcuts["open"],
            icon="folder-open.svg",
            tip=self.tr("Open image or label file"),
        )
        open_dir = action(
            text=self.tr("Open Dir"),
            slot=self._open_dir_with_dialog,
            shortcut=shortcuts["open_dir"],
            icon="folder-open.svg",
            tip=self.tr("Open Dir"),
        )
        close = action(
            text=self.tr("&Close"),
            slot=self.closeFile,
            shortcut=shortcuts["close"],
            icon="x-circle.svg",
            tip=self.tr("Close current file"),
        )
        delete_file = action(
            text=self.tr("&Delete File"),
            slot=self.deleteFile,
            shortcut=shortcuts["delete_file"],
            icon="file-x.svg",
            tip=self.tr("Delete current label file"),
            enabled=False,
        )
        toggle_keep_prev_mode = action(
            text=self.tr("Keep Previous Annotation"),
            slot=self.toggleKeepPrevMode,
            shortcut=shortcuts["toggle_keep_prev_mode"],
            icon=None,
            tip=self.tr('Toggle "keep previous annotation" mode'),
            checkable=True,
        )
        toggle_keep_prev_mode.setChecked(self._config["keep_prev"])
        toggle_keep_prev_brightness_contrast = action(
            text=self.tr("Keep Previous Brightness/Contrast"),
            slot=lambda: self._config.__setitem__(
                "keep_prev_brightness_contrast",
                not self._config["keep_prev_brightness_contrast"],
            ),
            checkable=True,
            checked=self._config["keep_prev_brightness_contrast"],
        )
        delete = action(
            self.tr("Delete Shapes"),
            self.deleteSelectedShape,
            shortcuts["delete_shape"],
            icon="trash.svg",
            tip=self.tr("Delete the selected shapes"),
            enabled=False,
        )
        edit = action(
            self.tr("&Edit Label"),
            self._edit_label,
            shortcuts["edit_label"],
            icon="note-pencil.svg",
            tip=self.tr("Modify the label of the selected shape"),
            enabled=False,
        )
        duplicate = action(
            self.tr("Duplicate Shapes"),
            self.duplicateSelectedShape,
            shortcuts["duplicate_shape"],
            icon="copy.svg",
            tip=self.tr("Create a duplicate of the selected shapes"),
            enabled=False,
        )
        copy = action(
            self.tr("Copy Shapes"),
            self.copySelectedShape,
            shortcuts["copy_shape"],
            "copy_clipboard",
            self.tr("Copy selected shapes to clipboard"),
            enabled=False,
        )
        paste = action(
            self.tr("Paste Shapes"),
            self.pasteSelectedShape,
            shortcuts["paste_shape"],
            "paste",
            self.tr("Paste copied shapes"),
            enabled=False,
        )
        undo_last_point = action(
            self.tr("Undo last point"),
            self._canvas_widgets.canvas.undoLastPoint,
            shortcuts["undo_last_point"],
            icon="arrow-u-up-left.svg",
            tip=self.tr("Undo last drawn point"),
            enabled=False,
        )
        undo = action(
            self.tr("Undo\n"),
            self.undoShapeEdit,
            shortcuts["undo"],
            icon="arrow-u-up-left.svg",
            tip=self.tr("Undo last add and edit of shape"),
            enabled=False,
        )
        remove_point = action(
            text=self.tr("Remove Selected Point"),
            slot=self.removeSelectedPoint,
            shortcut=shortcuts["remove_selected_point"],
            icon="trash.svg",
            tip=self.tr("Remove selected point from polygon"),
            enabled=False,
        )
        create_mode = action(
            text=self.tr("Create Polygons"),
            slot=lambda: self._switch_canvas_mode(edit=False, createMode="polygon"),
            shortcut=shortcuts["create_polygon"],
            icon="polygon.svg",
            tip=self.tr("Start drawing polygons"),
            enabled=False,
        )
        edit_mode = action(
            self.tr("Edit Shapes"),
            lambda: self._switch_canvas_mode(edit=True),
            shortcuts["edit_shape"],
            icon="note-pencil.svg",
            tip=self.tr("Move and edit the selected shapes"),
            enabled=False,
        )
        create_rectangle_mode = action(
            text=self.tr("Create Rectangle"),
            slot=lambda: self._switch_canvas_mode(edit=False, createMode="rectangle"),
            shortcut=shortcuts["create_rectangle"],
            icon="rectangle.svg",
            tip=self.tr("Start drawing rectangles"),
            enabled=False,
        )
        create_circle_mode = action(
            text=self.tr("Create Circle"),
            slot=lambda: self._switch_canvas_mode(edit=False, createMode="circle"),
            shortcut=shortcuts["create_circle"],
            icon="circle.svg",
            tip=self.tr("Start drawing circles"),
            enabled=False,
        )
        create_line_mode = action(
            text=self.tr("Create Line"),
            slot=lambda: self._switch_canvas_mode(edit=False, createMode="line"),
            shortcut=shortcuts["create_line"],
            icon="line-segment.svg",
            tip=self.tr("Start drawing lines"),
            enabled=False,
        )
        create_point_mode = action(
            text=self.tr("Create Point"),
            slot=lambda: self._switch_canvas_mode(edit=False, createMode="point"),
            shortcut=shortcuts["create_point"],
            icon="circles-four.svg",
            tip=self.tr("Start drawing points"),
            enabled=False,
        )
        create_line_strip_mode = action(
            text=self.tr("Create LineStrip"),
            slot=lambda: self._switch_canvas_mode(edit=False, createMode="linestrip"),
            shortcut=shortcuts["create_linestrip"],
            icon="line-segments.svg",
            tip=self.tr("Start drawing linestrip. Ctrl+LeftClick ends creation."),
            enabled=False,
        )
        create_ai_polygon_mode = action(
            self.tr("Create AI-Polygon"),
            lambda: self._switch_canvas_mode(edit=False, createMode="ai_polygon"),
            None,
            "ai-polygon.svg",
            self.tr("Start drawing ai_polygon. Ctrl+LeftClick ends creation."),
            enabled=False,
        )
        create_ai_mask_mode = action(
            self.tr("Create AI-Mask"),
            lambda: self._switch_canvas_mode(edit=False, createMode="ai_mask"),
            None,
            "ai-mask.svg",
            self.tr("Start drawing ai_mask. Ctrl+LeftClick ends creation."),
            enabled=False,
        )
        # --- YOUR CUSTOM ACTION ---
        actionAutoDetect = action(
            text=self.tr("Auto-Detect Linee"),
            slot=self.auto_detect_lines, 
            shortcut="Ctrl+Shift+X",
            icon="magic.svg", 
            tip=self.tr("Rileva automaticamente le linee nella vista corrente"),
            enabled=False, 
        )

        actionProjectlines = action(
            text=self.tr("Projections Lines"),
            slot=self.project_lines_preview, 
            shortcut="Ctrl+Shift+P",
            icon="Projection_and_rejection.svg", 
            tip=self.tr("Proietta le linee fino all'intersezione con i bordi dell'immagine"),
            enabled=False, 
        )

        actionProjectlines2txt = action(
            text=self.tr("Save Projected Lines"),
            slot=self.export_segments_to_txt, 
            shortcut="Ctrl+Shift+K", 
            tip=self.tr("Salva le linee proiettate in txt"),
            enabled=False, 
        )

        actionMergeLines = action(
            text = self.tr("Merge Lines"),
            slot = self.merge_parallel_lines,
            shortcut="Ctrl+Shift+M", 
            icon="merging.svg", 
            tip=self.tr("Fonde le linee parallele entro un certo epsilon"),
            enabled=False
        )
        ######################################################
        
        open_next_img = action(
            text=self.tr("&Next Image"),
            slot=self._open_next_image,
            shortcut=shortcuts["open_next"],
            icon="arrow-fat-right.svg",
            tip=self.tr("Open next (hold Ctl+Shift to copy labels)"),
            enabled=False,
        )
        open_prev_img = action(
            text=self.tr("&Prev Image"),
            slot=self._open_prev_image,
            shortcut=shortcuts["open_prev"],
            icon="arrow-fat-left.svg",
            tip=self.tr("Open prev (hold Ctl+Shift to copy labels)"),
            enabled=False,
        )
        keep_prev_scale = action(
            self.tr("&Keep Previous Scale"),
            self.enableKeepPrevScale,
            tip=self.tr("Keep previous zoom scale"),
            checkable=True,
            checked=self._config["keep_prev_scale"],
            enabled=True,
        )
        fit_window = action(
            self.tr("&Fit Window"),
            self.setFitWindow,
            shortcuts["fit_window"],
            icon="frame-corners.svg",
            tip=self.tr("Zoom follows window size"),
            checkable=True,
            enabled=False,
        )
        fit_width = action(
            self.tr("Fit &Width"),
            self.setFitWidth,
            shortcuts["fit_width"],
            icon="frame-arrows-horizontal.svg",
            tip=self.tr("Zoom follows window width"),
            checkable=True,
            enabled=False,
        )
        brightness_contrast = action(
            self.tr("&Brightness Contrast"),
            self.brightnessContrast,
            None,
            "brightness-contrast.svg",
            self.tr("Adjust brightness and contrast"),
            enabled=False,
        )
        zoom_in = action(
            self.tr("Zoom &In"),
            lambda _: self._add_zoom(increment=1.1),
            shortcuts["zoom_in"],
            icon="magnifying-glass-minus.svg",
            tip=self.tr("Increase zoom level"),
            enabled=False,
        )
        zoom_out = action(
            self.tr("&Zoom Out"),
            lambda _: self._add_zoom(increment=0.9),
            shortcuts["zoom_out"],
            icon="magnifying-glass-plus.svg",
            tip=self.tr("Decrease zoom level"),
            enabled=False,
        )
        zoom_org = action(
            self.tr("&Original size"),
            self._set_zoom_to_original,
            shortcuts["zoom_to_original"],
            icon="image-square.svg",
            tip=self.tr("Zoom to original size"),
            enabled=False,
        )
        reset_layout = action(
            text=self.tr("Reset Layout"),
            slot=self._reset_layout,
            icon="layout-duotone.svg",
        )
        fill_drawing = action(
            self.tr("Fill Drawing Polygon"),
            self._canvas_widgets.canvas.setFillDrawing,
            None,
            icon="paint-bucket.svg",
            tip=self.tr("Fill polygon while drawing"),
            checkable=True,
            enabled=True,
        )
        if self._config["canvas"]["fill_drawing"]:
            fill_drawing.trigger()
        hide_all = action(
            self.tr("&Hide\nShapes"),
            functools.partial(self.toggleShapes, False),
            shortcuts["hide_all_shapes"],
            icon="eye.svg",
            tip=self.tr("Hide all shapes"),
            enabled=False,
        )
        show_all = action(
            self.tr("&Show\nShapes"),
            functools.partial(self.toggleShapes, True),
            shortcuts["show_all_shapes"],
            icon="eye.svg",
            tip=self.tr("Show all shapes"),
            enabled=False,
        )
        toggle_all = action(
            self.tr("&Toggle\nShapes"),
            functools.partial(self.toggleShapes, None),
            shortcuts["toggle_all_shapes"],
            icon="eye.svg",
            tip=self.tr("Toggle all shapes"),
            enabled=False,
        )

        zoom_widget_action = QtWidgets.QWidgetAction(self)
        zoom_box_layout = QtWidgets.QVBoxLayout()
        zoom_label = QtWidgets.QLabel(self.tr("Zoom"))
        zoom_label.setAlignment(Qt.AlignCenter)
        zoom_box_layout.addWidget(zoom_label)
        zoom_box_layout.addWidget(self._canvas_widgets.zoom_widget)
        zoom_widget_action.setDefaultWidget(QtWidgets.QWidget())
        zoom_widget_action.defaultWidget().setLayout(zoom_box_layout)
        self._canvas_widgets.zoom_widget.setWhatsThis(
            str(
                self.tr(
                    "Zoom in or out of the image. Also accessible with "
                    "{} and {} from the canvas."
                )
            ).format(
                utils.fmtShortcut(f"{shortcuts['zoom_in']},{shortcuts['zoom_out']}"),
                utils.fmtShortcut(self.tr("Ctrl+Wheel")),
            )
        )
        self._canvas_widgets.zoom_widget.setEnabled(False)

        self._zoom_mode = _ZoomMode.FIT_WINDOW
        fit_window.setChecked(Qt.Checked)

        self._canvas_widgets.canvas.vertexSelected.connect(remove_point.setEnabled)

        draw = [
            ("polygon", create_mode),
            ("rectangle", create_rectangle_mode),
            ("circle", create_circle_mode),
            ("point", create_point_mode),
            ("line", create_line_mode),
            ("linestrip", create_line_strip_mode),
            ("ai_polygon", create_ai_polygon_mode),
            ("ai_mask", create_ai_mask_mode),
            ("Auto-Detect Linee", actionAutoDetect),
            ("Projections Lines",actionProjectlines),
            ("Save Projected Lines", actionProjectlines2txt),
            ("Merge Lines", actionMergeLines)
        ]
        zoom = (
            self._canvas_widgets.zoom_widget,
            zoom_in,
            zoom_out,
            zoom_org,
            fit_window,
            fit_width,
        )
        on_load_active = (
            close,
            create_mode,
            create_rectangle_mode,
            create_circle_mode,
            create_line_mode,
            create_point_mode,
            create_line_strip_mode,
            create_ai_polygon_mode,
            create_ai_mask_mode,
            brightness_contrast,
            actionAutoDetect,
            actionProjectlines,
            actionProjectlines2txt,
            actionMergeLines,
        )
        on_shapes_present = (save_as, hide_all, show_all, toggle_all)
        context_menu = (
            *[draw_action for _, draw_action in draw],
            actionAutoDetect,
            actionProjectlines,
            actionProjectlines2txt,
            actionMergeLines,
            edit_mode,
            edit,
            duplicate,
            copy,
            paste,
            delete,
            undo,
            undo_last_point,
            remove_point,
        )
        edit_menu = (
            edit,
            duplicate,
            copy,
            paste,
            delete,
            None,
            undo,
            undo_last_point,
            None,
            remove_point,
            None,
            toggle_keep_prev_mode,
        )
    
        
        return _Actions(
            about=about,
            save=save,
            save_as=save_as,
            save_auto=save_auto,
            save_with_image_data=save_with_image_data,
            change_output_dir=change_output_dir,
            open=open_,
            close=close,
            delete_file=delete_file,
            toggle_keep_prev_mode=toggle_keep_prev_mode,
            toggle_keep_prev_brightness_contrast=toggle_keep_prev_brightness_contrast,
            delete=delete,
            edit=edit,
            duplicate=duplicate,
            copy=copy,
            paste=paste,
            undo_last_point=undo_last_point,
            undo=undo,
            remove_point=remove_point,
            create_mode=create_mode,
            edit_mode=edit_mode,
            create_rectangle_mode=create_rectangle_mode,
            create_circle_mode=create_circle_mode,
            create_line_mode=create_line_mode,
            create_point_mode=create_point_mode,
            create_line_strip_mode=create_line_strip_mode,
            create_ai_polygon_mode=create_ai_polygon_mode,
            create_ai_mask_mode=create_ai_mask_mode,
            open_next_img=open_next_img,
            open_prev_img=open_prev_img,
            keep_prev_scale=keep_prev_scale,
            fit_window=fit_window,
            fit_width=fit_width,
            brightness_contrast=brightness_contrast,
            zoom_in=zoom_in,
            zoom_out=zoom_out,
            zoom_org=zoom_org,
            reset_layout=reset_layout,
            fill_drawing=fill_drawing,
            hide_all=hide_all,
            show_all=show_all,
            toggle_all=toggle_all,
            open_dir=open_dir,
            zoom_widget_action=zoom_widget_action,
            draw=draw,
            zoom=zoom,
            on_load_active=on_load_active,
            on_shapes_present=on_shapes_present,
            context_menu=context_menu,
            edit_menu=edit_menu,
        )
    
        
    def get_next_label(self, prefix="L_"):
        """Trova il numero più alto tra le etichette esistenti e suggerisce il successivo."""
        max_id = -1
        target_canvas = self._canvas_widgets.canvas
        
        # Scansiona tutte le forme già presenti per trovare l'indice massimo
        for shape in target_canvas.shapes:
            if shape.label and shape.label.startswith(prefix):
                try:
                    # Estrae la parte numerica (es. da "L_005" prende "005")
                    num_str = shape.label.replace(prefix, "")
                    num = int(num_str)
                    if num > max_id:
                        max_id = num
                except ValueError:
                    continue
        
        # Restituisce il prossimo ID formattato con tre cifre (es. L_011)
        return f"{prefix}{max_id + 1:03d}"



        
    def auto_detect_lines(self):
        """Estrae i segmenti LSD, esegue lo Snap dei vertici contigui e li inietta nel Canvas."""
        
        print("DEBUG: Avvio auto-detect con Snap...") 

        # 1. Ricerca del file path (Invariato)
        file_path = None
        possibili_variabili = ['imagePath', 'image_path', '_image_path', 'filename', '_filename', 'filePath', '_image_file']
        for var_name in possibili_variabili:
            val = getattr(self, var_name, None)
            if isinstance(val, str) and os.path.exists(val):
                file_path = val
                break

        if not file_path:
            self.statusBar().showMessage("Errore: Percorso file non trovato.")
            return

        # 2. Lettura e conversione (Invariato)
        img_arr = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img_arr is None: return
        gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
        
        # 3. Rilevamento LSD
        lsd = cv2.createLineSegmentDetector(0)
        lines = lsd.detect(gray)[0]
        if lines is None: return
            
        # 4. Filtraggio e preparazione lista coordinate
        min_length = 30.0 
        raw_coords = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = math.hypot(x2 - x1, y2 - y1)
            if length >= min_length:
                raw_coords.append([x1, y1, x2, y2])
        
        # --- [INIZIO LOGICA SNAP] ---
        # Uniamo gli estremi che sono molto vicini (Epsilon pixel)
        
        snap_epsilon = 5.0 
        for i in range(len(raw_coords)):
            for j in range(i + 1, len(raw_coords)):
                # Indici degli estremi: P1=(0,1), P2=(2,3)
                for idx_i in [(0,1), (2,3)]:
                    for idx_j in [(0,1), (2,3)]:
                        dist = math.hypot(raw_coords[i][idx_i[0]] - raw_coords[j][idx_j[0]], 
                                          raw_coords[i][idx_i[1]] - raw_coords[j][idx_j[1]])
                        if dist < snap_epsilon:
                            # Il punto del segmento j "salta" esattamente sulle coordinate del segmento i
                            raw_coords[j][idx_j[0]] = raw_coords[i][idx_i[0]]
                            raw_coords[j][idx_j[1]] = raw_coords[i][idx_i[1]]
                        
        
        target_canvas = self._canvas_widgets.canvas
        
        # Limite per performance GUI
        raw_coords = raw_coords[:800]

        for idx, coords in enumerate(raw_coords):
            x1_raw, y1_raw, x2_raw, y2_raw = coords
            # --- CHIAMATA ALLO SNAP ---
            # Applichiamo la "calamita" sia al punto d'inizio che a quello di fine
            x1, y1 = self._apply_snap(x1_raw, y1_raw)
            x2, y2 = self._apply_snap(x2_raw, y2_raw)
            # --------------------------
            
            # 2. GENERAZIONE ETICHETTA UNICA (Richiamo funzione)
            # Questo garantisce che non ci siano conflitti nel file TXT/JSON
            unique_label = self.get_next_label(prefix="L_")
                
            shape = Shape(label=unique_label, shape_type="polygon")
            shape.addPoint(QtCore.QPointF(x1, y1))
            shape.addPoint(QtCore.QPointF(x2, y2))

            shape.group_id = None
            shape.description = ""
            shape.flags = {}
            shape.close() 

            target_canvas.shapes.append(shape)
            
            if hasattr(self, 'addLabel'):
                self.addLabel(shape)
            elif hasattr(self, 'labelList'):
                self.labelList.addShape(shape)
        
        # 6. Sincronizzazione Selezione (Punto 2 della tua richiesta)
        # Colleghiamo il segnale del canvas per evidenziare la riga corrispondente
        try:
            target_canvas.selectionChanged.connect(self.sync_selection_to_list)
        except:
            pass # Evita errori se già connesso

        if hasattr(target_canvas, 'storeShapes'):
            target_canvas.storeShapes()       
            
        target_canvas.update()
        self.setDirty() 
        self.statusBar().showMessage(f"Rilevati {len(raw_coords)} segmenti con Snap attivo.")
        # FIX SELEZIONE: Riporta la modalità in Edit così puoi cliccare sulle linee create
        self._switch_canvas_mode(edit=True)
            
    def sync_selection_to_list(self):
        """Sincronizza click su linea e lista laterale senza crash."""
        try:
            canvas = self._canvas_widgets.canvas
            # Accesso diretto alla lista etichette
            label_list_widget = self._docks.label_list
            
            if not canvas.selectedShapes or label_list_widget is None:
                return

            shape = canvas.selectedShapes[-1]
            # Accediamo alla view interna della lista etichette
            label_list_widget.clearSelection()
        
            # FIX: Iterazione diretta, LabelListWidget non supporta .count() in questa versione
            for item in label_list_widget:
                # LabelMe memorizza la shape nel metodo shape() dell'item
                if item.shape() == shape:
                    item.setSelected(True)
                    label_list_widget.scrollToItem(item)
                    break
        except Exception as e:
            # Chiudendo il blocco try con except, il SyntaxError sparisce
            print(f"Errore sincronizzazione: {e}")

    def _apply_snap(self, x, y, epsilon=10.0):
        """Cerca un vertice vicino nel raggio epsilon e ne restituisce le coordinate precise."""
        target_canvas = self._canvas_widgets.canvas
        for shape in target_canvas.shapes:
            for p in shape.points:
                dist = math.hypot(x - p.x(), y - p.y())
                if dist < epsilon:
                    return p.x(), p.y()
        return x, y
            
    def project_lines_preview(self):
        """Proietta ESCLUSIVAMENTE i segmenti adiacenti (P_i -> P_i+1) ai bordi."""
        target_canvas = self._canvas_widgets.canvas
        if not target_canvas.pixmap:
            return
            
        img_w = target_canvas.pixmap.width()
        img_h = target_canvas.pixmap.height()
        
        # Usiamo una lista temporanea per non modificare la lista mentre la cicliamo
        original_shapes = list(target_canvas.shapes)
        new_projected_shapes = []

        for shape in original_shapes:
            if len(shape.points) < 2:
                continue
            
            # Iteriamo SOLO sulle coppie di punti adiacenti originali
            for i in range(len(shape.points) - 1):
                p1 = shape.points[i]
                p2 = shape.points[i+1]
                
                x1, y1 = p1.x(), p1.y()
                x2, y2 = p2.x(), p2.y()

                dx, dy = x2 - x1, y2 - y1
                if abs(dx) < 1e-6 and abs(dy) < 1e-6: 
                    continue

                # Calcolo geometrico della retta passante per i due punti consecutivi
                t_candidates = []
                if abs(dx) > 1e-10:
                    t_candidates.extend([-x1 / dx, (img_w - x1) / dx])
                if abs(dy) > 1e-10:
                    t_candidates.extend([-y1 / dy, (img_h - y1) / dy])

                valid_pts = []
                for t in t_candidates:
                    ix, iy = x1 + t * dx, y1 + t * dy
                    # Verifichiamo l'intersezione effettiva con il perimetro dell'immagine
                    if -0.5 <= ix <= img_w + 0.5 and -0.5 <= iy <= img_h + 0.5:
                        valid_pts.append((ix, iy))
                
                if len(valid_pts) >= 2:
                    # Troviamo i due punti di uscita dai bordi per quel segmento specifico
                    valid_pts.sort(key=lambda p: (p[0], p[1]))
                    ps, pe = valid_pts[0], valid_pts[-1]
                    
                    # Creiamo la proiezione come entità separata
                    new_shape = Shape(label=shape.label, shape_type="line")
                    new_shape.addPoint(QtCore.QPointF(ps[0], ps[1]))
                    new_shape.addPoint(QtCore.QPointF(pe[0], pe[1]))
                    
                    # Manteniamo i metadati per la ricerca
                    new_shape.group_id = shape.group_id
                    new_shape.close()
                    new_projected_shapes.append(new_shape)

        # SOSTITUZIONE: Sincronizziamo canvas E lista UI per evitare crash su cancellazione
        target_canvas.shapes = []
        if hasattr(self._docks, 'label_list'):
            self._docks.label_list.clear()
            
        for s in new_projected_shapes:
            target_canvas.shapes.append(s)
            self.addLabel(s)
            
        target_canvas.update()
        self.setDirty() 
        self.statusBar().showMessage(f"Proiettati {len(new_projected_shapes)} segmenti adiacenti.")
        # FIX SELEZIONE: Riporta la modalità in Edit così puoi cliccare sulle linee create
        self._switch_canvas_mode(edit=True)

    def export_segments_to_txt(self):
        """Salva JSON e TXT (x1, x2, y1, y2, H, W) in un colpo solo."""
        import os
        # Recupero dinamico del percorso file
        img_path = getattr(self, 'imagePath', None) or getattr(self, '_image_path', None)
        if not img_path:
            # Ultima spiaggia: recupero dal caricatore di file
            img_path = self.filename if hasattr(self, 'filename') else None

        if not img_path or not os.path.exists(img_path):
            self.statusBar().showMessage("Errore: Percorso immagine non trovato.")
            return

        # 1. SALVATAGGIO JSON (Metodo robusto)
        json_path = os.path.splitext(img_path)[0] + ".json"
        try:
            # Usiamo il metodo di salvataggio diretto delle labels
            self.saveLabels(json_path)
        except Exception as e:
            print(f"Errore salvataggio JSON: {e}")

        # 2. GENERAZIONE TXT
        canvas = self._canvas_widgets.canvas
        img_w, img_h = canvas.pixmap.width(), canvas.pixmap.height()
        
        lines_output = []
        for shape in canvas.shapes:
            # Scomponiamo ogni polilinea in segmenti reali
            for i in range(len(shape.points) - 1):
                p1, p2 = shape.points[i], shape.points[i+1]
                # Formato richiesto: x1, x2, y1, y2, H, W
                lines_output.append(f"{p1.x():.2f}, {p2.x():.2f}, {p1.y():.2f}, {p2.y():.2f}, {img_h}, {img_w}")

        txt_path = os.path.splitext(img_path)[0] + ".txt"
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines_output))
        
        self.setDirty()
        self.statusBar().showMessage(f"Dataset salvato: {len(lines_output)} segmenti.")      
    
    def merge_parallel_lines(self):
        """Fonde segmenti paralleli e vicini (ottimizzato per la tua MainWindow)."""
        import numpy as np
        canvas = self._canvas_widgets.canvas
        if not canvas.shapes: 
            return

        DIST_EPSILON = 15.0
        ANGLE_EPSILON = 2.0

        shapes = list(canvas.shapes)
        merged_list = []
        used = [False] * len(shapes)

        for i in range(len(shapes)):
            if used[i] or len(shapes[i].points) < 2: 
                continue
            
            group = [shapes[i]]
            used[i] = True
            
            p1, p2 = shapes[i].points[0], shapes[i].points[1]
            vec_i = np.array([p2.x() - p1.x(), p2.y() - p1.y()])
            angle_i = np.arctan2(vec_i[1], vec_i[0]) % np.pi

            for j in range(i + 1, len(shapes)):
                if used[j] or len(shapes[j].points) < 2: 
                    continue
                
                p3, p4 = shapes[j].points[0], shapes[j].points[1]
                vec_j = np.array([p4.x() - p3.x(), p4.y() - p3.y()])
                angle_j = np.arctan2(vec_j[1], vec_j[0]) % np.pi

                diff_angle = abs(angle_i - angle_j)
                diff_angle = min(diff_angle, np.pi - diff_angle)

                if diff_angle < np.radians(ANGLE_EPSILON):
                    mid_j = np.array([(p3.x() + p4.x())/2, (p3.y() + p4.y())/2])
                    dist = self._dist_point_to_line(mid_j, p1, p2)
                    
                    if dist < DIST_EPSILON:
                        group.append(shapes[j])
                        used[j] = True

            if len(group) > 1:
                new_shape = self._create_average_line(group)
                merged_list.append(new_shape)
            else:
                merged_list.append(shapes[i])

        # --- SINCRONIZZAZIONE BLINDATA PER LA TUA STRUTTURA ---
        
        # 1. Pulizia corretta usando self._docks
        canvas.shapes = []
        canvas.selectedShapes = []
        # Accediamo alla lista reale dentro il dock
        if hasattr(self._docks, 'label_list'):
            self._docks.label_list.clear()

        # 2. Re-inserimento Ufficiale
        for s in merged_list:
            if s.label == "Linea_Merged" or not s.label:
                # Usa il tuo metodo per ottenere il prossimo ID (es. L_001)
                s.label = self.get_next_label(prefix="L_")
            
            # addLabel() collegherà correttamente la shape al widget nel dock
            self.addLabel(s) 
            canvas.shapes.append(s)

        # 3. Ripristino Interfaccia
        # FIX SELEZIONE: Riporta la modalità in Edit così puoi cliccare sulle linee create
        self._switch_canvas_mode(edit=True)
        canvas.setEditing(True)
        canvas.update()
        
        self.setDirty() # Usa il metodo standard di LabelMe
        self.statusBar().showMessage(f"Merge completato: {len(canvas.shapes)} linee.")    
        
    def _dist_point_to_line(self, p, l1, l2):
        """Calcola la distanza minima tra un punto P e la retta passante per l1-l2."""
        import numpy as np
        p1 = np.array([l1.x(), l1.y()])
        p2 = np.array([l2.x(), l2.y()])
        return np.abs(np.cross(p2-p1, p1-p)) / np.linalg.norm(p2-p1)

    def _create_average_line(self, group):
        """Genera una retta media basata sui punti del gruppo."""

        all_pts = []
        for s in group:
            for p in s.points:
                all_pts.append([p.x(), p.y()])
        all_pts = np.array(all_pts)

        # Usiamo la PCA (SVD) per trovare la direzione principale della nuvola di punti
        centroid = np.mean(all_pts, axis=0)
        _, _, vh = np.linalg.svd(all_pts - centroid)
        direction = vh[0] # Vettore direzione principale

        # Proiettiamo i punti sulla direzione per trovare gli estremi
        projections = (all_pts - centroid) @ direction
        p_min = centroid + np.min(projections) * direction
        p_max = centroid + np.max(projections) * direction

        # --- APPLICAZIONE SNAP SUI NUOVI ESTREMI ---
        # Questo assicura che se la retta media finisce vicino a un vertice 
        # di una linea NON mergiata, vi si agganci.
        x1, y1 = self._apply_snap(p_min[0], p_min[1])
        x2, y2 = self._apply_snap(p_max[0], p_max[1])

        new_s = Shape(label="Linea_Merged", shape_type="polygon")
        new_s.addPoint(QtCore.QPointF(x1, y1))
        new_s.addPoint(QtCore.QPointF(x2, y2))
        new_s.close()
        return new_s
 
    
    def _setup_menus(self) -> _Menus:
        action = functools.partial(utils.newAction, self)
        shortcuts = self._config["shortcuts"]

        quit_ = action(
            text=self.tr("&Quit"),
            slot=self.close,
            shortcut=shortcuts["quit"],
            icon=None,
            tip=self.tr("Quit application"),
        )
        open_config = action(
            text=self.tr("Preferences…"),
            slot=self._open_config_file,
            shortcut="Ctrl+," if platform.system() == "Darwin" else "Ctrl+Shift+,",
            icon=None,
            tip=self.tr("Open config file in text editor"),
        )
        open_config.setMenuRole(QtWidgets.QAction.PreferencesRole)
        help_ = action(
            self.tr("&Tutorial"),
            self.tutorial,
            icon="question.svg",
            tip=self.tr("Show tutorial page"),
        )

        file_menu = self.menu(self.tr("&File"))
        edit_menu = self.menu(self.tr("&Edit"))
        view_menu = self.menu(self.tr("&View"))
        help_menu = self.menu(self.tr("&Help"))
        recent_files = QtWidgets.QMenu(self.tr("Open &Recent"))

        label_menu = QtWidgets.QMenu()
        utils.addActions(label_menu, (self._actions.edit, self._actions.delete))
        self._docks.label_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self._docks.label_list.customContextMenuRequested.connect(self.popLabelListMenu)

        utils.addActions(
            file_menu,
            (
                self._actions.open,
                self._actions.open_next_img,
                self._actions.open_prev_img,
                self._actions.open_dir,
                recent_files,
                self._actions.save,
                self._actions.save_as,
                self._actions.save_auto,
                self._actions.change_output_dir,
                self._actions.save_with_image_data,
                self._actions.close,
                self._actions.delete_file,
                None,
                open_config,
                None,
                quit_,
            ),
        )
        utils.addActions(help_menu, (help_, self._actions.about))
        utils.addActions(
            view_menu,
            (
                self._docks.flag_dock.toggleViewAction(),
                self._docks.label_dock.toggleViewAction(),
                self._docks.shape_dock.toggleViewAction(),
                self._docks.file_dock.toggleViewAction(),
                None,
                self._actions.reset_layout,
                None,
                self._actions.fill_drawing,
                None,
                self._actions.hide_all,
                self._actions.show_all,
                self._actions.toggle_all,
                None,
                self._actions.zoom_in,
                self._actions.zoom_out,
                self._actions.zoom_org,
                self._actions.keep_prev_scale,
                None,
                self._actions.fit_window,
                self._actions.fit_width,
                None,
                self._actions.brightness_contrast,
                self._actions.toggle_keep_prev_brightness_contrast,
            ),
        )

        file_menu.aboutToShow.connect(self.updateFileMenu)

        utils.addActions(
            self._canvas_widgets.canvas.menus[0], self._actions.context_menu
        )
        utils.addActions(
            self._canvas_widgets.canvas.menus[1],
            (
                action("&Copy here", self.copyShape),
                action("&Move here", self.moveShape),
            ),
        )

        return _Menus(
            file=file_menu,
            edit=edit_menu,
            view=view_menu,
            help=help_menu,
            recent_files=recent_files,
            label_list=label_menu,
        )

    def _setup_toolbars(self) -> None:
        select_ai_model = QtWidgets.QWidgetAction(self)
        select_ai_model.setDefaultWidget(self._ai_annotation)

        ai_prompt_action = QtWidgets.QWidgetAction(self)
        ai_prompt_action.setDefaultWidget(self._ai_text)

        self.addToolBar(
            Qt.TopToolBarArea,
            ToolBar(
                title="Tools",
                actions=[
                    self._actions.open,
                    self._actions.open_dir,
                    self._actions.open_prev_img,
                    self._actions.open_next_img,
                    self._actions.save,
                    self._actions.delete_file,
                    None,
                    self._actions.edit_mode,
                    self._actions.duplicate,
                    self._actions.delete,
                    self._actions.undo,
                    self._actions.brightness_contrast,
                    None,
                    self._actions.fit_window,
                    self._actions.zoom_widget_action,
                    None,
                    select_ai_model,
                    None,
                    ai_prompt_action,
                ],
                font_base=self.font(),
            ),
        )
        self.addToolBar(
            Qt.LeftToolBarArea,
            ToolBar(
                title="CreateShapeTools",
                actions=[a for _, a in self._actions.draw],
                orientation=Qt.Vertical,
                button_style=Qt.ToolButtonTextUnderIcon,
                font_base=self.font(),
            ),
        )

    def _setup_app_state(
        self,
        *,
        output_dir: str | None,
        filename: str | None,
    ) -> None:
        self._output_dir = output_dir

        self._image = QtGui.QImage()
        self._label_file = None
        self._image_path = None
        self._max_recent = 7
        self._other_data = None
        self._zoom_values = {}
        self._brightness_contrast_values = {}
        self._scroll_values = {
            Qt.Horizontal: {},
            Qt.Vertical: {},
        }

        if self._config["file_search"]:
            self._docks.file_search.setText(self._config["file_search"])

        self._default_state = self.saveState()
        #
        # XXX: Could be completely declarative.
        # Restore application settings.
        self.settings = QtCore.QSettings("labelme", "labelme")
        #
        # Bump this when dock/toolbar layout changes to reset window state
        # for users upgrading from an older version.
        SETTINGS_VERSION: int = 1
        if self.settings.value("settingsVersion", 0, type=int) != SETTINGS_VERSION:
            self._reset_layout()
            self.settings.setValue("settingsVersion", SETTINGS_VERSION)
        #
        self._recent_files = self.settings.value("recentFiles", []) or []
        self.resize(self.settings.value("window/size", QtCore.QSize(900, 500)))
        self.move(self.settings.value("window/position", QtCore.QPoint(0, 0)))
        self.restoreState(self.settings.value("window/state", QtCore.QByteArray()))
        # Recover window position when the saved screen is no longer connected.
        if not any(
            s.availableGeometry().intersects(self.frameGeometry())
            for s in QtWidgets.QApplication.screens()
        ) and (primary_screen := QtWidgets.QApplication.primaryScreen()):
            self.move(primary_screen.availableGeometry().topLeft())

        if filename:
            if osp.isdir(filename):
                self._import_images_from_dir(
                    root_dir=filename, pattern=self._docks.file_search.text()
                )
                self._open_next_image()
            else:
                self._load_file(filename=filename)
        else:
            self._filename = None

    def _setup_status_bar(self) -> _StatusBarWidgets:
        message = QtWidgets.QLabel(self.tr("%s started.") % __appname__)
        stats = StatusStats()
        self.statusBar().addWidget(message, 1)
        self.statusBar().addWidget(stats, 0)
        self.statusBar().show()
        return _StatusBarWidgets(message=message, stats=stats)

    def _setup_canvas(self) -> _CanvasWidgets:
        zoom_widget = ZoomWidget()

        canvas = Canvas(
            epsilon=self._config["epsilon"],
            double_click=self._config["canvas"]["double_click"],
            num_backups=self._config["canvas"]["num_backups"],
            crosshair=self._config["canvas"]["crosshair"],
        )
        canvas.zoomRequest.connect(self._zoom_requested)
        canvas.mouseMoved.connect(self._update_status_stats)
        canvas.statusUpdated.connect(
            lambda text: self._status_bar.message.setText(text)
        )

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(canvas)
        scroll_area.setWidgetResizable(True)
        scroll_bars = {
            Qt.Vertical: scroll_area.verticalScrollBar(),
            Qt.Horizontal: scroll_area.horizontalScrollBar(),
        }
        canvas.scrollRequest.connect(self.scrollRequest)

        canvas.newShape.connect(self.newShape)
        canvas.shapeMoved.connect(self.setDirty)
        canvas.selectionChanged.connect(self.shapeSelectionChanged)
        canvas.drawingPolygon.connect(self.toggleDrawingSensitive)

        self.setCentralWidget(scroll_area)

        return _CanvasWidgets(
            canvas=canvas,
            zoom_widget=zoom_widget,
            scroll_bars=scroll_bars,
        )

    def _setup_dock_widgets(self) -> _DockWidgets:
        flag_list = QtWidgets.QListWidget()
        flag = QtWidgets.QDockWidget(self.tr("Flags"), self)
        flag.setObjectName("Flags")
        if self._config["flags"]:
            self._load_flags(
                flags={k: False for k in self._config["flags"]},
                widget=flag_list,
            )
        flag.setWidget(flag_list)
        flag_list.itemChanged.connect(self.setDirty)

        label_list = LabelListWidget()
        label_list.itemSelectionChanged.connect(self._label_selection_changed)
        label_list.itemDoubleClicked.connect(self._edit_label)
        label_list.itemChanged.connect(self.labelItemChanged)
        label_list.itemDropped.connect(self.labelOrderChanged)
        shape = QtWidgets.QDockWidget(self.tr("Annotation List"), self)
        shape.setObjectName("Labels")
        shape.setWidget(label_list)

        unique_label_list = UniqueLabelQListWidget()
        unique_label_list.setToolTip(
            self.tr("Select label to start annotating for it. Press 'Esc' to deselect.")
        )
        if self._config["labels"]:
            for lbl in self._config["labels"]:
                unique_label_list.add_label_item(
                    label=lbl,
                    color=self._get_rgb_by_label(
                        label=lbl, unique_label_list=unique_label_list
                    ),
                )
        label = QtWidgets.QDockWidget(self.tr("Label List"), self)
        label.setObjectName("Label List")
        label.setWidget(unique_label_list)

        file_search = QtWidgets.QLineEdit()
        file_search.setPlaceholderText(self.tr("Search Filename"))
        file_search.textChanged.connect(self.fileSearchChanged)
        file_list = QtWidgets.QListWidget()
        file_list.itemSelectionChanged.connect(self.fileSelectionChanged)
        file_list_layout = QtWidgets.QVBoxLayout()
        file_list_layout.setContentsMargins(0, 0, 0, 0)
        file_list_layout.setSpacing(0)
        file_list_layout.addWidget(file_search)
        file_list_layout.addWidget(file_list)
        file = QtWidgets.QDockWidget(self.tr("File List"), self)
        file.setObjectName("Files")
        file_list_container = QtWidgets.QWidget()
        file_list_container.setLayout(file_list_layout)
        file.setWidget(file_list_container)

        for config_key, dock_widget in [
            ("flag_dock", flag),
            ("label_dock", label),
            ("shape_dock", shape),
            ("file_dock", file),
        ]:
            features = QtWidgets.QDockWidget.DockWidgetFeatures()
            if self._config[config_key]["closable"]:
                features = features | QtWidgets.QDockWidget.DockWidgetClosable
            if self._config[config_key]["floatable"]:
                features = features | QtWidgets.QDockWidget.DockWidgetFloatable
            if self._config[config_key]["movable"]:
                features = features | QtWidgets.QDockWidget.DockWidgetMovable
            dock_widget.setFeatures(features)
            if self._config[config_key]["show"] is False:
                dock_widget.setVisible(False)
            self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)

        return _DockWidgets(
            flag_dock=flag,
            flag_list=flag_list,
            shape_dock=shape,
            label_list=label_list,
            label_dock=label,
            unique_label_list=unique_label_list,
            file_dock=file,
            file_search=file_search,
            file_list=file_list,
        )

    def _load_config(
        self, config_file: Path | None, config_overrides: dict | None
    ) -> tuple[Path | None, dict]:
        try:
            config = load_config(
                config_file=config_file, config_overrides=config_overrides or {}
            )
        except ValueError as e:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle(self.tr("Configuration Errors"))
            msg_box.setText(
                self.tr(
                    "Errors were found while loading the configuration. "
                    "Please review the errors below and reload your configuration or "
                    "ignore the erroneous lines."
                )
            )
            msg_box.setInformativeText(str(e))
            msg_box.setStandardButtons(QMessageBox.Ignore)
            msg_box.setModal(False)
            msg_box.show()

            config_file = None
            config_overrides = {}
            config = load_config(
                config_file=config_file, config_overrides=config_overrides
            )
        return config_file, config

    def menu(self, title, actions=None):
        menu = self.menuBar().addMenu(title)
        if actions:
            utils.addActions(menu, actions)
        return menu

    # Support Functions

    def noShapes(self) -> bool:
        return not len(self._docks.label_list)

    def populateModeActions(self) -> None:
        self._canvas_widgets.canvas.menus[0].clear()
        utils.addActions(
            self._canvas_widgets.canvas.menus[0], self._actions.context_menu
        )
        self._menus.edit.clear()
        actions = (
            *[draw_action for _, draw_action in self._actions.draw],
            self._actions.edit_mode,
            *self._actions.edit_menu,
        )
        utils.addActions(self._menus.edit, actions)

    def _get_window_title(self, dirty: bool) -> str:
        window_title: str = __appname__
        if self._image_path:
            window_title = f"{window_title} - {self._image_path}"
            if self._docks.file_list.count() and self._docks.file_list.currentItem():
                window_title = (
                    f"{window_title} "
                    f"[{self._docks.file_list.currentRow() + 1}"
                    f"/{self._docks.file_list.count()}]"
                )
        if dirty:
            window_title = f"{window_title}*"
        return window_title

    def setDirty(self) -> None:
        # Even if we autosave the file, we keep the ability to undo
        self._actions.undo.setEnabled(self._canvas_widgets.canvas.isShapeRestorable)

        if self._config["auto_save"] or self._actions.save_auto.isChecked():
            assert self._image_path
            label_file = f"{osp.splitext(self._image_path)[0]}.json"
            if self._output_dir:
                label_file_without_path = osp.basename(label_file)
                label_file = osp.join(self._output_dir, label_file_without_path)
            self.saveLabels(label_file)
            return
        self._is_changed = True
        self._actions.save.setEnabled(True)
        self.setWindowTitle(self._get_window_title(dirty=True))

    def setClean(self) -> None:
        self._is_changed = False
        self._actions.save.setEnabled(False)
        for _, action in self._actions.draw:
            action.setEnabled(True)
        self.setWindowTitle(self._get_window_title(dirty=False))

        if self.hasLabelFile():
            self._actions.delete_file.setEnabled(True)
        else:
            self._actions.delete_file.setEnabled(False)

    def toggleActions(self, value: bool = True) -> None:
        """Enable/Disable widgets which depend on an opened image."""
        for z in self._actions.zoom:
            z.setEnabled(value)
        for action in self._actions.on_load_active:
            action.setEnabled(value)

    def queueEvent(self, function: Callable[[], None]) -> None:
        QtCore.QTimer.singleShot(0, function)

    def show_status_message(self, message: str, delay: int = 500) -> None:
        self.statusBar().showMessage(message, delay)

    def _submit_ai_prompt(self, _) -> None:
        if (
            self._canvas_widgets.canvas.createMode
            not in _AI_TEXT_TO_ANNOTATION_CREATE_MODE_TO_SHAPE_TYPE
        ):
            logger.warning(
                "Unsupported createMode={!r}", self._canvas_widgets.canvas.createMode
            )
            return
        shape_type: Literal["rectangle", "polygon", "mask"] = (
            _AI_TEXT_TO_ANNOTATION_CREATE_MODE_TO_SHAPE_TYPE[
                self._canvas_widgets.canvas.createMode
            ]
        )

        texts = self._ai_text.get_text_prompt().split(",")

        model_name: str = self._ai_text.get_model_name()
        model_type = osam.apis.get_model_type_by_name(model_name)
        if not (_is_already_downloaded := model_type.get_size() is not None):
            if not download_ai_model(model_name=model_name, parent=self):
                return
        if (
            self._text_osam_session is None
            or self._text_osam_session.model_name != model_name
        ):
            self._text_osam_session = OsamSession(model_name=model_name)

        boxes, scores, labels, masks = bbox_from_text.get_bboxes_from_texts(
            session=self._text_osam_session,
            image=utils.img_qt_to_arr(self._image)[:, :, :3],
            image_id=str(hash(self._image_path)),
            texts=texts,
        )

        SCORE_FOR_EXISTING_SHAPE: float = 1.01
        for shape in self._canvas_widgets.canvas.shapes:
            if shape.shape_type != shape_type or shape.label not in texts:
                continue
            points: NDArray[np.float64] = np.array(
                [[p.x(), p.y()] for p in shape.points]
            )
            xmin, ymin = points.min(axis=0)
            xmax, ymax = points.max(axis=0)
            box = np.array([xmin, ymin, xmax, ymax], dtype=np.float32)
            boxes = np.r_[boxes, [box]]
            scores = np.r_[scores, [SCORE_FOR_EXISTING_SHAPE]]
            labels = np.r_[labels, [texts.index(shape.label)]]

        boxes, scores, labels, indices = bbox_from_text.nms_bboxes(
            boxes=boxes,
            scores=scores,
            labels=labels,
            iou_threshold=self._ai_text.get_iou_threshold(),
            score_threshold=self._ai_text.get_score_threshold(),
            max_num_detections=100,
        )

        is_new = scores != SCORE_FOR_EXISTING_SHAPE
        boxes = boxes[is_new]
        scores = scores[is_new]
        labels = labels[is_new]
        indices = indices[is_new]

        if masks is not None:
            masks = masks[indices]
        del indices

        shapes: list[Shape] = bbox_from_text.get_shapes_from_bboxes(
            boxes=boxes,
            scores=scores,
            labels=labels,
            texts=texts,
            masks=masks,
            shape_type=shape_type,
        )

        self._canvas_widgets.canvas.storeShapes()
        self._load_shapes(shapes, replace=False)
        self.setDirty()

    def resetState(self) -> None:
        self._docks.label_list.clear()
        self._filename = None
        self._image_path = None
        self.imageData = None
        self._label_file = None
        self._other_data = None
        self._canvas_widgets.canvas.resetState()

    def currentItem(self) -> LabelListWidgetItem | None:
        items = self._docks.label_list.selectedItems()
        if items:
            return items[0]
        return None

    def addRecentFile(self, filename: str) -> None:
        if filename in self._recent_files:
            self._recent_files.remove(filename)
        elif len(self._recent_files) >= self._max_recent:
            self._recent_files.pop()
        self._recent_files.insert(0, filename)

    # Callbacks

    def undoShapeEdit(self) -> None:
        self._canvas_widgets.canvas.restoreShape()
        self._docks.label_list.clear()
        self._load_shapes(self._canvas_widgets.canvas.shapes)
        self._actions.undo.setEnabled(self._canvas_widgets.canvas.isShapeRestorable)

    def tutorial(self):
        url = "https://github.com/labelmeai/labelme/tree/main/examples/tutorial"  # NOQA
        webbrowser.open(url)

    def toggleDrawingSensitive(self, drawing=True):
        """Toggle drawing sensitive.

        In the middle of drawing, toggling between modes should be disabled.
        """
        self._actions.edit_mode.setEnabled(not drawing)
        self._actions.undo_last_point.setEnabled(drawing)
        self._actions.undo.setEnabled(not drawing)
        self._actions.delete.setEnabled(not drawing)

    def _switch_canvas_mode(
        self, edit: bool = True, createMode: str | None = None
    ) -> None:
        self._canvas_widgets.canvas.setEditing(edit)
        if createMode is not None:
            self._canvas_widgets.canvas.createMode = createMode
        if edit:
            for _, draw_action in self._actions.draw:
                draw_action.setEnabled(True)
        else:
            for draw_mode, draw_action in self._actions.draw:
                draw_action.setEnabled(createMode != draw_mode)
        self._actions.edit_mode.setEnabled(not edit)
        self._ai_text.setEnabled(
            not edit and createMode in _AI_TEXT_TO_ANNOTATION_CREATE_MODE_TO_SHAPE_TYPE
        )
        self._ai_annotation.setEnabled(
            not edit and createMode in ("ai_polygon", "ai_mask")
        )

    def updateFileMenu(self):
        current = self._filename

        def exists(filename):
            return osp.exists(str(filename))

        menu = self._menus.recent_files
        menu.clear()
        files = [f for f in self._recent_files if f != current and exists(f)]
        for i, f in enumerate(files):
            icon = utils.newIcon("labels")
            action = QtWidgets.QAction(
                icon, f"&{i + 1} {QtCore.QFileInfo(f).fileName()}", self
            )
            action.triggered.connect(functools.partial(self.loadRecent, f))
            menu.addAction(action)

    def popLabelListMenu(self, point: QtCore.QPoint) -> None:
        self._menus.label_list.exec(self._docks.label_list.mapToGlobal(point))  # type: ignore[invalid-argument-type]

    def validateLabel(self, label):
        # no validation
        if self._config["validate_label"] is None:
            return True

        for i in range(self._docks.unique_label_list.count()):
            label_i = self._docks.unique_label_list.item(i).data(Qt.UserRole)  # type: ignore[attr-defined,union-attr]
            if self._config["validate_label"] in ["exact"]:
                if label_i == label:
                    return True
        return False

    def _edit_label(self, value=None):
        items = self._docks.label_list.selectedItems()
        if not items:
            logger.warning("No label is selected, so cannot edit label.")
            return

        shape = items[0].shape()

        if len(items) == 1:
            edit_text = True
            edit_flags = True
            edit_group_id = True
            edit_description = True
        else:
            edit_text = all(item.shape().label == shape.label for item in items[1:])
            edit_flags = all(item.shape().flags == shape.flags for item in items[1:])
            edit_group_id = all(
                item.shape().group_id == shape.group_id for item in items[1:]
            )
            edit_description = all(
                item.shape().description == shape.description for item in items[1:]
            )

        if not edit_text:
            self._label_dialog.edit.setDisabled(True)
            self._label_dialog.labelList.setDisabled(True)
        if not edit_group_id:
            self._label_dialog.edit_group_id.setDisabled(True)
        if not edit_description:
            self._label_dialog.editDescription.setDisabled(True)

        text, flags, group_id, description = self._label_dialog.popUp(
            text=shape.label if edit_text else "",
            flags=shape.flags if edit_flags else None,
            group_id=shape.group_id if edit_group_id else None,
            description=shape.description if edit_description else None,
            flags_disabled=not edit_flags,
        )

        if not edit_text:
            self._label_dialog.edit.setDisabled(False)
            self._label_dialog.labelList.setDisabled(False)
        if not edit_group_id:
            self._label_dialog.edit_group_id.setDisabled(False)
        if not edit_description:
            self._label_dialog.editDescription.setDisabled(False)

        if text is None:
            assert flags is None
            assert group_id is None
            assert description is None
            return

        if not self.validateLabel(text):
            self.errorMessage(
                self.tr("Invalid label"),
                self.tr("Invalid label '{}' with validation type '{}'").format(
                    text, self._config["validate_label"]
                ),
            )
            return

        self._canvas_widgets.canvas.storeShapes()
        for item in items:
            shape: Shape = item.shape()  # type: ignore[no-redef]

            if edit_text:
                shape.label = text
            if edit_flags:
                shape.flags = flags
            if edit_group_id:
                shape.group_id = group_id
            if edit_description:
                shape.description = description

            self._update_shape_color(shape)
            if shape.group_id is None:
                r, g, b = shape.fill_color.getRgb()[:3]
                item.setText(
                    f"{html.escape(shape.label)} "
                    f'<font color="#{r:02x}{g:02x}{b:02x}">●</font>'
                )
            else:
                item.setText(f"{shape.label} ({shape.group_id})")
            self.setDirty()
            if self._docks.unique_label_list.find_label_item(shape.label) is None:
                self._docks.unique_label_list.add_label_item(
                    label=shape.label,
                    color=self._get_rgb_by_label(
                        label=shape.label,
                        unique_label_list=self._docks.unique_label_list,
                    ),
                )

    def fileSearchChanged(self):
        self._import_images_from_dir(
            root_dir=self._prev_opened_dir, pattern=self._docks.file_search.text()
        )

    def fileSelectionChanged(self) -> None:
        items = self._docks.file_list.selectedItems()
        if not items:
            return
        item = items[0]

        if not self._can_continue():
            return

        curr_index = self.imageList.index(str(item.text()))
        if curr_index < len(self.imageList):
            filename = self.imageList[curr_index]
            if filename:
                self._load_file(filename)

    # React to canvas signals.
    def shapeSelectionChanged(self, selected_shapes: list[Shape]) -> None:
        self._docks.label_list.itemSelectionChanged.disconnect(
            self._label_selection_changed
        )
        for shape in self._canvas_widgets.canvas.selectedShapes:
            shape.selected = False
        self._docks.label_list.clearSelection()
        self._canvas_widgets.canvas.selectedShapes = selected_shapes
        for shape in self._canvas_widgets.canvas.selectedShapes:
            shape.selected = True
            item = self._docks.label_list.findItemByShape(shape)
            self._docks.label_list.selectItem(item)
            self._docks.label_list.scrollToItem(item)
        self._docks.label_list.itemSelectionChanged.connect(
            self._label_selection_changed
        )
        n_selected = len(selected_shapes) > 0
        self._actions.delete.setEnabled(n_selected)
        self._actions.duplicate.setEnabled(n_selected)
        self._actions.copy.setEnabled(n_selected)
        self._actions.edit.setEnabled(n_selected)

    def addLabel(self, shape: Shape) -> None:
        assert shape.label is not None
        if shape.group_id is None:
            text = shape.label
        else:
            text = f"{shape.label} ({shape.group_id})"
        label_list_item = LabelListWidgetItem(text, shape)
        self._docks.label_list.addItem(label_list_item)
        if self._docks.unique_label_list.find_label_item(shape.label) is None:
            self._docks.unique_label_list.add_label_item(
                label=shape.label,
                color=self._get_rgb_by_label(
                    label=shape.label,
                    unique_label_list=self._docks.unique_label_list,
                ),
            )
        self._label_dialog.addLabelHistory(shape.label)
        for action in self._actions.on_shapes_present:
            action.setEnabled(True)

        self._update_shape_color(shape)
        r, g, b = shape.fill_color.getRgb()[:3]
        label_list_item.setText(
            f'{html.escape(text)} <font color="#{r:02x}{g:02x}{b:02x}">●</font>'
        )

    def _update_shape_color(self, shape: Shape) -> None:
        assert shape.label is not None
        r, g, b = self._get_rgb_by_label(
            shape.label, unique_label_list=self._docks.unique_label_list
        )
        shape.line_color = QtGui.QColor(r, g, b)
        shape.vertex_fill_color = QtGui.QColor(r, g, b)
        shape.hvertex_fill_color = QtGui.QColor(255, 255, 255)
        shape.fill_color = QtGui.QColor(r, g, b, 128)
        shape.select_line_color = QtGui.QColor(255, 255, 255)
        shape.select_fill_color = QtGui.QColor(r, g, b, 155)

    def _get_rgb_by_label(
        self,
        label: str,
        unique_label_list: UniqueLabelQListWidget,
    ) -> tuple[int, int, int]:
        if self._config["shape_color"] == "auto":
            item = unique_label_list.find_label_item(label)
            item_index: int = (
                unique_label_list.indexFromItem(item).row()
                if item
                else unique_label_list.count()
            )
            label_id: int = (
                1  # skip black color by default
                + item_index
                + self._config["shift_auto_shape_color"]
            )
            rgb: tuple[int, int, int] = tuple(
                LABEL_COLORMAP[label_id % len(LABEL_COLORMAP)].tolist()
            )
            return rgb
        elif (
            self._config["shape_color"] == "manual"
            and self._config["label_colors"]
            and label in self._config["label_colors"]
        ):
            if not (
                len(self._config["label_colors"][label]) == 3
                and all(0 <= c <= 255 for c in self._config["label_colors"][label])
            ):
                raise ValueError(
                    "Color for label must be 0-255 RGB tuple, but got: "
                    f"{self._config['label_colors'][label]}"
                )
            return tuple(self._config["label_colors"][label])
        elif self._config["default_shape_color"]:
            return self._config["default_shape_color"]
        return (0, 255, 0)

    def remLabels(self, shapes: list[Shape]) -> None:
        for shape in shapes:
            item = self._docks.label_list.findItemByShape(shape)
            self._docks.label_list.removeItem(item)

    def _load_shapes(self, shapes: list[Shape], replace: bool = True) -> None:
        self._docks.label_list.itemSelectionChanged.disconnect(
            self._label_selection_changed
        )
        shape: Shape
        for shape in shapes:
            self.addLabel(shape)
        self._docks.label_list.clearSelection()
        self._docks.label_list.itemSelectionChanged.connect(
            self._label_selection_changed
        )
        self._canvas_widgets.canvas.loadShapes(shapes=shapes, replace=replace)

    def _load_shape_dicts(self, shape_dicts: list[ShapeDict]) -> None:
        shapes: list[Shape] = []
        shape_dict: ShapeDict
        for shape_dict in shape_dicts:
            shape: Shape = Shape(
                label=shape_dict["label"],
                shape_type=shape_dict["shape_type"],
                group_id=shape_dict["group_id"],
                description=shape_dict["description"],
                mask=shape_dict["mask"],
            )
            for x, y in shape_dict["points"]:
                shape.addPoint(QtCore.QPointF(x, y))
            shape.close()

            default_flags = {}
            if self._config["label_flags"]:
                for pattern, keys in self._config["label_flags"].items():
                    if not isinstance(shape.label, str):
                        logger.warning("shape.label is not str: {}", shape.label)
                        continue
                    if re.match(pattern, shape.label):
                        for key in keys:
                            default_flags[key] = False
            shape.flags = default_flags
            shape.flags.update(shape_dict["flags"])
            shape.other_data = shape_dict["other_data"]

            shapes.append(shape)
        self._load_shapes(shapes=shapes)

    def _load_flags(
        self,
        flags: dict[str, bool],
        widget: QtWidgets.QListWidget,
    ) -> None:
        widget.clear()
        key: str
        flag: bool
        for key, flag in flags.items():
            item: QtWidgets.QListWidgetItem = QtWidgets.QListWidgetItem(key)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if flag else Qt.Unchecked)
            widget.addItem(item)

    def saveLabels(self, filename):
        lf = LabelFile()

        def format_shape(s):
            data = s.other_data.copy()
            data.update(
                dict(
                    label=s.label,
                    points=[(p.x(), p.y()) for p in s.points],
                    group_id=s.group_id,
                    description=s.description,
                    shape_type=s.shape_type,
                    flags=s.flags,
                    mask=None
                    if s.mask is None
                    else utils.img_arr_to_b64(s.mask.astype(np.uint8)),
                )
            )
            return data

        shapes = [format_shape(item.shape()) for item in self._docks.label_list]
        flags = {}
        for i in range(self._docks.flag_list.count()):
            item = self._docks.flag_list.item(i)
            assert item
            key = item.text()
            flag = item.checkState() == Qt.Checked
            flags[key] = flag
        try:
            assert self._image_path
            imagePath = osp.relpath(self._image_path, osp.dirname(filename))
            imageData = self.imageData if self._config["with_image_data"] else None
            if osp.dirname(filename) and not osp.exists(osp.dirname(filename)):
                os.makedirs(osp.dirname(filename))
            lf.save(
                filename=filename,
                shapes=shapes,
                imagePath=imagePath,
                imageData=imageData,
                imageHeight=self._image.height(),
                imageWidth=self._image.width(),
                otherData=self._other_data,
                flags=flags,
            )
            self._label_file = lf
            items = self._docks.file_list.findItems(self._image_path, Qt.MatchExactly)
            if len(items) > 0:
                if len(items) != 1:
                    raise RuntimeError("There are duplicate files.")
                items[0].setCheckState(Qt.Checked)
            # disable allows next and previous image to proceed
            # self._filename = filename
            return True
        except LabelFileError as e:
            self.errorMessage(
                self.tr("Error saving label data"), self.tr("<b>%s</b>") % e
            )
            return False

    def duplicateSelectedShape(self) -> None:
        self.copySelectedShape()
        self.pasteSelectedShape()

    def pasteSelectedShape(self) -> None:
        self._load_shapes(shapes=self._copied_shapes, replace=False)
        self._canvas_widgets.canvas.selectShapes(self._copied_shapes)
        self.setDirty()

    def copySelectedShape(self) -> None:
        self._copied_shapes = [
            s.copy() for s in self._canvas_widgets.canvas.selectedShapes
        ]
        self._actions.paste.setEnabled(len(self._copied_shapes) > 0)

    def _label_selection_changed(self) -> None:
        selected_shapes: list[Shape] = []
        for item in self._docks.label_list.selectedItems():
            selected_shapes.append(item.shape())
        if selected_shapes:
            self._canvas_widgets.canvas.selectShapes(selected_shapes)
        else:
            if self._canvas_widgets.canvas.deSelectShape():
                self._canvas_widgets.canvas.update()

    def labelItemChanged(self, item: LabelListWidgetItem) -> None:
        shape = item.shape()
        self._canvas_widgets.canvas.setShapeVisible(
            shape, item.checkState() == Qt.Checked
        )

    def labelOrderChanged(self) -> None:
        self.setDirty()
        self._canvas_widgets.canvas.loadShapes(
            [item.shape() for item in self._docks.label_list]
        )

        
    def newShape(self) -> None:
        """Pop-up con suggerimento automatico dell'etichetta e focus sull'editor."""
        items = self._docks.unique_label_list.selectedItems()
        text = None
        
        # 1. Recupero suggerimento automatico
        # Se non c'è un'etichetta selezionata nella lista 'unique', usiamo il contatore
        if items:
            text = items[0].data(Qt.UserRole)
        else:
            text = self.get_next_label(prefix="L_") # Chiama la funzione di conteggio

        flags = {}
        group_id = None
        description = ""
        
        if self._config["display_label_popup"] or not text:
            # Impostiamo il testo suggerito nel campo di edit prima del popUp
            self._label_dialog.edit.setText(text)
            
            # Mostra il dialogo
            res = self._label_dialog.popUp(text)
            if res is not None:
                text, flags, group_id, description = res
            else:
                text = None # Utente ha premuto Cancel

        if text and not self.validateLabel(text):
            self.errorMessage(
                self.tr("Invalid label"),
                self.tr("Invalid label '{}'").format(text)
            )
            text = ""

        if text:
            self._docks.label_list.clearSelection()
            # Imposta l'etichetta sul canvas
            shape = self._canvas_widgets.canvas.setLastLabel(text, flags)
            shape.group_id = group_id
            shape.description = description
            
            # 2. Registrazione ufficiale (Fondamentale per il salvataggio JSON)
            self.addLabel(shape)
            
            self._actions.edit_mode.setEnabled(True)
            self._actions.undo_last_point.setEnabled(False)
            self._actions.undo.setEnabled(True)
            
            # 3. Stato Dirty (Abilita il tasto Save)
            self.setDirty()
        else:
            self._canvas_widgets.canvas.undoLastLine()
            if self._canvas_widgets.canvas.shapesBackups:
                self._canvas_widgets.canvas.shapesBackups.pop()
    # Callback functions:

    
    def scrollRequest(self, delta: int, orientation: Qt.Orientation) -> None:
        units = -delta * 0.1  # natural scroll
        bar = self._canvas_widgets.scroll_bars[orientation]
        value = bar.value() + bar.singleStep() * units
        self.setScroll(orientation, value)

    def setScroll(self, orientation: Qt.Orientation, value: float) -> None:
        self._canvas_widgets.scroll_bars[orientation].setValue(int(value))
        if self._filename is not None:
            self._scroll_values[orientation][self._filename] = value

    def _set_zoom(self, value: int, pos: QtCore.QPointF | None = None) -> None:
        if self._filename is None:
            logger.warning("filename is None, cannot set zoom")
            return

        if pos is None:
            pos = QtCore.QPointF(
                self._canvas_widgets.canvas.visibleRegion().boundingRect().center()
            )
        canvas_width_old: int = self._canvas_widgets.canvas.width()

        self._actions.fit_width.setChecked(self._zoom_mode == _ZoomMode.FIT_WIDTH)
        self._actions.fit_window.setChecked(self._zoom_mode == _ZoomMode.FIT_WINDOW)
        self._canvas_widgets.canvas.enableDragging(
            enabled=value > int(self._scalers[_ZoomMode.FIT_WINDOW]() * 100)
        )
        self._canvas_widgets.zoom_widget.setValue(value)  # triggers self._paint_canvas
        self._zoom_values[self._filename] = (self._zoom_mode, value)

        canvas_width_new: int = self._canvas_widgets.canvas.width()
        if canvas_width_old == canvas_width_new:
            return
        canvas_scale_factor = canvas_width_new / canvas_width_old
        x_shift: float = pos.x() * canvas_scale_factor - pos.x()
        y_shift: float = pos.y() * canvas_scale_factor - pos.y()
        self.setScroll(
            Qt.Horizontal,
            self._canvas_widgets.scroll_bars[Qt.Horizontal].value() + x_shift,
        )
        self.setScroll(
            Qt.Vertical,
            self._canvas_widgets.scroll_bars[Qt.Vertical].value() + y_shift,
        )

    def _set_zoom_to_original(self):
        self._zoom_mode = _ZoomMode.MANUAL_ZOOM
        self._set_zoom(value=100)

    def _add_zoom(self, increment: float, pos: QtCore.QPointF | None = None) -> None:
        zoom_value: int
        if increment > 1:
            zoom_value = math.ceil(self._canvas_widgets.zoom_widget.value() * increment)
        else:
            zoom_value = math.floor(
                self._canvas_widgets.zoom_widget.value() * increment
            )
        self._zoom_mode = _ZoomMode.MANUAL_ZOOM
        self._set_zoom(value=zoom_value, pos=pos)

    def _zoom_requested(self, delta: int, pos: QtCore.QPointF) -> None:
        self._add_zoom(increment=1.1 if delta > 0 else 0.9, pos=pos)

    def setFitWindow(self, value=True):
        if value:
            self._actions.fit_width.setChecked(False)
        self._zoom_mode = _ZoomMode.FIT_WINDOW if value else _ZoomMode.MANUAL_ZOOM
        self._adjust_scale()

    def setFitWidth(self, value=True):
        if value:
            self._actions.fit_window.setChecked(False)
        self._zoom_mode = _ZoomMode.FIT_WIDTH if value else _ZoomMode.MANUAL_ZOOM
        self._adjust_scale()

    def enableKeepPrevScale(self, enabled):
        self._config["keep_prev_scale"] = enabled
        self._actions.keep_prev_scale.setChecked(enabled)

    def onNewBrightnessContrast(self, qimage):
        self._canvas_widgets.canvas.loadPixmap(
            QtGui.QPixmap.fromImage(qimage), clear_shapes=False
        )

    def brightnessContrast(self, value: bool, is_initial_load: bool = False):
        if self._filename is None:
            logger.warning("filename is None, cannot set brightness/contrast")
            return

        brightness: int | None
        contrast: int | None
        brightness, contrast = self._brightness_contrast_values.get(
            self._filename, (None, None)
        )
        if is_initial_load:
            prev_filename: str = self._recent_files[0] if self._recent_files else ""
            if self._config["keep_prev_brightness_contrast"] and prev_filename:
                brightness, contrast = self._brightness_contrast_values.get(
                    prev_filename, (None, None)
                )
            if brightness is None and contrast is None:
                return

        logger.debug(
            "Opening brightness/contrast dialog with brightness={}, contrast={}",
            brightness,
            contrast,
        )
        dialog = BrightnessContrastDialog(
            utils.img_data_to_pil(self.imageData),
            self.onNewBrightnessContrast,
            parent=self,
        )

        if brightness is not None:
            dialog.slider_brightness.setValue(brightness)
        if contrast is not None:
            dialog.slider_contrast.setValue(contrast)

        if is_initial_load:
            dialog.onNewValue(None)
        else:
            dialog.exec_()
            brightness = dialog.slider_brightness.value()
            contrast = dialog.slider_contrast.value()

        self._brightness_contrast_values[self._filename] = (brightness, contrast)
        logger.debug(
            "Updated states for {}: brightness={}, contrast={}",
            self._filename,
            brightness,
            contrast,
        )

    def toggleShapes(self, value):
        flag = value
        for item in self._docks.label_list:
            if value is None:
                flag = item.checkState() == Qt.Unchecked
            item.setCheckState(Qt.Checked if flag else Qt.Unchecked)

    def _load_file(self, filename=None):
        """Load the specified file, or the last opened file if None."""
        # changing fileListWidget loads file
        if filename in self.imageList and (
            self._docks.file_list.currentRow() != self.imageList.index(filename)
        ):
            self._docks.file_list.setCurrentRow(self.imageList.index(filename))
            self._docks.file_list.repaint()
            return

        prev_shapes: list[Shape] = (
            self._canvas_widgets.canvas.shapes
            if self._config["keep_prev"]
            or QtWidgets.QApplication.keyboardModifiers()
            == (Qt.ControlModifier | Qt.ShiftModifier)
            else []
        )
        self.resetState()
        self._canvas_widgets.canvas.setEnabled(False)
        if filename is None:
            filename = self.settings.value("filename", "")
        filename = str(filename)
        if not QtCore.QFile.exists(filename):
            self.errorMessage(
                self.tr("Error opening file"),
                self.tr("No such file: <b>%s</b>") % filename,
            )
            return False
        # assumes same name, but json extension
        self.show_status_message(self.tr("Loading %s...") % osp.basename(str(filename)))
        t0_load_file = time.time()
        label_file = f"{osp.splitext(filename)[0]}.json"
        if self._output_dir:
            label_file_without_path = osp.basename(label_file)
            label_file = osp.join(self._output_dir, label_file_without_path)
        if QtCore.QFile.exists(label_file) and LabelFile.is_label_file(label_file):
            try:
                self._label_file = LabelFile(label_file)
            except LabelFileError as e:
                self.errorMessage(
                    self.tr("Error opening file"),
                    self.tr(
                        "<p><b>%s</b></p>"
                        "<p>Make sure <i>%s</i> is a valid label file.</p>"
                    )
                    % (e, label_file),
                )
                self.show_status_message(self.tr("Error reading %s") % label_file)
                return False
            assert self._label_file is not None
            self.imageData = self._label_file.imageData
            assert self._label_file.imagePath
            self._image_path = osp.join(
                osp.dirname(label_file),
                self._label_file.imagePath,
            )
            self._other_data = self._label_file.otherData
        else:
            try:
                self.imageData = LabelFile.load_image_file(filename)
            except OSError as e:
                self.errorMessage(
                    self.tr("Error opening file"),
                    self.tr(
                        "<p><b>%s</b></p>"
                        "<p>Make sure <i>%s</i> is a valid image file.</p>"
                    )
                    % (e, filename),
                )
                self.show_status_message(self.tr("Error reading %s") % filename)
                return False
            if self.imageData:
                self._image_path = filename
            self._label_file = None
        assert self.imageData is not None
        t0 = time.time()
        image = QtGui.QImage.fromData(self.imageData)
        logger.debug("Created QImage in {:.0f}ms", (time.time() - t0) * 1000)

        if image.isNull():
            formats = [
                f"*.{fmt.data().decode()}"
                for fmt in QtGui.QImageReader.supportedImageFormats()
            ]
            self.errorMessage(
                self.tr("Error opening file"),
                self.tr(
                    "<p>Make sure <i>{0}</i> is a valid image file.<br/>"
                    "Supported image formats: {1}</p>"
                ).format(filename, ",".join(formats)),
            )
            self.show_status_message(self.tr("Error reading %s") % filename)
            return False
        self._image = image
        self._filename = filename
        t0 = time.time()
        self._canvas_widgets.canvas.loadPixmap(QtGui.QPixmap.fromImage(image))
        logger.debug("Loaded pixmap in {:.0f}ms", (time.time() - t0) * 1000)
        flags = {k: False for k in self._config["flags"] or []}
        if self._label_file:
            self._load_shape_dicts(shape_dicts=self._label_file.shapes)
            if self._label_file.flags is not None:
                flags.update(self._label_file.flags)
        self._load_flags(flags=flags, widget=self._docks.flag_list)
        if prev_shapes and self.noShapes():
            self._load_shapes(shapes=prev_shapes, replace=False)
            self.setDirty()
        else:
            self.setClean()
        self._canvas_widgets.canvas.setEnabled(True)
        # set zoom values
        is_initial_load = not self._zoom_values
        if self._filename in self._zoom_values:
            self._zoom_mode = self._zoom_values[self._filename][0]
            self._set_zoom(self._zoom_values[self._filename][1])
        elif is_initial_load or not self._config["keep_prev_scale"]:
            self._zoom_mode = _ZoomMode.FIT_WINDOW
            self._adjust_scale()
        # set scroll values
        for orientation in self._scroll_values:
            if self._filename in self._scroll_values[orientation]:
                self.setScroll(
                    orientation, self._scroll_values[orientation][self._filename]
                )
        self.brightnessContrast(value=False, is_initial_load=True)
        self._paint_canvas()
        self.addRecentFile(self._filename)
        self.toggleActions(True)
        self._canvas_widgets.canvas.setFocus()
        self.show_status_message(self.tr("Loaded %s") % osp.basename(filename))
        logger.info(
            "Loaded file: {!r} in {:.0f}ms",
            filename,
            (time.time() - t0_load_file) * 1000,
        )
        return True

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        if (
            self._canvas_widgets.canvas
            and not self._image.isNull()
            and self._zoom_mode != _ZoomMode.MANUAL_ZOOM
        ):
            self._adjust_scale()
        super().resizeEvent(a0)

    def _paint_canvas(self) -> None:
        if self._image.isNull():
            logger.warning("image is null, cannot paint canvas")
            return
        self._canvas_widgets.canvas.scale = (
            0.01 * self._canvas_widgets.zoom_widget.value()
        )
        self._canvas_widgets.canvas.adjustSize()
        self._canvas_widgets.canvas.update()

    def _adjust_scale(self) -> None:
        self._set_zoom(value=int(self._scalers[self._zoom_mode]() * 100))

    def scaleFitWindow(self) -> float:
        EPSILON_TO_HIDE_SCROLLBAR: float = 2.0
        w1: float = self.centralWidget().width() - EPSILON_TO_HIDE_SCROLLBAR
        h1: float = self.centralWidget().height() - EPSILON_TO_HIDE_SCROLLBAR
        a1: float = w1 / h1

        w2: float = self._canvas_widgets.canvas.pixmap.width()
        h2: float = self._canvas_widgets.canvas.pixmap.height()
        a2: float = w2 / h2

        return w1 / w2 if a2 >= a1 else h1 / h2

    def scaleFitWidth(self):
        EPSILON_TO_HIDE_SCROLLBAR: float = 15.0
        w = self.centralWidget().width() - EPSILON_TO_HIDE_SCROLLBAR
        return w / self._canvas_widgets.canvas.pixmap.width()

    def enableSaveImageWithData(self, enabled):
        self._config["with_image_data"] = enabled
        self._actions.save_with_image_data.setChecked(enabled)

    def _reset_layout(self):
        self.settings.remove("window/state")
        self.restoreState(self._default_state)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if not self._can_continue():
            a0.ignore()
        self.settings.setValue("filename", self._filename if self._filename else "")
        self.settings.setValue("window/size", self.size())
        self.settings.setValue("window/position", self.pos())
        self.settings.setValue("window/state", self.saveState())
        self.settings.setValue("recentFiles", self._recent_files)

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        extensions = [
            f".{fmt.data().decode().lower()}"
            for fmt in QtGui.QImageReader.supportedImageFormats()
        ]
        if a0.mimeData().hasUrls():
            items = [i.toLocalFile() for i in a0.mimeData().urls()]
            if any([i.lower().endswith(tuple(extensions)) for i in items]):
                a0.accept()
        else:
            a0.ignore()

    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        if not self._can_continue():
            a0.ignore()
            return
        items = [i.toLocalFile() for i in a0.mimeData().urls()]
        self.importDroppedImageFiles(items)

    # User Dialogs #

    def loadRecent(self, filename):
        if self._can_continue():
            self._load_file(filename)

    def _open_prev_image(self, _value=False) -> None:
        row_prev: int = self._docks.file_list.currentRow() - 1
        if row_prev < 0:
            logger.debug("there is no prev image")
            return

        logger.debug("setting current row to {:d}", row_prev)
        self._docks.file_list.setCurrentRow(row_prev)
        self._docks.file_list.repaint()

    def _open_next_image(self, _value=False) -> None:
        row_next: int = self._docks.file_list.currentRow() + 1
        if row_next >= self._docks.file_list.count():
            logger.debug("there is no next image")
            return

        logger.debug("setting current row to {:d}", row_next)
        self._docks.file_list.setCurrentRow(row_next)
        self._docks.file_list.repaint()

    def _open_file_with_dialog(self, _value: bool = False) -> None:
        if not self._can_continue():
            return
        path = osp.dirname(str(self._filename)) if self._filename else "."
        formats = [
            f"*.{fmt.data().decode()}"
            for fmt in QtGui.QImageReader.supportedImageFormats()
        ]
        filters = self.tr("Image & Label files (%s)") % " ".join(
            formats + [f"*{LabelFile.suffix}"]
        )
        fileDialog = FileDialogPreview(self)
        fileDialog.setFileMode(FileDialogPreview.ExistingFile)
        fileDialog.setNameFilter(filters)
        fileDialog.setWindowTitle(
            self.tr("%s - Choose Image or Label file") % __appname__,
        )
        
        fileDialog.setWindowFilePath(path)
        fileDialog.setViewMode(FileDialogPreview.Detail)
        if fileDialog.exec_():
            fileName = fileDialog.selectedFiles()[0]
            if fileName:
                self._load_file(fileName)

    def changeOutputDirDialog(self, _value=False):
        default_output_dir = self._output_dir
        if default_output_dir is None and self._filename:
            default_output_dir = osp.dirname(self._filename)
        if default_output_dir is None:
            default_output_dir = self.currentPath()

        output_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            self.tr("%s - Save/Load Annotations in Directory") % __appname__,
            default_output_dir,
            QtWidgets.QFileDialog.ShowDirsOnly
            | QtWidgets.QFileDialog.DontResolveSymlinks,
        )
        output_dir = str(output_dir)

        if not output_dir:
            return

        self._output_dir = output_dir

        self.statusBar().showMessage(
            self.tr("%s . Annotations will be saved/loaded in %s")
            % ("Change Annotations Dir", self._output_dir)
        )
        self.statusBar().show()

        current_filename = self._filename
        self._import_images_from_dir(root_dir=self._prev_opened_dir)

        if current_filename in self.imageList:
            # retain currently selected file
            self._docks.file_list.setCurrentRow(self.imageList.index(current_filename))
            self._docks.file_list.repaint()

    def saveFile(self, _value: bool = False) -> None:
        assert not self._image.isNull(), "cannot save empty image"
        if self._label_file:
            self._saveFile(self._label_file.filename)
        else:
            self._saveFile(self.saveFileDialog())

    def saveFileAs(self, _value: bool = False) -> None:
        assert not self._image.isNull(), "cannot save empty image"
        self._saveFile(self.saveFileDialog())

    def saveFileDialog(self) -> str:
        assert self._filename is not None
        caption = self.tr("%s - Choose File") % __appname__
        filters = self.tr("Label files (*%s)") % LabelFile.suffix
        start_dir = self._output_dir if self._output_dir else self.currentPath()
        dlg = QtWidgets.QFileDialog(self, caption, start_dir, filters)
        dlg.setDefaultSuffix(LabelFile.suffix[1:])
        dlg.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dlg.setOption(QtWidgets.QFileDialog.DontConfirmOverwrite, False)
        dlg.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, False)
        basename = osp.basename(osp.splitext(self._filename)[0])
        if self._output_dir:
            default_labelfile_name = osp.join(
                self._output_dir, basename + LabelFile.suffix
            )
        else:
            default_labelfile_name = osp.join(
                self.currentPath(), basename + LabelFile.suffix
            )
        filename = dlg.getSaveFileName(
            self,
            self.tr("Choose File"),
            default_labelfile_name,
            self.tr("Label files (*%s)") % LabelFile.suffix,
        )
        if isinstance(filename, tuple):
            return filename[0]
        return filename

    def _saveFile(self, filename: str | None) -> None:
        if filename and self.saveLabels(filename):
            self.addRecentFile(filename)
            self.setClean()

    def closeFile(self, _value: bool = False) -> None:
        if not self._can_continue():
            return
        self.resetState()
        self.setClean()
        self.toggleActions(False)
        self._canvas_widgets.canvas.setEnabled(False)
        self._docks.file_list.setFocus()
        self._actions.save_as.setEnabled(False)

    def getLabelFile(self) -> str:
        assert self._filename is not None
        if self._filename.lower().endswith(".json"):
            return self._filename
        return f"{osp.splitext(self._filename)[0]}.json"

    def deleteFile(self) -> None:
        mb = QtWidgets.QMessageBox
        msg = self.tr(
            "You are about to permanently delete this label file, proceed anyway?"
        )
        answer = mb.warning(self, self.tr("Attention"), msg, mb.Yes | mb.No)
        if answer != mb.Yes:
            return

        label_file = self.getLabelFile()
        if osp.exists(label_file):
            os.remove(label_file)
            logger.info(f"Label file is removed: {label_file}")

        item = self._docks.file_list.currentItem()
        if item:
            item.setCheckState(Qt.Unchecked)

        # FIX: Resettiamo SEMPRE l'interfaccia e la lista grafica per svuotare il Canvas
        self.resetState()
        self.setClean()
        self._canvas_widgets.canvas.update()

    def _open_config_file(self) -> None:
        if self._config_file is None:
            QtWidgets.QMessageBox.information(
                self,
                self.tr("No Config File"),
                self.tr(
                    "Configuration was provided as a YAML expression via "
                    "command line.\n\n"
                    "To use the preferences editor, start Labelme with a config file:\n"
                    "  labelme --config ~/.labelmerc"
                ),
            )
            return
        config_file: Path = self._config_file

        system: str = platform.system()
        if system == "Darwin":
            subprocess.Popen(["open", "-t", config_file])
        elif system == "Windows":
            os.startfile(config_file)  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["xdg-open", config_file])

    # Message Dialogs. #
    def hasLabels(self) -> bool:
        if self.noShapes():
            self.errorMessage(
                "No objects labeled",
                "You must label at least one object to save the file.",
            )
            return False
        return True

    def hasLabelFile(self) -> bool:
        if self._filename is None:
            return False

        label_file = self.getLabelFile()
        return osp.exists(label_file)

    def _can_continue(self) -> bool:
        if not self._is_changed:
            return True
        mb = QtWidgets.QMessageBox
        msg = self.tr('Save annotations to "{}" before closing?').format(self._filename)
        answer = mb.question(
            self,
            self.tr("Save annotations?"),
            msg,
            mb.Save | mb.Discard | mb.Cancel,
            mb.Save,
        )
        if answer == mb.Discard:
            return True
        elif answer == mb.Save:
            self.saveFile()
            return True
        else:  # answer == mb.Cancel
            return False

    def errorMessage(self, title: str, message: str) -> int:
        return QtWidgets.QMessageBox.critical(
            self, title, f"<p><b>{title}</b></p>{message}"
        )

    def currentPath(self) -> str:
        return osp.dirname(str(self._filename)) if self._filename else "."

    def toggleKeepPrevMode(self) -> None:
        self._config["keep_prev"] = not self._config["keep_prev"]

    def removeSelectedPoint(self) -> None:
        self._canvas_widgets.canvas.removeSelectedPoint()
        self._canvas_widgets.canvas.update()
        if (
            self._canvas_widgets.canvas.hShape
            and not self._canvas_widgets.canvas.hShape.points
        ):
            self._canvas_widgets.canvas.deleteShape(self._canvas_widgets.canvas.hShape)
            self.remLabels([self._canvas_widgets.canvas.hShape])
            if self.noShapes():
                for action in self._actions.on_shapes_present:
                    action.setEnabled(False)
        self.setDirty()

    def deleteSelectedShape(self) -> None:
        yes, no = QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No
        msg = self.tr(
            "You are about to permanently delete {} shapes, proceed anyway?"
        ).format(len(self._canvas_widgets.canvas.selectedShapes))
        if yes == QtWidgets.QMessageBox.warning(
            self, self.tr("Attention"), msg, yes | no, yes
        ):
            self.remLabels(self._canvas_widgets.canvas.deleteSelected())
            self.setDirty()
            if self.noShapes():
                for action in self._actions.on_shapes_present:
                    action.setEnabled(False)

    def copyShape(self) -> None:
        self._canvas_widgets.canvas.endMove(copy=True)
        for shape in self._canvas_widgets.canvas.selectedShapes:
            self.addLabel(shape)
        self._docks.label_list.clearSelection()
        self.setDirty()

    def moveShape(self) -> None:
        self._canvas_widgets.canvas.endMove(copy=False)
        self.setDirty()

    def _open_dir_with_dialog(self, _value: bool = False) -> None:
        if not self._can_continue():
            return

        defaultOpenDirPath: str
        if self._prev_opened_dir and osp.exists(self._prev_opened_dir):
            defaultOpenDirPath = self._prev_opened_dir
        else:
            defaultOpenDirPath = osp.dirname(self._filename) if self._filename else "."

        targetDirPath = str(
            QtWidgets.QFileDialog.getExistingDirectory(
                self,
                self.tr("%s - Open Directory") % __appname__,
                defaultOpenDirPath,
                QtWidgets.QFileDialog.ShowDirsOnly
                | QtWidgets.QFileDialog.DontResolveSymlinks,
            )
        )
        self._import_images_from_dir(root_dir=targetDirPath)
        self._open_next_image()

    @property
    def imageList(self) -> list[str]:
        lst = []
        for i in range(self._docks.file_list.count()):
            item = self._docks.file_list.item(i)
            assert item
            lst.append(item.text())
        return lst

    def importDroppedImageFiles(self, imageFiles):
        extensions = [
            f".{fmt.data().decode().lower()}"
            for fmt in QtGui.QImageReader.supportedImageFormats()
        ]

        self._filename = None
        for file in imageFiles:
            if file in self.imageList or not file.lower().endswith(tuple(extensions)):
                continue
            label_file = f"{osp.splitext(file)[0]}.json"
            if self._output_dir:
                label_file_without_path = osp.basename(label_file)
                label_file = osp.join(self._output_dir, label_file_without_path)
            item = QtWidgets.QListWidgetItem(file)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            if QtCore.QFile.exists(label_file) and LabelFile.is_label_file(label_file):
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self._docks.file_list.addItem(item)

        if len(self.imageList) > 1:
            self._actions.open_next_img.setEnabled(True)
            self._actions.open_prev_img.setEnabled(True)

        self._open_next_image()

    def _import_images_from_dir(
        self, root_dir: str | None, pattern: str | None = None
    ) -> None:
        self._actions.open_next_img.setEnabled(True)
        self._actions.open_prev_img.setEnabled(True)

        if not self._can_continue() or not root_dir:
            return

        self._prev_opened_dir = root_dir
        self._filename = None
        self._docks.file_list.clear()

        filenames = _scan_image_files(root_dir=root_dir)
        if pattern:
            try:
                filenames = [f for f in filenames if re.search(pattern, f)]
            except re.error:
                pass
        for filename in filenames:
            label_file = f"{osp.splitext(filename)[0]}.json"
            if self._output_dir:
                label_file_without_path = osp.basename(label_file)
                label_file = osp.join(self._output_dir, label_file_without_path)
            item = QtWidgets.QListWidgetItem(filename)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            if QtCore.QFile.exists(label_file) and LabelFile.is_label_file(label_file):
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self._docks.file_list.addItem(item)

    def _update_status_stats(self, mouse_pos: QtCore.QPointF) -> None:
        stats: list[str] = []
        stats.append(f"mode={self._canvas_widgets.canvas.mode.name}")
        stats.append(f"x={mouse_pos.x():6.1f}, y={mouse_pos.y():6.1f}")
        self._status_bar.stats.setText(" | ".join(stats))


def _scan_image_files(root_dir: str) -> list[str]:
    extensions: list[str] = [
        f".{fmt.data().decode().lower()}"
        for fmt in QtGui.QImageReader.supportedImageFormats()
    ]

    images: list[str] = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(tuple(extensions)):
                relativePath = os.path.normpath(osp.join(root, file))
                images.append(relativePath)

    logger.debug("found {:d} images in {!r}", len(images), root_dir)
    return natsort.os_sorted(images)
