import ollama

from config.config import OLLAMA_MODEL

from memory.memory_manager import (
    search_memory,
    show_memories,
    delete_by_keyword,
    save_smart_memory,
    save_web_knowledge,
)

from tools.calculator import (
    calculator,
    is_calculation,
)

from tools.datetime_tool import (
    get_current_date,
    get_current_time,
)

from tools.web_search import (
    web_search,
    needs_web_search,
    answer_from_web,
)


# ==========================================
# AI AGENT START
# ==========================================

print("🤖 AI Agent Starting...")
print("🧠 Memory connected!")
print("🤖 AI Agent Ready!")


conversation_history = []


# ==========================================
# MAIN CHAT LOOP
# ==========================================

while True:

    user_input = input("\nYou: ").strip()

    # --------------------------------------
    # EMPTY INPUT
    # --------------------------------------

    if not user_input:
        print("Agent: Please type something.")
        continue

    text = user_input.lower().strip()


    # ======================================
    # EXIT
    # ======================================

    if text == "exit":
        print("Agent: Bye! 👋")
        break


    # ======================================
    # DATE TOOL
    # ======================================

    date_keywords = [
        "what is today's date",
        "what's today's date",
        "today's date",
        "current date",
        "what date is it",
        "what is the date",
        "tell me today's date",
    ]

    if any(keyword in text for keyword in date_keywords):

        print(
            "\nAgent: Today's date:",
            get_current_date()
        )

        continue


    # ======================================
    # TIME TOOL
    # ======================================

    time_keywords = [
        "what time is it",
        "what is the time",
        "what's the time",
        "current time",
        "time now",
        "tell me the time",
    ]

    if any(keyword in text for keyword in time_keywords):

        print(
            "\nAgent: Current time:",
            get_current_time()
        )

        continue


    # ======================================
    # CALCULATOR
    # ======================================

    if text.startswith("calculate "):

        expression = user_input[
            len("calculate "):
        ].strip()

        result = calculator(expression)

        print("\nAgent:", result)

        continue


    # ======================================
    # AUTOMATIC CALCULATOR
    # ======================================

    if is_calculation(text):

        result = calculator(text)

        print("\nAgent:", result)

        continue


    # ======================================
    # MANUAL WEB SEARCH
    # ======================================

    if text.startswith("search "):

        query = user_input[
            len("search "):
        ].strip()

        if not query:

            print(
                "Agent: Please tell me what to search."
            )

            continue

        results = web_search(query)

        if not results:

            print(
                "Agent: No search results found."
            )

            continue

        answer = answer_from_web(
            user_input,
            results
        )

        print("\nAgent:", answer)

        # Save useful web knowledge
        save_web_knowledge(
            user_input,
            answer
        )

        continue


    # ======================================
    # AUTOMATIC WEB SEARCH
    # ======================================

    if needs_web_search(text):

        results = web_search(user_input)

        if results:

            answer = answer_from_web(
                user_input,
                results
            )

            print("\nAgent:", answer)

            # Self-learning
            save_web_knowledge(
                user_input,
                answer
            )

        else:

            print(
                "\nAgent: I could not find fresh information on the web."
            )

        continue


    # ======================================
    # SHOW MEMORIES
    # ======================================

    if text in [
        "show my memories",
        "show memories",
        "my memories",
    ]:

        show_memories()

        continue


    # ======================================
    # FORGET / DELETE MEMORY
    # ======================================

    if (
        text.startswith("forget ")
        or text.startswith("delete ")
        or text.startswith("remove ")
    ):

        keyword = user_input.split(
            " ",
            1
        )[1].strip()

        keyword = keyword.replace(
            "that i am learning",
            ""
        ).strip()

        keyword = keyword.replace(
            "that i'm learning",
            ""
        ).strip()

        keyword = keyword.replace(
            "i am learning",
            ""
        ).strip()

        keyword = keyword.replace(
            "i'm learning",
            ""
        ).strip()

        if keyword:

            delete_by_keyword(keyword)

        else:

            print(
                "Agent: Please tell me what you want me to forget."
            )

        continue


    # ======================================
    # SEARCH LONG-TERM MEMORY
    # ======================================

    memories = search_memory(
        user_input
    )

    memory_text = "\n".join(
        item.get("memory", "")
        for item in memories.get(
            "results",
            []
        )
    )


    # ======================================
    # SAVE USER MESSAGE IN HISTORY
    # ======================================

    conversation_history.append(
        {
            "role": "user",
            "content": user_input,
        }
    )


    # ======================================
    # LAST 10 MESSAGES
    # ======================================

    recent_history = conversation_history[-10:]


    # ======================================
    # CREATE HISTORY TEXT
    # ======================================

    history_text = ""

    for message in recent_history:

        role = message["role"]
        content = message["content"]

        if role == "user":

            history_text += (
                f"User: {content}\n"
            )

        else:

            history_text += (
                f"Assistant: {content}\n"
            )


    # ======================================
    # AI PROMPT
    # ======================================

    prompt = f"""
You are a helpful AI assistant.

Relevant long-term memories:

{memory_text}

Recent conversation:

{history_text}

Current user message:

{user_input}

IMPORTANT RULES:

1. Use long-term memories only when relevant.
2. Use recent conversation to understand context.
3. If the user says "it", "that", "this", "he",
   "she", or similar words, use recent conversation.
4. Do not invent personal information.
5. If information is not available, say you don't know.
6. Give a clear and concise answer.
"""


    # ======================================
    # ASK OLLAMA
    # ======================================

    try:

        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        answer = response[
            "message"
        ][
            "content"
        ]

    except Exception as e:

        print(
            "⚠️ Ollama error:",
            e
        )

        continue


    # ======================================
    # SAVE ASSISTANT RESPONSE
    # ======================================

    conversation_history.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


    # ======================================
    # DISPLAY ANSWER
    # ======================================

    print(
        "\nAgent:",
        answer
    )


    # ======================================
    # SMART MEMORY
    # ======================================

    save_smart_memory(
        user_input
    )