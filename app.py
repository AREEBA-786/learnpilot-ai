# import streamlit as st
# from utils import run_agent_sync

# st.set_page_config(page_title="MCP POC", page_icon="🤖", layout="wide")
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

# html, body, [class*="css"] {
#     font-family: 'IBM Plex Sans', sans-serif;
# }

# h1, h2, h3 {
#     font-family: 'Space Grotesk', sans-serif;
# }

# h1 {
#     color: #1B4332;
# }

# section[data-testid="stSidebar"] {
#     background-color: #F4F7F5;
#     border-right: 1px solid #D8E2DC;
# }

# section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
#     color: #1B4332;
# }

# button[kind="primary"] {
#     background-color: #1B4332;
#     border-radius: 6px;
#     font-weight: 600;
# }
# button[kind="primary"]:hover {
#     background-color: #2D6A4F;
# }

# div[data-testid="stAlert"] {
#     background-color: #FFF8E7;
#     border-left: 4px solid #D4A017;
#     border-radius: 4px;
# }

# div[data-testid="stTextInput"] input {
#     border-radius: 6px;
#     border: 1px solid #D8E2DC;
# }
# </style>
# """, unsafe_allow_html=True)

# #st.title("Model Context Protocol(MCP) - Learning Path Generator")
# st.markdown("""
# <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.2rem;">
#     <span style="font-size:2rem;">🧭</span>
#     <div>
#         <h1 style="margin-bottom:0;">Learning Path Generator</h1>
#         <p style="color:#52796F; margin-top:0;">Model Context Protocol (MCP) se apna goal ek day-wise plan mein badlo</p>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Initialize session state for progress
# if 'current_step' not in st.session_state:
#     st.session_state.current_step = ""
# if 'progress' not in st.session_state:
#     st.session_state.progress = 0
# if 'last_section' not in st.session_state:
#     st.session_state.last_section = ""
# if 'is_generating' not in st.session_state:
#     st.session_state.is_generating = False

# # Sidebar for API and URL configuration
# st.sidebar.header("Configuration")

# # API Key input
# google_api_key = st.sidebar.text_input("Google API Key", type="password")

# # Pipedream URLs
# st.sidebar.subheader("Pipedream URLs")
# youtube_pipedream_url = st.sidebar.text_input("YouTube URL (Required)", 
#     placeholder="Enter your Pipedream YouTube URL")

# # Secondary tool selection
# secondary_tool = st.sidebar.radio(
#     "Select Secondary Tool:",
#     ["Drive", "Notion"]
# )

# # Secondary tool URL input
# if secondary_tool == "Drive":
#     drive_pipedream_url = st.sidebar.text_input("Drive URL", 
#         placeholder="Enter your Pipedream Drive URL")
#     notion_pipedream_url = None
# else:
#     notion_pipedream_url = st.sidebar.text_input("Notion URL", 
#         placeholder="Enter your Pipedream Notion URL")
#     drive_pipedream_url = None

# # Quick guide before goal input
# st.info("""
# **Quick Guide:**
# 1. Enter your Google API key and YouTube URL (required)
# 2. Select and configure your secondary tool (Drive or Notion)
# 3. Enter a clear learning goal, for example:
#     - "I want to learn python basics in 3 days"
#     - "I want to learn data science basics in 10 days"
# """)

# # Main content area
# st.header("Enter Your Goal")
# user_goal = st.text_input("Enter your learning goal:",
#                         help="Describe what you want to learn, and we'll generate a structured path using YouTube content and your selected tool.")

# # Progress area
# progress_container = st.container()
# progress_bar = st.empty()

# def update_progress(message: str):
#     """Update progress in the Streamlit UI"""
#     st.session_state.current_step = message

#     # Determine section and update progress
#     if "Setting up agent with tools" in message:
#         section = "Setup"
#         st.session_state.progress = 0.1
#     elif "Added Google Drive integration" in message or "Added Notion integration" in message:
#         section = "Integration"
#         st.session_state.progress = 0.2
#     elif "Creating AI agent" in message:
#         section = "Setup"
#         st.session_state.progress = 0.3
#     elif "Generating your learning path" in message:
#         section = "Generation"
#         st.session_state.progress = 0.5
#     elif "Learning path generation complete" in message:
#         section = "Complete"
#         st.session_state.progress = 1.0
#         st.session_state.is_generating = False
#     else:
#         section = st.session_state.last_section or "Progress"

#     is_new_section = (section != st.session_state.last_section)
#     st.session_state.last_section = section

#     # Show progress bar
#     progress_bar.progress(st.session_state.progress)

#     # Update progress container with current status
#     with progress_container:
#         # Show section header if it changed
#         if is_new_section and section != "Complete":
#             st.write(f"**{section}**")

#         # Show message with tick for completed steps
#         if message == "Learning path generation complete!":
#             st.success("All steps completed! 🎉")
#         else:
#             prefix = "✓" if st.session_state.progress >= 0.5 else "→"
#             st.write(f"{prefix} {message}")

# # Generate Learning Path button
# if st.button("Generate Learning Path", type="primary", disabled=st.session_state.is_generating):
#     if not google_api_key:
#         st.error("Please enter your Google API key in the sidebar.")
#     elif not youtube_pipedream_url:
#         st.error("YouTube URL is required. Please enter your Pipedream YouTube URL in the sidebar.")
#     elif (secondary_tool == "Drive" and not drive_pipedream_url) or (secondary_tool == "Notion" and not notion_pipedream_url):
#         st.error(f"Please enter your Pipedream {secondary_tool} URL in the sidebar.")
#     elif not user_goal:
#         st.warning("Please enter your learning goal.")
#     else:
#         try:
#             # Set generating flag
#             st.session_state.is_generating = True
            
#             # Reset progress
#             st.session_state.current_step = ""
#             st.session_state.progress = 0
#             st.session_state.last_section = ""
            
#             result = run_agent_sync(
#                 google_api_key=google_api_key,
#                 youtube_pipedream_url=youtube_pipedream_url,
#                 drive_pipedream_url=drive_pipedream_url,
#                 notion_pipedream_url=notion_pipedream_url,
#                 user_goal=user_goal,
#                 progress_callback=update_progress
#             )
            
#             # Display results
#             st.header("Your Learning Path")
#             # print(result)
#             if result and "messages" in result:
#                 for msg in result["messages"]:
#                     st.markdown(f"📚 {msg.content}")

#             else:
#                 st.error("No results were generated. Please try again.")
#                 st.session_state.is_generating = False
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")
#             st.error("Please check your API keys and URLs, and try again.")
#             st.session_state.is_generating = False

# import re
# import streamlit as st
# from utils import run_agent_sync

# st.set_page_config(page_title="MCP Learning Path Generator", page_icon="🧭", layout="wide")

# # ---------- Custom styling ----------
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

# html, body, [class*="css"] {
#     font-family: 'IBM Plex Sans', sans-serif;
# }
# h1, h2, h3 {
#     font-family: 'Space Grotesk', sans-serif;
# }
# h1 { color: #1B4332; }

# section[data-testid="stSidebar"] {
#     background-color: #F4F7F5;
#     border-right: 1px solid #D8E2DC;
# }
# section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
#     color: #1B4332;
# }

# button[kind="primary"] {
#     background-color: #1B4332;
#     border-radius: 6px;
#     font-weight: 600;
#     transition: transform 0.15s ease, box-shadow 0.15s ease;
# }
# button[kind="primary"]:hover {
#     background-color: #2D6A4F;
#     transform: translateY(-2px);
#     box-shadow: 0 4px 10px rgba(27, 67, 50, 0.25);
# }

# button[kind="secondary"] {
#     border-radius: 20px;
#     border: 1px solid #1B4332;
#     color: #1B4332;
#     background-color: #FFFFFF;
#     font-size: 0.85rem;
# }
# button[kind="secondary"]:hover {
#     background-color: #F4F7F5;
#     border-color: #2D6A4F;
# }

# div[data-testid="stAlert"] {
#     background-color: #FFF8E7;
#     border-left: 4px solid #D4A017;
#     border-radius: 4px;
# }
# </style>
# """, unsafe_allow_html=True)

# # ---------- Header ----------
# st.markdown("""
# <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.2rem;">
#     <span style="font-size:2rem;">🧭</span>
#     <div>
#         <h1 style="margin-bottom:0;">Learning Path Generator</h1>
#         <p style="color:#52796F; margin-top:0;">Turn any goal into a personalized, day-wise learning path</p>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # ---------- Session state ----------
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "is_generating" not in st.session_state:
#     st.session_state.is_generating = False

# # ---------- Sidebar: Configuration ----------
# st.sidebar.header("Configuration")
# google_api_key = st.sidebar.text_input("Google API Key", type="password")
# st.sidebar.divider()

# st.sidebar.subheader("Pipedream URLs")
# youtube_pipedream_url = st.sidebar.text_input(
#     "YouTube URL (Required)", placeholder="Enter your Pipedream YouTube URL"
# )
# st.sidebar.divider()

# secondary_tool = st.sidebar.radio("Select Secondary Tool:", ["Drive", "Notion"])

# if secondary_tool == "Drive":
#     drive_pipedream_url = st.sidebar.text_input(
#         "Drive URL", placeholder="Enter your Pipedream Drive URL"
#     )
#     notion_pipedream_url = None
# else:
#     notion_pipedream_url = st.sidebar.text_input(
#         "Notion URL", placeholder="Enter your Pipedream Notion URL"
#     )
#     drive_pipedream_url = None

# # ---------- Helper: pull document/playlist links out of the final answer ----------
# def extract_links(text: str):
#     urls = re.findall(r'(https?://[^\s\)\]]+)', text)
#     doc_link, playlist_link = None, None
#     for u in urls:
#         if "youtube.com/playlist" in u or "youtu.be" in u:
#             playlist_link = u
#         elif "drive.google.com" in u or "notion.so" in u or "notion.site" in u:
#             doc_link = u
#     return doc_link, playlist_link

# def render_link_buttons(text: str):
#     doc_link, playlist_link = extract_links(text)
#     if doc_link or playlist_link:
#         cols = st.columns(2)
#         if doc_link:
#             cols[0].link_button("📄 Open Document", doc_link, use_container_width=True)
#         if playlist_link:
#             cols[1].link_button("🎵 Open Playlist", playlist_link, use_container_width=True)

# # ---------- Render past conversation ----------
# for msg in st.session_state.chat_history:
#     avatar = "🧭" if msg["role"] == "assistant" else None
#     with st.chat_message(msg["role"], avatar=avatar):
#         st.markdown(msg["content"])
#         if msg["role"] == "assistant":
#             render_link_buttons(msg["content"])

# # ---------- Example prompts (shown only before the first message) ----------
# example_goal = None
# if not st.session_state.chat_history:
#     st.markdown("<p style='color:#666; margin-top:1rem;'>Try one of these:</p>", unsafe_allow_html=True)
#     examples = [
#         "I want to learn python basics in 3 days",
#         "I want to learn data science basics in 10 days",
#         "I want to learn web development in 7 days",
#     ]
#     ex_cols = st.columns(3)
#     for col, ex in zip(ex_cols, examples):
#         if col.button(ex, use_container_width=True):
#             example_goal = ex

# # ---------- Chat input (stays pinned at the bottom, like ChatGPT) ----------
# typed_goal = st.chat_input("Describe your learning goal, e.g. 'I want to learn python basics in 3 days'")
# user_goal = typed_goal or example_goal

# # ---------- Handle a new goal ----------
# if user_goal and not st.session_state.is_generating:
#     if not google_api_key:
#         st.error("Please enter your Google API key in the sidebar.")
#     elif not youtube_pipedream_url:
#         st.error("YouTube URL is required. Please enter your Pipedream YouTube URL in the sidebar.")
#     elif (secondary_tool == "Drive" and not drive_pipedream_url) or (secondary_tool == "Notion" and not notion_pipedream_url):
#         st.error(f"Please enter your Pipedream {secondary_tool} URL in the sidebar.")
#     else:
#         st.session_state.is_generating = True
#         st.session_state.chat_history.append({"role": "user", "content": user_goal})

#         with st.chat_message("user"):
#             st.markdown(user_goal)

#         with st.chat_message("assistant", avatar="🧭"):
#             status_box = st.status("Setting up agent...", expanded=True)

#             def update_progress(message: str):
#                 status_box.update(label=message)
#                 status_box.write(message)

#             try:
#                 result = run_agent_sync(
#                     google_api_key=google_api_key,
#                     youtube_pipedream_url=youtube_pipedream_url,
#                     drive_pipedream_url=drive_pipedream_url,
#                     notion_pipedream_url=notion_pipedream_url,
#                     user_goal=user_goal,
#                     progress_callback=update_progress
#                 )
#                 status_box.update(label="Done!", state="complete", expanded=False)

#                 if result and "messages" in result and result["messages"]:
#                     final_text = result["messages"][-1].content
#                 else:
#                     final_text = "No results were generated. Please try again."

#                 st.markdown(final_text)
#                 render_link_buttons(final_text)
#                 st.session_state.chat_history.append({"role": "assistant", "content": final_text})

#             except Exception as e:
#                 error_text = f"An error occurred: {str(e)}. Please check your API keys and URLs, and try again."
#                 status_box.update(label="Failed", state="error", expanded=True)
#                 st.error(error_text)
#                 st.session_state.chat_history.append({"role": "assistant", "content": error_text})

#         st.session_state.is_generating = False


import re
import streamlit as st
from utils import run_agent_sync
from chat_store import (
    load_all_chats,
    create_new_session,
    update_session_messages,
    delete_session,
    get_sorted_sessions,
)

st.set_page_config(page_title="Learning Path Generator", page_icon="🧭", layout="wide")

# ---------- Custom styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: linear-gradient(180deg, #FAFCFA 0%, #F4F7F5 100%);
}

section[data-testid="stSidebar"] {
    background-color: #F0F5F1;
    border-right: 1px solid #D8E2DC;
}

button[kind="primary"] {
    background-color: #1B4332;
    border-radius: 8px;
    font-weight: 600;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
button[kind="primary"]:hover {
    background-color: #2D6A4F;
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(27, 67, 50, 0.25);
}

button[kind="secondary"] {
    border-radius: 8px;
    border: 1px solid #D8E2DC;
    color: #1B4332;
    background-color: #FFFFFF;
}
button[kind="secondary"]:hover {
    background-color: #EAF1EC;
    border-color: #1B4332;
}

div[data-testid="stAlert"] {
    background-color: #FFF8E7;
    border-left: 4px solid #D4A017;
    border-radius: 4px;
}

/* Chat input bar at the bottom */
div[data-testid="stChatInput"] {
    background-color: #FAFCFA;
    border-top: 1px solid #D8E2DC;
    padding: 0.8rem 1rem;
}
div[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    border: 1.5px solid #1B4332 !important;
    border-radius: 12px !important;
    color: #1B1B1B !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: #8a9a92;
}

/* Chat bubbles */
div[data-testid="stChatMessage"] {
    background-color: #FFFFFF;
    border: 1px solid #E8EDE9;
    border-radius: 12px;
    padding: 0.5rem 1rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.03);
}
</style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "current_session_id" not in st.session_state:
    sessions = get_sorted_sessions()
    st.session_state.current_session_id = sessions[0][0] if sessions else create_new_session()

if "is_generating" not in st.session_state:
    st.session_state.is_generating = False

# ---------- Sidebar: chat sessions ----------
st.sidebar.markdown("### 🧭 Learning Path Generator")

if st.sidebar.button("➕ New Chat", use_container_width=True, type="primary"):
    st.session_state.current_session_id = create_new_session()
    st.rerun()

st.sidebar.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)

for sid, data in get_sorted_sessions():
    col1, col2 = st.sidebar.columns([5, 1])
    label = data.get("title", "New Chat")
    is_active = (sid == st.session_state.current_session_id)
    if col1.button(label, key=f"sess_{sid}", use_container_width=True,
                    type="primary" if is_active else "secondary"):
        st.session_state.current_session_id = sid
        st.rerun()
    if col2.button("🗑️", key=f"del_{sid}"):
        delete_session(sid)
        if st.session_state.current_session_id == sid:
            remaining = get_sorted_sessions()
            st.session_state.current_session_id = remaining[0][0] if remaining else create_new_session()
        st.rerun()

st.sidebar.divider()

# ---------- Sidebar: Configuration ----------
st.sidebar.header("Configuration")
google_api_key = st.sidebar.text_input("Google API Key", type="password")
st.sidebar.divider()

st.sidebar.subheader("Pipedream URLs")
youtube_pipedream_url = st.sidebar.text_input(
    "YouTube URL (Required)", placeholder="Enter your Pipedream YouTube URL"
)
st.sidebar.divider()

secondary_tool = st.sidebar.radio("Select Secondary Tool:", ["Drive", "Notion"])

if secondary_tool == "Drive":
    drive_pipedream_url = st.sidebar.text_input("Drive URL", placeholder="Enter your Pipedream Drive URL")
    notion_pipedream_url = None
else:
    notion_pipedream_url = st.sidebar.text_input("Notion URL", placeholder="Enter your Pipedream Notion URL")
    drive_pipedream_url = None

# ---------- Helpers ----------
def extract_links(text: str):
    urls = re.findall(r'(https?://[^\s\)\]]+)', text)
    doc_link, playlist_link = None, None
    for u in urls:
        if "youtube.com/playlist" in u or "youtu.be" in u:
            playlist_link = u
        elif "drive.google.com" in u or "notion.so" in u or "notion.site" in u:
            doc_link = u
    return doc_link, playlist_link


def render_link_buttons(text: str):
    doc_link, playlist_link = extract_links(text)
    if doc_link or playlist_link:
        cols = st.columns(2)
        if doc_link:
            cols[0].link_button("📄 Open Document", doc_link, use_container_width=True)
        if playlist_link:
            cols[1].link_button("🎵 Open Playlist", playlist_link, use_container_width=True)


# ---------- Load current session ----------
chats = load_all_chats()
current_id = st.session_state.current_session_id
current_messages = chats.get(current_id, {}).get("messages", [])

clicked_example = None

if not current_messages:
    st.markdown("""
    <div style="text-align:center; margin-top:8vh;">
        <div style="font-size:3rem;">🧭</div>
        <h2 style="margin-bottom:0.2rem; color:#1B4332;">Learning Path Generator</h2>
        <p style="color:#8a9a92; font-size:1.15rem; margin-top:0;">What's on the agenda today?</p>
    </div>
    """, unsafe_allow_html=True)

    ex_cols = st.columns(3)
    examples = [
        "I want to learn python basics in 3 days",
        "I want to learn data science basics in 10 days",
        "I want to learn web development in 7 days",
    ]
    for col, ex in zip(ex_cols, examples):
        if col.button(ex, use_container_width=True):
            clicked_example = ex
else:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:0.4rem; padding:0.2rem 0 0.6rem 0;">
        <span style="font-size:1.3rem;">🧭</span>
        <span style="font-weight:600; color:#1B4332;">Learning Path Generator</span>
    </div>
    """, unsafe_allow_html=True)

    for msg in current_messages:
        avatar = "🧭" if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                render_link_buttons(msg["content"])

# ---------- Chat input (pinned at the bottom) ----------
typed_goal = st.chat_input("Describe your learning goal, e.g. 'I want to learn python basics in 3 days'")
user_goal = typed_goal or clicked_example

# ---------- Handle a new goal ----------
if user_goal and not st.session_state.is_generating:
    if not google_api_key:
        st.error("Please enter your Google API key in the sidebar.")
    elif not youtube_pipedream_url:
        st.error("YouTube URL is required. Please enter your Pipedream YouTube URL in the sidebar.")
    elif (secondary_tool == "Drive" and not drive_pipedream_url) or (secondary_tool == "Notion" and not notion_pipedream_url):
        st.error(f"Please enter your Pipedream {secondary_tool} URL in the sidebar.")
    else:
        st.session_state.is_generating = True
        current_messages.append({"role": "user", "content": user_goal})

        with st.chat_message("user"):
            st.markdown(user_goal)

        with st.chat_message("assistant", avatar="🧭"):
            status_box = st.status("Setting up agent...", expanded=True)

            def update_progress(message: str):
                status_box.update(label=message)
                status_box.write(message)

            try:
                result = run_agent_sync(
                    google_api_key=google_api_key,
                    youtube_pipedream_url=youtube_pipedream_url,
                    drive_pipedream_url=drive_pipedream_url,
                    notion_pipedream_url=notion_pipedream_url,
                    user_goal=user_goal,
                    progress_callback=update_progress
                )
                status_box.update(label="Done!", state="complete", expanded=False)

                if result and "messages" in result and result["messages"]:
                    final_text = result["messages"][-1].content
                else:
                    final_text = "No results were generated. Please try again."

                st.markdown(final_text)
                render_link_buttons(final_text)
                current_messages.append({"role": "assistant", "content": final_text})

            except Exception as e:
                error_text = f"An error occurred: {str(e)}. Please check your API keys and URLs, and try again."
                status_box.update(label="Failed", state="error", expanded=True)
                st.error(error_text)
                current_messages.append({"role": "assistant", "content": error_text})

        update_session_messages(current_id, current_messages)
        st.session_state.is_generating = False
        st.rerun()