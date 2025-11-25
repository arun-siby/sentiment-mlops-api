# 1. Start with a lightweight Python image
FROM python:3.9-slim

# 2. Set the folder inside the container
WORKDIR /app

# 3. Copy the requirements file into the container
COPY requirements.txt .

# 4. Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your code into the container
COPY . .

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. The command to run your app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]