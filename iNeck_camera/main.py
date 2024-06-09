import cv2
import dlib
import numpy as np
from imutils import face_utils

# 脸部特征点模型
face_landmark_path = 'shape_predictor_68_face_landmarks.dat'
# 相机参数，用相机标定程序计算得到
K = [821.4438864, 0.0, 321.59586002,
     0.0, 818.06766317, 222.64326701,
     0.0, 0.0, 1.0]
D = [-1.21551899e-01, 8.80513056e-01, -7.98281873e-03, -3.46685305e-03, -3.83211727e+00]
# 相机矩阵
cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)
dist_coeffs = np.array(D).reshape(5, 1).astype(np.float32)

# 14个特征点
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

# 定义显示立方体的顶点
reprojectsrc = np.float32([[10.0, 10.0, 10.0],
                           [10.0, 10.0, -10.0],
                           [10.0, -10.0, -10.0],
                           [10.0, -10.0, 10.0],
                           [-10.0, 10.0, 10.0],
                           [-10.0, 10.0, -10.0],
                           [-10.0, -10.0, -10.0],
                           [-10.0, -10.0, 10.0]])

# 根据立方体顶点定义的边
line_pairs = [[0, 1], [1, 2], [2, 3], [3, 0],
              [4, 5], [5, 6], [6, 7], [7, 4],
              [0, 4], [1, 5], [2, 6], [3, 7]]


# 获得头部姿态
def get_head_pose(shape):
    # 14个特征点
    image_pts = np.float32([shape[17], shape[21], shape[22], shape[26], shape[36],
                            shape[39], shape[42], shape[45], shape[31], shape[35],
                            shape[48], shape[54], shape[57], shape[8]])
    # 旋转向量与位移向量
    _, rotation_vec, translation_vec = cv2.solvePnP(object_pts, image_pts, cam_matrix, dist_coeffs)

    reprojectdst, _ = cv2.projectPoints(reprojectsrc, rotation_vec, translation_vec, cam_matrix,
                                        dist_coeffs)

    reprojectdst = tuple(map(tuple, reprojectdst.reshape(8, 2)))

    # 计算欧拉角Euler
    rotation_mat, _ = cv2.Rodrigues(rotation_vec)
    pose_mat = cv2.hconcat((rotation_mat, translation_vec))
    _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_mat)

    return reprojectdst, euler_angle


def main(index):
    # 打开摄像头
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"[IO Error]无法连接至摄像头{index}.")
        return
    # 初始化检测器
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_landmark_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            face_rects = detector(frame, 0)

            if len(face_rects) > 0:
                shape = predictor(frame, face_rects[0])
                shape = face_utils.shape_to_np(shape)

                reprojectdst, euler_angle = get_head_pose(shape)

                if abs(euler_angle[1, 0]) < 5:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)

                for (x, y) in shape:
                    cv2.circle(frame, (x, y), 1, color, -1)

                for start, end in line_pairs:
                    print(reprojectdst[start])
                    print(reprojectdst[end])
                    cv2.line(frame, (int(reprojectdst[start][0]),int(reprojectdst[start][1])), (int(reprojectdst[end][0]),int(reprojectdst[end][1])), color)

                cv2.putText(frame, "X: " + "{:7.2f}".format(euler_angle[0, 0]), (20, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 0), thickness=2)
                cv2.putText(frame, "Y: " + "{:7.2f}".format(euler_angle[1, 0]), (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 0), thickness=2)
                cv2.putText(frame, "Z: " + "{:7.2f}".format(euler_angle[2, 0]), (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 0), thickness=2)

            cv2.imshow("Camera Calibration", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    temp = input("请输入待校准的相机编号(数字)：")
    temp = int(temp)
    main(temp)
