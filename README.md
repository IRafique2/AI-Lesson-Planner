# **AI Lesson Planner**

## **Overview**

The AI Lesson Planner is an interactive web application designed for educators, trainers, instructional designers, and students who need fast, structured, and high-quality learning materials. By leveraging a custom Groq-powered LLM and LangChain pipelines, the app can automatically generate:

* Learning objectives
* Detailed lesson plans
* Bloom’s Taxonomy classifications
* Course Learning Outcomes (CLOs)
* Teaching materials 
* Assessment rubrics
* EdTech tool recommendations




## **Key Features**

* **Learning Objectives:** Generates well-structured general and specific objectives.
* **Lesson Planning:** Produces full, teacher-ready lesson plans.
* **Bloom’s Taxonomy:** Classifies outcomes across all levels with rewritten measurable statements.
* **Teaching Materials:** Includes worksheets, quizzes, discussion prompts, PPT outlines, and class activities.
* **Rubrics:** Creates clear, practical assessment rubrics.
* **EdTech Tools:** Recommends tools aligned with the lesson content.
* **Course Learning Outcomes (CLOs)**:enerates measurable, higher-order outcomes mapped to Bloom’s levels for course-level mastery.



## **Technology Stack**

* **GROQ** – User interface
* **Groq API** – LLM inference via a custom `GroqLLM` wrapper
* **LangChain** – Prompt templates and processing pipelines
* **dotenv** – Environment variable management



## **Project Structure**

```
├── app.py
├── README.md
├── .env
└── requirements.txt
```



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
   groq  app.py
   ```



## **Usage**

Enter a lesson topic in the sidebar and select an action. The generated content will appear in the output panel, formatted for immediate classroom or planning use.





## **Known Limitations**

* Requires a valid Groq API key if running locally
* Long outputs may take some time depending on the model
* Generation quality depends heavily on prompt design — template refinement may be needed for best results



## **Future Enhancements**

Potential improvements include:

* Editable text fields for users to refine LLM outputs
* Support for multi-topic lesson sequences
* A persistent project workspace or user accounts
* Enhanced UI / UX design


## **License**

This project is provided under an open and modifiable structure. Add your preferred license if distributing publicly.


## **Try It Online / Contact**

You can try the hosted version here:
[**AI Lesson Planner on Hugging Face Spaces**](https://huggingface.co/spaces/iRafique/AiEducationtoolkit)

For questions, feedback or contributions, feel free to open an issue or pull request on the repo, or just connect here.



