# app.py — Cerebro: The Knowledge Brain
import streamlit as st, time
from datetime import datetime
from chatbot import get_response

st.set_page_config(page_title="Cerebro — The Knowledge Brain", page_icon="🧠", layout="wide", initial_sidebar_state="expanded")

USERS = {
    "demo@gmail.com":    {"password": "demo123",    "name": "Demo User"},
    "student@mca.com":   {"password": "cerebro123", "name": "MCA Student"},
    "admin@cerebro.com": {"password": "admin123",   "name": "Admin"},
}

for k,v in {"logged_in":False,"user_email":"","user_name":"","dark_mode":False,"chat_history":[],"chat_sessions":[],"show_settings":False,"confidence_threshold":0.85}.items():
    if k not in st.session_state: st.session_state[k] = v

def welcome_msg():
    return {"role":"cerebro","content":f"🧠 Welcome, <b>{st.session_state.user_name}</b>! Cerebro AI is online — your genius-level assistant. Ask me anything about science, history, technology, NLP, coding, or literally anything else!","time":datetime.now().strftime("%I:%M %p"),"badge":"🧠 Cerebro"}

D = st.session_state.dark_mode
if D:
    BG="#0b0b0f";SB="#111118";CARD="#18181f";BOT_BG="#14141c";BORDER="#252535";TEXT="#f0f0f8";SUBTEXT="#8888aa";ACCENT="#00d4ff";ACCENT2="#8b5cf6";BADGE_BG="#1a1a2e";INPUT_BG="#18181f";HOVER="#1f1f2e";USER_GRAD="linear-gradient(135deg,#8b5cf6,#4f46e5)"
else:
    BG="#f4f4ff";SB="#eeeef8";CARD="#ffffff";BOT_BG="#f8f8ff";BORDER="#ddddf0";TEXT="#1a1a30";SUBTEXT="#6666aa";ACCENT="#6c3cf7";ACCENT2="#06b6d4";BADGE_BG="#ede9fe";INPUT_BG="#ffffff";HOVER="#f0f0ff";USER_GRAD="linear-gradient(135deg,#6c3cf7,#4f46e5)"

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');
*{{box-sizing:border-box;}}
html,body,[class*="css"]{{font-family:'Plus Jakarta Sans',sans-serif!important;background:{BG}!important;color:{TEXT}!important;}}
.stApp{{background:{BG}!important;}}
section[data-testid="stSidebar"]{{background:{SB}!important;border-right:1px solid {BORDER}!important;min-width:270px!important;max-width:270px!important;}}
section[data-testid="stSidebar"] *{{color:{TEXT}!important;}}
[data-testid="collapsedControl"]{{display:flex!important;visibility:visible!important;background:{SB}!important;border-right:1px solid {BORDER}!important;}}
#MainMenu,footer,header,.stDeployButton{{display:none!important;}}
.stButton>button{{background:transparent!important;border:1px solid {BORDER}!important;color:{TEXT}!important;border-radius:10px!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-size:0.8rem!important;font-weight:500!important;transition:all 0.2s!important;padding:8px 14px!important;}}
.stButton>button:hover{{border-color:{ACCENT}!important;color:{ACCENT}!important;background:{HOVER}!important;}}
.stTextInput>div>div>input{{background:{INPUT_BG}!important;color:{TEXT}!important;border:1.5px solid {BORDER}!important;border-radius:12px!important;font-size:0.92rem!important;padding:12px 16px!important;}}
.stTextInput>div>div>input:focus{{border-color:{ACCENT}!important;box-shadow:0 0 0 3px {ACCENT}22!important;}}
.stTextInput label{{color:{SUBTEXT}!important;font-size:0.82rem!important;}}
[data-testid="stChatInput"]>div{{background:transparent!important;border:none!important;border-bottom:1.5px solid {BORDER}!important;border-radius:0!important;box-shadow:none!important;}}
[data-testid="stChatInput"] textarea{{color:{TEXT}!important;background:transparent!important;caret-color:{TEXT}!important;}}
[data-testid="stChatInput"] textarea::placeholder{{color:{SUBTEXT}!important;}}
@keyframes brainPulse{{0%,100%{{filter:drop-shadow(0 0 8px {ACCENT}) drop-shadow(0 0 18px {ACCENT}55);transform:scale(1);}}50%{{filter:drop-shadow(0 0 22px {ACCENT}) drop-shadow(0 0 44px {ACCENT}77);transform:scale(1.07);}}}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(20px);}}to{{opacity:1;transform:translateY(0);}}}}
@keyframes msgIn{{from{{opacity:0;transform:translateY(8px);}}to{{opacity:1;transform:translateY(0);}}}}
@keyframes bounce{{0%,60%,100%{{transform:translateY(0);opacity:0.3;}}30%{{transform:translateY(-8px);opacity:1;}}}}
.msg-user{{background:{USER_GRAD};color:#fff!important;padding:14px 20px;border-radius:20px 20px 4px 20px;font-size:0.92rem;line-height:1.7;box-shadow:0 4px 24px rgba(109,57,247,0.2);animation:msgIn 0.25s ease;margin:4px 0 2px;}}
.msg-bot{{background:{BOT_BG};color:{TEXT}!important;padding:15px 20px;border-radius:20px 20px 20px 4px;font-size:0.92rem;line-height:1.7;border:1px solid {BORDER};box-shadow:0 2px 14px rgba(0,0,0,0.1);animation:msgIn 0.25s ease;margin:4px 0 2px;}}
.msg-meta{{font-size:0.68rem;color:{SUBTEXT};margin-top:4px;text-align:right;}}
.msg-meta-l{{font-size:0.68rem;color:{SUBTEXT};margin-top:4px;}}
.msg-badge{{display:inline-flex;align-items:center;gap:4px;background:{BADGE_BG};border:1px solid {BORDER};border-radius:20px;padding:3px 12px;font-size:0.67rem;color:{ACCENT};margin-bottom:6px;font-weight:500;}}
.dot{{width:8px;height:8px;border-radius:50%;background:{ACCENT};display:inline-block;animation:bounce 1.3s ease-in-out infinite;}}
.dot:nth-child(2){{animation-delay:.18s;}}.dot:nth-child(3){{animation-delay:.36s;}}
.sb-brand{{padding:18px 18px 14px;border-bottom:1px solid {BORDER};display:flex;align-items:center;gap:10px;}}
.sb-label{{font-size:0.67rem;color:{SUBTEXT};font-weight:700;text-transform:uppercase;letter-spacing:2px;padding:14px 18px 6px;}}
.sb-chat-item{{padding:9px 14px;border-radius:10px;font-size:0.79rem;color:{TEXT};margin:2px 8px;display:flex;align-items:flex-start;gap:8px;border:1px solid transparent;}}
.sb-stat{{background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:12px;text-align:center;}}
.sb-stat-n{{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:700;color:{ACCENT};line-height:1;}}
.sb-stat-l{{font-size:0.66rem;color:{SUBTEXT};text-transform:uppercase;letter-spacing:1px;margin-top:3px;}}
.sb-user{{border-top:1px solid {BORDER};padding:14px 18px 8px;display:flex;align-items:center;gap:10px;}}
.avatar{{width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,{ACCENT},{ACCENT2});display:flex;align-items:center;justify-content:center;font-weight:700;font-size:0.95rem;color:#fff;flex-shrink:0;}}
.settings-box{{background:{CARD};border:1px solid {BORDER};border-radius:16px;padding:24px;margin-bottom:20px;box-shadow:0 8px 32px rgba(0,0,0,0.12);}}
.cline{{height:1px;background:linear-gradient(90deg,transparent,{ACCENT}99,{ACCENT2}99,transparent);margin:20px 0;}}
</style>""", unsafe_allow_html=True)

# LOGIN
if not st.session_state.logged_in:
    st.markdown(f"""<div style='text-align:center;padding:40px 0 30px;animation:fadeUp 0.5s ease;'>
    <div style='font-size:4rem;animation:brainPulse 3s ease-in-out infinite;display:inline-block;filter:drop-shadow(0 0 20px {ACCENT});'>🧠</div>
    <div style='font-family:Syne,sans-serif;font-weight:800;font-size:2.8rem;color:{ACCENT};letter-spacing:-1px;margin-top:6px;'>CEREBRO</div>
    <div style='font-size:0.75rem;color:{SUBTEXT};letter-spacing:4px;text-transform:uppercase;margin-top:8px;'>The Knowledge Brain · NLP Project MCA Sem 2</div>
    </div>""", unsafe_allow_html=True)
    _, mid, _ = st.columns([1,1.4,1])
    with mid:
        st.markdown(f"""<div style='background:{CARD};border:1px solid {BORDER};border-radius:24px;padding:40px 38px 32px;box-shadow:0 24px 80px rgba(0,0,0,0.25);animation:fadeUp 0.5s ease;'>
        <div style='font-family:Syne,sans-serif;font-weight:800;font-size:1.5rem;color:{TEXT};margin-bottom:4px;'>Welcome back 👋</div>
        <div style='font-size:0.83rem;color:{SUBTEXT};margin-bottom:28px;'>Sign in to access your genius AI assistant</div>
        </div>""", unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("📧  Email Address", placeholder="you@email.com")
            password = st.text_input("🔒  Password", type="password", placeholder="Enter your password")
            st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
            s1,s2 = st.columns(2)
            with s1: login_btn = st.form_submit_button("🚀  Sign In", use_container_width=True)
            with s2: demo_btn = st.form_submit_button("👁️  Try Demo", use_container_width=True)
            if login_btn:
                if email in USERS and USERS[email]["password"]==password:
                    st.session_state.logged_in=True; st.session_state.user_email=email
                    st.session_state.user_name=USERS[email]["name"]
                    st.session_state.chat_history=[welcome_msg()]; st.rerun()
                else: st.error("❌ Wrong email or password.")
            if demo_btn:
                st.session_state.logged_in=True; st.session_state.user_email="demo@gmail.com"
                st.session_state.user_name="Demo User"
                st.session_state.chat_history=[welcome_msg()]; st.rerun()
        st.markdown(f"""<div style='background:{HOVER};border:1px solid {BORDER};border-radius:12px;padding:14px 18px;margin-top:16px;'>
        <div style='font-size:0.72rem;font-weight:600;color:{SUBTEXT};margin-bottom:6px;text-transform:uppercase;letter-spacing:1px;'>Demo Accounts</div>
        <div style='font-size:0.8rem;color:{TEXT};line-height:2;'>📧 demo@gmail.com · <b>demo123</b><br>🎓 student@mca.com · <b>cerebro123</b></div>
        </div>""", unsafe_allow_html=True)
    st.stop()

# SIDEBAR
with st.sidebar:
    st.markdown(f"""<div class='sb-brand'>
    <span style='font-size:1.7rem;filter:drop-shadow(0 0 8px {ACCENT});'>🧠</span>
    <div><div style='font-family:Syne,sans-serif;font-weight:800;font-size:1rem;color:{ACCENT};letter-spacing:1px;'>CEREBRO</div>
    <div style='font-size:0.58rem;color:{SUBTEXT};letter-spacing:2px;'>THE KNOWLEDGE BRAIN</div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        if st.button("＋ New Chat", use_container_width=True, key="new_chat_btn"):
            uq=[m for m in st.session_state.chat_history if m["role"]=="user"]
            if uq: st.session_state.chat_sessions.append({"name":uq[0]["content"][:38],"history":st.session_state.chat_history.copy()})
            st.session_state.chat_history=[welcome_msg()]; st.rerun()
    with c2:
        if st.button("☀️ Light" if D else "🌙 Dark", use_container_width=True, key="theme_btn"):
            st.session_state.dark_mode=not st.session_state.dark_mode; st.rerun()
    if st.button("⚙️  Settings", use_container_width=True, key="settings_btn"):
        st.session_state.show_settings=not st.session_state.show_settings; st.rerun()
    st.markdown(f"<div class='sb-label'>📊 Overview</div>", unsafe_allow_html=True)
    tq=len([m for m in st.session_state.chat_history if m["role"]=="user"])
    ts=len(st.session_state.chat_sessions)
    s1,s2=st.columns(2)
    with s1: st.markdown(f"<div class='sb-stat'><div class='sb-stat-n'>{tq}</div><div class='sb-stat-l'>Asked</div></div>", unsafe_allow_html=True)
    with s2: st.markdown(f"<div class='sb-stat'><div class='sb-stat-n'>{ts}</div><div class='sb-stat-l'>Sessions</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sb-label'>🕐 Current Chat</div>", unsafe_allow_html=True)
    um=[m for m in st.session_state.chat_history if m["role"]=="user"]
    if um:
        for m in um[-6:][::-1]:
            p=(m['content'][:40]+"…") if len(m['content'])>40 else m['content']
            st.markdown(f"<div class='sb-chat-item'><span>💬</span><div><div style='white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:180px;font-size:0.79rem;'>{p}</div><div style='font-size:0.63rem;color:{SUBTEXT};'>{m.get('time','')}</div></div></div>", unsafe_allow_html=True)
    else: st.markdown(f"<div style='font-size:0.77rem;color:{SUBTEXT};padding:6px 18px;'>No messages yet!</div>", unsafe_allow_html=True)
    if st.session_state.chat_sessions:
        st.markdown(f"<div class='sb-label'>📁 Past Sessions</div>", unsafe_allow_html=True)
        for i,sess in enumerate(reversed(st.session_state.chat_sessions[-5:])):
            p=(sess['name'][:34]+"…") if len(sess['name'])>34 else sess['name']
            if st.button(f"📄 {p}", key=f"sess_{i}", use_container_width=True):
                st.session_state.chat_history=sess["history"]; st.rerun()
    st.markdown(f"<div class='sb-label'>🧪 NLP Techniques</div>", unsafe_allow_html=True)
    for t in ["Tokenization","Stopword Removal","Lemmatization","TF-IDF Vectorization","Cosine Similarity"]:
        st.markdown(f"<div style='padding:3px 18px;font-size:0.77rem;color:{SUBTEXT};'>▸ {t}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='padding:6px 18px;font-size:0.76rem;color:{SUBTEXT};line-height:1.9;'>🔵 <span style='color:{TEXT};font-weight:600;'>Layer 1</span> NLP Dataset<br>🟣 <span style='color:{TEXT};font-weight:600;'>Layer 2</span> Cerebro AI (Gemini)</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    if st.button("🗑️  Clear Chat", use_container_width=True, key="clear_btn"):
        st.session_state.chat_history=[welcome_msg()]; st.rerun()
    init=st.session_state.user_name[0].upper() if st.session_state.user_name else "U"
    st.markdown(f"""<div class='sb-user'><div class='avatar'>{init}</div>
    <div style='overflow:hidden;flex:1;'><div style='font-weight:600;font-size:0.83rem;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{st.session_state.user_name}</div>
    <div style='font-size:0.67rem;color:{SUBTEXT};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{st.session_state.user_email}</div></div></div>""", unsafe_allow_html=True)
    if st.button("🚪  Logout", use_container_width=True, key="logout_btn"):
        for k in ["logged_in","user_email","user_name","chat_history","chat_sessions"]:
            st.session_state[k]=False if k=="logged_in" else ([] if k in ["chat_history","chat_sessions"] else "")
        st.rerun()
    st.markdown(f"<div style='text-align:center;font-size:0.62rem;color:{SUBTEXT};padding:8px 0 4px;'>MCA Sem 2 · NLP Project · Python 🐍</div>", unsafe_allow_html=True)

# MAIN

st.markdown(f"""<div style='text-align:center;padding:24px 0 6px;'>
<span style='font-size:3.6rem;display:inline-block;animation:brainPulse 3s ease-in-out infinite;line-height:1;margin-bottom:10px;'>🧠</span>
<div style='font-family:Syne,sans-serif;font-weight:800;font-size:3rem;letter-spacing:-1px;color:{ACCENT};'>CEREBRO</div>
<div style='font-size:0.77rem;color:{SUBTEXT};letter-spacing:4px;text-transform:uppercase;margin-top:8px;'>The Knowledge Brain &nbsp;·&nbsp; Ask Anything</div>
</div><div class='cline'></div>""", unsafe_allow_html=True)

suggestions=["What is quantum computing?","Explain black holes","What is machine learning?","Who was Einstein?","How does the internet work?","What is recursion?"]
cols=st.columns(6)
for i,s in enumerate(suggestions):
    with cols[i]:
        if st.button(s,key=f"chip_{i}",use_container_width=True):
            st.session_state.chat_history.append({"role":"user","content":s,"time":datetime.now().strftime("%I:%M %p")})
            response,confidence,source=get_response(s)
            badge="🧠 Cerebro AI" if source=="cerebro" else f"📚 Dataset · {confidence}%"
            st.session_state.chat_history.append({"role":"cerebro","content":response,"time":datetime.now().strftime("%I:%M %p"),"badge":badge})
            st.rerun()

st.markdown("<div class='cline'></div>", unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    if msg["role"]=="user":
        _,c2=st.columns([1,3])
        with c2: st.markdown(f"<div class='msg-user'>{msg['content']}</div><div class='msg-meta'>You &nbsp;·&nbsp; {msg.get('time','')}</div>", unsafe_allow_html=True)
    else:
        c1,_=st.columns([3,1])
        with c1:
            badge=msg.get("badge","🧠 Cerebro")
            st.markdown(f"<div class='msg-badge'>{badge}</div><div class='msg-bot'>{msg['content']}</div><div class='msg-meta-l'>Cerebro &nbsp;·&nbsp; {msg.get('time','')}</div>", unsafe_allow_html=True)

user_input=st.chat_input("Ask Cerebro anything...")
if user_input and user_input.strip():
    now=datetime.now().strftime("%I:%M %p")
    st.session_state.chat_history.append({"role":"user","content":user_input,"time":now})
    ph=st.empty()
    ph.markdown(f"<div style='display:flex;align-items:center;gap:6px;padding:14px 20px;background:{BOT_BG};border:1px solid {BORDER};border-radius:20px;width:fit-content;'><div class='dot'></div><div class='dot'></div><div class='dot'></div></div>", unsafe_allow_html=True)
    response,confidence,source=get_response(user_input)
    time.sleep(0.4); ph.empty()
    badge="🧠 Cerebro AI" if source=="cerebro" else f"📚 Dataset · {confidence}%"
    st.session_state.chat_history.append({"role":"cerebro","content":response,"time":datetime.now().strftime("%I:%M %p"),"badge":badge})
    st.rerun()
