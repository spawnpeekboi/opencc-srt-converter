FROM python:3.9-slim
WORKDIR /app
RUN pip install opencc-python-reimplemented crc64iso
COPY convert_srt.py .
CMD ["python", "convert_srt.py"]

