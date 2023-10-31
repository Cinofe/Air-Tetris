import cv2, mediapipe as mp, numpy as np, keyboard as kb

# 모션 벡터 정보 저장
def writing(f, data, key):
    for num in data:
        f.write(str(num))
        f.write(',')
    # 0 : ready, 1 : left, 2 : right, 3 : turn, 4 : instant
    f.write(key)
    f.write('\n')

if __name__ == "__main__":
    # Mediapipe hand tracking 객체 생성
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_style = mp.solutions.drawing_styles
    hands = mp_hands.Hands(
        model_complexity=0,
        max_num_hands=1)

    # 손의 움직임에 따른 index 지정
    motion = {0:'ready',1:'left',2:'right',3:'turn',4:'instant'}
    file = np.genfromtxt('streaming/dataSet.txt',delimiter=',')
    cv = file[:,:-1].astype(np.float32)
    label = file[:,-1].astype(np.float32)

    # KNN 모델 생성
    knn = cv2.ml.KNearest_create()
    knn.train(cv,cv2.ml.ROW_SAMPLE,label)

    cap = cv2.VideoCapture(0)
    cnt = 0

    with open('test.txt','w') as f:
        while True:
            _, frame = cap.read()
            frame = cv2.flip(frame,0)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            h, w, _ =  frame.shape
            results = hands.process(frame)
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

            if results.multi_hand_landmarks:
                for res in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                            frame,
                            res,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_style.get_default_hand_landmarks_style(),
                            mp_drawing_style.get_default_hand_connections_style()
                            )
                    joint = np.zeros((21,2))
                    for j, lm in enumerate(res.landmark):
                        # 각 좌표의 중심 좌표를 0이 아닌 0.5를 기준으로 잡고 벡터 구하기
                        joint[j] = [lm.x - 0.5, 0.5 - lm.y]
                    # 엄지 좌표를 제외한 각 좌표의 벡터 시작점, 끝점 지정
                    v1 = joint[[0, 5, 6, 7, 0, 9,10,11, 0,13,14,15, 0,17,18,19],:]
                    v2 = joint[[5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20],:]
                    # 각 좌표 상의 벡터 계산
                    v = v2 - v1
                    # 벡터의 크기 도출
                    v = v / np.linalg.norm(v, axis=1)[:,np.newaxis]

                    # 각 좌표 벡터의 x,y 의 곱 계산
                    result = [round(i * (j+0.2),6) for i,j in v]

                    # 1 : ready, 2 : left, 3 : right, 4 : turn, 5 : instant
                    if kb.is_pressed('1'):
                        writing(f,result,'0.000000')
                        cnt += 1
                    elif kb.is_pressed('2'):
                        writing(f,result,'1.000000')
                        cnt += 1
                    elif kb.is_pressed('3'):
                        writing(f,result,'2.000000')
                        cnt += 1
                    elif kb.is_pressed('4'):
                        writing(f,result,'3.000000') 
                        cnt += 1
                    elif kb.is_pressed('5'):
                        writing(f,result,'4.000000')
                        cnt += 1
                    cv2.putText(frame, str(cnt),(20,20),0,0.8,(0,0,0),2)

                    data = np.array([result],dtype=np.float32)

                    ret, result, neighbours, dist = knn.findNearest(data,2)
                    index = int(result[0][0])
                    if index in motion.keys():
                        cv2.putText(frame, motion[index].upper(),
                                (int(res.landmark[0].x * frame.shape[1] -10),
                                int(res.landmark[0].y * frame.shape[0] + 40)),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)
                    
            cv2.imshow('frame',frame)
            cv2.waitKey(50)
            if kb.is_pressed('b'):
                break