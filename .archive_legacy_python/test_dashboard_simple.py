#!/usr/bin/env python3
"""
test_dashboard_simple.py - Simple test to verify Streamlit interactivity
"""
import streamlit as st

st.set_page_config(
    page_title="RICK Test Dashboard",
    layout="wide"
)

st.title("🚀 RICK Dashboard - Interactivity Test")

# Test session state
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Test tabs
tab1, tab2, tab3 = st.tabs(["✅ Tab 1", "✅ Tab 2", "✅ Tab 3"])

with tab1:
    st.header("Tab 1 - Buttons Test")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Click Me! 🎯", key="btn1"):
            st.session_state.counter += 1
            st.success(f"Button clicked {st.session_state.counter} times!")
    
    with col2:
        if st.button("Reset Counter", key="btn2"):
            st.session_state.counter = 0
            st.info("Counter reset!")
    
    st.metric("Click Counter", st.session_state.counter)

with tab2:
    st.header("Tab 2 - Input Test")
    
    name = st.text_input("Enter your name:", key="name_input")
    
    if name:
        st.success(f"Hello, {name}! 👋")
    
    option = st.selectbox(
        "Choose an option:",
        ["Option 1", "Option 2", "Option 3"],
        key="select1"
    )
    
    st.info(f"You selected: {option}")

with tab3:
    st.header("Tab 3 - Data Test")
    
    import pandas as pd
    
    df = pd.DataFrame({
        'Name': ['RICK', 'GPT', 'GROK'],
        'Status': ['Active', 'Active', 'Idle'],
        'Score': [95, 88, 72]
    })
    
    st.dataframe(df, use_container_width=True)
    
    st.checkbox("Test Checkbox", key="check1")
    st.radio("Test Radio", ["A", "B", "C"], key="radio1")

# Footer
st.divider()
st.caption("If you can click tabs and buttons, Streamlit is working correctly! ✅")
