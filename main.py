import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import time

st.title('My first app')

st.write('Interactive Widgets')
'start!!'

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i+1)
    time.sleep(0.1)

'Done!!'



left_column, right_column = st.columns(2)
button = left_column.button('Press me')
if button:
    right_column.write('Wow!')

expander = st.expander('FAQ1')
expander.write('1 Here you could put in some really, really long explanations...')
expander = st.expander('FAQ2')
expander.write('2 Here you could put in some really, really long explanations...')
expander = st.expander('FAQ3')
expander.write('3 Here you could put in some really, really long explanations...')

# text = st.text_input('Tell me Your hobby',)
# condition = st.slider('How is your condition?', 0, 100, 50)

# 'Your hobby is ', text
# 'Your condition is ', condition


# if st.checkbox('Display image'):
#     img = Image.open('image.jpg')
#     st.image(img, caption='Sunset', use_column_width=True)
