FROM python:3

COPY . .

RUN python3 -m pip install discord.py python-dotenv
CMD python -u main.py