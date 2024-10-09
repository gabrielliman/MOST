To install requirements:
pip install requirements.txt
To compile C++:
python setup.py build_ext --inplace
To run code:
python main.py
To acess online interface:
http://127.0.0.1:5000


docker build -t most_challenge . --debug
docker run -p 5000:5000 most_challenge
