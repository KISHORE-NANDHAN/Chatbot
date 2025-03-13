from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset

# Load tokenizer and model
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.eos_token  # Use EOS token as padding

model = AutoModelForCausalLM.from_pretrained(model_name)

# Load dataset
dataset = load_dataset("text", data_files={"train": "../data/college_knowledge.txt"})
dataset = dataset["train"].train_test_split(test_size=0.2)  # 80% train, 20% validation

# Tokenization function
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

# Apply tokenization
tokenized_train = dataset["train"].map(tokenize_function, batched=True, remove_columns=["text"])
tokenized_eval = dataset["test"].map(tokenize_function, batched=True, remove_columns=["text"])

# Training settings
training_args = TrainingArguments(
    output_dir="./college_chatbot_model",
    evaluation_strategy="epoch",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=5,
    save_total_limit=2,
    save_steps=500,
    logging_dir="./logs",
    remove_unused_columns=False  # ✅ Prevents auto-removal of required columns
)

# Data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_eval,  # ✅ Properly tokenized evaluation dataset
    tokenizer=tokenizer,
    data_collator=data_collator
)

# Train model
trainer.train()
trainer.save_model("../training/college_chatbot_model")
print("✅ Model training complete!")
