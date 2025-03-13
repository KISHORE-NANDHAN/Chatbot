from transformers import AutoModelForCausalLM, AutoTokenizer

# Load trained model
model_path = "../training/college_chatbot_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

def get_response(question):
    inputs = tokenizer(question, return_tensors="pt")
    output = model.generate(**inputs, max_length=100)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Example usage
while True:
    question = input("Ask a question: ")
    if question.lower() == "exit":
        break
    print(get_response(question))
