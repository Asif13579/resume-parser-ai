# import libraries
import re
import json
import yaml
from transformers import pipeline

CONFIG_PATH=r"config.yaml"

# Optional config loading
with open (CONFIG_PATH) as file:
    data=yaml.load(file,Loader=yaml.FullLoader)

# Load model locally
pipe = pipeline("text2text-generation",model="microsoft/phi-3-mini-4k-instruct")

def ats_extractor(resume_data):
    # limit resume length
    #resume_data=resume_data[:1500]

    prompt=f"""
You are a strict JSON generator.

Extract resume information and return ONLY valid JSON.

RULES:
- Output must be valid JSON only
- No explanations
- No markdown
- No extra text
- All keys must be in double quotes
- If value not found use null

JSON FORMAT:
{{
  "full_name": "",
  "email": "",
  "github": "",
  "linkedin": "",
  "technical_skills": [],
  "soft_skills": [],
  "employment_details": ""
}}

RESUME:
{resume_data[:2000]}
"""
    response=pipe(prompt,max_new_tokens=300)
    
    raw_response =response[0]["generated_text"]
    print("RAW RESPONSE:\n", raw_response)
    # Remove markdown code blocks if any
    raw_response=raw_response.replace("```json","").replace("```","")
    # extract json safely
    match=re.search(r'\{[\s\S]*\}', raw_response)
    if not match:
        return {
            "error": "No JSON found",
            "raw_response": raw_response
        }

    json_text=match.group(0)
    # Fix common LLM mistakes
    json_text = json_text.replace("'", '"')

    try:
        return json.loads(json_text)

    except Exception as e:
        return {
            "error": str(e),
            "raw_response": raw_response,
            "extracted_json": json_text
        }

# if __name__ == "__main__":

#     sample = """
#     John Doe
#     Email: johndoe@gmail.com
#     GitHub: github.com/johndoe
#     LinkedIn: linkedin.com/in/johndoe

#     Skills:
#     Python, Machine Learning, SQL, Communication

#     Experience:
#     Data Scientist at ABC Company for 2 years
#     """

#     result = ats_extractor(sample)

#     print(result)