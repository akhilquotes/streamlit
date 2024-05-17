import streamlit as st

st.set_page_config(page_title="Contract Upload", page_icon="📈")

st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

import os
# enable hf_transfer for faster ckpt download
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from deepspeed.linear.config import QuantizationConfig

tokenizer = AutoTokenizer.from_pretrained(
    "Snowflake/snowflake-arctic-instruct",
    trust_remote_code=True
)
quant_config = QuantizationConfig(q_bits=8)

model = AutoModelForCausalLM.from_pretrained(
    "Snowflake/snowflake-arctic-instruct",
    trust_remote_code=True,
    low_cpu_mem_usage=True,
    device_map="auto",
    ds_quantization_config=quant_config,
    max_memory={i: "150GiB" for i in range(8)},
    torch_dtype=torch.bfloat16)


content = "5x + 35 = 7x - 60 + 10. Solve for x"
messages = [{"role": "user", "content": content}]
input_ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")

outputs = model.generate(input_ids=input_ids, max_new_tokens=256)
st.write(tokenizer.decode(outputs[0]))
