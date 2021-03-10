# coding:utf-8
from kivy.app import App
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.pagelayout import PageLayout
from kivy.uix.button import Button

from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np
from pyzbar.pyzbar import decode

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)

        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)


    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            for barcode in decode(frame):
                myData = barcode.data.decode('utf-8')
                # print(myData)
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (255, 0, 255), 5)
                pts2 = barcode.rect
                cv2.putText(frame, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture
                # with self.canvas:
                #     Rectangle(texture=image_texture, pos=self.pos, size=(64, 64))


class CamApp(App):
    def build(self):

        layout = BoxLayout(orientation='vertical')

        self.capture = cv2.VideoCapture(0)
        # self.capture.resolution = (300, 300)

        self.camaraClick = Button(text="Bulk Scan")
        self.camaraClick.size_hint = (.5, .2)
        self.camaraClick.pos_hint = {'x': .25, 'y': .75}

        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        # self.my_camera.resolution = (300, 300)

        layout.add_widget(self.camaraClick)
        layout.add_widget(self.my_camera)

        return layout

    def on_stop(self):
        # without this, app will not exit even if the window is closed
        self.capture.release()


if __name__ == '__main__':
    CamApp().run()
