import streamlit as st

def is_load_complete():
    return st.experimental_user.to_dict() != {}

def write_center_txt(text="default", type="h1"):
    st.markdown(f"<{type} style='text-align: center; color: white;'>{text}</{type}>", 
                unsafe_allow_html=True)
    

write_center_txt(text="MINDPIXELS")
write_center_txt(text="Generate moving images with your MIND!", type="h3")

if not is_load_complete():
    print("Not done yet!")
else:
    print("DONE")
    st.write("Done")


    