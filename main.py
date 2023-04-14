import os
from imageai.Detection import ObjectDetection
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def ViewMedia(widget, media_path, width, height):
    if media_path:
        pixmap = QPixmap(media_path)
        pixmap = pixmap.scaled(width, height, QtCore.Qt.KeepAspectRatio)
        widget.setPixmap(pixmap)


def ResizeMediaLabel(event):
    global media_size
    media_size = [event.size().width(), event.size().height()]
    global current_mediaPath
    ViewMedia(dlg.label_media, current_mediaPath, media_size[0], media_size[1])


def changeResizeEvent(widget, func):
    widget.resizeEvent = func


def importMedia():
    global current_mediaPath
    file_path = QFileDialog.getOpenFileName(None, "Открытие",
                                            current_mediaPath)[0]
    if file_path:
        current_mediaPath = file_path[file_path.rfind("/") + 1:]
        global temporary_file_path
        global media_size
        temporary_file_path = file_path
        with open(file_path, "rb") as file:
            global media
            media = file.read()
        ViewMedia(dlg.label_media, temporary_file_path, media_size[0],
                  media_size[1])


def setTypes():
    types = dlg.lineEdit_types.text()
    types = types.replace(",", "").replace(".", "").split()
    for type in types:
        if customObjects.get(type) != None:
            customObjects.update({type: True})


def detectTypes():
    objects, pathes = detector.detectObjectsFromImage(
        custom_objects=customObjects,
        input_image=current_mediaPath,
        output_image_path=f"detected_{current_mediaPath}",
        extract_detected_objects=True,
        minimum_percentage_probability=30)
    for result in objects:
        print(result["name"])


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    dlg = uic.loadUi("ui.ui")
    dlg.setWindowTitle("Программа запущена...")

    current_mediaPath = ""
    media_size = [488, 249]

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("yolov3.pt")
    detector.loadModel()

    customObjects = detector.CustomObjects()
    """
    'person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 
    'boat', 'traffic_light', 'fire_hydrant', 'stop_sign', 'parking_meter', 'bench', 
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 
    'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 
    'skis', 'snowboard', 'sports_ball', 'kite', 'baseball_bat', 'baseball_glove', 
    'skateboard', 'surfboard', 'tennis_racket', 'bottle', 'wine_glass', 'cup', 'fork', 
    'knife', 'spoon', 'sofa', 'pottedplant', 'bed', 'diningtable', 'toilet', 'tvmonitor', 
    'laptop', 'mouse', 'remote', 'keyboard', 'cell_phone', 'microwave', 'oven', 'toaster', 
    'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy_bear', 'hair_drier', 'toothbrush'
    """

    dlg.pushButton_import.clicked.connect(importMedia)
    dlg.pushButton_setTypes.clicked.connect(setTypes)
    dlg.pushButton_detect.clicked.connect(detectTypes)

    changeResizeEvent(dlg.label_media, ResizeMediaLabel)

    dlg.show()
    app.exec()