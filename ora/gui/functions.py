from os.path import join

from PyQt5.Qt import QIcon, QSize
from PyQt5.QtWidgets import QFileDialog

SRC_PATH = './ora/gui/images'


def dynamic_base_class(instance, cls, cls_name):
    instance.__class__ = type(cls_name, (cls, instance.__class__), {})
    return instance


def set_background_img(widget, file_name, path='/bgs/'):
    widget.setStyleSheet("background-image: url(%s)" % (SRC_PATH + path + file_name))


def set_background_color(widget, color):
    widget.setStyleSheet("background-color: %s" % color)


def set_plain_text(widget, text):
    widget.setPlainText(text)


def pic_to_icon(file_name, path='icons'):
    return QIcon(join(SRC_PATH, path, file_name))


def set_full_icon(widget, file_name, path='icons'):
    qicon = pic_to_icon(file_name, path)
    widget.setIcon(qicon)
    widget.setIconSize(QSize(100, 100))


def remove_listwidget_item(listwidget):
    listwidget.takeItem(listwidget.currentRow())

def open_file_dialog(parent):
    filename, _ = QFileDialog.getOpenFileName(parent, u'select video')
    return filename

def set_qclass_child_widgets_style(widget, qclass, style):
    for c in get_qclass_child_widgets(widget, qclass):
        c.setStyleSheet(style)


def get_qclass_child_widgets(widget, qclass):
    for c in widget.children():
        if isinstance(c, qclass):
            yield c