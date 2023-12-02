import RPi.GPIO as GPIO
from enum import Enum
import os
from time import sleep
import sys
import random
from motor import Motor, GuideMotorStep
from sensor import Sensor
from server_communication import ServerComm

# 현재 스크립트 파일의 디렉토리 경로
current_path = os.path.dirname(__file__)
# 외부 폴더의 경로 지정 (예: /home/pi/external_folder)
external_path = os.path.join(current_path, '/home/admin/test/common')
# sys.path에 외부 폴더 경로 추가
sys.path.append(external_path)

from enum import Enum
# 모듈 또는 파일 불러오기
from server_communication import ServerComm
from sensor import Sensor
from motor import Motor, GuideMotorStep

class Step( Enum ) :    #각 스텝별 이름, 동사형으로 지을것, 무엇을 하는 스텝인지 알 수 있는 네이밍
    
    start = 0
    fourth_part_irsensor_post = 11
    fourth_part_process_start = 22
    fourth_part_process_sleep = 33
    fourth_part_sensor_measure_and_endpost = 44 ##여기서는 4공정 정보를 false,left,right 값을 받고 
    go_rail_next_1 = 55
    stop_rail_1 = 66
    end_time =77

pass_or_fail1 = ''
pass_or_fail2 = ''

# GPIO 핀 번호 설정
LIGHT_SENSOR_PIN = 6
IR_SENSOR_PIN = 7
SERVO_MOTOR_1_PIN = 17
SERVO_MOTOR_2_PIN = 18

currnet_step = Step.start   #기본설정
running = True  
sensor = Sensor()   #센서 참조
server_comm = ServerComm()  #서버참조
svmotor_1 = Motor(SERVO_MOTOR_1_PIN,50) # 주파수 50Hz
svmotor_2 = Motor(SERVO_MOTOR_2_PIN,50)
motor = Motor # DC모터

while running:
    print( "running : " + str( running ) )# 디버깅확인용
    sleep( 0.1 )
    FOURTH_IR = sensor.get_ir_sensor( IR_SENSOR_PIN )  ##마지막에 활용
    match currnet_step :
        case Step.start: 
            print( Step.start )
            svmotor_2.doGuideMotor( GuideMotorStep.stop )
            svmotor_1.doGuideMotor( GuideMotorStep.stop )
            #시작하기전에 검사할것들: 통신확인여부, 모터정렬, 센서 검수
            currnet_step = Step.fourth_part_irsensor_post #다음스텝으로 이동sd

        case Step.fourth_part_irsensor_post:  
            print( Step.fourth_part_irsensor_post )
            #서버에서 적외선 센서 감지 여부 전송
            detect_reply = server_comm.confirmationObject(4, FOURTH_IR)
            # 답변 중 msg 변수에 "ok" 를 확인할 시
            if( detect_reply == "ok"):
                current_step = Step.fourth_part_process_start
            else:
                current_step = Step.fourth_part_irsensor_post


        case Step.fourth_part_process_start:  #계산함수 시작조건 - 센서감지
            print( Step.fourth_part_process_start )
            start_reply = server_comm.metalWiringStart() 
            # 조도센서가 임무를 수행   
            # 답변 중 msg 변수에 "ok" 를 확인할 시
            if( start_reply == "ok"):
                current_step = Step.fourth_part_process_sleep
            else:
                current_step = Step.fourth_part_process_start

        case Step.fourth_part_process_sleep:
            # 랜덤값 변수 대입 후 딜레이 (제조 시간 구현)
            print( Step.fourth_part_process_sleep )
            random_time = random.randint(4, 8)
            sleep(random_time)
            # 딜레이(제조)가 다 끝나면
            current_step = Step.fourth_part_sensor_measure_and_endpost     

        case Step.fourth_part_sensor_measure_and_endpost:
            print( Step.fourth_part_sensor_measure_and_endpost)
            #조도센서값을 판단
            light_value = sensor.get_light_sensor()
            #조도센서 값을 서버에 전송
            end_light = server_comm.metalWiringStart(light_value)
            if(end_light == "fail"):
                pass_or_fail1 = GuideMotorStep.fail
                pass_or_fail2 = GuideMotorStep.reset  
            else:
                if (end_light == "left"):
                    pass_or_fail2 = GuideMotorStep.badGrade
                    pass_or_fail1 = GuideMotorStep.good
                elif (end_light == "right"):
                    pass_or_fail2 = GuideMotorStep.goodGrade
                    pass_or_fail1 = GuideMotorStep.good
            svmotor_1.doGuidemotor(pass_or_fail1)
            svmotor_2.doGuidemotor(pass_or_fail2)   
            currnet_step = Step.go_rail_next_1

        case Step.go_rail_next_1:
            print( Step.go_rail_next_1 )
            motor.doConveyor()        
            currnet_step = Step.end_time

        case Step.end_time:
            print (Step.end_time)
            server_reply = server_comm.notifyProcessEnd()
            if server_reply == "ok":
                print("Process completed successfully.")
                motor.stopConveyor()
                current_step = Step.end
            else:
                print("Error:Process completion confirmation failed.")
                running = False
            
