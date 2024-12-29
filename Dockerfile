FROM python:3.10-slim
WORKDIR /app
EXPOSE 5002
COPY . .
RUN apt-get update && apt-get install -y --no-install-recommends \
    dos2unix curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip && pip install -r requirements.txt
RUN chmod +x bin/install.sh bin/menu.sh bin/launch.sh bin/launch_app.sh
RUN mkdir -p /app/data
ENTRYPOINT ["bash", "bin/menu.sh"]