from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    jsonify,
    make_response,
)
from datetime import datetime, timedelta
import calendar
from utils.dua_generator import generate_all_night_duas
from utils.pdf_generator import generate_plan_pdf

app = Flask(__name__)
app.config.from_object("config.Config")


def calculate_ramadan_dates():
    """Calculate approximate dates for Ramadan nights (last 10 nights)."""
    today = datetime.now()
    ramadan_21 = datetime(2026, 3, 10)  # 21st night of Ramadan

    dates = []
    for night in range(21, 31):
        night_date = ramadan_21 + timedelta(days=(night - 21))
        dates.append(
            {
                "night": night,
                "date": night_date.strftime("%B %d, %Y"),
                "day_name": night_date.strftime("%A"),
                "is_odd": night % 2 == 1,
            }
        )
    return dates


NIGHT_DATA = {
    21: {
        "title": "Night 21",
        "recitation": ["Surah Al-Mulk (67)", "Surah Al-Kahf (18)"],
        "recitation_benefit": "Surah Al-Mulk protects from punishment in the grave; Surah Al-Kahf brings light for 10 days",
        "dhikr": {
            "subhanallah": 33,
            "alhamdullilah": 33,
            "allahu_akbar": 34,
            "astaghfirullah": 100,
        },
        "tahajjud": "2 rakat recommended",
        "worship_tip": "Start your 10-night journey with strong intention. Make this night special with extended worship.",
        " Dua": "اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي",
    },
    22: {
        "title": "Night 22",
        "recitation": [
            "Surah Al-Waqiah (56)",
            "Surah Yusuf (12)",
            "Surah As-Sajdah (32)",
        ],
        "recitation_benefit": "Surah Al-Waqiah guarantees provision and removes poverty",
        "dhikr": {
            "subhanallah": 33,
            "alhamdullilah": 33,
            "allahu_akbar": 34,
            "astaghfirullah": 100,
        },
        "tahajjud": "2-4 rakat recommended",
        "worship_tip": "Build upon your momentum from Night 21. Increase your duas and seek Allah's mercy.",
        " Dua": "اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي",
    },
    23: {
        "title": "Night 23",
        "recitation": [
            "Surah Al-Muzzammil (73)",
            "Surah Al-Mudaththir (74)",
            "Surah Al-Qadr (97)",
        ],
        "recitation_benefit": "These surahs were revealed for Laylatul Qadr worship",
        "dhikr": {
            "subhanallah": 100,
            "alhamdullilah": 100,
            "allahu_akbar": 100,
            "durud": 100,
        },
        "tahajjud": "4 rakat recommended",
        "worship_tip": "🌟 FIRST LIKELY NIGHT - Increase worship intensity! This is one of the odd nights most associated with Laylatul Qadr.",
        " Dua": "اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي",
    },
    24: {
        "title": "Night 24",
        "recitation": [
            "Surah Ar-Rahman (55)",
            "Surah An-Najm (53)",
            "Surah Al-Baqarah 255 (Ayatul Kursi)",
        ],
        "recitation_benefit": "Surah Ar-Rahman is a reminder of Allah's 31 blessings; Ayatul Kursi is the greatest verse",
        "dhikr": {
            "subhanallah": 33,
            "alhamdullilah": 33,
            "allahu_akbar": 34,
            "astaghfirullah": 100,
        },
        "tahajjud": "2 rakat recommended",
        "worship_tip": "Maintain your consistency. Don't let the energy from last night fade.",
        " Dua": "اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي",
    },
    25: {
        "title": "Night 25",
        "recitation": [
            "Surah Al-Qadr (97)",
            "Surah Al-Baqarah 1-5",
            "Surah Al-Ikhlas (112) x3",
        ],
        "recitation_benefit": "Reading Surah Al-Qadr 100 times equals reading the whole Quran",
        "dhikr": {
            "subhanallah": 100,
            "alhamdullilah": 100,
            "allahu_akbar": 100,
            "la_ilaha_illa_allah": 100,
        },
        "tahajjud": "4 rakat recommended",
        "worship_tip": "🌟 SECOND LIKELY NIGHT - Double your efforts! This is one of the most blessed nights.",
        " Dua": "اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي",
    },
    26: {
        "title": "Night 26",
        "recitation": [
            "Surah Al-Infitar (82)",
            "Surah At-Takwir (81)",
            "Surah Al-Balad (90)",
        ],
        "recitation_benefit": "These surahs emphasize accountability and the oath of the city",
        "dhikr": {
            "subhanallah": 33,
            "alhamdullilah": 33,
            "allahu_akbar": 34,
            "astaghfirullah": 100,
        },
        "tahajjud": "2 rakat recommended",
        "worship_tip": "Continue your dedicated worship. The peak of Laylatul Qadr is approaching.",
        " Dua": "اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي",
    },
    27: {
        "title": "Night 27",
        "recitation": [
            "Surah Al-Qiyamah (75)",
            "Surah Al-Mursalat (77)",
            "Surah Al-Wathiah (56:1-29)",
            "Surah Al-Qadr (97) x7",
        ],
        "recitation_benefit": "This is traditionally one of the strongest nights for Laylatul Qadr",
        "dhikr": {
            "subhanallah": 100,
            "alhamdullilah": 100,
            "allahu_akbar": 100,
            "durud": 100,
            "astaghfirullah": 200,
        },
        "tahajjud": "4-6 rakat recommended",
        "worship_tip": "🌟 MOST LIKELY NIGHT - Go all out! Many scholars believe Night 27 is Laylatul Qadr. Make this your strongest worship session.",
        " Dua": "اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي",
    },
    28: {
        "title": "Night 28",
        "recitation": [
            "Surah Al-Haqqah (69)",
            "Surah Al-Ma'arij (70)",
            "Surah Al-Jinn (72)",
        ],
        "recitation_benefit": "Surah Al-Jinn shows how even jinn benefited from Quran recitation",
        "dhikr": {
            "subhanallah": 33,
            "alhamdullilah": 33,
            "allahu_akbar": 34,
            "astaghfirullah": 100,
        },
        "tahajjud": "2 rakat recommended",
        "worship_tip": "Don't weaken after last night. Continue with full dedication.",
        " Dua": "اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي",
    },
    29: {
        "title": "Night 29",
        "recitation": [
            "Surah Al-Jathiyah (45)",
            "Surah Al-Ahqaf (46)",
            "Surah Ad-Dukhan (44)",
            "Surah Al-Qadr (97) x7",
        ],
        "recitation_benefit": "Surah Ad-Dukhan (smoke) was revealed on Laylatul Qadr",
        "dhikr": {
            "subhanallah": 100,
            "alhamdullilah": 100,
            "allahu_akbar": 100,
            "la_ilaha_illa_allah": 100,
        },
        "tahajjud": "4 rakat recommended",
        "worship_tip": "🌟 THIRD LIKELY NIGHT - Almost the end! One more strong night of potential Laylatul Qadr.",
        " Dua": "اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي",
    },
    30: {
        "title": "Night 30",
        "recitation": [
            "Surah Ad-Dukhan (44)",
            "Surah Al-Baqarah 284-286",
            "Surah Al-Ikhlas (112) x11",
        ],
        "recitation_benefit": "Ending Ramadan with Quran and seeking acceptance",
        "dhikr": {
            "subhanallah": 33,
            "alhamdullilah": 33,
            "allahu_akbar": 34,
            "shukran": 100,
        },
        "tahajjud": "2 rakat recommended",
        "worship_tip": "🌙 FINAL NIGHT - Thank Allah for Ramadan and pray that He accepts all your worship. Make heartfelt dua for forgiveness and blessings.",
        " Dua": "رَبَّنَا تَقَبَّلْ مِنَّا إِنَّكَ أَنتَ السَّمِيعُ الْعَلِيمُ",
    },
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    user_intention = request.form.get("intention", "").strip()
    praying_for = request.form.get("praying_for", "").strip()

    if not user_intention:
        user_intention = "whatever goodness Allah wills for me"

    session["user_intention"] = user_intention
    session["praying_for"] = praying_for

    return render_template("loading.html")


@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    user_intention = session.get("user_intention", "")
    praying_for = session.get("praying_for", "")

    if not user_intention:
        user_intention = "whatever goodness Allah wills for me"

    duas = generate_all_night_duas(user_intention, praying_for)

    session["duas"] = duas
    session["dates"] = calculate_ramadan_dates()

    return redirect(url_for("plan"))


@app.route("/plan")
def plan():
    user_intention = session.get("user_intention", "")
    praying_for = session.get("praying_for", "")
    duas = session.get("duas", [])
    dates = session.get("dates", [])

    if not duas:
        duas = generate_all_night_duas(user_intention, praying_for)
        dates = calculate_ramadan_dates()

    night_plans = []
    for i, night in enumerate(range(21, 31)):
        night_data = NIGHT_DATA[night]
        dua_data = duas[i] if i < len(duas) else {"dua": "", "is_odd": False}
        date_data = dates[i] if i < len(dates) else {"date": "", "is_odd": False}

        night_plans.append(
            {
                "night": night,
                "date": date_data.get("date", ""),
                "day_name": date_data.get("day_name", ""),
                "is_odd": night % 2 == 1,
                **night_data,
                "personal_dua": dua_data.get("dua", ""),
            }
        )

    return render_template(
        "plan.html",
        user_intention=user_intention,
        praying_for=praying_for,
        nights=night_plans,
    )


@app.route("/download-pdf")
def download_pdf():
    user_intention = session.get("user_intention", "")
    praying_for = session.get("praying_for", "")
    duas = session.get("duas", [])
    dates = session.get("dates", [])

    if not duas:
        duas = generate_all_night_duas(user_intention, praying_for)
        dates = calculate_ramadan_dates()

    night_plans = []
    for i, night in enumerate(range(21, 31)):
        night_data = NIGHT_DATA[night]
        dua_data = duas[i] if i < len(duas) else {"dua": "", "is_odd": False}
        date_data = dates[i] if i < len(dates) else {"date": "", "is_odd": False}

        night_plans.append(
            {
                "night": night,
                "date": date_data.get("date", ""),
                "day_name": date_data.get("day_name", ""),
                "is_odd": night % 2 == 1,
                **night_data,
                "personal_dua": dua_data.get("dua", ""),
            }
        )

    pdf_content = generate_plan_pdf(night_plans, user_intention, praying_for)

    response = make_response(pdf_content)
    response.headers["Content-Type"] = "application/pdf; charset=utf-8"
    response.headers["Content-Disposition"] = (
        "attachment; filename=laylatul-qadr-plan.pdf"
    )
    return response


@app.route("/night/<int:night_num>")
def night_detail(night_num):
    if night_num < 21 or night_num > 30:
        return redirect(url_for("plan"))

    user_intention = session.get("user_intention", "")
    duas = session.get("duas", [])

    dua_data = None
    for dua in duas:
        if dua["night"] == night_num:
            dua_data = dua
            break

    night_data = NIGHT_DATA[night_num]
    dates = calculate_ramadan_dates()
    date_info = dates[night_num - 21]  # Index 0-9 for nights 21-30

    worship_steps = [
        {
            "title": "🌙 Prepare for Worship",
            "description": "Make intention (niyyah) for Laylatul Qadr worship. Perform ghusl (bath) before starting. Wear clean clothes.",
            "dua": "نَوَيْتُ أَنْ أُصَلِّيَ تَهَجُّدًَا لِلَّهِ تَعَالَى",
        },
        {
            "title": "📖 Recite the Quran",
            "description": f"Recite: {', '.join(night_data['recitation'])}",
            "benefit": night_data["recitation_benefit"],
            "dua": None,
        },
        {
            "title": "🔥 Perform Dhikr",
            "description": f"SubhanAllah {night_data['dhikr']['subhanallah']}x, Alhamdullilah {night_data['dhikr']['alhamdullilah']}x, Allahu Akbar {night_data['dhikr']['allahu_akbar']}x"
            + (
                f", Astaghfirullah {night_data['dhikr'].get('astaghfirullah', 100)}x"
                if "astaghfirullah" in night_data["dhikr"]
                else ""
            ),
            "dua": night_data[" Dua"],
        },
        {
            "title": "🤲 Make Personal Dua",
            "description": "This is the time to make your personal dua with complete humility and hope.",
            "dua": dua_data.get("dua", "") if dua_data else "",
            "is_personal": True,
        },
        {
            "title": "💤 End with Tahajjud",
            "description": night_data["tahajjud"],
            "dua": None,
        },
    ]

    return render_template(
        "night.html",
        night=night_num,
        night_info=night_data,
        date_info=date_info,
        user_intention=user_intention,
        worship_steps=worship_steps,
    )


@app.route("/api/save-journal", methods=["POST"])
def save_journal():
    data = request.json
    if data:
        session[f"journal_{data.get('night')}"] = data.get("content", "")
    return jsonify({"success": True})


@app.route("/api/get-journal/<int:night_num>")
def get_journal(night_num):
    content = session.get(f"journal_{night_num}", "")
    return jsonify({"content": content})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
