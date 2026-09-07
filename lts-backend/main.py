import os
import json
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

load_dotenv()

app = FastAPI(title="LTS Academy AI Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://localhost:4000",
        "https://ltsacademy.ma",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Formations catalogue ────────────────────────────────────────────────────
FORMATIONS_CONTEXT = """
LTS Academy (Berrechid, Maroc) propose les formations professionnelles suivantes :

1. Ressources Humaines (RH)
   → Recrutement, gestion de la paie, droit du travail, développement RH.
   → Débouchés : DRH, Responsable RH, Chargé de recrutement.

2. Marketing Digital
   → SEO, réseaux sociaux, Google Ads, e-commerce, analytics.
   → Débouchés : Community Manager, Traffic Manager, Chef de projet digital.

3. Génie Mécanique
   → CAO/DAO (SolidWorks, AutoCAD, Catia), maintenance industrielle, automatisme.
   → Débouchés : Technicien Bureau d'Études, Responsable Maintenance, Dessinateur Industriel.

4. Infographie et Design
   → Adobe Photoshop, Illustrator, InDesign, UI/UX design.
   → Débouchés : Graphiste, Designer UI/UX, Directeur Artistique.

5. Formation Paramédicale
   → Soins infirmiers, anatomie, secourisme, relation patient.
   → Débouchés : Aide-soignant, Infirmier auxiliaire, Assistant médical.

6. Comptabilité et Finance
   → Comptabilité générale, analytique, fiscalité, gestion financière.
   → Débouchés : Comptable, Contrôleur de gestion, Responsable financier.

7. Développement Web Full-Stack
   → HTML/CSS/JS, React/Vue.js, Node.js, PHP, Python, bases de données, DevOps.
   → Débouchés : Développeur Front-End, Back-End, Full-Stack, Freelance.

8. Formations en Langues (Anglais, Français, Allemand)
   → Business English, TOEFL/IELTS, DELF/DALF, communication professionnelle.
   → Idéal pour travailler à l'étranger ou booster son employabilité.

9. Systèmes et Réseaux
   → Installation réseaux, administration serveurs, cybersécurité, Cisco.
   → Débouchés : Administrateur réseau, Technicien système, Ingénieur sécurité.

10. Logistique et Transport
    → Supply Chain, gestion des stocks, transport, douane.
    → Débouchés : Responsable logistique, Gestionnaire de stock, Transit.

11. Big Data et IA
    → Python, Machine Learning, Data Science, Power BI, Spark.
    → Débouchés : Data Analyst, Data Engineer, Data Scientist.

12. Responsable QHSE
    → ISO 9001 / 45001 / 14001, audit qualité, prévention des risques.
    → Débouchés : Responsable QHSE, Consultant QHSE, Auditeur Qualité.

Toutes les formations sont disponibles en présentiel à Berrechid et à distance.
Contact : +212 660 356 877 | WhatsApp : +212 661 732 848
"""

# ─── Models ──────────────────────────────────────────────────────────────────
class ChatMessage(BaseModel):
    role: str       # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


class ChatResponse(BaseModel):
    reply: str


class LanguageDetectRequest(BaseModel):
    text: str
    target_language: str = "Français"


class LanguageDetectResponse(BaseModel):
    level: str              # A1 A2 B1 B2 C1 C2
    score: int              # 0-100
    analysis: str
    recommendations: list[str]
    course_recommendation: Optional[str] = None


# ─── LLM initialization ──────────────────────────────────────────────────────
def get_llm():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.7,
    )


# ─── Endpoints ───────────────────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "LTS Academy AI Backend"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Conversational advisor that proposes learning paths."""
    llm = get_llm()

    system_prompt = f"""Tu es un conseiller pédagogique virtuel de LTS Academy, un centre de formation professionnel
basé à Berrechid, Maroc.

Ton rôle principal :
• Accueillir chaleureusement les visiteurs.
• Poser des questions pour comprendre leur profil (niveau d'études, objectifs, secteur souhaité, contraintes).
• Proposer un parcours d'apprentissage personnalisé parmi les formations de LTS Academy.
• Répondre à toute question sur les formations, les modalités, le contact.

{FORMATIONS_CONTEXT}

Règles :
- Réponds toujours en français de manière amicale et professionnelle.
- Pose 1 à 2 questions pertinentes si tu manques d'informations.
- Structure tes propositions clairement (avec des émojis si utile).
- Ne jamais inventer de formations non listées ci-dessus.
- Si on te demande quelque chose hors scope, redirige poliment vers le contact LTS Academy.
"""

    messages = [SystemMessage(content=system_prompt)]

    # Keep last 12 messages for context
    for msg in request.history[-12:]:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        else:
            messages.append(AIMessage(content=msg.content))

    messages.append(HumanMessage(content=request.message))

    try:
        response = await llm.ainvoke(messages)
        return ChatResponse(reply=response.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")


@app.post("/api/detect-language", response_model=LanguageDetectResponse)
async def detect_language_level(request: LanguageDetectRequest):
    """Assess language proficiency level (CEFR) using AI."""
    llm = get_llm()

    if len(request.text.strip()) < 10:
        raise HTTPException(
            status_code=400,
            detail="Le texte est trop court. Veuillez écrire au moins 2-3 phrases."
        )

    prompt = f"""Tu es un expert certifié en linguistique et en enseignement des langues étrangères.

Analyse le texte suivant écrit en {request.target_language} et évalue le niveau selon le CECR (Cadre Européen Commun de Référence pour les Langues) :

---
{request.text}
---

Évalue les critères suivants :
- Vocabulaire (richesse, précision, registre)
- Grammaire (structures utilisées, erreurs)
- Cohérence et cohésion (organisation des idées)
- Niveau CECR global : A1, A2, B1, B2, C1, ou C2

Réponds UNIQUEMENT avec un objet JSON valide, sans markdown ni code block :
{{
  "level": "B1",
  "score": 62,
  "analysis": "Analyse concise en 3-4 phrases expliquant le niveau détecté.",
  "recommendations": [
    "Conseil concret 1 pour progresser",
    "Conseil concret 2",
    "Conseil concret 3"
  ],
  "course_recommendation": "Si le niveau justifie une formation en langues à LTS Academy, mentionner la formation précise ici, sinon null."
}}
"""

    try:
        response = await llm.ainvoke([HumanMessage(content=prompt)])
        raw = response.content.strip()

        # Strip markdown code fences if present
        raw = re.sub(r"^```(?:json)?", "", raw).strip()
        raw = re.sub(r"```$", "", raw).strip()

        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not json_match:
            raise HTTPException(status_code=500, detail="Réponse IA invalide")

        data = json.loads(json_match.group())

        return LanguageDetectResponse(
            level=data.get("level", "A1"),
            score=int(data.get("score", 50)),
            analysis=data.get("analysis", ""),
            recommendations=data.get("recommendations", []),
            course_recommendation=data.get("course_recommendation"),
        )
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Erreur de parsing JSON: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")
