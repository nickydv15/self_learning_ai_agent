# ==============================
# WEB SEARCH TOOL
# ==============================

from ddgs import DDGS
import ollama


# ==============================
# WEB SEARCH
# ==============================

def web_search(query):

    try:
        print("\n🌐 Searching the web...")

        results = DDGS().text(
            query,
            max_results=5
        )

        if not results:
            return []

        return results

    except Exception as e:
        print("⚠️ Web search error:", e)
        return []


# ==============================
# WEB SEARCH DECISION
# ==============================

def needs_web_search(text):

    text = text.lower()

    web_keywords = [
        "current",
        "currently",
        "latest",
        "today",
        "now",
        "recent",
        "recently",
        "news",
        "who is the pm",
        "prime minister",
        "president",
        "ceo",
        "latest version",
        "current version",
        "price",
        "weather",
        "score",
        "result",
        "election",
        "stock",
        "share price",
        "what happened",
        "who won",
        "when is",
        "this year",
        "this month"
    ]

    for keyword in web_keywords:
        if keyword in text:
            return True

    return False


# ==============================
# FORMAT WEB RESULTS
# ==============================

def format_web_results(results):

    search_text = ""

    for number, result in enumerate(
        results,
        start=1
    ):

        title = result.get(
            "title",
            "No title"
        )

        body = result.get(
            "body",
            "No description"
        )

        url = result.get(
            "href",
            ""
        )

        search_text += (
            f"\nResult {number}:\n"
            f"Title: {title}\n"
            f"Description: {body}\n"
            f"URL: {url}\n"
        )

    return search_text


# ==============================
# ANSWER FROM WEB
# ==============================

def answer_from_web(
    user_question,
    results
):

    web_text = format_web_results(
        results
    )

    prompt = f"""
You are a helpful AI assistant.

The user asked:

{user_question}

Here are fresh web search results:

{web_text}

Answer the user's question using the search results.

IMPORTANT RULES:

1. Prefer information supported by the search results.
2. Do not invent facts.
3. If the results are unclear or conflicting, say so.
4. Give a short and clear answer.
5. Mention the most relevant source URLs at the end.
"""

    try:

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response[
            "message"
        ][
            "content"
        ]

    except Exception as e:

        return (
            "⚠️ Could not summarize "
            "web results: "
            + str(e)
        )


# ==============================
# SAVE WEB KNOWLEDGE
# ==============================

def save_web_knowledge(
    user_question,
    answer,
    memory,
    user_id
):

    try:

        extraction_prompt = f"""
You are a knowledge extraction assistant.

User question:
{user_question}

Web-based answer:
{answer}

Extract only useful, factual, reusable knowledge.

Rules:
1. Keep only important facts.
2. Remove greetings and source lists.
3. Do not invent information.
4. Keep the result short.
5. If there is no useful knowledge,
return exactly: NONE.
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

        if (
            not knowledge
            or knowledge.upper() == "NONE"
        ):

            print(
                "🧠 No useful web knowledge to save."
            )

            return

        existing = memory.search(
            knowledge,
            filters={
                "user_id": user_id
            }
        )

        for item in existing.get(
            "results",
            []
        ):

            old_memory = item.get(
                "memory",
                ""
            ).strip().lower()

            if old_memory == knowledge.lower():

                print(
                    "🧠 Knowledge already exists."
                )

                return

        memory.add(
            f"Learned web knowledge: {knowledge}",
            user_id=user_id
        )

        print(
            "🧠 Smart Web Knowledge Saved!"
        )

        print(
            "📚 Learned:",
            knowledge
        )

    except Exception as e:

        print(
            "⚠️ Could not save web knowledge:",
            e
        )