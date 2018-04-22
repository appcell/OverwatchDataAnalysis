from os.path import join

from PyQt5.Qt import QIcon, QSize

SRC_PATH = './images'


def dynamic_base_class(instance, cls, cls_name):
    instance.__class__ = type(cls_name, (cls, instance.__class__), {})
    return instance


def set_background_img(widget, file_name, path='/bgs/'):
    widget.setStyleSheet("background-image: url(%s)" % (SRC_PATH + path + file_name))


def set_background_color(widget, color):
    widget.setStyleSheet("background-color: %s" % color)


def pic_to_icon(file_name, path='icons'):
    return QIcon(join(SRC_PATH, path, file_name))


def set_full_icon(self, widget, file_name, path='icons'):
    qicon = self._get_icon(file_name, path)
    widget.setIcon(qicon)
    widget.setIconSize(QSize(100, 100))


def set_qclass_child_widgets_style(widget, qclass, style):
    for c in get_qclass_child_widgets(widget, qclass):
        c.setStyleSheet(style)


def get_qclass_child_widgets(widget, qclass):
    for c in widget.children():
        if isinstance(c, qclass):
            yield c