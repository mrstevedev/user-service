# Dockerize your application:
# Create a Dockerfile: Define the necessary environment, dependencies, and the command to run your application within the container. 

# Build image
# docker build -t user-service .

# Run container:
# docker run -p 5000:5000 user-service

FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential

# Install production dependencies.
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python3", "app.py"]