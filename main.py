import streamlit as st
import requests

def set_is_queued(value: bool):
    st.session_state["is_queued"] = value

def disable_check(value: bool = True):
    st.session_state["disable_check"] = value

def set_id(id: int):
    st.session_state["id"] = id

uploaded_file = st.file_uploader("uploadfile",label_visibility="hidden", 
                                 disabled=st.session_state.get("is_queued", False), 
                                 type=["pdf"])
st.write(" ")
st.write(" ")
st.write("**Select no. of copies**")
# slider = st.slider(label="number of copies", min_value=1, max_value=10, 
# label_visibility="collapsed")
nCopies = st.number_input('number of copies',max_value=10, min_value=1, step=1,
                          label_visibility="collapsed")
st.write(" ")
st.write("**Double side or single side print**")
print_double_side = st.checkbox(label="print double side")
is_colour_print = st.checkbox(label="colour print")

st.write(" ")
st.write(" ")
# submit = st.button(label="submit", disabled=st.session_state.get('is_queued', False))
submit = st.button(label="submit")

url = "http://localhost:8000/uploadfile/"

if uploaded_file is None and submit is True and st.session_state.get("is_queued", False) is False:
    st.warning("**Choose a file first!!**")

if(uploaded_file is not None and submit is True and 
                    st.session_state.get("is_queued",False) is False):
    st.write(f"uploading {uploaded_file.name}")
    file = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    payload = {
        "no_of_copies": nCopies,
        "is_double_side": print_double_side,
        "is_colour_print": is_colour_print,
        "page_count": -1,
    }
    
    res = requests.post(url, data=payload, files=file)
    content = res.json()
    # st.write(f"res = {res}")

    id = content["info"]["id"]

    st.write(f"your id is {id}")
    set_id(content["info"]["id"])
    st.write("Done uploading")
    set_is_queued(True)
    disable_check(False)

if st.session_state.get("is_queued", False) is True and submit is True:
    st.write("Already a file uploaded plz wait untill it is completed")

check_status_button = submit = st.button(label="Check Status", 
                                disabled = st.session_state.get("disable_check", True))

if check_status_button:
    payload = {
        "id" : st.session_state.get("id")
    }
    status_url = f"http://localhost:8000/status/?file_id={st.session_state['id']}"
    res = requests.get(status_url)
    content = res.json()
    st.write(f"In queue at position {content['position']}")
