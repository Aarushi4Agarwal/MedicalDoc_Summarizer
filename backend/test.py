
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

import google.generativeai as genai
GEMINI_API_KEY="{your api key}"
 
#configure gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
sample_pdf = genai.upload_file("C:\\Users\\aarushia\\Downloads\\sample.pdf")
response = model.generate_content(["Give me a summary of this pdf file.", sample_pdf])
print(response.text)
