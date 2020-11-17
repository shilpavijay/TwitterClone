from django.shortcuts import render
from datetime import datetime

# Create your views here.
def get_cur_time(): return datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')