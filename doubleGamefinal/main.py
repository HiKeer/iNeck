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
import keyboard

camera_index = 0
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

def run_camera1(index):
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
            face_rects = detector(frame, 0)
            for rect in face_rects:
                shape = predictor(frame, rect)
                shape = face_utils.shape_to_np(shape)
                reprojectdst, euler_angle = get_head_pose(shape)

                # 键盘操作逻辑
                if (euler_angle[1, 0] < -20 or euler_angle[2, 0] > 25) and counter1 >= 13:  # 左转超过25度
                    keyboard.press('a')
                    keyboard.release('a')
                    #pyautogui.press('a')
                    #print("press a")
                    counter1 = 0
                    counter1 = counter1 + 1
                else:
                    print("still")
                    counter1 = counter1 + 1

                if (euler_angle[1, 0] > 20 or euler_angle[2, 0] < -25) and counter3 >= 13:  # 右转超过25度
                    keyboard.press('d')
                    keyboard.release('d')
                    #pyautogui.press('d')
                    #print("press d")
                    counter3 = 0
                    counter3 = counter3 + 1
                else:
                    print("still")
                    counter3 = counter3 + 1

                if euler_angle[0, 0] < -15 and counter2 >= 13:  # 抬头超过15度
                    keyboard.press(Key.space)
                    keyboard.release(Key.space)
                    #pyautogui.press('space')ddaa
                    #print("press space")
                    counter2 = 0
                else:
                    #print("still")
                    counter2 = counter2 + 1

                # 显示图像和姿态数据
                for start, end in line_pairs:
                    cv2.line(frame, (int(reprojectdst[start][0]), int(reprojectdst[start][1])),
                             (int(reprojectdst[end][0]), int(reprojectdst[end][1])), (0, 255, 0), 2)
                cv2.imshow("Head Pose Estimation", frame)
                keep_window_on_top("Head Pose Estimation")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

def run_camera2(index):
    counter1 = 0
    counter2 = 0
    counter3 = 0
    counter4 = 0
    counter5 = 0
    counter6 = 0
    counter7 = 0
    counter8 = 0
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
            cv2.line(frame, (middle_line_x, 0), (middle_line_x, height), (255, 255, 255), 2)  # 画中线

            # 在左右两侧添加白色方框
            box_size = 240
            box_top_y = height // 3 - box_size // 2
            box_center_left = (middle_line_x // 2, height // 2)
            box_center_right = (middle_line_x + middle_line_x // 2, height // 2)
            # 白色方框
            cv2.rectangle(frame, (box_center_left[0] - box_size // 2, box_center_left[1] - box_size // 2),
                          (box_center_left[0] + box_size // 2, box_center_left[1] + box_size // 2),
                          (255, 255, 255), 2)  # 左侧
            # 白色方框
            cv2.rectangle(frame, (box_center_right[0] - box_size // 2, box_center_right[1] - box_size // 2),
                          (box_center_right[0] + box_size // 2, box_center_right[1] + box_size // 2),
                          (255, 255, 255), 2)  # 右侧

            face_rects = detector(frame, 0)
            left_face_detected = False
            right_face_detected = False

            for rect in face_rects:
                if rect.width() < width and rect.height() < height:  # 检查人脸框的大小是否合理
                    shape = predictor(frame, rect)
                    shape = face_utils.shape_to_np(shape)
                    reprojectdst, euler_angle = get_head_pose(shape)

                    # 判断人脸所在位置
                    face_x = rect.center().x
                    if face_x < middle_line_x:
                        left_face_detected = True
                        # 键盘操作逻辑
                        if (euler_angle[1, 0] < -20 or euler_angle[2, 0] > 25) and counter1 >= 13:  # 左转超过25度
                            keyboard.press(Key.left)
                            keyboard.release(Key.left)
                            counter1 = 0
                        else:
                            print("still")
                            counter1 = counter1 + 1

                        if (euler_angle[1, 0] > 20 or euler_angle[2, 0] < -25) and counter3 >= 13:  # 右转超过25度
                            keyboard.press(Key.right)
                            keyboard.release(Key.right)
                            counter3 = 0
                        else:
                            print("still")
                            counter3 = counter3 + 1

                        if euler_angle[0, 0] < -15 and counter2 >= 13:  # 抬头超过15度
                            keyboard.press(Key.up)
                            keyboard.release(Key.up)
                            counter2 = 0
                        else:
                            print("still")
                            counter2 = counter2 + 1

                        if euler_angle[0, 0] > 15 and counter4 >= 13:  # 低头超过15度
                            keyboard.press(Key.down)
                            keyboard.release(Key.down)
                            counter4 = 0
                        else:
                            print("still")
                            counter4 = counter4 + 1


                    else:
                        right_face_detected = True
                        # 键盘操作逻辑
                        if (euler_angle[1, 0] < -20 or euler_angle[2, 0] > 25) and counter5 >= 13:  # 左转超过25度
                            keyboard.press('a')
                            keyboard.release('a')
                            counter5 = 0
                        else:
                            print("still")
                            counter5 = counter5 + 1


                        if (euler_angle[1, 0] > 20 or euler_angle[2, 0] < -25) and counter6 >= 13:  # 右转超过25度
                            keyboard.press('d')
                            keyboard.release('d')
                            counter6 = 0
                        else:
                            print("still")
                            counter6 = counter6 + 1

                        if euler_angle[0, 0] < -15 and counter7 >= 13:  # 抬头超过15度
                            keyboard.press(Key.space)
                            keyboard.release(Key.space)
                            counter7 = 0
                        else:
                            print("still")
                            counter7 = counter7 + 1

                        if euler_angle[0, 0] > 15 and counter8 >= 13:  # 低头超过15度
                            keyboard.press('s')
                            keyboard.release('s')
                            counter8 = 0
                        else:
                            print("still")
                            counter8 = counter8 + 1


                    # 显示图像和姿态数据
                    # 显示图像和姿态数据
                    # 显示图像和姿态数据
                    for start, end in line_pairs:
                        pt1 = (int(reprojectdst[start][0]), int(reprojectdst[start][1]))
                        pt2 = (int(reprojectdst[end][0]), int(reprojectdst[end][1]))

                        # 修剪坐标，确保不超出范围
                        pt1 = (max(0, min(pt1[0], width - 1)), max(0, min(pt1[1], height - 1)))
                        pt2 = (max(0, min(pt2[0], width - 1)), max(0, min(pt2[1], height - 1)))

                        if face_x < middle_line_x:
                            cv2.line(frame, pt1, pt2, (191, 63, 127), 2)  # 左侧
                        else:
                            cv2.line(frame, pt1, pt2, (191, 95, 255), 2)  # 右侧

            # 放大画面
            frame = cv2.resize(frame, (int(width * 1.5), int(height * 1.5)))

            cv2.imshow("Left Camera", frame[:, :int(middle_line_x * 1.5)])
            cv2.imshow("Right Camera", frame[:, int(middle_line_x * 1.5):])
            keep_window_on_top("Left Camera")
            keep_window_on_top("Right Camera")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


def run_ineck():
    subprocess.run(["./Build3/iNeck.exe"])

def stop_camera():
    global camera_running, camera_thread
    if camera_running:
        camera_running = False
        print("Stopping camera thread...")
        camera_thread.join()  # 确保线程结束
        camera_thread = None
        print("Camera thread has been stopped.")

def on_key_event(event):
    global camera_running
    global camera_thread

    if event.event_type == keyboard.KEY_DOWN:
        if event.name == "1":
            camera_running = True
            camera_thread = threading.Thread(target=run_camera1, args=(camera_index,))
            camera_thread.start()
        elif event.name == "2":
            camera_running = True
            camera_thread = threading.Thread(target=run_camera2, args=(camera_index,))
            camera_thread.start()
        elif event.name == "3":
            # if camera_running:
            #     camera_running = False
            #     camera_thread.join()  # 等待当前线程结束
            stop_camera()

if __name__ == '__main__':
    #camera_index = input("请输入待校准的相机编号(数字)：")
    #camera_index = int(camera_index)

    # 创建线程
    ineck_thread = threading.Thread(target=run_ineck)
    # 启动线程
    ineck_thread.start()

    keyboard.on_press(on_key_event)

    # 等待线程结束
    ineck_thread.join()