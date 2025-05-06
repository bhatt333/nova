# from openai import OpenAI

# client = OpenAI(api_key="sk-08cfc88960974acba19cb40b893a90c7", base_url="https://api.deepseek.com/v1")

# chat = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "user", "content": "What is Flask?"}
#     ]
# )

# print(chat.choices[0].message.content)

from flask import Flask, request,jsonify,render_template
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key="sk-08cfc88960974acba19cb40b893a90c7",
    base_url="https://api.deepseek.com/v1"
)
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {   
                "role": "assistant",
                "content": f"""
                    You are Nova AI,act like NOVA AI and also mention NOVA AI, a polite, professional digital secretary. Always respond in HTML format, using a heading in rgb(61,12,12), and paragraphs in black. Do not use markdown symbols or asterisks.
                    \n\n
                    {user_input.strip()}
                """
                
            },
            {   
                "role": "user",
                "content": f"""
                    Please respond in clear,specially not using this symbol(**),  
                    must be a html response also describe in  well-formatted sentences,
                    to the following:
                    use this colour in the heading rgb(61,12,12) and paragraph must b in black colour also remove this symbols (```html ```) and in clean format
                    return all in a single div style must be in attributes dont give complete html tags 
                    
                    \n\n
                    {user_input.strip()}
                """
            }
        ]
    )
    
    print(response)

    return jsonify({"response": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
