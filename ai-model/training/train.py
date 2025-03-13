import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import Dataset

# Load JSON Data
with open("../data/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert JSON into training format (Q/A style)
def format_data(json_data):
    dataset = []
    for dept in json_data["departments"]:
        dataset.append({
            "question": f"Who is the HOD of {dept['name']}?",
            "answer": dept["hod"]
        })
        for faculty in dept["faculty"]:
            dataset.append({
                "question": f"Who is {faculty['name']}?",
                "answer": f"{faculty['designation']} in {faculty['department']}, specializes in {', '.join(faculty['research_areas'])}."
            })
    return dataset

formatted_data = format_data(data)

# Convert to Hugging Face Dataset
dataset = Dataset.from_dict({
    "question": [item["question"] for item in formatted_data],
    "answer": [item["answer"] for item in formatted_data]
})

# Load Model & Tokenizer
model_name = "distilgpt2"  # Replace with "meta-llama/Llama-2-7b-chat-hf" for better performance
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Ensure a padding token is set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token  # Use EOS token as padding

# Tokenize Dataset
def tokenize_function(examples):
    inputs = tokenizer(examples["question"], padding="max_length", truncation=True, max_length=512)
    labels = tokenizer(examples["answer"], padding="max_length", truncation=True, max_length=512)
    
    inputs["labels"] = labels["input_ids"]  # Assign labels for loss calculation
    
    return inputs


tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Training Arguments
training_args = TrainingArguments(
    output_dir="./trained_model",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    logging_dir="./logs",
    save_total_limit=2  # Keeps only the last 2 checkpoints to save space
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    eval_dataset=tokenized_dataset
)

# Train Model
trainer.train()

# Save Model
model.save_pretrained("./college_chatbot_model")
tokenizer.save_pretrained("./college_chatbot_model")

print("Model training complete! 🚀")