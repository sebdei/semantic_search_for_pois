# cannot install py_stringmatching in 3.7 with pip https://github.com/anhaidgroup/py_stringmatching/issues/53
FROM python:3.6

WORKDIR /recommender

COPY ./ /recommender

# first need to install numpy because of scikit-surprise
# https://github.com/NicolasHug/Surprise/issues/187
RUN pip install numpy==1.16.0
RUN pip install -r requirements.txt

CMD python3 main.py