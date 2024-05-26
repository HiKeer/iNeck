import cv2
import dlib
import numpy as np
import subprocess
import threading
import pyautogui
import time
from pynput.keyboard import Key, Controller
from imutils import face_utils
import win32gui
import win32con

# 脸部特征点模型路径
face_landmark_path = 'shape_predictor_68_face_landmarks.dat'

# 相机参数，用相机标定程序计算得到
K = [821.4438864, 0.0, 321.59586002,
     0.0, 818.06766317, 222.64326701,
     0.0, 0.0, 1.0]
D = [-0.121551899, 0.880513056, -0.00798281873, -0.00346685305, -3.83211727]

# 相机矩阵和畸变系数
cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)
dist_coeffs = np.array(D).reshape(5, 1).astype(np.float32)

# 3D模型点
object_pts = np.float32([[6.825897, 6.760612, 4.402142],
                         [1.330353, 7.122144, 6.903745],
                         [-1.330353, 7.122144, 6.903745],
                         [-6.825897, 6.760612, 4.402142],
                         [5.311432, 5.485328, 3.987654],
                         [1.789930, 5.393625, 4.413414],
                         [-1.789930, 5.393625, 4.413414],
                         [-5.311432, 5.485328, 3.987654],
                         [2.005628, 1.409845, 6.165652],
                         [-2.005628, 1.409845, 6.165652],
                         [2.774015, -2.080775, 5.048531],
                         [-2.774015, -2.080775, 5.048531],
                         [0.000000, -3.116408, 6.097667],
                         [0.000000, -7.415691, 4.070434]])

# 立方体顶点
reprojectsrc = np.float32([[10.0, 10.0, 10.0],
                           [10.0, 10.0, -10.0],
                           [10.0, -10.0, -10.0],
                           [10.0, -10.0, 10.0],
                           [-10.0, 10.0, 10.0],
                           [-10.0, 10.0, -10.0],
                           [-10.0, -10.0, -10.0],
                           [-10.0, -10.0, 10.0]])

# 立方体顶点连线对
line_pairs = [[0, 1], [1, 2], [2, 3], [3, 0],
              [4, 5], [5, 6], [6, 7], [7, 4],
              [0, 4], [1, 5], [2, 6], [3, 7]]

def get_head_pose(shape):
    # 选择的2D图像点
    image_pts = np.float32([shape[17], shape[21], shape[22], shape[26], shape[36],
                            shape[39], shape[42], shape[45], shape[31], shape[35],
                            shape[48], shape[54], shape[57], shape[8]])
    # 计算头部姿态
    _, rotation_vec, translation_vec = cv2.solvePnP(object_pts, image_pts, cam_matrix, dist_coeffs)
    reprojectdst, _ = cv2.projectPoints(reprojectsrc, rotation_vec, translation_vec, cam_matrix, dist_coeffs)
    reprojectdst = tuple(map(tuple, reprojectdst.reshape(8, 2)))

    # 计算欧拉角
    rotation_mat, _ = cv2.Rodrigues(rotation_vec)
    pose_mat = cv2.hconcat((rotation_mat, translation_vec))
    _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_mat)

    return reprojectdst, euler_angle

def keep_window_on_top(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

# def run_camera(index):
#     counter1 = 0
#     counter2 = 0
#     counter3 = 0
#     cap = cv2.VideoCapture(index)
#     if not cap.isOpened():
#         print(f"[IO Error]无法连接至摄像头{index}.")
#         return
#
#     detector = dlib.get_frontal_face_detector()
#     predictor = dlib.shape_predictor(face_landmark_path)
#
#     # 创建键盘模拟器
#     keyboard = Controller()
#
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if ret:
#             face_rects = detector(frame, 0)
#             for rect in face_rects:
#                 shape = predictor(frame, rect)
#                 shape = face_utils.shape_to_np(shape)
#                 reprojectdst, euler_angle = get_head_pose(shape)
#
#                 # 键盘操作逻辑
#                 if (euler_angle[1, 0] < -20 or euler_angle[2, 0] > 25) and counter1 >= 13:  # 左转超过25度
#                     keyboard.press('a')
#                     keyboard.release('a')
#                     #pyautogui.press('a')
#                     #print("press a")
#                     counter1 = 0
#                     counter1 = counter1 + 1
#                 else:
#                     print("still")
#                     counter1 = counter1 + 1
#
#                 if (euler_angle[1, 0] > 20 or euler_angle[2, 0] < -25) and counter3 >= 13:  # 右转超过25度
#                     keyboard.press('d')
#                     keyboard.release('d')
#                     #pyautogui.press('d')
#                     #print("press d")
#                     counter3 = 0
#                     counter3 = counter3 + 1
#                 else:
#                     print("still")
#                     counter3 = counter3 + 1
#
#                 if euler_angle[0, 0] < -15 and counter2 >= 13:  # 抬头超过15度
#                     keyboard.press(Key.space)
#                     keyboard.release(Key.space)
#                     #pyautogui.press('space')ddaa
#                     #print("press space")
#                     counter2 = 0
#                 else:
#                     #print("still")
#                     counter2 = counter2 + 1
#
#                 # 显示图像和姿态数据
#                 for start, end in line_pairs:
#                     cv2.line(frame, (int(reprojectdst[start][0]), int(reprojectdst[start][1])),
#                              (int(reprojectdst[end][0]), int(reprojectdst[end][1])), (0, 255, 0), 2)
#                 cv2.imshow("Head Pose Estimation", frame)
#                 keep_window_on_top("Head Pose Estimation")
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

def run_camera(index):
    counter1 = 0
    counter2 = 0
    counter3 = 0
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"[IO Error]无法连接至摄像头{index}.")
        return

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_landmark_path)

    # 创建键盘模拟器
    keyboard = Controller()

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            height, width = frame.shape[:2]
            middle_line_x = width // 2
            cv2.line(frame, (middle_line_x, 0), (middle_line_x, height), (255, 0, 0), 2)  # 画中线

            face_rects = detector(frame, 0)
            left_face_detected = False
            right_face_detected = False

            for rect in face_rects:
                shape = predictor(frame, rect)
                shape = face_utils.shape_to_np(shape)
                reprojectdst, euler_angle = get_head_pose(shape)

                # 判断人脸所在位置
                face_x = rect.center().x
                if face_x < middle_line_x:
                    left_face_detected = True
                    # 键盘操作逻辑
                    if euler_angle[1, 0] < -20 and counter1 >= 13:  # 左转超过25度
                        keyboard.press('a')
                        keyboard.release('a')
                        counter1 = 0
                    elif euler_angle[1, 0] > 20 and counter1 >= 13:  # 右转超过25度
                        keyboard.press('d')
                        keyboard.release('d')
                        counter1 = 0
                    elif euler_angle[0, 0] < -15 and counter2 >= 13:  # 抬头超过15度
                        keyboard.press('w')
                        keyboard.release('w')
                        counter2 = 0
                    elif euler_angle[0, 0] > 15 and counter3 >= 13:  # 低头超过15度
                        keyboard.press('s')
                        keyboard.release('s')
                        counter3 = 0
                    else:
                        counter1 += 1
                        counter2 += 1
                        counter3 += 1

                else:
                    right_face_detected = True
                    # 键盘操作逻辑
                    if euler_angle[1, 0] < -20 and counter1 >= 13:  # 左转超过25度
                        keyboard.press(Key.left)
                        keyboard.release(Key.left)
                        counter1 = 0
                    elif euler_angle[1, 0] > 20 and counter1 >= 13:  # 右转超过25度
                        keyboard.press(Key.right)
                        keyboard.release(Key.right)
                        counter1 = 0
                    elif euler_angle[0, 0] < -15 and counter2 >= 13:  # 抬头超过15度
                        keyboard.press(Key.up)
                        keyboard.release(Key.up)
                        counter2 = 0
                    elif euler_angle[0, 0] > 15 and counter3 >= 13:  # 低头超过15度
                        keyboard.press(Key.down)
                        keyboard.release(Key.down)
                        counter3 = 0
                    else:
                        counter1 += 1
                        counter2 += 1
                        counter3 += 1

                # 显示图像和姿态数据
                for start, end in line_pairs:
                    pt1 = (int(reprojectdst[start][0]), int(reprojectdst[start][1]))
                    pt2 = (int(reprojectdst[end][0]), int(reprojectdst[end][1]))
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

            cv2.imshow("Head Pose Estimation", frame)
            keep_window_on_top("Head Pose Estimation")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


def run_ineck():
    subprocess.run(["D:/Desktop/CAMAREandGame/iNeck/iNeck.exe"])

if __name__ == '__main__':
    camera_index = input("请输入待校准的相机编号(数字)：")
    camera_index = int(camera_index)

    # 创建线程
    ineck_thread = threading.Thread(target=run_ineck)
    camera_thread = threading.Thread(target=run_camera, args=(camera_index,))

    # 启动线程
    #ineck_thread.start()
    camera_thread.start()

    # 等待线程结束
    #ineck_thread.join()
    camera_thread.join()