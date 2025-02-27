import csv
import time

# CSV 파일 경로 (사용자 환경에 맞게 변경 필요)
csv_file_path = "C:\\path\\to\\your\\csvfile.csv"

# 시뮬레이션 데이터를 저장할 리스트
simulation_data = []


def load_csv_data(file_path):
    """
    CSV 파일을 로드하여 각 행의 데이터를 딕셔너리 리스트로 변환
    """
    data = []
    try:
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # 각 행에서 각 속도 데이터를 가져와서 리스트로 변환
                    angular_velocity = [
                        float(row.get("Angular Velocity X", 0.0)),
                        float(row.get("Angular Velocity Y", 0.0)),
                        float(row.get("Angular Velocity Z", 0.0))
                    ]
                    linear_velocity = [
                        float(row.get("Linear Velocity X", 0.0)),
                        float(row.get("Linear Velocity Y", 0.0)),
                        float(row.get("Linear Velocity Z", 0.0))
                    ]
                    
                    # 변환된 데이터를 리스트에 추가
                    data.append({
                        "angular_velocity": angular_velocity,
                        "linear_velocity": linear_velocity
                    })
                except ValueError as e:
                    print(f"Error parsing row {row}: {e}")
        print("CSV file loaded successfully!")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
    return data


def downsample_data(data, target_fps, source_fps):
    """
    원본 FPS에서 타겟 FPS로 다운샘플링 (프레임 수 줄이기)
    """
    step = int(source_fps / target_fps)  # 몇 프레임마다 하나를 선택할지 결정
    return data[::step]  # 지정한 간격으로 데이터를 샘플링하여 반환


# CSV 데이터 로드
simulation_data = load_csv_data(csv_file_path)

# 원본 및 타겟 프레임 레이트 설정
source_fps = 93.3  # 원본 데이터의 FPS
target_fps = 93.3  # 목표 FPS

# 데이터 다운샘플링 (현재 FPS가 같으므로 변경 없음)
simulation_data = downsample_data(simulation_data, target_fps, source_fps)

# 프레임 지속 시간 계산
target_frame_duration = 1.0 / target_fps  # 각 프레임의 시간 간격
last_update_time = time.time()  # 마지막 업데이트 시간 기록

frame = 0  # 현재 프레임 인덱스
is_playing = True  # 시뮬레이션 실행 여부


def compute(db):
    """
    프레임마다 실행되는 함수. 시뮬레이션 데이터를 기반으로 출력값을 갱신.
    """
    global frame, simulation_data, last_update_time, is_playing

    # 시뮬레이션이 정지된 경우 종료
    if not is_playing:
        print("Playback stopped.")
        return

    # 현재 시간이 마지막 업데이트 시간보다 프레임 간격보다 적다면 대기
    current_time = time.time()
    if current_time - last_update_time < target_frame_duration:
        return  # 아직 프레임을 갱신할 시간이 되지 않음

    # 모든 데이터를 재생한 경우 종료
    if frame >= len(simulation_data):
        print("End of simulation data. Stopping playback.")
        db.outputs.angularVelocity = (0.0, 0.0, 0.0)  # 정지 상태로 설정
        db.outputs.linearVelocity = (0.0, 0.0, 0.0)
        is_playing = False  # 재생 중지
        return

    # 현재 프레임의 데이터 가져오기
    data = simulation_data[frame]
    angular_velocity = data["angular_velocity"]
    linear_velocity = data["linear_velocity"]

    # 출력 값 업데이트
    db.outputs.angularVelocity = tuple(angular_velocity)
    db.outputs.linearVelocity = tuple(linear_velocity)

    # 10프레임마다 로그 출력
    if frame % 10 == 0:
        print(f"Frame {frame}: Angular Velocity = {angular_velocity}, Linear Velocity = {linear_velocity}")

    # 다음 프레임으로 이동
    frame += 1
    last_update_time = current_time