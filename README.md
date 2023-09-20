# questions-answering-system

System that streamlines the handling of textual questions, developed as part of master thesis.The system
allows for the addition of images, recognition of questions from those images, and generating answers to
them. Tesseract OCR is used for text recognition. ChatGPT is used via an OpenAI API to extract questions
from text and generate answers to them. It is also used to improve the quality of the text obtained from the
image. Additional image processing with OpenCV is used to improve results. Celery task queue is used to
enable concurrent processing of multiple images. The mobile application is implemented using React
Native, and the server is implemented using FastAPI. The data in the system is stored in the MongoDB
database. The system is containerized using Docker.
 
MobileApp folder contains mobile application which has been made for and tested on Android devices. It has not been tested on IOS devices.
Server folder contains whole backend logic like API calls, database updates and task queue. docker-compose.yml file in this folder contains system configuration.

## System

![image](https://github.com/ikozul00/questions-answering-system/assets/73161194/d72df761-83b3-4d1d-b1f7-52ea2c3e9497)

## Mobile app
Setting up environment: https://reactnative.dev/docs/environment-setup (follow directions for Android)

Starting an app: yarn android

### Screens
Home screen | Screen which displays uploaded image
------------ | ----------------------------------
![image](https://github.com/ikozul00/questions-answering-system/assets/73161194/2d30febb-9b00-4a6d-97cb-a9c3944e6692) | ![image](https://github.com/ikozul00/questions-answering-system/assets/73161194/e0878ff6-22dd-4d29-a8b6-1443818178bf)

List of images | Results for an image
------------ | ----------------------------------
![image](https://github.com/ikozul00/questions-answering-system/assets/73161194/fc39a564-f6a3-4a1d-b907-b4ab2c820295) | ![image](https://github.com/ikozul00/questions-answering-system/assets/73161194/4f2f3077-85a2-41aa-937b-6e91dc7e4e1b)


## Backend
To run rest of the system:
- position in server folder
- run: **docker-compose up**





