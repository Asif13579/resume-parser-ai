from transformers import pipeline

pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)