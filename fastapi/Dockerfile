FROM python:3.10.6

# Pull the base docker image of python with tag 3.10.6

RUN pip install --upgrade pip
RUN pip install "python-jose[cryptography]"

WORKDIR /app
# Change the working dir inside the container - cd /app

COPY main.py requirements.txt ./
# Copy main.py as source cod and req.txt as dependency

RUN pip install -r requirements.txt
# Install the dependency

ADD base_model.py basic_func.py location.db test_main.py users.db /app/

### Container Env same as local at this point

EXPOSE 8080

CMD ["gunicorn" ,"-w", "4", "-k", "uvicorn.workers.UvicornWorker" , "--bind", "0.0.0.0:8080", "main:app"]