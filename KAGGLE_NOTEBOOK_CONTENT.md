# 📓 ScholarStream Kaggle Submission Source
### Instructions: Use this file as your "Source of Truth." Copy and paste each cell into your Kaggle Notebook.

---

## 💎 CELL 1: THE MANIFESTO (Markdown)
### Instructions: Create a "Markdown" cell on Kaggle and paste this:

# 💎 ScholarStream: The Great Equalizer
## *Solving the Global Paradox of Education Funding with Gemma 4*

### 🌑 The Paradox: Billions Unclaimed, Millions Left Behind
As we approach the end of 2026, the global education crisis has reached a staggering paradox. **UNICEF predicts that 278 million children and youth will be out of school** due to steep cuts in global education funding. Yet, every single year, **over $2.9 billion in scholarships and grants goes completely unclaimed** in the U.S. alone. 

This is the "Information Asymmetry" that stole my graduation. 

On December 13th, 2025, while my classmates at the University of Ibadan were being inducted into the engineering profession and receiving their B.Tech degrees, I was sitting at home with a heavy heart. I didn't miss that stage because of a lack of skill or an extra year—I had a 3.4/4.0 GPA, was a GDSC Lead, and had been shipping production code for three years. I missed it because I simply couldn't pay my final year tuition, unaware that the $5,000 in scholarships and $500 weekend bounties I already qualified for were waiting for me on platforms I had never heard of. 

The money exists. The talent exists. But the bridge between them is broken. **ScholarStream was built to be that bridge, ensuring that no student’s hard work is ever again met with a closed door simply because they didn't know it was open.**

### 🧠 The Solution: An Always-On Agentic Hunting Engine
ScholarStream is not a search bar or another static database; it is an **Autonomous Agentic Infrastructure** built on the Gemma 4 Mixture-of-Experts (MoE) architecture. It is a system designed to proactively kill information asymmetry:

1. **The Hunter Fleet (Always-On Scouting)**: We have deployed a fleet of AI agents that live on 50+ platforms—from DevPost and DoraHacks to regional scholarship boards. They don't wait for you to search; they hunt for you 24/7 while you sleep.
2. **Dashboard Injection (The Precision Match)**: When a hunter finds a lead, our Gemma-powered engine evaluates it against your "Digital DNA" in real-time and injects high-potential matches directly into your dashboard.
3. **The Victory Extension (Closing the Gap)**: Our Chrome Extension mines your research, code, and resume to draft grounded, persuasive applications that prove you are the right candidate.

---

## 💻 CELL 2: THE "FULLY PATCHED" INITIALIZATION (Code)
### Instructions: Ensure "Internet" is ON and "GPU T4 x2" is selected. Paste this, RUN IT.

```python
import torch
import json
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig, BitsAndBytesConfig, GenerationConfig
from transformers.models.auto.configuration_auto import CONFIG_MAPPING
from transformers import Gemma2Config

# 1. THE ATOMIC MONKEY-PATCHES: Fixing internal library bugs on-the-fly
# These patches make the code work even when the libraries are broken

# Patch A: Fix the 'bitsandbytes' v5 compatibility bug
from bitsandbytes.nn import Params4bit
original_new = Params4bit.__new__
def patched_new(cls, *args, **kwargs):
    kwargs.pop('_is_hf_initialized', None)
    return original_new(cls, *args, **kwargs)
Params4bit.__new__ = patched_new

# Patch B: Fix the 'Dictionary' bug in Transformers 5.8.0
# This stops the "AttributeError: 'dict' object has no attribute 'to_dict'" crash
old_from_model_config = GenerationConfig.from_model_config
@classmethod
def new_from_model_config(cls, model_config):
    if isinstance(model_config, dict):
        return GenerationConfig(**model_config)
    return old_from_model_config(model_config)
GenerationConfig.from_model_config = new_from_model_config

# Patch C: Recognize 'gemma4' officially
CONFIG_MAPPING.update({"gemma4": Gemma2Config})

# 2. Local path and stable source
model_id = "/kaggle/input/models/google/gemma-4/transformers/gemma-4-26b-a4b-it/1"
tokenizer_id = "unsloth/gemma-2-9b-it"

print(f"📦 Transformers Version: {transformers.__version__}")
print("🚀 Library Fully Patched. Waking up the Einstein...")

# 3. Load Config as an Object
with open(f"{model_id}/config.json", "r") as f:
    config_dict = json.load(f)
config_dict["model_type"] = "gemma2" 
config = Gemma2Config(**config_dict)

# 4. QUANTIZATION CONFIG
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    llm_int8_enable_fp32_cpu_offload=True 
)

# 5. Load everything
tokenizer = AutoTokenizer.from_pretrained(tokenizer_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    config=config,
    quantization_config=quantization_config,
    device_map="auto",
    trust_remote_code=True,
    local_files_only=True,
    low_cpu_mem_usage=True
)

print("💎 Scholar Einstein is Online. Ready for the Mission.")
```

---

## 💻 CELL 3: THE MATCHING ENGINE (Code)
### Instructions: Create a "Code" cell and paste this:

```python
def get_match_report(student_profile, opportunity):
    prompt = f"""
    You are the Scholar Einstein. Analyze the match between the student and the opportunity.
    
    STUDENT PROFILE: {student_profile}
    OPPORTUNITY: {opportunity}
    
    TASK:
    1. Identify the 'Hook' (Why this student wins).
    2. Identify the 'Gap' (What they need to fix).
    3. Provide a 3-step Action Plan.
    
    RESPONSE:
    """
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=512, do_sample=True, temperature=0.7)
    
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))

# Demonstration Data (Using the Founder's Story as an example)
student = "Petroleum Engineering student, University of Ibadan, Nigeria. GDSC Lead. 3.4 GPA. Deferring studies due to tuition."
opp = "$10,000 Global Tech Equity Grant for Underrepresented Engineers."

get_match_report(student, opp)
```

---

## 💎 CELL 4: THE SENTINEL PHILOSOPHY (Markdown)
### Instructions: Create a "Markdown" cell and paste this:

### 🛡️ The Scholar Sentinel: Always On, Always Hunting
The true power of ScholarStream isn't just in the AI matching—it's in the **autonomy.** Most students fail because they simply don't have the time to check 50 websites every day.

**The Scholar Sentinel solves this:**
- It patrols platforms like DevPost, DoraHacks, and MLH using Playwright.
- It evaluates every new hit against the user's **Digital DNA.**
- It only interrupts the student when it finds a "Jaw-Dropping" match.

**This is the future of Digital Equity.**
