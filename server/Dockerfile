FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt-get update && apt-get install -y libgl1-mesa-glx
# Install Tesseract
RUN apt-get update && apt-get install -y tesseract-ocr
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
# Set the PATH environment variable to include Tesseract
ENV PATH="/usr/bin/tesseract:${PATH}"
CMD ["uvicorn", "app.main:app","--reload", "--host", "0.0.0.0", "--port", "8000"]