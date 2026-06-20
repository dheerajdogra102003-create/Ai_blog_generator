import streamlit as st
from backend import generate_blog

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

import json
import os
from datetime import datetime
import io

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Blog Studio",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

#
st.markdown("""
<style>

.stApp{
background: linear-gradient(
    135deg,
    #000000,
    #020617,
    #0D1117,
    #111827,
    #1E293B,
    #334155,
    #2563EB,
    #3B82F6,
    #60A5FA
);

background-size:400% 400%;
animation:gradient 12s ease infinite;

}

@keyframes gradient{

0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
    background: linear-gradient(

}

</style>
""", unsafe_allow_html=True)
# ============================================================
# HISTORY
# ============================================================

HISTORY_FILE = "history.json"

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)


def load_history():
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(topic):
    history = load_history()

    history.insert(
        0,
        {
            "topic": topic,
            "time": datetime.now().strftime("%d %b %Y  %I:%M %p")
        }
    )

    history = history[:20]

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


# ============================================================
# PDF FUNCTION
# ============================================================

# def create_pdf(text):

#     buffer = io.BytesIO()

#     doc = SimpleDocTemplate(buffer)
#             "time": datetime.now().strftime("%d %b %Y %I:%M %p"),
#     styles = getSampleStyleSheet()

#     story = [
#         Paragraph(
#             text.replace("\n", "<br/>"),
#             styles["BodyText"]
#         )
#     ]

#     doc.build(story)

#     buffer.seek(0)

#     return buffer


def create_pdf(text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(
            text.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    ]
    doc.build(story)
    buffer.seek(0)
    return buffer


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("📚 Blog History")

    history = load_history()

    if history:

        for item in history:

            with st.container(border=True):

                st.markdown(f"### 📄 {item['topic'][:35]}")

                st.caption(item["time"])

    else:

        st.info("No blogs generated yet.")

    st.divider()

    st.subheader("💡 Tips")

    st.write("• Be specific with your topic.")

    st.write("• Include keywords for better blogs.")

    st.write("• Technical topics produce richer content.")


# ============================================================
# HEADER
# ============================================================

st.title("✍️ AI BLOG STUDIO")

st.caption(
    "Generate professional AI-powered blogs in seconds."
)

st.divider()

# ============================================================
# INPUT AREA
# ============================================================

st.markdown("## 📝 Blog Topic")

topic = st.text_input(
    "",
    placeholder="Enter any topic...",
    label_visibility="collapsed"
)

left, middle, right = st.columns([1.5, 2, 1.5])

with middle:

    generate = st.button(
        "🚀 Generate Blog",
        use_container_width=True
    )

# st.divider()

# ============================================================
# PLACEHOLDER
# ============================================================

output_container = st.container()

# ============================================================
# BLOG GENERATION
# ============================================================

if generate:

    if not topic.strip():

        st.warning("⚠ Please enter a blog topic.")

    else:

        with st.spinner("🤖 Generating your blog..."):

            blog_content = generate_blog(topic)

        save_history(topic)

        words = len(blog_content.split())

        reading_time = max(1, words // 200)

        st.success("✅ Blog generated successfully!")

        st.divider()

        # ====================================================
        # BLOG SUMMARY
        # ====================================================

        st.subheader("📊 Blog Summary")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                label="📝 Total Words",
                value=words
            )

        with c2:
            st.metric(
                label="⏱ Reading Time",
                value=f"{reading_time} min"
            )

        with c3:
            st.metric(
                label="📚 Topic",
                value=topic[:20] + "..." if len(topic) > 20 else topic
            )

        st.divider()

        # ====================================================
        # BLOG CONTENT
        # ====================================================

        st.subheader("📖 Generated Blog")

        with st.container(border=True):

            st.markdown(blog_content)

        st.divider()

        # ====================================================
        # DOWNLOAD SECTION
        # ====================================================

        st.subheader("📥 Export Blog")

        txt_col, pdf_col = st.columns(2)

        with txt_col:

            st.download_button(
                label="📄 Download as TXT",
                data=blog_content,
                file_name=f"{topic.replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

        with pdf_col:

            pdf_file = create_pdf(blog_content)

            st.download_button(
                label="📕 Download as PDF",
                data=pdf_file,
                file_name=f"{topic.replace(' ','_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        st.divider()

        # ====================================================
        # BLOG INFORMATION
        # ====================================================

        with st.expander("ℹ Blog Information", expanded=False):

            st.write(f"**Topic:** {topic}")

            st.write(f"**Total Words:** {words}")

            st.write(f"**Estimated Reading Time:** {reading_time} minute(s)")

            st.write(f"**Generated On:** {datetime.now().strftime('%d %B %Y')}")

        # ====================================================
        # FEEDBACK
        # ====================================================

        st.divider()

        st.subheader("⭐ Feedback")

        feedback = st.radio(
            "How was the generated blog?",
            [
                "⭐⭐⭐⭐⭐ Excellent",
                "⭐⭐⭐⭐ Good",
                "⭐⭐⭐ Average",
                "⭐⭐ Needs Improvement"
            ],
            horizontal=True
        )
        if st.button("Submit Feedback"):
            st.success("🙏 Thank you for your feedback!")

# ============================================================
# HOME SCREEN
# ============================================================

else:
    st.info("👈 Enter a topic above and click **Generate** to create your AI-powered blog.")

   
st.divider()
st.caption("🚀 Built with Streamlit • AI Blog Studio")