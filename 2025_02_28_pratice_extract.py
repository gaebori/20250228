import csv
import os

# CSV 파일 경로 (사용자 환경에 맞게 변경 필요) 
#예시: csv_file_path = "C:\\Users\\jgh\\Desktop\\omniverse\\driving\\driving_data_velocity.csv"
csv_file_path = "C:\\path\\to\\your\\csvfile.csv"

# 폴더가 없으면 생성
if not os.path.exists(os.path.dirname(csv_file_path)):
    os.makedirs(os.path.dirname(csv_file_path))  # 지정된 경로의 폴더를 생성

def compute(db):
    # 입력 문자열 데이터 가져오기
    input_string = db.inputs.stringData
    if not input_string:
        print("Debug: No data received in stringData")  # 데이터가 없을 경우 경고 출력
        return

    # 수신된 데이터 출력
    print(f"Debug: Received data: {input_string}")

    # 입력 문자열에서 Angular Velocity와 Linear Velocity 추출
    try:
        # 문자열을 파싱하여 Angular Velocity 부분 추출
        angular_velocity_part = input_string.split("Angular Velocity : ")[1].split("  Linear Velocity : ")[0]
        # Linear Velocity 부분 추출
        linear_velocity_part = input_string.split("Linear Velocity : ")[1]

        # 문자열을 리스트 형태로 변환
        angular_velocity = eval(angular_velocity_part)
        linear_velocity = eval(linear_velocity_part)

        # CSV 파일이 존재하지 않으면 헤더 작성
        if not os.path.exists(csv_file_path):
            print(f"Debug: File does not exist. Creating new file at {csv_file_path}")
            with open(csv_file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                # CSV 헤더 작성
                writer.writerow(["Angular Velocity X", "Angular Velocity Y", "Angular Velocity Z",
                                 "Linear Velocity X", "Linear Velocity Y", "Linear Velocity Z"])  # 헤더 추가

        # 데이터 저장
        with open(csv_file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            # Angular Velocity와 Linear Velocity 값을 CSV 파일에 추가
            writer.writerow([angular_velocity[0], angular_velocity[1], angular_velocity[2],
                             linear_velocity[0], linear_velocity[1], linear_velocity[2]])  # 데이터 추가
            print(f"Debug: Data written to file: {angular_velocity}, {linear_velocity}")  # 저장된 데이터 출력

    except Exception as e:
        print(f"Error: {e}")  # 오류 발생 시 오류 메시지 출력
