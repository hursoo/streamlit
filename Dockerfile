# 1. 베이스 이미지로 파이썬 3.11 버전을 지정합니다.
FROM python:3.11-slim

# 2. 컨테이너 안에서 작업할 디렉토리를 설정합니다.
WORKDIR /app

# 3. 시스템 도구 설치를 위해 packages.txt 파일을 복사하고 실행합니다.
COPY packages.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends $(cat packages.txt) && rm -rf /var/lib/apt/lists/*

# 4. 파이썬 라이브러리 설치를 위해 requirements.txt 파일을 복사합니다.
COPY requirements.txt ./

# 5. requirements.txt에 명시된 라이브러리들을 설치합니다.
RUN pip install --no-cache-dir -r requirements.txt

# 6. 나머지 모든 앱 소스 코드를 복사합니다.
COPY . .

# 7. Streamlit이 사용할 포트(8501)를 외부에 노출시킵니다.
EXPOSE 8501

# 8. 앱을 실행할 기본 명령어를 설정합니다.
CMD ["streamlit", "run", "streamlit_app.py"]