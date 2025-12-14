
import os
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import requests
from langchain_core.runnables import Runnable

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont


#LOAD ENV and INITIALIZE LLM
import os

# Load GROQ API key from environment (Hugging Face Space secret)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Check if the key exists
if GROQ_API_KEY is None:
    raise ValueError(
        "Missing GROQ_API_KEY. Please set it in HuggingFace → Settings → Variables & secrets"
    )





from langchain_core.runnables import Runnable

class GroqLLM(Runnable):
    def __init__(self, model_name="openai/gpt-oss-20b", temperature=0.3):
        self.model_name = model_name
        self.temperature = temperature

    def invoke(self, input, config=None):
        # Handle LangChain PromptValue objects
        if hasattr(input, "to_string"):
            prompt = input.to_string()
        elif isinstance(input, str):
            prompt = input
        elif isinstance(input, dict):
            prompt = input.get("topic", "")
        else:
            prompt = str(input)

        # Groq API endpoint
        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are an AI study planner and educational consultant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1024,
            "temperature": self.temperature
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

# ----------------- Usage -----------------
# Replace ChatGroq with this wrapper
llm = GroqLLM(temperature=0.0)  # temperature 0 for deterministic output


parser = StrOutputParser()

#WRITE ALL LLM TASK FUNCTIONS (LCEL)
def process_topic(topic: str) -> str:
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Process the following topic and provide a structured summary:\n\n{topic}"
    )
    chain = prompt | llm | parser
    return chain.invoke({"topic": topic})



#Generate Objectives & Outcomes
def generate_objectives(topic: str) -> str:
    template = """
    Generate clear, concise educational objectives for the topic: "{topic}".

    Output ONLY the following sections:

    1. General Objectives:
       - Broad learning goals.
       - What learners should understand or appreciate.

    2. Specific Objectives:
       - Measurable outcomes.
       - Use action verbs.
       - Do NOT include teaching activities.

   3. Student Learning Outcomes:
        - Explain key concepts of the topic clearly.
        - Apply core ideas in practical situations.
        - Analyze information to draw informed conclusions.
    """

    prompt = PromptTemplate(
        input_variables=["topic"],
        template=template
    )
    chain = prompt | llm | parser
    return chain.invoke({"topic": topic})


def generate_lesson_plan(objectives_text: str) -> str:
    template = """
    Using the following objectives, generate a complete and detailed lesson plan.
    Rewrite EVERYTHING in your own words. Do NOT copy the objectives directly.

    Objectives:
    {objectives_text}

    The lesson plan must include:

    1. Introduction and Announcement
    2. Methodology (teaching steps, strategies, activities)
    3. Previous Knowledge Questions
    4. Announcing the Topic (teacher action)
    5. Presentation (lesson delivery + student activities)
    6. Homework
    7. Assessment and Feedback

    Requirements:
    - Expand each section with practical, teacher-style content.
    - Add timings, steps, and examples where relevant.
    - DO NOT repeat objectives inside the lesson plan.
    """

    prompt = PromptTemplate(
        input_variables=["objectives_text"],
        template=template
    )
    chain = prompt | llm | parser
    return chain.invoke({"objectives_text": objectives_text})


#EdTech Tools Recommendation
def recommend_edtech_tools(lesson_plan: str) -> str:
    template = """
    Based on the following lesson plan, recommend at least 5 EdTech tools.

    For each tool provide:
    - Tool Name
    - Description
    - Purpose / Why it fits the lesson
    - Type (Interactive, Simulation, etc.)
    - Cost (Free / Paid)

    Lesson plan content:
    {lesson_plan}
    """

    prompt = PromptTemplate(
        input_variables=["lesson_plan"],
        template=template
    )

    chain = prompt | llm | parser
    return chain.invoke({"lesson_plan": lesson_plan})

def generate_CLOs(topic: str) -> str:
    template = """
    Generate 4–6 high-quality CLOs (Course Learning Outcomes) for the topic "{topic}".

    Requirements:
    - Use measurable action verbs.
    - Outcomes should be higher-order (Bloom’s: Apply → Create).
    - Should reflect course-level abilities, not lesson-level tasks.
    - Write in bullet format.

    Output sections:
    1. Course Learning Outcomes (CLOs)
    2. Mapping with Bloom’s Levels
    """

    prompt = PromptTemplate(
        input_variables=["topic"],
        template=template
    )
    chain = prompt | llm | parser
    return chain.invoke({"topic": topic})

def generate_blooms_taxonomy(objectives_text: str) -> str:
    template = """
    Based on the following objectives, classify learning outcomes into Bloom’s Taxonomy levels:

    Levels required:
    - Knowledge
    - Comprehension
    - Application
    - Analysis
    - Evaluation
    - Creation

    For each level:
    - Provide 2–3 measurable learning outcomes.
    - Rewrite objectives as needed (do not copy text).

    Objectives:
    {objectives_text}
    """

    prompt = PromptTemplate(
        input_variables=["objectives_text"],
        template=template
    )
    chain = prompt | llm | parser
    return chain.invoke({"objectives_text": objectives_text})

def generate_teaching_materials(topic: str) -> str:
    template = """
    Generate teaching materials for the topic "{topic}".

    Provide:
    - Worksheet (5 questions)
    - Multiple-choice quiz (5 items with correct answers)
    - PPT outline (6–8 slides)
    - Classroom activities (2 activities)

    Keep content practical and ready-to-use.
    """

    prompt = PromptTemplate(
        input_variables=["topic"],
        template=template
    )
    chain = prompt | llm | parser
    return chain.invoke({"topic": topic})

def generate_rubric(topic: str) -> str:
    template = """
    Create an assessment rubric for the topic "{topic}".

    Include:
    - 4 criteria (e.g., understanding, participation, task completion, skills)
    - 4 performance levels (Excellent, Good, Fair, Needs Improvement)
    - Scoring scale (1–4)
    - Descriptor for each level under each criterion
    """

    prompt = PromptTemplate(
        input_variables=["topic"],
        template=template
    )
    chain = prompt | llm | parser
    return chain.invoke({"topic": topic})



import gradio as gr
import re

import re

def format_output(content: str) -> str:
    import re

    # Remove ALL markdown symbols globally first
    content = re.sub(r"[*`_]+", "", content)

    lines = content.strip().split("\n")
    final_html = []
    table_rows = []
    inside_table = False

    def clean_text(txt):
        return re.sub(r"[#*\-:`]+", "", txt).strip()

    def render_table(rows):
        html = "<div class='table-container'><table class='result-table'>"
        header_done = False

        for r in rows:
            # Skip markdown separator rows like |-----|
            if re.match(r"^\s*\|?[-\s|]+\|?\s*$", r):
                continue

            cells = [clean_text(c) for c in r.split("|") if c.strip()]

            if not header_done:
                html += "<tr>" + "".join([f"<th>{c}</th>" for c in cells]) + "</tr>"
                header_done = True
            else:
                html += "<tr>" + "".join([f"<td>{c}</td>" for c in cells]) + "</tr>"

        html += "</table></div>"
        return html

    for line in lines:
        stripped = line.strip()

        # ---------- TABLE DETECTION ----------
        if "|" in stripped:
            inside_table = True
            table_rows.append(stripped)
            continue

        if inside_table and stripped == "":
            final_html.append(render_table(table_rows))
            table_rows = []
            inside_table = False
            continue

        # ---------- HEADING DETECTION (100% reliable) ----------
        if (
            stripped.endswith(":")
            or stripped.startswith("#")
            or stripped.lower() in ["introduction", "conclusion"]
            or re.match(r"^[A-Za-z ]+$", stripped)  # plain headings
        ):
            clean = clean_text(stripped)
            if len(clean.split()) <= 8:  # avoid matching full sentences
                final_html.append(
                    "<div style='color:#1E90FF;font-weight:900;font-size:24px;"
                    "margin-top:16px;margin-bottom:8px;'>"
                    f"{clean}</div>"
                )
                continue

        # ---------- BULLETS ----------
        if stripped.startswith(("*", "-", "•")):
            clean = clean_text(stripped)
            final_html.append(
                f"<div style='margin-left:18px;margin-bottom:4px;'>• {clean}</div>"
            )
            continue

        # ---------- NORMAL TEXT ----------
        if stripped:
            clean = clean_text(stripped)
            final_html.append(f"<div>{clean}</div>")

    # Render table if ends last
    if inside_table and table_rows:
        final_html.append(render_table(table_rows))

    return "<div class='result-card'>" + "\n".join(final_html) + "</div>"



# Define callbacks for each function
def generate_objectives_page(topic):
    raw = generate_objectives(topic)
    html = format_output(raw)
    return html

def generate_lesson_plan_page(topic):
    if not topic:
        return "<div class='card'><p>Please enter a topic first.</p></div>"
    objectives = generate_objectives(topic)
    raw= generate_lesson_plan(objectives)
    output = format_output(raw)
    return output

def generate_blooms_page(topic):
    if not topic:
        return "<div class='card'><p>Please enter a topic first.</p></div>"
    objectives = generate_objectives(topic)
    raw = generate_blooms_taxonomy(objectives)
    output = format_output(raw)
    return output

def generate_materials_page(topic):
    raw = generate_teaching_materials(topic)
    output = format_output(raw)
    return output

def generate_rubric_page(topic):
    raw = generate_rubric(topic)
    output = format_output(raw)
    return output

def generate_clos_page(topic):
    raw = generate_CLOs(topic)
    output = format_output(raw)
    return output

def generate_edtech_page(topic):
    objectives = generate_objectives(topic)
    lesson_plan = generate_lesson_plan(objectives)
    raw = recommend_edtech_tools(lesson_plan)
    output = format_output(raw)
    return output


def export_to_pdf(html_content):
    import os
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    import re

    # Create safe folder
    output_dir = "generated_files"
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, "generated_output.pdf")

    # Register Unicode font
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))

    stylesheet = getSampleStyleSheet()
    style = stylesheet["Normal"]
    style.fontName = "HeiseiMin-W3"
    style.fontSize = 11
    style.leading = 15

    # Clean HTML → Plain text
    clean_text = re.sub("<[^>]*>", "", html_content)
    clean_text = clean_text.replace("&nbsp;", " ")

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    story = [Paragraph(clean_text.replace("\n", "<br/>"), style)]

    doc.build(story)

    return file_path



custom_css = """
/* Full page gradient background */
body, html, .gradio-container, .block-container {
    background: linear-gradient(135deg, #091833, #123466, #145f7a) !important;
    min-height: 100vh;
    padding: 0;
    margin: 0;
}

/* Headings */
h1, h2 {
    color: white!important;
    text-align: center;
    font-weight: bolder;
    margin-top: 20px;
    font-size: 2rem;
}

/* Card styling */
.card {
    background-color: white !important;
    border-radius: 25px !important;
    padding: 30px;
    width: 90%;
    max-width: 900px;
    margin: 30px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}



/* Topic input container */
.topic-container {
    width: 90%;
    max-width: 900px;
    margin: 5px auto;  /* closer to card */
}

/* Style the input inside container */
.topic-container input[type="text"] {
    width: 100% !important;
    border-radius: 25px !important;  /* increased roundness */
    padding: 15px 20px !important;   /* bigger padding for nicer look */
    font-size: 16px !important;
    border: none !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}


/* Buttons styling */
button.custom-btn {
    border: none !important;
    border-radius: 15px !important;
    padding: 15px !important;
    font-size: 16px !important;
    color: white !important;
    cursor: pointer !important;
    transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s;
}

/* Hover effect */
button.custom-btn:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
    opacity: 0.9 !important;
}
/* Result card */
.result-card {
    background: white !important;
    border-radius: 25px !important;
    padding: 25px !important;
    width: 90%;
    max-width: 900px;
    margin: 20px auto !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.3) !important;
    overflow-wrap: break-word !important;
}

/* Heading style */
.result-card .result-heading {
    color: #1E90FF !important;
    font-weight: 900 !important;
    font-size: 22px !important;
    padding-top: 10px !important;
    padding-bottom: 4px !important;
}


/* Table wrapper (prevents overflow) */
.table-container {
    overflow-x: auto;
    margin-top: 10px;
    margin-bottom: 15px;
}

/* Table styling */
.result-table {
    width: 100%;
    border-collapse: collapse;
    border: 2px solid #1E90FF;
    border-radius: 10px;
}

.result-table th {
    background: #1E90FF;
    color: white;
    padding: 10px;
    border: 1px solid #1E90FF;
    font-weight: bold;
    text-align: left;
}

.result-table td {
    padding: 10px;
    border: 1px solid #1E90FF;
}

/* Prevent floating */
.result-card div {
    display: block;
}



/* Export button look */
button.custom-btn {
    border-radius: 20px !important;
    padding: 14px 22px !important;
}

/* Button gradient backgrounds */
button.custom-btn.bg1 { background: linear-gradient(135deg, #20BF55, #01BAEF) !important; }
button.custom-btn.bg2 { background: linear-gradient(135deg, #4B79A1, #283E51) !important; }
button.custom-btn.bg3 { background: linear-gradient(135deg, #FF416C, #FF4B2B) !important; }
button.custom-btn.bg4 { background: linear-gradient(135deg, #9D50BB, #6E48AA) !important; }
button.custom-btn.bg5 { background: linear-gradient(135deg, #11998e, #38ef7d) !important; }
button.custom-btn.bg6 { background: linear-gradient(135deg, #fc4a1a, #f7b733) !important; }
button.custom-btn.bg7 { background: linear-gradient(135deg, #36D1DC, #5B86E5) !important; }
button.custom-btn.bg2 {
    background: linear-gradient(135deg, #4B79A1, #283E51) !important;
}

"""

# Gradio app
with gr.Blocks() as demo:
    gr.HTML(f"<style>{custom_css}</style>")

    gr.Markdown("<h1>📘Education Toolkit</h1>")
    gr.Markdown("<h2>Enter topic and select an option:</h2>")

    # Topic input wrapped in a container
    with gr.Column(elem_classes="topic-container"):
        topic_input = gr.Textbox(label="", placeholder="Type your topic here...")

    # Single card for buttons
    with gr.Column(elem_classes="card"):
        # First row
        with gr.Row():
            lo_btn = gr.Button("Learning objectives", elem_classes="custom-btn bg1")
            lp_btn = gr.Button("Lesson plans",       elem_classes="custom-btn bg2")
            bt_btn = gr.Button("Bloom’s Taxonomy",   elem_classes="custom-btn bg3")

        # Second row
        with gr.Row():
            clo_btn = gr.Button("CLOs",               elem_classes="custom-btn bg4")
            mat_btn = gr.Button("Teaching materials",elem_classes="custom-btn bg5")
            rub_btn = gr.Button("Assessment rubrics",elem_classes="custom-btn bg6")

        # Third row
        with gr.Row():
            edt_btn = gr.Button("EdTech Tools",      elem_classes="custom-btn bg7")

    output_html = gr.HTML()
    export_pdf_btn = gr.Button("⬇ Export as PDF", elem_classes="custom-btn bg2")


    # Connect buttons to callbacks
    lo_btn.click(generate_objectives_page, inputs=topic_input, outputs=output_html)
    lp_btn.click(generate_lesson_plan_page, inputs=topic_input, outputs=output_html)
    bt_btn.click(generate_blooms_page, inputs=topic_input, outputs=output_html)
    clo_btn.click(generate_clos_page, inputs=topic_input, outputs=output_html)
    mat_btn.click(generate_materials_page, inputs=topic_input, outputs=output_html)
    rub_btn.click(generate_rubric_page, inputs=topic_input, outputs=output_html)
    edt_btn.click(generate_edtech_page, inputs=topic_input, outputs=output_html)
    export_pdf_btn.click(export_to_pdf, inputs=output_html, outputs=gr.File())


demo.launch()
