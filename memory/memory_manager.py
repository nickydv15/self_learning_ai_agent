import ollama

from mem0 import Memory

from config.config import (
    MEM0_CONFIG,
    USER_ID,
)


# ==============================
# MEM0 INITIALIZATION
# ==============================

memory = Memory.from_config(MEM0_CONFIG)


# ==============================
# SEARCH MEMORY
# ==============================

def search_memory(query):
    try:
        results = memory.search(
            query,
            filters={
                "user_id": USER_ID
            }
        )

        return results

    except Exception as e:
        print("Memory Search Error:", e)
        return {
            "results": []
        }


# ==============================
# SHOW ALL MEMORIES
# ==============================

def show_memories():
    try:
        results = memory.get_all(
            filters={
                "user_id": USER_ID
            }
        )

        memories = results.get("results", [])

        if not memories:
            print("\n🧠 No memories found.")
            return

        print("\n🧠 Your Memories:")

        for index, item in enumerate(memories, start=1):
            print(f"{index}. {item.get('memory', '')}")

    except Exception as e:
        print("Memory Error:", e)


# ==============================
# DELETE MEMORY
# ==============================

def delete_by_keyword(keyword):
    try:
        results = memory.get_all(
            filters={
                "user_id": USER_ID
            }
        )

        memories = results.get("results", [])

        found = False

        for item in memories:

            memory_text = item.get(
                "memory",
                ""
            )

            if keyword.lower() in memory_text.lower():

                memory_id = item.get("id")

                if memory_id:

                    memory.delete(memory_id)

                    print(
                        f"\n🗑️ Memory deleted: {memory_text}"
                    )

                    found = True

        if not found:
            print(
                f"\n🧠 No memory found for: {keyword}"
            )

    except Exception as e:
        print("Delete Memory Error:", e)


# ==============================
# SMART MEMORY
# ==============================

def save_smart_memory(user_input):

    text = user_input.lower().strip()

    important_patterns = [

        "my name is",
        "i am nick",
        "i'm nick",

        "i am learning",
        "i'm learning",
        "i want to learn",
        "i am studying",
        "i'm studying",

        "i know",
        "i can",
        "my skill",
        "my skills",

        "my goal is",
        "my goal",
        "i want to become",
        "i want to be",

        "i like",
        "i love",
        "i prefer",
        "i don't like",
        "i hate",

        "my project",
        "this project",
        "my ai agent",
    ]

    is_important = any(
        pattern in text
        for pattern in important_patterns
    )

    if not is_important:
        print("🧠 No important memory.")
        return

    try:

        existing = search_memory(user_input)

        existing_memories = existing.get(
            "results",
            []
        )

        for item in existing_memories:

            old_memory = item.get(
                "memory",
                ""
            )

            if old_memory.lower() == text:

                print("🧠 Memory already exists.")
                return

        memory.add(
            user_input,
            user_id=USER_ID
        )

        print("🧠 Important Memory Saved!")

    except Exception as e:

        print(
            "Memory Save Error:",
            e
        )


# ==============================
# SAVE WEB KNOWLEDGE
# ==============================

def save_web_knowledge(
    user_question,
    answer
):

    try:

        extraction_prompt = f"""
You are a knowledge extraction system.

Question:
{user_question}

Answer:
{answer}

Extract only useful factual knowledge
that may remain useful in future.

Do not include:
- greetings
- opinions
- temporary wording
- unnecessary explanations

Return only the reusable knowledge.
"""

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": extraction_prompt
                }
            ]
        )

        knowledge = response[
            "message"
        ][
            "content"
        ].strip()

        if not knowledge:
            return

        existing = search_memory(
            knowledge
        )

        existing_memories = existing.get(
            "results",
            []
        )

        for item in existing_memories:

            old_memory = item.get(
                "memory",
                ""
            )

            if knowledge.lower() in old_memory.lower():

                print(
                    "🧠 Web knowledge already exists."
                )

                return

        memory.add(
            f"Learned web knowledge: {knowledge}",
            user_id=USER_ID
        )

        print(
            "🧠 Web Knowledge Saved!"
        )

    except Exception as e:

        print(
            "Web Knowledge Save Error:",
            e
        )