from sqlalchemy import create_engine
import os, json
import pandas as pd

path = "./Brand_name.txt"
with open(path, 'r') as f:
    car_num = json.loads(f.read())

