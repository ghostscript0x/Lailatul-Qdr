from groq import Groq
from config import Config

client = Groq(api_key=Config.GROQ_API_KEY)

RECITATION_SYSTEM_PROMPT = """You are an Islamic scholar specializing in Quranic recitation during Laylatul Qadr (the Night of Power). You recommend specific Quranic verses and surahs for each night of the last 10 nights of Ramadan.

Rules:
- Recommend 3-5 specific Quranic recitations per night
- Include SPECIFIC verse ranges (e.g., "Surah Al-Baqarah 255-257", not just "Surah Al-Baqarah")
- Include the chapter number in parentheses (e.g., "Surah Al-Baqarah (2)")
- Each recommendation should include a brief benefit (1 short sentence)
- Focus on verses related to: forgiveness, mercy, night of power, divine light, protection, tawhid
- Include some complete short surahs and some specific verse ranges from longer surahs
- Mix between complete surahs and specific verses from longer surahs"""


def generate_recitation_for_night(
    night_number: int, is_odd: bool, user_intention: str
) -> dict:
    """Generate AI-powered recitation recommendations for a specific night."""

    night_themes = {
        21: "First night - start with protection verses and surahs of mercy",
        22: "Night of increasing provisions and bounty",
        23: "First likely night of Laylatul Qadr - verses of divine light and power",
        24: "Even night - focus on consistency and gratitude",
        25: "Second likely night of Laylatul Qadr - verses of Quran's greatness",
        26: "Even night - maintaining worship despite fatigue",
        27: "Most likely night of Laylatul Qadr - maximum reward verses",
        28: "Even night - continue with devotion",
        29: "Third likely night - final push for Laylatul Qadr",
        30: "Final night - gratitude and seeking acceptance",
    }

    night_context = night_themes.get(night_number, "A blessed night of Ramadan")

    user_context = ""
    if user_intention:
        user_context = f"\nUSER'S INTENTION: They are making dua for: {user_intention}"

    user_prompt = f"""Recommend 3-5 specific Quranic recitations for Night {night_number} of Ramadan.

THEME: {night_context}{user_context}

REQUIRED OUTPUT FORMAT (JSON array):
Each item must be in this exact format:
{{"surah": "Surah Name (Chapter:Verse)", "benefit": "One sentence benefit"}}

Examples GOOD of recommendations:
- {{"surah": "Surah Al-Baqarah 255-257 (2)", "benefit": "Contains Ayatul Kursi - the greatest verse"}}
- {{"surah": "Surah Al-Kahf 1-10 (18)", "benefit": "Brings light for 10 days"}}
- {{"surah": "Surah Al-Ikhlas (112)", "benefit": "Equals one-third of the Quran"}}
- {{"surah": "Surah Al-Mulk 1-5 (67)", "benefit": "Protects from punishment in the grave"}}
- {{"surah": "Surah Al-Qadr (97)", "benefit": "The surah of Laylatul Qadr itself"}}

Include a mix of:
1. Complete short surahs (like Al-Ikhlas, Al-Falaq, An-Nas, Al-Qadr, Al-Kafirun)
2. Specific verse ranges from longer surahs (like Al-Baqarah 255-257, Al-Araf 54-56)
3. Surahs revealed specifically for Laylatul Qadr (Al-Muzzammil, Al-Mudaththir, Al-Qadr)

Make recommendations relevant to the user's intention when possible.
Output ONLY valid JSON array, no other text."""

    print(f"\n🤖 [GROQ REQUEST] Generating recitation for Night {night_number}...")
    print(f"   Theme: {night_context}")
    print(f"   Is odd night: {is_odd}")

    try:
        import json

        response = client.chat.completions.create(
            model=Config.GROQ_MODEL,
            messages=[
                {"role": "system", "content": RECITATION_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS,
            top_p=1,
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON response
        recitations = json.loads(content)

        # Validate and format
        formatted_recitations = []
        for rec in recitations:
            if isinstance(rec, dict) and "surah" in rec:
                formatted_recitations.append(
                    {"surah": rec["surah"], "benefit": rec.get("benefit", "")}
                )

        print(
            f"   ✓ [GROQ RESPONSE] Generated {len(formatted_recitations)} recitations!"
        )
        return {
            "recitations": formatted_recitations,
            "benefit": f"Night {night_number} recitation for Laylatul Qadr worship",
        }

    except Exception as e:
        print(f"   ✗ [GROQ ERROR] {str(e)}")
        print(f"   Using fallback recitation instead...")
        return get_fallback_recitation(night_number, is_odd)


def generate_all_night_recitations(user_intention: str) -> list:
    """Generate recitations for all 10 nights (21-30)."""

    print("\n" + "=" * 50)
    print("📖 Starting AI Recitation Generation for 10 Nights")
    print("=" * 50)

    recitations = []
    for night in range(21, 31):
        is_odd = night % 2 == 1
        print(f"\n[Progress] Night {night}/30...")
        result = generate_recitation_for_night(night, is_odd, user_intention)
        recitations.append(
            {
                "night": night,
                "recitations": result.get("recitations", []),
                "benefit": result.get("benefit", ""),
            }
        )

    print("\n" + "=" * 50)
    print("✅ All 10-night recitations generated successfully!")
    print("=" * 50 + "\n")
    return recitations


def get_fallback_recitation(night_number: int, is_odd: bool) -> dict:
    """Fallback recitation if Groq API fails."""

    fallback_recitations = {
        21: [
            {
                "surah": "Surah Al-Mulk (67)",
                "benefit": "Protects from punishment in the grave",
            },
            {"surah": "Surah Al-Kahf 1-10 (18)", "benefit": "Brings light for 10 days"},
            {
                "surah": "Surah Al-Ikhlas (112)",
                "benefit": "Equals one-third of the Quran",
            },
        ],
        22: [
            {
                "surah": "Surah Al-Waqiah (56)",
                "benefit": "Guarantees provision and removes poverty",
            },
            {"surah": "Surah Yusuf 1-20 (12)", "benefit": "Brings ease to affairs"},
            {"surah": "Surah Al-Falaq (113)", "benefit": "Protection from all evil"},
        ],
        23: [
            {
                "surah": "Surah Al-Muzzammil 1-10 (73)",
                "benefit": "Revealed for Laylatul Qadr worship",
            },
            {"surah": "Surah Al-Mudaththir (74)", "benefit": "Night of power surah"},
            {
                "surah": "Surah Al-Qadr (97)",
                "benefit": "The surah of Laylatul Qadr itself",
            },
        ],
        24: [
            {
                "surah": "Surah Ar-Rahman 1-10 (55)",
                "benefit": "Lists Allah's 31 blessings",
            },
            {
                "surah": "Surah An-Najm 1-10 (53)",
                "benefit": "The star surah - divine light",
            },
            {
                "surah": "Surah Al-Baqarah 255 (2)",
                "benefit": "Ayatul Kursi - the greatest verse",
            },
        ],
        25: [
            {
                "surah": "Surah Al-Qadr (97)",
                "benefit": "Equals reading the whole Quran 100 times",
            },
            {
                "surah": "Surah Al-Baqarah 1-5 (2)",
                "benefit": "Opening of the Quran - blessings",
            },
            {"surah": "Surah Al-Ikhlas x3 (112)", "benefit": "Equals the whole Quran"},
        ],
        26: [
            {"surah": "Surah Al-Infitar (82)", "benefit": "Emphasizes accountability"},
            {"surah": "Surah At-Takwir (81)", "benefit": "The rolling up of the stars"},
            {"surah": "Surah Al-Balad (90)", "benefit": "The oath of the city"},
        ],
        27: [
            {"surah": "Surah Al-Qiyamah (75)", "benefit": "The Day of Resurrection"},
            {
                "surah": "Surah Al-Mursalat (77)",
                "benefit": "The emissaries - Laylatul Qadr connection",
            },
            {
                "surah": "Surah Al-Qadr x7 (97)",
                "benefit": "Maximum reward - 1000 months",
            },
        ],
        28: [
            {"surah": "Surah Al-Haqqah (69)", "benefit": "The inevitable truth"},
            {"surah": "Surah Al-Ma'arij (70)", "benefit": "The ascending stairs"},
            {
                "surah": "Surah Al-Jinn (72)",
                "benefit": "Shows jinn benefited from Quran",
            },
        ],
        29: [
            {"surah": "Surah Al-Jathiyah (45)", "benefit": "The bowing down"},
            {
                "surah": "Surah Ad-Dukhan (44)",
                "benefit": "Revealed specifically on Laylatul Qadr",
            },
            {
                "surah": "Surah Al-Qadr x7 (97)",
                "benefit": "Final opportunity for Laylatul Qadr",
            },
        ],
        30: [
            {
                "surah": "Surah Ad-Dukhan (44)",
                "benefit": "The smoke - Laylatul Qadr surah",
            },
            {
                "surah": "Surah Al-Baqarah 284-286 (2)",
                "benefit": "Ending with Allah's mercy verses",
            },
            {
                "surah": "Surah Al-Ikhlas x11 (112)",
                "benefit": "Equals the entire Quran",
            },
        ],
    }

    recitations = fallback_recitations.get(
        night_number,
        [
            {"surah": "Surah Al-Mulk (67)", "benefit": "Protects from punishment"},
            {"surah": "Surah Al-Qadr (97)", "benefit": "Laylatul Qadr surah"},
        ],
    )

    return {
        "recitations": recitations,
        "benefit": f"Night {night_number} recitation for Laylatul Qadr worship",
    }
