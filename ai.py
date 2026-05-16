import google.generativeai as genai
import json
import os

genai.configure(api_key=os.environ.get("YOUR API KEY(GEMINI USED)"))

def analyze_resume(resume_text, user_goal):
    prompt = f"""You are a senior software engineer and hiring manager.
    Evaluate the resume based on user's goal.
    User goal: "{user_goal}"
        
    STRICT RULES:
    - Extract only relevant skills for this goal
    - Remove irrelevant tools (e.g. Excel for backend roles)
    - Identify real gaps
    - Generate roadmap only for missing fields
    - Make output different based on goal

    Return ONLY valid JSON, no extra text:
    {{
        "skills": [],
        "missing_skills": [],
        "roadmap": [],
        "interview_questions": []
    }}

    Resume:
    {resume_text}
    """

    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={"temperature": 0.3}
        )

        response = model.generate_content(prompt)
        content = response.text.strip()

        # Clean markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]

        start = content.find("{")
        end = content.rfind("}") + 1
        return json.loads(content[start:end])

    except Exception as e:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }






































# from openai import OpenAI
# import json 

# client = OpenAI()

# def analyze_resume(resume_text, user_goal):
#     prompt = f"""  you are a senior software engineer and hiring manager.
#     evalueate the resume based on user's goal.
#     user goal : "{user_goal}"
        
#     STRICT RULE:
#     - Extract only relevant skills for this goal
#     -Remove irrelevant tools [excel for backend, etc]
#     - identify real gaps 
#     - Generate roadmap only for missing fields
#     - make output Different based on goal
#     return only JSON 
#     {{
#     "skills: [],
#     "missing_skills":[],
#     "roadmap":[],
#     "interview_questions":[]
#     }}
#     Resume:
#     {resume_text} 

    
#     """
#         try:
#             response = cilent.chat.completions.create(
#                 model = "",
#                 temperature = 0.3,
#                 message = [
#                     {"role":"system", "content":"You are a strict hiring manager"}
#                     {"role":"user","content":prompt}
#                 ]
#             )
#             content = response.choices[0].message.content.strip()
#             start = content.find("{")
#             end = content.rfind("}") + 1
#             return json.loads(content[start:end])
    
#         except Exception as e:
#             return {
#                 "skills":[],
#                 "missing_skills":[],
#                 "roadmap":[],
#                 "interview_questions":[],
#                 "error":str(e)

#             }
        
