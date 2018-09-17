from threading import Thread
from time import sleep

import cv2


from tf_session.tf_session_runner import SessionRunner
from tf_session.tf_session_utils import Pipe, Inference
from weapon_detection.tf_api.tf_weapon_detection_api import TFWeaponDetectionAPI

#cap = cv2.VideoCapture(-1)
cap = cv2.VideoCapture("/home/developer/PycharmProjects/SecureIt/weapon_detection/tf_api/data/video4.mp4")
if __name__ == '__main__':
    session_runner = SessionRunner(threading=True)
    while True:
        ret, image = cap.read()
        if ret:
            break

    detection = TFWeaponDetectionAPI(image.shape, 'tf_api', False)
    ip = detection.get_in_pipe()
    # op = detection.get_out_pipe()
    detection.use_session_runner(session_runner)

    session_runner.start()
    detection.run()

    ret_pipe = Pipe()

    # for i in range(1000):
    while True:
        ret, image = cap.read()
        if not ret:
            continue
        ip.push(Inference(image,ret_pipe,{}))

        ret, inference = ret_pipe.pull()
        if ret:
            # print(inference.get_classes())
            cv2.imshow("", inference.get_result().anotate())
            cv2.waitKey(1)
        else:
            ret_pipe.wait()

    session_runner.stop()