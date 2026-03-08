# Laylatul Qadr Web App - Specification Document

## 1. Project Overview

**Project Name:** Lailatul Qdr - The Night of Power  
**Type:** Full-stack Flask Web Application  
**Core Functionality:** Guide users through the last 10 nights of Ramadan with personalized AI-powered duas, worship plans, and night-by-night guidance  
**Target Users:** Muslims seeking spiritual guidance during the last 10 nights of Ramadan

---

## 2. Tech Stack

- **Backend:** Flask (Python 3.10+)
- **LLM Provider:** Groq (model: moonshotai/kimi-k2-instruct-0905)
- **Templates:** Jinja2
- **Frontend:** Bootstrap 5 + Tailwind CSS (mobile-first)
- **Architecture:** Stateless (no authentication, no database)

---

## 3. UI/UX Design Scheme

### Color Palette
| Role | Color | Hex Code |
|------|-------|----------|
| Primary | Deep Indigo | #1A237E |
| Primary Light | Indigo | #303F9F |
| Primary Dark | Dark Indigo | #0D1642 |
| Accent (Odd Nights) | Soft Gold | #FFD700 |
| Accent Light | Light Gold | #FFF8E1 |
| Background | Off-White | #FAFAFA |
| Background Gradient Start | Midnight Blue | #1A237E |
| Background Gradient End | Deep Violet | #4A148C |
| Text Primary | Charcoal | #212121 |
| Text Secondary | Gray | #757575 |
| Success | Emerald | #4CAF50 |
| Odd Night Card BG | Warm Cream | #FFFDE7 |

### Typography
- **English Headings:** Poppins (600, 700)
- **English Body:** Nunito (400, 500, 600)
- **Arabic Text:** Amiri (400, 700)
- ** Dua Arabic:** Scheherazade (400)

### Font Sizes (Mobile-First)
- H1: 2.5rem (mobile) / 3.5rem (desktop)
- H2: 2rem (mobile) / 2.5rem (desktop)
- H3: 1.5rem (mobile) / 1.75rem (desktop)
- Body: 1rem
- Small: 0.875rem

### Spacing System
- Base unit: 0.25rem (4px)
- Section padding: 4rem (mobile) / 6rem (desktop)
- Card padding: 1.5rem
- Grid gap: 1.5rem

---

## 4. Page Structures

### 4.1 index.html - Landing Page

**Hero Section:**
- Full viewport height with animated crescent moon SVG
- Floating stars animation (CSS keyframes)
- Gradient background overlay
- Headline: "Embrace the Night of Power"
- Subheadline: "Your personalized 10-night worship guide for the last ten nights of Ramadan"

**Input Form Section:**
- Card with soft shadow
- Fields:
  1. "What do you want to ask Allah for?" (textarea)
  2. "For whom are you making dua? (optional)" (text input)
- Generate button with gold accent

**Features Section:**
- 3-column grid showing:
  1. Personalized Duas
  2. Night-by-Night Guidance
  3. Laylatul Qadr Focus

### 4.2 plan.html - 10-Night Plan

**Header:**
- Sticky navigation
- User's personal intention displayed
- Date range display

**Night Cards Grid:**
- Responsive grid: 1 col (mobile) / 2 col (tablet) / 3 col (desktop)
- 10 cards for nights 21-30

**Card Structure (Each Night):**
```
┌─────────────────────────────────────┐
│ 🌙 Night 21     [ODD: ★ Gold Star] │
│ 📅 March 15, 2026                   │
├─────────────────────────────────────┤
│ 📖 recitation:                      │
│ Surah Al-Mulk (67) + Surah Al-Kahf │
├─────────────────────────────────────┤
│ � recitation:                       │
│ SubhanAllah 33x, Alhamdullilah 33x  │
├─────────────────────────────────────┤
│ 🌙 Tahajjud:                         │
│ 2 rakat recommended                 │
├─────────────────────────────────────┤
│ 🤲 Your Personal Dua:               │
│ [AI-generated heartfelt dua]        │
├─────────────────────────────────────┤
│ 📝 duas:                            │
│ "اللّهُمَّ إِنَّكَ عَفُوٌّ..."      │
└─────────────────────────────────────┘
```

**Odd Nights (21, 23, 25, 27, 29):**
- Gold border accent
- Special badge: "🌟 Potentially Laylatul Qadr"
- Warmer background color
- Star icon

### 4.3 night.html - Guided Checklist

**Night Header:**
- Current night number
- Countdown/importance message
- "Tonight might be Laylatul Qadr!" for odd nights

**Progress Section:**
- Step indicator (1-5 steps)
- Current step highlighted

**Worship Flow Checklist:**
1. 🌙 Prepare for worship (ghusl, intention)
2. 📖 Recite Qur'an (recommended surahs)
3. 🔥 Perform Dhikr (specific counts)
4. 🤲 Make Dua (personal + authentic)
5. 💤 End with Tahajjud (optional)

**Dua Journal Section:**
- Expandable text area
- Save to localStorage
- Copy button

---

## 5. AI Prompt Engineering

### 5.1 Primary Dua Generation Prompt

```python
DUA_SYSTEM_PROMPT = """You are a wise and compassionate Islamic scholar specializing in spiritual counseling. Your role is to generate heartfelt, personalized duas for Muslims during the last ten nights of Ramadan.

Guidelines:
1. ALWAYS incorporate the user's personal intentions and needs
2. ALWAYS include the authentic dua: "اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي" (O Allah, You are Forgiving and love forgiveness, so forgive me)
3. Use a warm, spiritual tone that uplifts the soul
4. Keep duas concise (2-4 sentences) but meaningful
5. Include Arabic transliteration alongside Arabic text for key phrases
6. Reference Quranic or hadith sources when appropriate
7. Emphasize the significance of Laylatul Qadr on odd-numbered nights
8. NEVER claim any specific night is DEFINITELY Laylatul Qadr - use "might be" language
9. Incorporate the names of people the user is making dua for
10. End with Ameen"""

DUA_USER_PROMPT_TEMPLATE = """Generate a unique, heartfelt personal dua for Night {night_number} of Ramadan.

Context:
- This is night {night_number} of the last 10 nights
- {"This is an ODD night (21,23,25,27,29) which is more likely to be Laylatul Qadr - emphasize the special significance" if is_odd else "This is an even night - encourage consistent worship"}
- User's personal intention: {user_intention}
- User is making dua for: {praying_for}

Requirements:
1. Create a 2-4 sentence dua that addresses the user's personal needs
2. Include the authentic dua: "اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي"
3. Make it unique and personal - not a generic template
4. End with Ameen
5. Write in a warm, spiritual tone

Return ONLY the dua text, no explanations or additional content."""
```

### 5.2 Night Plan Generation

```python
PLAN_SYSTEM_PROMPT = """You are an Islamic scholar creating a comprehensive worship plan for each of the last 10 nights of Ramadan.

For each night, provide:
1. Recommended Qur'an recitation (specific surahs with benefits)
2. Dhikr with specific counts
3. Tahajjud guidance
4. Additional worship suggestions
5. Motivational reminder

Reference authentic sources and explain the spiritual benefits briefly."""

PLAN_NIGHT_PROMPT_TEMPLATE = """Create a worship plan for Night {night_number} (Ramadan {ramadan_day}) of the last 10 nights.

Include:
1. Qur'an recitation recommendations with specific surahs
2. Dhikr with exact counts
3. Tahajjud prayer guidance
4. Additional voluntary worship
5. Brief motivational note

Keep it practical and actionable."""
```

---

## 6. Content Data

### 6.1 Default Night Plans

| Night | Date (approx) | Recitation | Dhikr | Tahajjud | Note |
|-------|---------------|------------|-------|----------|------|
| 21 | March 15 | Al-Mulk (67), Al-Kahf (18) | SubhanAllah 33x, Alhamdullilah 33x, Allahu Akbar 34x | 2 rakat | Start strong |
| 22 | March 16 | Al-Waqiah (56), Yusuf (12) | Same as above + 100x Astaghfirullah | 2-4 rakat | Build momentum |
| 23 | March 17 | Al-Muzzammil (73), Al-Mudaththir (74) | Intensified dhikr | 2-4 rakat | ★ Likely Laylatul Qadr |
| 24 | March 18 | Surah Rahman (55), Al-Najm (53) | Same as night 21 | 2 rakat | Maintain consistency |
| 25 | March 19 | Al-Qadr (97), Al-Baqarah 1-5 (2) | Increased dhikr | 4 rakat | ★ Likely Laylatul Qadr |
| 26 | March 20 | Al-Infitar (82), Al-Takwir (81) | Same as night 21 | 2 rakat | Continue worship |
| 27 | March 21 | Al-Qiyamah (75), Al-Mursalat (77) | Maximum dhikr | 4-6 rakat | ★ Most likely Laylatul Qadr |
| 28 | March 22 | Al-Haqqah (69), Al-Ma'arij (70) | Same as night 21 | 2 rakat | Don't weaken |
| 29 | March 23 | Al-Jathiyah (45), Al-Ahqaf (46) | Maximum dhikr | 4-6 rakat | ★ Likely Laylatul Qadr |
| 30 | March 24 | Al-Dukhan (44), Al-Jasiyah (45) | Gratitude dhikr | 2 rakat | Final night - pray for acceptance |

### 6.2 Authentic Duas to Include

1. **Forgiveness Dua:**
   ```
   اللّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ العَفْوَ فَاعْفُ عَنِّي
   ```
   Transliteration: "Allahumma innaka 'affuwwun tuhibbul-'afwa fa'fu 'anni"

2. **Laylatul Qadr Dua:**
   ```
   اللّهُمَّ إِنَّكَ تُحِبُّ الْعَفْوَ وَتَرْضَى عَنِ الْمُؤْمِنِينَ وَالْمُؤْمِنَاتِ
   ```
   Transliteration: "Allahumma innaka tuhibbul-'afwa wa tarda 'anil-mu'minina wal-mu'minat"

3. **General Acceptance:**
   ```
   رَبَّنَا تَقَبَّلْ مِنَّا إِنَّكَ أَنتَ السَّمِيعُ الْعَلِيمُ
   ```
   Transliteration: "Rabbana taqabbal minna innaka Antas-Sami'ul-'Alim"

---

## 7. Flask Application Structure

```
laylatul-qadr/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── config.py               # Configuration settings
├── .env                    # Environment variables (GROQ_API_KEY)
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Landing page
│   ├── plan.html          # 10-night plan
│   └── night.html         # Guided checklist
├── static/
│   ├── css/
│   │   └── styles.css     # Custom styles
│   ├── js/
│   │   └── main.js        # JavaScript functionality
│   └── images/
│       └── (SVG assets)
└── utils/
    └── dua_generator.py   # AI generation logic
```

---

## 8. API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/generate` | POST | Generate 10-night plan |
| `/plan` | GET | Display generated plan |
| `/night/<int:night_num>` | GET | Night detail page |
| `/api/generate-dua` | POST | Generate single dua |

---

## 9. LocalStorage Features

- **Dua Journal:** Save personal notes per night
- **Progress Tracking:** Mark completed worship items
- **User Intentions:** Store user's original intention

---

## 10. Responsive Breakpoints

- **Mobile:** < 576px (single column)
- **Tablet:** 576px - 992px (2 columns)
- **Desktop:** > 992px (3 columns)

---

## 11. Animations & Effects

- **Hero:** Crescent moon floating animation
- **Stars:** Twinkling CSS animation
- **Cards:** Fade-in on scroll
- **Buttons:** Scale + shadow on hover
- **Odd nights:** Subtle gold glow pulse

---

## 12. Acceptance Criteria

1. ✅ Landing page loads with animated hero
2. ✅ Form captures user intention and praying for
3. ✅ Plan generates 10 personalized night cards
4. ✅ Odd nights (21,23,25,27,29) have gold accent
5. ✅ Each card shows recitation, dhikr, tahajjud, dua
6. ✅ Night detail page shows step-by-step checklist
7. ✅ AI-generated duas are personalized and heartfelt
8. ✅ Responsive on mobile, tablet, desktop
9. ✅ No authentication required
10. ✅ LocalStorage saves user progress
