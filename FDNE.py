import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image # import images


# Make some shortcuts
zeros = np.zeros
pi = np.pi
inverse = np.linalg.inv


Ns=501; # Number of frequency samples
Nc=2; # Size of Y (after reduction)
bigY=zeros((Nc,Nc,Ns), dtype=complex)
Y=zeros((4,4), dtype=complex);

f=np.logspace(1,5,Ns)
s=2*pi*1j*f;
s = [ f[i]*2*pi*1j for i in range(0, Ns)]


# Component values
R1=1; L1=1e-3; C1=1e-6;
R2=5; L2=5e-3;
R3=1; C3=1e-6;
L4=1e-3;
R4=1e-2; L5=20e-3;
R6=10; C6=10e-6;
R7=1; C7=2e-6;

for k in range(0,Ns):
    sk=s[k];
    y1=1/( R1+sk*L1+1/(sk*C1) );
    y2=1/( R2+sk*L2 );
    y3=1/( R3+1/(sk*C3));
    y4=1/( R4+sk*L4);
    y5=1/( sk*L5 );
    y6=1/( R6+1/(sk*C6) );
    y7=1/( R7+1/(sk*C7) );
    
    Y[0,0]= y1+y3;
    Y[1,1]= y4;
    Y[2,2]= y3 +y4 +y5 +y6;
    Y[3,3]= y1 +y2 +y6 +y7;
    
    Y[0,2]=-y3; Y[0,3]= -y1;
    Y[1,2]=-y4;
    Y[2,0]=-y3; Y[2,1]= -y4; Y[2,3]= -y6;
    Y[3,0]=-y1; Y[3,2]= -y6;
    
    # Eliminating nodes 3 and 4
    dum1=np.dot(inverse(Y[2:4,2:4]),Y[2:4,0:2])
    dum2=np.dot(Y[0:2,2:4],dum1)
    Yred= Y[0:2,0:2] - dum2
    bigY[:,:,k]=Yred



source = pd.DataFrame({
  #'f': f,
  'Y11': np.absolute(bigY[0, 0, :]),
  'Y12': np.absolute(bigY[0, 1, :]),
  'Y22': np.absolute(bigY[1, 1, :]),
    "index": f
})

source['Y33'] = np.absolute(bigY[0, 0, :])



df = px.data.gapminder()
fig = px.line(source, x="index", y=["Y11", "Y12", "Y22"],
              labels={"index": "Frequency (Hz)",
                     "value": "Admittance [S]",
                     "variable": "Matrix Element"},
              log_x=True, log_y=True)
st.plotly_chart(fig, use_container_width=False)



st.markdown('[ref] User manual - Matrix Fitting Toolbox for rational modeling from Y-parameter and'
            'S-parameter data')

#fig = alt.Chart(source).mark_line().encode(
#    x=alt.X('index', scale=alt.Scale(type="log")),
#    y=alt.Y('Y12', scale=alt.Scale(type="log"))
#)
#st.altair_chart(fig)

