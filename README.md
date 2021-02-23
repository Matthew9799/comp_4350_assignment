# 4350 Assignment
An application for retrieving top posts and answers from stackoverflow based on keywords.

Application is offered as a docker image, to retrieve run 
```shellscript
docker pull mattlew42/flask:stack_overflow_api
```
To run the image then execute 
```shellscript
docker run -d -p 8080:8080 mattlew42/flask:stack_overflow_api
```
