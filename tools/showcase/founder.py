"""Public founder copy shared by the IMPERIAL Core showcase and founder profile."""

from html import escape

ROLE = "Founder · Owner · CEO · Chief Systems Architect of IMPERIAL Core"
ROLE_RU = "Основатель · Владелец · Генеральный директор · Главный системный архитектор IMPERIAL Core"
BIOGRAPHIES = {
    "en": {
        "statement": "Engineering the Future of Artificial Intelligence.",
        "intro": "Alexander Romaskevich is an independent technology founder, AI systems architect, and developer focused on building the next generation of intelligent digital ecosystems.",
        "architecture": "He is the creator and chief architect of IMPERIAL Core, an ambitious AI-native ecosystem designed around federated intelligence, autonomous agents, enterprise security, and verifiable execution.",
        "principles_intro": "His engineering philosophy is built on three principles:",
        "principles": ("Architecture Before Implementation.", "Evidence Before Claims.", "Human Authority Above Artificial Intelligence."),
        "federation": "Rather than approaching artificial intelligence as a collection of isolated tools, Alexander is developing a unified architectural vision in which specialized AI systems, professional agent teams, and independent orchestration domains operate under clearly defined governance and security boundaries.",
        "portfolio": "His engineering portfolio includes HANTER, VELION, Nano Core Agents, CONSTRUCTOR AI, CYBER HAK, AI Passport, and AGY.",
        "purpose": "Each project contributes to a long-term vision of intelligent systems that can reason, coordinate, execute, and demonstrate their results while preserving human authority.",
        "vision_title": "The Vision",
        "vision": "To build intelligent systems that transform ambitious ideas into real, secure, and verifiable technology.",
        "ambition": "Alexander’s ambition extends beyond individual software products. His goal is to establish a lasting technological ecosystem capable of evolving across industries, organizations, and generations.",
        "message_title": "A Message from the Founder",
        "message": (
            "I don’t measure engineering excellence by the complexity of an idea. I measure it by what we can build, verify, improve, and ultimately deliver.",
            "My ambition is to create technology that will continue to evolve long after its first version.",
        ),
        "signature_role": "Founder · Owner · CEO",
        "closing": "One Vision. One Architecture. Infinite Possibilities.",
    },
    "ru": {
        "statement": "Создавая будущее искусственного интеллекта.",
        "intro": "Александр Ромаскевич — независимый основатель технологических проектов, архитектор ИИ-систем и разработчик. Он создаёт новое поколение интеллектуальных цифровых экосистем.",
        "architecture": "Александр создал IMPERIAL Core и возглавляет его архитектуру. В основе этой AI-native экосистемы лежат федеративный интеллект, автономные агенты, безопасность корпоративного уровня и проверяемое исполнение.",
        "principles_intro": "Его инженерная философия опирается на три принципа.",
        "principles": ("Сначала архитектура, затем реализация.", "Сначала доказательства, затем заявления.", "Право окончательного решения всегда остаётся за человеком."),
        "federation": "Александр развивает общую архитектуру, в которой специализированные ИИ-системы, профессиональные команды агентов и независимые домены оркестрации работают в чётко заданных границах управления и безопасности.",
        "portfolio": "В его инженерное портфолио входят HANTER, VELION, Nano Core Agents, CONSTRUCTOR AI, CYBER HAK, AI Passport и AGY.",
        "purpose": "Каждый проект служит долгосрочной цели: создать системы, которые умеют рассуждать, координировать работу, выполнять задачи и предъявлять проверяемые результаты под руководством человека.",
        "vision_title": "Видение",
        "vision": "Создавать интеллектуальные системы, которые превращают амбициозные идеи в реальные, безопасные и проверяемые технологии.",
        "ambition": "Цель Александра выходит за рамки отдельных программных продуктов. Он стремится построить долговечную технологическую экосистему, способную развиваться в разных отраслях и организациях и оставаться востребованной для будущих поколений.",
        "message_title": "Слово основателя",
        "message": (
            "Я оцениваю качество инженерной работы по тому, что мы можем создать, проверить, улучшить и в итоге довести до результата. Сложность самой идеи для меня вторична.",
            "Я хочу создавать технологии, которые будут развиваться ещё долго после появления первой версии.",
        ),
        "signature_role": "Основатель · Владелец · Генеральный директор",
        "closing": "Одно видение. Единая архитектура. Безграничные возможности.",
    },
}


def render_biography(lang):
    """Render the paragraphs after the introductory sentence and headline."""
    t = BIOGRAPHIES[lang]
    principles = "".join(f"<li>{escape(item)}</li>" for item in t["principles"])
    first, second = map(escape, t["message"])
    return f"""<div class="founder-story">
  <p>{escape(t["architecture"])}</p>
  <p>{escape(t["principles_intro"])}</p>
  <ul class="founder-principles">{principles}</ul>
  <p>{escape(t["federation"])}</p>
  <p>{escape(t["portfolio"])}</p>
  <p>{escape(t["purpose"])}</p>
  <h3>{escape(t["vision_title"])}</h3>
  <p>{escape(t["vision"])}</p>
  <p>{escape(t["ambition"])}</p>
  <h3>{escape(t["message_title"])}</h3>
  <blockquote><p>“{first}</p><p>{second}”</p></blockquote>
  <p class="founder-signature"><strong>Alexander Romaskevich</strong><br>{escape(t["signature_role"])}<br>IMPERIAL Core</p>
  <p class="founder-closing">{escape(t["closing"])}</p>
</div>"""
