
import streamlit as st
from pathlib import Path
from textwrap import dedent

from ariane_engine import ArianeEngine


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ARIANE - UTT",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS
# ============================================================

css_path = Path(__file__).parent / "assets" / "style.css"

with open(css_path, "r", encoding="utf-8") as f:
    st.html(
        f"<style>{f.read()}</style>"
    )


# ============================================================
# HELPERS
# ============================================================

def render_html(content):
    st.html(
        dedent(content)
    )


@st.cache_resource(
    show_spinner=False
)
def load_ariane():
    return ArianeEngine()


# ============================================================
# NAVIGATION
# ============================================================

page = st.query_params.get(
    "page",
    "dashboard"
)


# ============================================================
# HEADER UTT
# ============================================================

render_html("""
<div class="utt-topbar">

    <div class="utt-brand">
        <div class="utt-logo">utt</div>
        <div class="eut-logo">— eUT+</div>
    </div>

    <div class="topnav">
        <a href="?page=dashboard">Tableau de bord</a>
        <a href="?page=courses">Mes cours</a>
        <a class="catalogue" href="#">⌕ Catalogue UE</a>
        <a href="#">Espaces d'information⌄</a>
    </div>

    <div class="top-actions">
        <span>Français (fr)⌄</span>
        <span>●</span>
        <span>👤</span>
    </div>

</div>

<div class="ariane-subbar">
    <div class="ariane-home">ARIANE</div>
</div>
""")


# ============================================================
# TABLEAU DE BORD ETUDIANT
# ============================================================

if page == "dashboard":

    render_html("""
    <div class="page-wrap">

        <div class="page-title-row">

            <h1 class="page-title">
                ☰ ARIANE – <span>Mon compagnon pédagogique</span>
            </h1>

            <a
                class="revision-btn"
                href="?page=revision"
            >
                ♧ Mon carnet de révision
            </a>

        </div>


        <div class="section-title">
            Mes cours ARIANE
        </div>


        <div class="course-grid">

            <div class="course-card">

                <div class="course-head">
                    <div class="course-icon">🎓</div>

                    <div class="course-code">
                        STAT_PROBA
                    </div>
                </div>

                <div class="course-body">

                    <div class="course-name">
                        Statistiques et probabilités
                    </div>

                    <div class="course-semester">
                        Semestre en cours
                    </div>

                    <a
                        class="primary-link"
                        href="?page=course&course=STAT_PROBA"
                    >
                        Accéder au cours ›
                    </a>

                </div>

            </div>


            <div class="course-card">

                <div class="course-head">
                    <div class="course-icon">⬡</div>

                    <div class="course-code">
                        GS10
                    </div>
                </div>

                <div class="course-body">

                    <div class="course-name">
                        Sécurité des SI
                    </div>

                    <div class="course-semester">
                        Semestre en cours
                    </div>

                    <a
                        class="primary-link"
                        href="?page=course&course=GS10"
                    >
                        Accéder au cours ›
                    </a>

                </div>

            </div>


            <div class="course-card">

                <div class="course-head">
                    <div class="course-icon">◯</div>

                    <div class="course-code">
                        LEM2
                    </div>
                </div>

                <div class="course-body">

                    <div class="course-name">
                        Anglais
                    </div>

                    <div class="course-semester">
                        Semestre en cours
                    </div>

                    <a
                        class="primary-link"
                        href="?page=course&course=LEM2"
                    >
                        Accéder au cours ›
                    </a>

                </div>

            </div>

        </div>


        <div class="dashboard-grid">

            <div class="dashboard-panel">

                <div class="panel-title">
                    À reprendre avec ARIANE
                </div>

                <div class="panel-row">
                    <div class="panel-row-left">
                        <span class="doc-icon">▧</span>
                        <span>Variance et écart-type</span>
                    </div>
                </div>

                <div class="panel-row">
                    <div class="panel-row-left">
                        <span class="doc-icon">▧</span>
                        <span>Gestion des accès LDAP</span>
                    </div>
                </div>

                <div class="panel-row">
                    <div class="panel-row-left">
                        <span class="doc-icon">▧</span>
                        <span>Lois de probabilité usuelles</span>
                    </div>
                </div>

            </div>


            <div class="dashboard-panel">

                <div class="panel-title">
                    Activité récente
                </div>

                <div class="panel-row">
                    <div class="panel-row-left">
                        <span class="doc-icon">▧</span>
                        <span>Explication : Loi normale</span>
                    </div>

                    <span class="activity-date">
                        Aujourd'hui, 08:12
                    </span>
                </div>

                <div class="panel-row">
                    <div class="panel-row-left">
                        <span class="doc-icon">▧</span>
                        <span>Synthèse : Gestion des comptes (AD)</span>
                    </div>

                    <span class="activity-date">
                        Hier, 17:46
                    </span>
                </div>

                <div class="panel-row">
                    <div class="panel-row-left">
                        <span class="doc-icon">▧</span>
                        <span>Rappel : Variance et écart-type</span>
                    </div>

                    <span class="activity-date">
                        12 nov., 14:28
                    </span>
                </div>

            </div>

        </div>

    </div>
    """)


# ============================================================
# VUE D'UN COURS
# ============================================================

elif page == "course":

    course = st.query_params.get(
        "course",
        "STAT_PROBA"
    )

    render_html("""
    <div class="page-wrap">

        <div class="course-page-header">

            <div class="breadcrumb">
                ⌂ Tableau de bord / Mes cours / STAT_PROBA
            </div>

            <div class="course-small-code">
                [STAT_PROBA]
            </div>

            <div class="course-big-title">
                Statistiques et probabilités
            </div>

        </div>


        <div class="course-tabs">

            <a class="course-tab active" href="#">
                Vue du cours
            </a>

            <a class="course-tab" href="#">
                Ressources
            </a>

            <a class="course-tab" href="#">
                Contributions
            </a>

            <a class="course-tab" href="?page=revision">
                Mon carnet
            </a>

        </div>


        <div class="course-layout">


            <!-- PLAN DU COURS -->

            <div class="course-plan">

                <div class="course-plan-title">
                    Plan du cours
                </div>

                <div class="plan-section">
                    1. Rappels et concepts de base
                </div>

                <div class="plan-section">
                    2. Variables aléatoires
                </div>

                <div class="plan-section">
                    3. Lois usuelles
                </div>

                <div class="plan-section">
                    4. Moments et dispersion
                </div>

                <div class="plan-subitem">
                    ▧ Slide 5 — Définition de la variance
                </div>

                <div class="plan-subitem">
                    ▧ Slide 6 — Pourquoi le carré ?
                </div>

                <div class="plan-subitem active">
                    ▧ Slide 7 — Propriétés
                </div>

                <div class="plan-subitem">
                    ▧ Slide 8 — Écart-type
                </div>

                <div class="plan-subitem">
                    ▧ Slide 9 — Unités
                </div>

                <div class="plan-section">
                    5. Estimation
                </div>

                <div class="plan-section">
                    6. Tests statistiques
                </div>

            </div>


            <!-- SUPPORT OFFICIEL -->

            <div class="slide-panel">

                <div class="slide-panel-head">
                    Slide 7 — Propriétés de la variance
                </div>

                <div class="fake-slide">

                    <div class="fake-slide-header">
                        <strong>utt</strong>

                        <span>
                            STAT_PROBA — Statistiques et probabilités
                        </span>
                    </div>

                    <div class="fake-slide-body">

                        <div class="fake-slide-title">
                            Propriétés de la variance
                        </div>

                        <ul>
                            <li>
                                La variance mesure la dispersion
                                autour de la moyenne.
                            </li>
                        </ul>

                        <div class="formula-box">
                            Var(aX + b) = a² Var(X)
                        </div>

                        <ul>
                            <li>V ≥ 0</li>

                            <li>
                                Ajouter une constante b ne change
                                pas la variance.
                            </li>

                            <li>
                                Multiplier toutes les valeurs par a
                                multiplie la variance par a².
                            </li>

                            <li>
                                Var(aX + b) = a² Var(X)
                            </li>
                        </ul>

                    </div>

                </div>

                <div class="slide-controls">

                    <a class="slide-nav-btn">
                        ‹ Slide précédente
                    </a>

                    <span>
                        7 / 19
                    </span>

                    <a class="slide-nav-btn">
                        Slide suivante ›
                    </a>

                </div>

            </div>


            <!-- PANNEAU ARIANE -->

            <div class="ariane-panel">

                <div class="ariane-panel-title">
                    ♙ Avec ARIANE
                </div>

                <div class="ariane-summary">

                    <div class="summary-title">
                        ♟ Synthèse de la promotion
                    </div>

                    <div class="summary-subtitle">
                        Synthèse issue de contributions validées
                    </div>

                    <ul>

                        <li>
                            La variance quantifie la dispersion
                            autour de la moyenne.
                        </li>

                        <li>
                            Elle est toujours positive ou nulle.
                        </li>

                        <li>
                            Elle est sensible au changement
                            d'échelle.
                        </li>

                    </ul>

                    <a
                        class="ask-ariane-btn"
                        href="?page=ask&course=STAT_PROBA&slide=7"
                    >
                        ▢ Interroger ARIANE sur cette partie
                    </a>

                </div>

                <div class="ariane-info">
                    ⓘ Réponse basée en priorité sur le support officiel
                    de l'enseignant et sur les synthèses collectives
                    validées.
                </div>

            </div>

        </div>

    </div>
    """)


# ============================================================
# INTERROGER ARIANE
# ============================================================

elif page == "ask":

    course = st.query_params.get(
        "course",
        "STAT_PROBA"
    )

    selected_slide = int(
        st.query_params.get(
            "slide",
            7
        )
    )


    # --------------------------------------------------------
    # EN-TETE
    # --------------------------------------------------------

    render_html(f"""
    <div class="page-wrap">

        <div class="breadcrumb">
            ⌂ Tableau de bord /
            Mes cours /
            {course} /
            Interroger ARIANE
        </div>

        <div class="ask-header">

            <div class="ask-title">
                ARIANE – Statistiques et probabilités
            </div>

            <div class="ask-course">
                Support officiel prioritaire ·
                réponses contextualisées et sourcées
            </div>

        </div>

    </div>
    """)


    # --------------------------------------------------------
    # CONTENU
    # --------------------------------------------------------

    _, center, _ = st.columns(
        [0.04, 0.92, 0.04]
    )


    with center:

        # ====================================================
        # SCOPE
        # ====================================================

        st.markdown(
            "**Portée de la réponse**"
        )

        scope_label = st.radio(
            "Portée",
            [
                "Cette diapositive",
                "Ce chapitre",
                "Tout le cours"
            ],
            horizontal=True,
            label_visibility="collapsed"
        )

        scope_map = {
            "Cette diapositive": "slide",
            "Ce chapitre": "chapter",
            "Tout le cours": "course"
        }


        # ====================================================
        # QUESTION
        # ====================================================

        question = st.text_input(
            "Question",
            placeholder=(
                "Posez votre question sur le contenu du cours..."
            ),
            label_visibility="collapsed"
        )


        ask_button = st.button(
            "Obtenir une explication",
            type="primary",
            use_container_width=True
        )


        # ====================================================
        # APPEL ARIANE
        # ====================================================

        if (
            ask_button
            and
            question.strip()
        ):

            engine = load_ariane()

            with st.spinner(
                "ARIANE analyse le support officiel..."
            ):

                result = engine.ask(
                    question,
                    scope=scope_map[scope_label],
                    slide=selected_slide
                )


            st.session_state[
                "ariane_result"
            ] = result

            st.session_state[
                "ariane_question"
            ] = question


        # ====================================================
        # REPONSE
        # ====================================================

        if (
            "ariane_result"
            in st.session_state
        ):

            result = st.session_state[
                "ariane_result"
            ]

            st.write("")


            response_col, sources_col = st.columns(
                [2.15, 1]
            )


            # ------------------------------------------------
            # REPONSE PRINCIPALE
            # ------------------------------------------------

            with response_col:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 🔒 Réponse d’ARIANE"
                    )

                    st.markdown(
                        "#### D’après le cours"
                    )

                    st.markdown(
                        result["answer"]
                    )

                    st.markdown("---")

                    st.markdown(
                        "#### 👥 Ce que les notes "
                        "de la promotion ajoutent"
                    )

                    st.info(
                        "Les contributions validées "
                        "reformulent notamment que "
                        "la variance décrit la dispersion "
                        "et que le changement d’échelle "
                        "agit sur sa valeur."
                    )

                    st.markdown(
                        """
                        <div class="answer-warning">

                        ⚠ <strong>Point d’attention</strong><br>

                        Le support officiel de l’enseignant
                        reste la source de référence.
                        Les synthèses collectives ne remplacent
                        jamais le contenu du cours.

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


            # ------------------------------------------------
            # SOURCES
            # ------------------------------------------------

            with sources_col:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 📄 Sources utilisées"
                    )

                    for source in result[
                        "sources"
                    ]:

                        st.markdown(
                            f"""
                            **Slide {source['slide']}**

                            Score de pertinence :
                            `{source['score']:.3f}`
                            """
                        )

                        st.divider()


                    st.caption(
                        f"Retrieval : "
                        f"{result['retrieval_time']:.2f} s"
                    )

                    st.caption(
                        f"Génération : "
                        f"{result['generation_time']:.2f} s"
                    )

                    st.caption(
                        f"Total : "
                        f"{result['total_time']:.2f} s"
                    )


            # ------------------------------------------------
            # ACTIONS
            # ------------------------------------------------

            col_a, col_b, col_c = st.columns(
                3
            )


            with col_a:

                st.button(
                    "♡ Ajouter à mon carnet",
                    use_container_width=True
                )


            with col_b:

                st.button(
                    "↻ Réviser cette notion",
                    use_container_width=True
                )


            with col_c:

                if st.button(
                    "← Retour au cours",
                    use_container_width=True
                ):

                    st.query_params[
                        "page"
                    ] = "course"

                    st.query_params[
                        "course"
                    ] = course

                    st.rerun()


# ============================================================
# PLACEHOLDERS AUTRES PAGES
# ============================================================

else:

    render_html("""
    <div class="page-wrap">

        <h1 class="page-title">
            Page en construction
        </h1>

        <br>

        <a
            class="primary-link"
            href="?page=dashboard"
        >
            ← Tableau de bord
        </a>

    </div>
    """)
