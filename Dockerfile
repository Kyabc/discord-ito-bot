FROM python:3.12-slim
WORKDIR /app
ENV DISCORD_TOKEN="MTUyMDI1Njc3NjM5MjQwOTIzMA.G9Ea2O.UeFd77EfQngtzNmjFqP_G5GyQKlRYhV8IyJZ8Q"
ENV OWNER_ID="514366500715364352"
ENV LOG_DIR="logs"
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev
COPY . .
CMD ["uv", "run", "python", "main.py"]