from groq import Groq
from config import Config

client = Groq(api_key=Config.GROQ_API_KEY)

DUA_SYSTEM_PROMPT = """You create SHORT Islamic duas. Rules:
- Maximum 2-3 sentences per dua
- Each dua must end with "Ameen" immediately (nothing after)
- NEVER repeat the same opener or structure
- Include the authentic Arabic dua naturally
- Be concise but heartfelt
- Make each one unique in structure and wording"""


# Unique openings and themes for each night to ensure variety
NIGHT_OPENINGS = {
    21: ["Ya Rabbul Ala", "Ilahi", "Ya Zul jalali"],  # Opening night
    22: ["Ya Wahhab", "Ya Razzaq", "Allahumma"],  # Provisions
    23: ["Ya Qadir", "Ya Kabir", "Subhani"],  # First likely Qadr
    24: ["Ya Salam", "Ya Muhyi", "Rabbee"],  # Even night
    25: ["Ya Nur", "Ya Hadi", "Ya Rafiq"],  # Second likely Qadr
    26: ["Ya Mughni", "Ya Bari", "Ilahi"],  # Even night
    27: ["Ya Malikul Mulk", "Ya Darr", "Allahumma"],  # Most likely Qadr
    28: ["Ya Musawwir", "Ya Ghani", "Rabbi"],  # Even night
    29: ["Ya Hakim", "Ya Lateef", "Ya Khabir"],  # Third likely Qadr
    30: ["Ya Shakur", "Subhanaka", "Alhamdullilah"],  # Final night - gratitude
}


def generate_personalized_dua(
    night_number: int, user_intention: str, praying_for: str, is_odd: bool
) -> str:
    """Generate a personalized dua for a specific night using Groq."""

    import random

    opening = random.choice(NIGHT_OPENINGS.get(night_number, ["Ya Rab"]))

    night_themes = {
        21: "the first night of the final ten - a fresh start to seek Laylatul Qadr",
        22: "continuing the journey with steadfast worship",
        23: "one of the most likely nights for Laylatul Qadr - increased reward",
        24: "maintaining consistency in worship",
        25: "another blessed odd night to maximize worship",
        26: "pressing forward with devotion",
        27: "possibly the night of Laylatul Qadr - the most significant night",
        28: "not weakening in worship despite fatigue",
        29: "one more opportunity to catch Laylatul Qadr",
        30: "the final night of Ramadan - seeking acceptance of all worship",
    }

    night_context = night_themes.get(night_number, "a blessed night of Ramadan")

    user_context = f"The person is making dua for: {user_intention}"
    if praying_for.strip():
        user_context += f". They are also praying for: {praying_for}"

    user_prompt = f"""Create a SHORT, unique dua for Night {night_number} of Ramadan (only 2-3 sentences).

CONTEXT: This is {night_context}.
OPENER: Start with "{opening}"

USER NEEDS: {user_context}

RULES:
1. Start exactly with "{opening}"
2. ONLY 2-3 sentences total
3. Include "اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي" naturally
4. End with "Ameen" - END IMMEDIATELY after Ameen
5. Be brief and heartfelt - no long paragraphs!

OUTPUT: Just the short dua."""

    print(f"\n🤖 [GROQ REQUEST] Generating dua for Night {night_number}...")
    print(
        f"   User intention: {user_intention[:50]}..."
        if len(user_intention) > 50
        else f"   User intention: {user_intention}"
    )
    print(f"   Praying for: {praying_for}" if praying_for else "   Praying for: None")
    print(f"   Is odd night: {is_odd}")

    try:
        response = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": DUA_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS,
            top_p=1,
        )
        dua = response.choices[0].message.content.strip()
        print(f"   ✓ [GROQ RESPONSE] Dua generated successfully!")
        print(f"   Preview: {dua[:80]}..." if len(dua) > 80 else f"   Preview: {dua}")
        return dua
    except Exception as e:
        print(f"   ✗ [GROQ ERROR] {str(e)}")
        print(f"   Using fallback dua instead...")
        return get_fallback_dua(night_number, user_intention, praying_for, is_odd)


def generate_all_night_duas(user_intention: str, praying_for: str) -> list:
    """Generate duas for all 10 nights (21-30)."""

    print("\n" + "=" * 50)
    print("🌙 Starting AI Dua Generation for 10 Nights")
    print("=" * 50)

    duas = []
    for night in range(21, 31):
        is_odd = night % 2 == 1
        print(f"\n[Progress] Night {night}/30...")
        dua = generate_personalized_dua(night, user_intention, praying_for, is_odd)
        duas.append({"night": night, "dua": dua, "is_odd": is_odd})

    print("\n" + "=" * 50)
    print("✅ All 10-night duas generated successfully!")
    print("=" * 50 + "\n")
    return duas


def get_fallback_dua(
    night_number: int, user_intention: str, praying_for: str, is_odd: bool
) -> str:
    """Fallback dua if Groq API fails."""

    base_dua = f"O Allah, You are The Most Forgiving and love forgiveness. Forgive me and accept my worship on this blessed night."

    if user_intention:
        base_dua += f" I humbly ask You to {user_intention}."

    if praying_for:
        base_dua += f" Bless and protect {praying_for} with Your mercy."

    if is_odd:
        base_dua += " This night might be Laylatul Qadr — the Night of Power. Make it a means of Your pleasure and forgiveness."

    base_dua += " Ameen."
    return base_dua
