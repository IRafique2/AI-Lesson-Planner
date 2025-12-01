# **AI Lesson Planner**

## **Overview**

The **AI Lesson Planner** is a streamlined Streamlit application designed to support educators by automating the creation of high-quality instructional materials. 
Powered by a custom Groq LLM wrapper and LangChain workflows, the tool generates clear learning objectives,
comprehensive lesson plans, Bloom’s Taxonomy classifications, teaching materials, rubrics, and tailored EdTech recommendations—all from a single topic input.

A live version is available on Hugging Face Spaces:
**[https://huggingface.co/spaces/iRafique/Lesson_planner](https://huggingface.co/spaces/iRafique/Lesson_planner)**

---

## **Key Features**

* **Learning Objectives:** Generates well-structured general and specific objectives.
* **Lesson Planning:** Produces full, teacher-ready lesson plans.
* **Bloom’s Taxonomy:** Classifies outcomes across all levels with rewritten measurable statements.
* **Teaching Materials:** Includes worksheets, quizzes, discussion prompts, PPT outlines, and class activities.
* **Rubrics:** Creates clear, practical assessment rubrics.
* **EdTech Tools:** Recommends tools aligned with the lesson content.

---

## **Technology Stack**

* **Streamlit** – User interface
* **Groq API** – LLM inference via a custom `GroqLLM` wrapper
* **LangChain** – Prompt templates and processing pipelines
* **dotenv** – Environment variable management

---

## **Installation & Setup**

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file and add your API key:

   ```
   GROQ_API_KEY=your_api_key_here
   ```
3. Launch the application:

   ```bash
   streamlit run app.py
   ```

---

## **Usage**

Enter a lesson topic in the sidebar and select an action. The generated content will appear in the output panel, formatted for immediate classroom or planning use.

---

## **License**

This project is open for personal, academic, and developmental use. Add your preferred license terms if distributing or deploying publicly.

---

