from google import genai 
from google.genai import types

client = genai.Client()

def ask_gemini(prompt: str,context: str ,think :bool = False) -> str:
  
    model = "gemini-3-flash-preview"
    if(think == True):
        model = "gemini-3.1-pro-preview"

    contents = types.Content(
        role ='user',
        parts = [types.Part(text=context),types.Part(text=prompt)]
    )

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0.7,
            top_p=0.9,
            top_k=40,
        ),
    )

    client.close()
    return response.text


if __name__ == "__main__":
    user_prompt = input("Enter prompt: ").strip()
    context = ""
    if not user_prompt:
        print("Prompt cannot be empty.")
    else:
        print(ask_gemini(user_prompt, context))