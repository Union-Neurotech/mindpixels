import streamlit as st

def write_center_txt(text="default", type="h1"):
    st.markdown(f"<{type} style='text-align: center; color: white;'>{text}</{type}>", 
                unsafe_allow_html=True)
    

write_center_txt(text="MINDPIXELS")
write_center_txt(text="Generate moving images with your MIND!", type="h3")



    