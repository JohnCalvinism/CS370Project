Setup Virtual Environment

Linux

source venv/bin/activate

pip freeze > requirements.txt

pip install -r requirements.txt

python3

Windows

python -m venv .venv

pip install -r requirements.txt

python

For Server 

python main/server/server.py

For Pi

python3 main/camera/motion.py
