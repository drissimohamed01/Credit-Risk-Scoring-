# -*- coding: utf-8 -*-
"""Generate French project overview PDF for Fin DataScience credit risk project."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUTPUT = Path(__file__).resolve().parent / "Presentation_Projet_Credit_Risk.pdf"


def build_pdf(path: Path) -> None:
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Presentation Projet Credit Risk Scoring",
        author="Fin DataScience",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=20,
        spaceAfter=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1a365d"),
    )
    h1 = ParagraphStyle(
        "H1",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=16,
        spaceAfter=8,
        textColor=colors.HexColor("#2c5282"),
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading3"],
        fontSize=12,
        spaceBefore=10,
        spaceAfter=6,
        textColor=colors.HexColor("#2d3748"),
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=10.5,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )
    bullet = ParagraphStyle(
        "Bullet",
        parent=body,
        leftIndent=12,
        bulletIndent=0,
        spaceAfter=4,
    )

    story = []

    story.append(Paragraph("Fin DataScience", styles["Normal"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Credit Risk Scoring — Vue d'ensemble du projet", title_style))
    story.append(
        Paragraph(
            "<i>Document de synthèse (lecture A à Z du dépôt de travail)</i>",
            ParagraphStyle("Sub", parent=styles["Normal"], alignment=TA_CENTER, fontSize=10),
        )
    )
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("1. Objectif du projet", h1))
    story.append(
        Paragraph(
            "Ce projet est un travail de <b>Finance Data Science</b> visant à construire un "
            "pipeline complet de <b>scoring du risque de crédit</b> pour des prêts à la consommation. "
            "L'objectif principal est de <b>prédire la probabilité de défaut</b> d'un emprunteur "
            "(variable cible <b>loan_status</b> : 0 = remboursement, 1 = défaut) à partir des "
            "caractéristiques de la demande et du profil client, puis de traduire ces prédictions "
            "en décisions et impacts métier (approbation, segmentation, perte attendue).",
            body,
        )
    )
    story.append(
        Paragraph(
            "Le notebook <b>Credit_Risk_Scoring.ipynb</b> suit un flux professionnel en quatre volets :",
            body,
        )
    )
    parts = [
        "<b>Partie 1</b> — Exploration et préparation des données (EDA, outliers, feature engineering).",
        "<b>Partie 2</b> — Construction et évaluation de trois modèles : régression logistique, XGBoost, LightGBM.",
        "<b>Partie 3</b> — Opérationnalisation : segments de risque, règle d'approbation, analyse de perte attendue (EL).",
        "<b>Chapitre 4</b> — Comparaison des modèles, choix stratégique et recommandations pour une institution de crédit.",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(p, bullet), leftIndent=18) for p in parts],
            bulletType="bullet",
            start="•",
        )
    )
    story.append(
        Paragraph(
            "En résumé, l'objectif n'est pas seulement d'obtenir un bon AUC, mais de montrer comment "
            "un modèle ML s'intègre dans la gestion du risque : équilibre entre <b>rappel sur les défauts</b> "
            "(éviter d'accorder de mauvais prêts) et <b>précision</b> (ne pas rejeter inutilement de bons clients), "
            "alignement réglementaire (interprétabilité) et quantification économique (PD, EL).",
            body,
        )
    )

    story.append(Paragraph("2. Contenu du dépôt (inventaire)", h1))
    inv_data = [
        ["Fichier", "Rôle"],
        ["Credit_Risk_Scoring.ipynb", "Notebook principal : workflow ML + business"],
        ["cr_loan2.csv", "Jeu de données (~32 000+ demandes de prêt)"],
        [".Rhistory", "Historique R (artefact local, hors pipeline Python)"],
    ]
    t_inv = Table(inv_data, colWidths=[5.5 * cm, 11 * cm])
    t_inv.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf2f7")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
            ]
        )
    )
    story.append(t_inv)
    story.append(Spacer(1, 0.3 * cm))

    story.append(Paragraph("3. Données utilisées", h1))
    story.append(
        Paragraph(
            "Source unique : <b>cr_loan2.csv</b>. Variables principales (sens métier) :",
            body,
        )
    )
    var_data = [
        ["Variable", "Type", "Signification"],
        ["person_age", "Numérique", "Âge du demandeur"],
        ["person_income", "Numérique", "Revenu annuel"],
        ["person_home_ownership", "Catégorielle", "Statut logement (RENT, OWN, MORTGAGE…)"],
        ["person_emp_length", "Numérique", "Ancienneté emploi (années)"],
        ["loan_intent", "Catégorielle", "Objet du prêt"],
        ["loan_grade", "Catégorielle", "Note interne de risque"],
        ["loan_amnt / loan_int_rate", "Numérique", "Montant et taux d'intérêt"],
        ["loan_percent_income", "Numérique", "Part du revenu consacrée au prêt"],
        ["cb_person_default_on_file", "Catégorielle", "Défaut antérieur (Y/N)"],
        ["cb_person_cred_hist_length", "Numérique", "Longueur historique crédit"],
        ["loan_status", "Cible", "0 = non-défaut, 1 = défaut"],
    ]
    t_var = Table(var_data, colWidths=[4.2 * cm, 2.5 * cm, 10 * cm])
    t_var.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf2f7")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(t_var)

    story.append(Paragraph("4. Méthodologie (résumé A à Z)", h1))

    story.append(Paragraph("4.1 Partie 1 — Exploration et préparation", h2))
    p1 = [
        "Inspection : dimensions, types, valeurs manquantes, doublons, statistiques descriptives.",
        "EDA : distribution de la cible, histogrammes, boxplots, countplots, heatmap de corrélation, analyse défaut vs non-défaut.",
        "Outliers : méthode IQR (Q1 − 1,5×IQR, Q3 + 1,5×IQR) avec winsorisation (clip) sur variables numériques clés.",
        "Traitement : imputation médiane (emploi ; taux par grade de prêt), suppression des doublons.",
        "Feature engineering : prior_default_flag, short_credit_history, high_payment_burden, income_to_loan_ratio, annual_interest_cost, income_tier, age_group.",
        "Encodage one-hot des catégories, StandardScaler (ajusté sur train uniquement), split train/test stratifié (random_state=42).",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(x, bullet), leftIndent=18) for x in p1],
            bulletType="bullet",
        )
    )

    story.append(Paragraph("4.2 Partie 2 — Modélisation", h2))
    story.append(
        Paragraph(
            "Trois classificateurs binaires comparés sur le même jeu de test, avec métriques "
            "Accuracy, Precision, Recall, F1, ROC-AUC, matrices de confusion et courbes ROC :",
            body,
        )
    )
    mod_data = [
        ["Modèle", "Rôle / particularité"],
        [
            "Régression logistique",
            "Baseline interprétable (coefficients, log-odds, PD) ; features standardisées.",
        ],
        [
            "XGBoost",
            "Gradient boosting ; scale_pos_weight pour déséquilibre des classes ; features non scalées.",
        ],
        [
            "LightGBM",
            "Boosting leaf-wise, histogrammes ; adapté aux grands jeux tabulaires.",
        ],
    ]
    t_mod = Table(mod_data, colWidths=[4 * cm, 12.5 * cm])
    t_mod.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf2f7")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
            ]
        )
    )
    story.append(t_mod)
    story.append(
        Paragraph(
            "Analyse d'erreurs : interprétation métier des faux positifs (bon client rejeté) "
            "et faux négatifs (mauvais prêt accordé). Importance des variables (coefficients LR, gain XGBoost, importance LightGBM).",
            body,
        )
    )

    story.append(Paragraph("4.3 Partie 3 — Opérationnalisation", h2))
    story.append(
        Paragraph(
            "Sur le portefeuille test, utilisation de la <b>probabilité de défaut (PD)</b> prédite par le modèle retenu pour l'opérationnel :",
            body,
        )
    )
    seg_data = [
        ["Segment", "Plage PD", "Politique indicative"],
        ["Faible risque", "PD &lt; 15 %", "Approbation — tarification standard"],
        ["Risque moyen", "15 % ≤ PD &lt; 35 %", "Approbation avec suivi / taux plus élevé"],
        ["Risque élevé", "PD ≥ 35 %", "Rejet ou garanties"],
    ]
    t_seg = Table(seg_data, colWidths=[3.5 * cm, 3.5 * cm, 9.5 * cm])
    t_seg.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf2f7")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
            ]
        )
    )
    story.append(t_seg)
    story.append(
        Paragraph(
            "<b>Règle implémentée dans le notebook :</b> approuver si PD &lt; 30 %, sinon rejeter. "
            "Calcul de la <b>perte attendue</b> : EL = PD × LGD × EAD, avec LGD = 45 % (hypothèse prêt non garanti) "
            "et EAD = montant du prêt (loan_amnt). Visualisation de l'EL par segment et comparaison EL sur dossiers approuvés vs rejetés.",
            body,
        )
    )

    story.append(Paragraph("4.4 Chapitre 4 — Stratégie", h2))
    ch4 = [
        "Tableau comparatif des métriques entre les trois modèles (meilleur modèle identifié notamment via ROC-AUC).",
        "Discussion : performance vs interprétabilité, coût de calcul, transparence réglementaire (scorecards vs modèles challenger).",
        "Recommandations : tarification basée sur le risque, approbation automatisée hybride (règles + score ML), monitoring des segments moyens, segmentation portefeuille, réduction de l'EL.",
        "Pistes d'amélioration : données bureau supplémentaires, CatBoost, ensembles, calibration PD, SHAP, stress tests.",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(x, bullet), leftIndent=18) for x in ch4],
            bulletType="bullet",
        )
    )

    story.append(PageBreak())

    story.append(Paragraph("5. Outils et bibliothèques utilisés", h1))

    story.append(Paragraph("5.1 Environnement et langage", h2))
    story.append(
        Paragraph(
            "<b>Python 3</b> exécuté dans un <b>Jupyter Notebook</b> (Credit_Risk_Scoring.ipynb). "
            "Pas de fichier requirements.txt dans le dépôt ; les imports du notebook définissent la stack.",
            body,
        )
    )

    story.append(Paragraph("5.2 Bibliothèques Python", h2))
    tools_data = [
        ["Catégorie", "Bibliothèque", "Usage dans le projet"],
        ["Données", "pandas, numpy", "Chargement CSV, manipulation, features, agrégations"],
        ["Visualisation", "matplotlib, seaborn", "Graphiques EDA, heatmaps, ROC, EL"],
        ["ML — scikit-learn", "sklearn", "Split, StandardScaler, LogisticRegression, métriques, ROC"],
        ["ML — boosting", "xgboost (XGBClassifier)", "Modèle gradient boosting"],
        ["ML — boosting", "lightgbm", "Modèle LightGBM"],
        ["Stdlib", "warnings", "Filtrage des avertissements"],
    ]
    t_tools = Table(tools_data, colWidths=[3.2 * cm, 4.5 * cm, 9 * cm])
    t_tools.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#edf2f7")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(t_tools)

    story.append(Paragraph("5.3 Concepts métier / réglementaires cités", h2))
    story.append(
        Paragraph(
            "PD (Probability of Default), EL (Expected Loss), LGD, EAD, IFRS 9 / Basel IRB (calibration PD), "
            "principes de gouvernance des modèles (SR 11-7 / ECB TRIM), scorecards vs modèles challenger.",
            body,
        )
    )

    story.append(Paragraph("6. Principaux facteurs de risque identifiés", h1))
    drivers = [
        "Charge de remboursement : loan_percent_income, high_payment_burden.",
        "Signaux de tarification : loan_int_rate, loan_grade.",
        "Historique bureau : prior_default_flag, cb_person_cred_hist_length.",
        "Capacité de remboursement : person_income, income_to_loan_ratio.",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(d, bullet), leftIndent=18) for d in drivers],
            bulletType="bullet",
        )
    )

    story.append(Paragraph("7. Limites mentionnées dans le projet", h1))
    lim = [
        "Données transversales (pas de validation out-of-time ni stress macro).",
        "loan_grade potentiellement endogène au moment de la demande.",
        "LGD et EAD simplifiés ; pas d'inférence sur les rejets (reject inference).",
    ]
    story.append(
        ListFlowable(
            [ListItem(Paragraph(x, bullet), leftIndent=18) for x in lim],
            bulletType="bullet",
        )
    )

    story.append(Spacer(1, 0.5 * cm))
    story.append(
        Paragraph(
            "<i>Document généré automatiquement à partir de l'analyse du dépôt Fin DataScience.</i>",
            ParagraphStyle("Foot", parent=styles["Normal"], fontSize=9, textColor=colors.grey),
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build_pdf(OUTPUT)
    print(f"PDF créé : {OUTPUT}")
