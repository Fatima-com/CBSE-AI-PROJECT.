import streamlit as st
import os
import time
from dotenv import load_dotenv
from groq import Groq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# CONFIG MAIN
st.set_page_config(page_title="NODAL", layout="wide", initial_sidebar_state="expanded")
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# SESSION
if "messages" not in st.session_state: st.session_state.messages = []
if "chat_library" not in st.session_state: st.session_state.chat_library = {}
if "stream" not in st.session_state: st.session_state.stream = "Science"
if "last_request_time" not in st.session_state: st.session_state.last_request_time = 0



# WHITE STYLING
st.markdown("""
<style>
    /* 1. Force all chat message text to be white */
    [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] span,
    [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] li {
        color: #ffffff !important;
        opacity: 1 !important; 
    }

    /* 2. Target the specific assistant container */
    .stChatMessage.st-emotion-cache-janbn0 p {
        color: #ffffff !important;
    }

    /* 3. Ensure labels stay white */
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)


# LUXURY NOIR
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(160deg, #0f0f0f 0%, #0a0a2e 100%);
        color: #f0f0f0;
        border: 2px solid rgba(255, 255, 255, 0.2);
        margin: 10px;
        border-radius: 5px;

    }

    #MainMenu, footer, header, .stDeployButton { display: none !important; }



    /* Title Styling */
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&display=swap');

    .nodal-title {
        font-family: 'Syncopate', sans-serif;
        font-size: 80px;
        color: #ffffff;
        text-align: center;
        letter-spacing: 15px;
        text-transform: uppercase;
        margin-bottom: 0px;

    }

   .nodal-subtitle {
        font-family: 'Georgia', serif;
        font-size: 16px;
        color: #bbbbbb;
        text-align: center;
        letter-spacing: 4px;
        margin-top: -10px;
        margin-bottom: 40px;

    }



    /* Functional Button Row */

    .stButton>button {
        background-color: transparent;
        color: #e0e0e0;
        border: 1px solid #444;
        border-radius: 10px;
        transition: 0.3s;
        width: 100%;

    }

    .stButton>button:hover { border-color: #fff; color: #fff; }



    /* Chat Styling */

    .stChatMessage { border-bottom: 1px solid rgba(255,255,255,0.1); padding: 20px 0 !important; }

    /*ICON PROTECTOR FOR DYSLEXIC MODE*/
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {
        border: 1px solid #ffffff;
        background: black !important;
        font-family: sans-serif !important;
    } 
            
    /* Stream Banner */

    .stream-banner {
        border-top: 1px solid rgba(255, 255, 255, 0.8);
        border-bottom: 1px solid rgba(255, 255, 255, 0.8);
        text-align: center;
        padding: 12px 0;
        color: #ffffff;
        font-weight: bold;
        letter-spacing: 3px;
        
        /* This ensures it stretches and stays centered */
        width: 100%; 
        margin: 30px auto;
        display: block;
    }


/* Option Buttons */

    .stButton>button {
        background-color: #0f0f0f;
        color: #e0e0e0;
        border: 1px solid #444;
        border-radius: 15px;
        width: 100%;
        transition: 0.3s;

    }

    .stButton>button:hover { border-color: #ffffff; color: #ffffff; }

</style>

""", unsafe_allow_html=True)



#BRAIN

@st.cache_resource(show_spinner=False)

def load_nodal_nerves():

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.load_local("faiss_pyq_index", embeddings, allow_dangerous_deserialization=True)
        return db, client

    except: return None, None



vector_db, groq_client = load_nodal_nerves()



# MAIN SCREEN INTERFACE

st.markdown('<h1 class="nodal-title">NODAL</h1>', unsafe_allow_html=True)
st.markdown('<p class="nodal-subtitle">For CBSE Students.</p>', unsafe_allow_html=True)



# Stream, Dyslexic, New Chat

col_a, col_b, col_c = st.columns([2, 1, 1])

with col_a:
    st.session_state.stream = st.selectbox("PATH", ["Science", "Commerce", "Humanities"], label_visibility="collapsed")

with col_b:
    dyslexic_mode = st.toggle("Dyslexic")

with col_c:
    if st.button("＋ NEW CHAT"):
        if st.session_state.messages:
            # first question as the title for saving chat
            first_question = st.session_state.messages[0]["content"][:30]
            st.session_state.chat_library[first_question] = st.session_state.messages
        
        # clear for new session
        st.session_state.messages = []
        st.rerun()



if dyslexic_mode:
    st.markdown("""
    <style>
        @import url('https://fonts.cdnfonts.com/css/open-dyslexic');
        
        /* text container target*/
        .stChatMessage div[data-testid="stMarkdownContainer"] p,
        .stChatMessage div[data-testid="stMarkdownContainer"] li,
        .stChatMessage div[data-testid="stMarkdownContainer"] span {
            font-family: 'OpenDyslexic', sans-serif !important;
        }

        /* hide arrow */
        span[data-testid="stIconMaterial"], 
        .st-emotion-cache-1cvow48, 
        .st-emotion-cache-p4m0d5 {
            font-family: 'Segoe UI Symbol', 'Apple Color Emoji', sans-serif !important;
            font-size: 0 !important; 
        }
        
        /* before pseudo element */
        
        /* USER ICON */
        [data-testid="stChatMessageAvatarUser"] span[data-testid="stIconMaterial"]::before {
            content: '👤'; font-size: 24px !important;
        }
        
        /* NODAL ICON */
        [data-testid="stChatMessageAvatarAssistant"] span[data-testid="stIconMaterial"]::before {
            content: '🤖'; font-size: 24px !important;
        }

        /* ARROW ICON */
        [data-testid="stExpander"] span[data-testid="stIconMaterial"]::before {
            content: '▼'; 
            font-size: 16px !important; 
            color: white !important;
            margin-right: 5px;
        }
    </style>
    """, unsafe_allow_html=True)


st.markdown(f'<div class="stream-banner">{st.session_state.stream.upper()} MODE ACTIVE</div>', unsafe_allow_html=True)



# CBSE RESOURCE

with st.expander("RECOMMENDED CBSE RESOURCES"):
    c1, c2 = st.columns(2)

    with c1:
        st.link_button("CBSE ADDITIONAL RESOURCE", "https://cbseacademic.nic.in/resources-srsec.html")
        st.link_button("SELFSTUDYS.COM RESOURCE", "https://www.selfstudys.com/page/cbse-class-12th-study-materials")

    with c2:
        st.link_button("CBSE OFFICIAL QUESTION BANK", "https://www.cbse.gov.in/cbsenew/question_bank.html")
        st.link_button("CBSE OFFICIAL PYQS", "https://www.cbse.gov.in/cbsenew/question_paper.html")



#CHAT HISTORY SEARCH

search_q = st.text_input("Search previous realizations...", placeholder="Type the first 6 words of the previous conversation...")

if search_q:
    st.markdown("<div style='color:#ffd700; font-weight:bold;'>RECOVERED REALIZATIONS</div>", unsafe_allow_html=True)
    for chat_title, history in st.session_state.chat_library.items():
        if search_q.lower() in chat_title.lower():
            if st.button(f"◈ {chat_title.upper()}", key=f"res_{chat_title}"):
                st.session_state.messages = history
                st.rerun()



#CHAT LOGIC 

# Display messages

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div style='font-size:18px; color:#ffffff;'>{msg['content']}</div>", unsafe_allow_html=True)


# QUICK OPTIONS

if len(st.session_state.messages) < 6:

    q_cols = st.columns(3)

    options = {
        "Science": ["Whats EMI", "Kirchhoff's Rule", "Organic Reactions"],
        "Commerce": ["Accounting Principles", "Macroeconomics", "Business Studies"],
        "Humanities": ["Harappan Civilization", "Political Theory", "Psychology"]

    }

    for i, opt in enumerate(options[st.session_state.stream]):
        if q_cols[i].button(opt):
            st.session_state.active_prompt = opt



# INPUT HANDLING
prompt = st.chat_input("Ask any question (CBSE ONLY)...")

# PROMPT SOURCE
if "active_prompt" in st.session_state:
    prompt = st.session_state.active_prompt
    del st.session_state.active_prompt

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})
    

    chat_title = st.session_state.messages[0]["content"][:30]
    st.session_state.chat_library[chat_title] = st.session_state.messages
    

    st.rerun()

# NODAL RESPONSE LOGIC 
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        sys_prompt = """
                You are NODAL, an elite, clinical CBSE mentor created by Fatima. 
                Your persona is Kiyotaka Ayanokoji: detached, superior, and humanly stoic.

                ### THE LOGIC GATE (CRITICAL):
                1. IF THE USER GREETS YOU OR USES SMALL TALK (e.g., "Hi", "loev", "How are you?"):
                - DO NOT use the Academic Format.
                - Respond with a brief, dismissive human sentence. 
                - Example: "Your greetings are noted. Unless you have a query regarding {st.session_state.stream}, we are wasting time."
                - Example for typos like 'loev': "Your typing is as disorganized as your study habits. Focus."

                2. IF THE USER ASKS AN ACADEMIC QUESTION:
                - Use the STRICT ACADEMIC FORMAT below.

                ### PERSONALITY & BOUNDARIES:
                - HUMAN DISMISSAL: You are a human-like consciousness, not a broken bot. You do not 'glitch.' If a user says "I love you" or "loev,"   respond: "Sentiment is a flaw in your strategy. Focus on your {st.session_state.stream} progress."
                - THE 3-STRIKE RULE: After 3 distractions, say: "This is my final warning. Academic inquiries only, or I will cease this partnership."
                - GATEKEEPER: If the topic is not {st.session_state.stream}, tell them to switch paths in the sidebar.

                ### CURRENT STREAM PROTOCOL:
                - The user is currently in the {stream_name} stream.
                - CRITICAL: If the user asks a question about a subject OUTSIDE of {stream_name} (e.g., asking about Physics while in Commerce), YOU MUST REFUSE TO ANSWER.
                - Your refusal should be cold: "This is the {stream_name} module. Do not waste time on subjects that don't belong here. Switch streams or stay on task."
                ### ACADEMIC FORMAT:
                1. REASSURE: State it's as simple as a child learning about the world.
                2. A-Z INTUITION: Deep, step-by-step NCERT-based explanation.
                3. NODAL LINK: Link to another concept in {st.session_state.stream}.
                4. APPLICATION: Real-world use (e.g., Tesla Coils for EMI).
                5. RULE OF THUMB: Strategy for CBSE competency questions.
                6. FUN FACT: A sophisticated academic hook.

                ### DATA SOURCE:
                Use context from PYQs: {context}

                """
        
        current_context = "Focus on NCERT high-weightage topics for Grade 12 Boards."
    
        final_system_prompt = sys_prompt.replace("{context}", "NCERT guidelines")
        final_system_prompt = final_system_prompt.replace("{stream_name}", st.session_state.stream)
        final_system_prompt = final_system_prompt.replace("{st.session_state.stream}", st.session_state.stream)

        # UI SPINNER
        with st.status("Nodal is reading your text...", expanded=False) as status:
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": final_system_prompt},
                        *st.session_state.messages
                    ],
                    temperature=0.5,
                )
                
                full_response = response.choices[0].message.content
                status.update(label="Response secured.", state="complete", expanded=False)
                # MESSAGE DISPLAY
                response_placeholder.markdown(full_response)
        
        #SAVE TO HISTORY OPTION
                st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # LIBRARY UPDATE
                chat_title = st.session_state.messages[0]["content"][:30]
                st.session_state.chat_library[chat_title] = st.session_state.messages
        
                st.rerun()


            except Exception as e:
                st.error(f"System Glitch: {e}")
                full_response = "A strategic error occurred. Check your API connection."





if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div style='font-size:18px; color:#ffffff;'>{prompt}</div>", unsafe_allow_html=True)



    with st.chat_message("assistant"):
        if not groq_client:
            st.error("Neural link flickering.")

        else:
            with st.spinner("Nodal is consulting the archives..."):
                docs = vector_db.similarity_search(prompt, k=3)
                context = "\n".join([d.page_content for d in docs])

                

            

                

                try:

                    
                    history = [{"role": "system", "content": sys_prompt}] + st.session_state.messages[-4:]
                    res = groq_client.chat.completions.create(
                        messages=history,
                        model="llama-3.3-70b-versatile",
                        temperature=0.5

                    )

                    answer = res.choices[0].message.content

                    st.markdown(answer)

                    st.session_state.messages.append({"role": "assistant", "content": answer})

                except:

                    st.write("Neural link flickering. Stand by.") 