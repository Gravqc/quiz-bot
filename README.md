# Quiz bot

This is a basic version of an interactive quiz bot that engages users in quizzes, evaluates their responses, and provides a final score based on their answers. In this we use Django channels websocket communication, redis as message broker, and Django sessions for temporary data storage.

Steps to run the project with Docker

1. Install Docker and Docker Compose (https://docs.docker.com/compose/install/)
2. Docker should be running
3. In the project root run `docker-compose build` and `docker-compose up`
4. Go to `localhost` to view the chatbot

Steps to run the project without Docker

1. Install required packages by running `pip install -r requirements.txt`
2. Install and run postgresql, and change the `DATABASES` config in `settings.py`, if required.
3. Install and run redis, and update the `CHANNEL_LAYERS` config in `settings.py`, if required.
4. In the project root run `python manage.py runserver`
5. Go to `127.0.0.1:8000` to view the chatbot

#Things to note:
i ran the project using docker and faced few challenges

- the .sh file either was not found in the /app/ or if it was present it could not be run
- both things can be overcome by:
- change entrypoint entrypoint: ["sh", "/app/run_server.sh"] in the docker compose file
- dos2unix run_server.sh; run this to make sure .sh script has the correct line ending
- chmod +x run_server.sh; to make sure .sh file has executable permissions
