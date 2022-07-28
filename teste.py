import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

t = np.linspace(0, 10, 111)
y1=np.cos(t)
y2=np.sin(t)
yy = [y1, y2]

source = pd.DataFrame({
     'cosseno': y1,
     'seno': y2,
     'index': t
})


fig = px.line(source, x="index", y=['cosseno', 'seno'],
              labels={"index": "h",
                     "value": "Z [ddd]",
                     "variable": ""})

st.plotly_chart(fig, use_container_width=False)