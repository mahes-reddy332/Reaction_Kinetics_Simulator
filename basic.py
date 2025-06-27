import streamlit as st
import numpy as np
from scipy.integrate import odeint
import plotly.graph_objs as go
from PIL import Image

# Page setup
st.set_page_config(page_title="🧼 Saponification Reaction Explorer", layout="wide")

# Custom CSS Styling
st.markdown("""
    <style>
    .main {
        background-color: #f6f9fc;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h2, h3 {
        color: #2c3e50;
    }
    .metric-label, .metric-value {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.image("https://img.icons8.com/ios-filled/100/chemical-plant.png", width=100)
st.sidebar.title("🔬 Navigation")
tab_choice = st.sidebar.radio("Choose a section:", ["📘 Overview", "📐 Theory", "🧪 Simulation", "📚 References"])

R = 8.314  # gas constant

# ------------------------------
if tab_choice == "📘 Overview":
    st.title("📘 Saponification Reaction Overview")
    st.info("Saponification is a chemical reaction involving ethyl acetate and sodium hydroxide (NaOH).")

    st.markdown("""
    #### Products Formed:
    - Sodium acetate (CH₃COONa)
    - Ethanol (C₂H₅OH)
    """)

    st.markdown("#### 🧪 Reaction: Triglyceride + NaOH → Glycerol + Soap")
    st.image("http://www.chem.latech.edu/~deddy/chem122m/SOAP01.gif", caption="Saponification Mechanism", use_column_width=True)

    st.success("This app simulates how reaction parameters like temperature and concentration affect NaOH levels over time.")

# ------------------------------
elif tab_choice == "📐 Theory":
    st.title("📐 Reaction Kinetics & Arrhenius Law")
    st.markdown("""
    The saponification reaction is modeled as a second-order irreversible reaction:
    """)
    st.latex(r"-\frac{dC}{dt} = kC^2")

    st.image("Integrated.png", caption="Integrated Second-Order Rate Law", use_column_width=True)

    st.markdown("### 🔬 Arrhenius Equation")
    st.latex(r"k = A \cdot e^{-E_a / RT}")

    st.image("arrhenius.png", caption="Activation Energy and Rate Dependence", use_column_width=True)

    st.markdown("""
    **Where:**
    - \( A \): Frequency factor (1/s)  
    - \( E_a \): Activation energy (J/mol)  
    - \( R \): 8.314 J/mol·K  
    - \( T \): Temperature (K)
    """)

# ------------------------------
elif tab_choice == "🧪 Simulation":
    st.title("🧪 Run the Reaction Simulation")
    st.markdown("""
    Use the controls to explore how parameters affect [NaOH] over time.
    """)

    with st.sidebar:
        st.subheader("🎛️ Simulation Settings")
        parameter = st.selectbox("Parameter to Analyze", ["Temperature", "Volume", "Agitation Rate", "Initial Concentration"])
        with st.expander("⚙️ Advanced Settings"):
            A_input = st.number_input("Frequency Factor A (1/s)", value=0.5)
            Ea_input = st.number_input("Activation Energy Ea (J/mol)", value=43094.0)
            T_sim = st.number_input("Temperature (K)", value=298.0)

    k_sim = A_input * np.exp(-Ea_input / (R * T_sim))
    st.metric("Calculated Rate Constant (k)", f"{k_sim:.2e} L/mol·s")

    if k_sim > 1:
        st.warning("⚠️ High rate constant: NaOH concentration may drop rapidly.")

    data_sets = {
        "Temperature": {
            "293K": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0333, 0.0233, 0.0178, 0.0156, 0.0144, 0.0125]),
            "303K": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0256, 0.0189, 0.0144, 0.0122, 0.0100, 0.0078]),
            "313K": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0200, 0.0133, 0.0100, 0.0083, 0.0067, 0.0061])
        },
        "Volume": {
            "1.2L": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0222, 0.0156, 0.0128, 0.0100, 0.0089, 0.0083]),
            "1.4L": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0289, 0.0222, 0.0178, 0.0156, 0.0144, 0.0133]),
            "1.8L": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.067, 0.0289, 0.0256, 0.0222, 0.0200, 0.0167])
        },
        "Agitation Rate": {
            "70rpm": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0189, 0.0133, 0.0100, 0.0078, 0.0067, 0.0056]),
            "110rpm": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0256, 0.0189, 0.0156, 0.0128, 0.0111, 0.0100]),
            "150rpm": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0333, 0.0267, 0.0222, 0.0200, 0.0178, 0.0156])
        },
        "Initial Concentration": {
            "0.025M": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0360, 0.0260, 0.0200, 0.0160, 0.0120, 0.0111]),
            "0.050M": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0389, 0.0300, 0.0244, 0.0211, 0.0189, 0.0167]),
            "0.075M": ([0, 480, 960, 1440, 1920, 2400, 2880], [0.0500, 0.0392, 0.0313, 0.0256, 0.0222, 0.0200, 0.0178])
        }
    }

    fig = go.Figure()
    exp_colors = ['red', 'green', 'blue']
    sim_colors = ['orange', 'lime', 'deepskyblue']

    for i, (label, (time_exp, conc_exp)) in enumerate(data_sets[parameter].items()):
        time_exp_min = np.array(time_exp) / 60
        conc_exp = np.array(conc_exp)

        fig.add_trace(go.Scatter(x=time_exp_min, y=conc_exp, mode='lines+markers', name=f"Exp {label}",
                                 line=dict(color=exp_colors[i], width=2)))

        def ode_model(C, t, k): return -k * C**2
        C0 = conc_exp[0]
        time_sim_sec = np.array(time_exp)

        try:
            temp_val = int(label.replace("K", ""))
            k_temp = A_input * np.exp(-Ea_input / (R * temp_val))
        except:
            k_temp = k_sim

        conc_sim = odeint(ode_model, C0, time_sim_sec, args=(k_temp,))
        time_sim_min = time_sim_sec / 60

        fig.add_trace(go.Scatter(x=time_sim_min, y=conc_sim.flatten(), mode='lines+markers',
                                 name=f"Sim {label}", line=dict(color=sim_colors[i], width=2, dash='dash')))

    fig.update_layout(
        title=f"[NaOH] vs Time — Effect of {parameter}",
        xaxis_title="Time (minutes)",
        yaxis_title="[NaOH] (mol/L)",
        template="plotly_white",
        hovermode="x unified",
        font=dict(size=14)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.success("✅ Graph plotted. Hover to inspect experimental and simulated data.")

# ------------------------------
elif tab_choice == "📚 References":
    st.title("📚 References")
    st.markdown("""
    - Al Mesfer, M. K. (2017). *Experimental Study of Batch Reactor Performance for Ethyl Acetate Saponification*, Int. J. of Chem Reactor Eng. [DOI](https://doi.org/10.1515/ijcre-2016-0174)
    - Fogler, H. S. (2006). *Elements of Chemical Reaction Engineering*.
    - Bursali, N., Ertunc, S., & Akay, B. (2006). *Chem. Eng. Process*, 45, 980–989.
    """)

st.markdown("""
---
<div style='text-align: center; font-size: 14px; color: grey;'>
    Made with ❤ by <b>Akshad Gajapure</b> & <b>Mahesh Reddy</b> | NIT Raipur
</div>
""", unsafe_allow_html=True)
 