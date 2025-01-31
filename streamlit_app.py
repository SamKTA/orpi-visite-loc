import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import io
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Dossier de candidature ORPI", page_icon="🏠", layout="wide")

# Style CSS
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #E4032E;
        color: white;
    }
    .stButton>button:hover {
        background-color: #B5021F;
    }
    .stExpander {
        background-color: #ffffff;
        border: 1px solid #e6e6e6;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Dossier de candidature location")
conseiller = st.selectbox("Sélectionnez votre conseiller", ["Killian COURET", "Samuel KITA"])
tabs = st.tabs(["Locataire", "Garant", "Finalisation"])

# Onglet Locataire
with tabs[0]:
    st.header("Informations du locataire")
    
    with st.expander("État civil", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            nom_loc = st.text_input("NOM", key="nom_loc")
            nom_jeune_fille_loc = st.text_input("NOM DE JEUNE FILLE", key="nom_jf_loc")
            prenom_loc = st.text_input("PRÉNOM", key="prenom_loc")
        with col2:
            date_naissance_loc = st.date_input("DATE DE NAISSANCE", min_value=datetime(1940, 1, 1), max_value=datetime.now(), format="DD/MM/YYYY", key="date_naiss_loc")
            lieu_naissance_loc = st.text_input("LIEU DE NAISSANCE", key="lieu_naiss_loc")
            departement_loc = st.text_input("DÉPARTEMENT", key="dep_loc")
            pays_loc = st.text_input("PAYS", key="pays_loc")
            nationalite_loc = st.text_input("NATIONALITÉ", key="nat_loc")
        
        situation_loc = st.selectbox("SITUATION", ["Célibataire", "Marié(e)", "En instance de divorce", "Pacsé(e)", "Divorcé(e)"], key="sit_loc")

    with st.expander("Coordonnées", expanded=True):
        col3, col4 = st.columns(2)
        with col3:
            adresse_loc = st.text_input("ADRESSE ACTUELLE", key="adr_loc")
            code_postal_loc = st.text_input("CODE POSTAL", key="cp_loc")
            ville_loc = st.text_input("VILLE", key="ville_loc")
        with col4:
            telephone_loc = st.text_input("TÉLÉPHONE", key="tel_loc")
            email_loc = st.text_input("EMAIL", key="email_loc")

    with st.expander("Situation actuelle", expanded=True):
        col5, col6 = st.columns(2)
        with col5:
            situation_logement_loc = st.radio("Actuellement, vous êtes :", ["Propriétaire", "Locataire", "Hébergé"], key="log_loc")
        with col6:
            nb_enfants_loc = st.number_input("NOMBRE D'ENFANTS AU FOYER", min_value=0, key="enfants_loc")
            if nb_enfants_loc > 0:
                ages_enfants_loc = st.text_input("ÂGE DES ENFANTS", key="ages_loc")

    with st.expander("Situation professionnelle", expanded=True):
        col7, col8 = st.columns(2)
        with col7:
            profession_loc = st.text_input("PROFESSION", key="prof_loc")
            employeur_loc = st.text_input("EMPLOYEUR", key="emp_loc")
            date_embauche_loc = st.date_input("DATE D'EMBAUCHE", key="date_emb_loc")
        with col8:
            adresse_employeur_loc = st.text_input("ADRESSE DE L'EMPLOYEUR", key="adr_emp_loc")
            cp_employeur_loc = st.text_input("CODE POSTAL DE L'EMPLOYEUR", key="cp_emp_loc")
            ville_employeur_loc = st.text_input("VILLE DE L'EMPLOYEUR", key="ville_emp_loc")
            tel_employeur_loc = st.text_input("TÉLÉPHONE DE L'EMPLOYEUR", key="tel_emp_loc")

    with st.expander("Ressources", expanded=True):
        col9, col10 = st.columns(2)
        with col9:
            revenus_loc = st.number_input("REVENUS MENSUELS (€)", min_value=0.0, step=100.0, key="rev_loc")
            autres_revenus_loc = st.number_input("AUTRES REVENUS JUSTIFIÉS (€)", min_value=0.0, step=100.0, key="autres_rev_loc")
        with col10:
            total_loc = revenus_loc + autres_revenus_loc
            st.metric("TOTAL DES REVENUS", f"{total_loc:,.2f} €")

# Onglet Garant
with tabs[1]:
    st.header("Informations du garant")
    
    with st.expander("État civil", expanded=True):
        col11, col12 = st.columns(2)
        with col11:
            nom_gar = st.text_input("NOM", key="nom_gar")
            nom_jeune_fille_gar = st.text_input("NOM DE JEUNE FILLE", key="nom_jf_gar")
            prenom_gar = st.text_input("PRÉNOM", key="prenom_gar")
        with col12:
            date_naissance_gar = st.date_input("DATE DE NAISSANCE", min_value=datetime(1940, 1, 1), max_value=datetime.now(), format="DD/MM/YYYY", key="date_naiss_gar")
            lieu_naissance_gar = st.text_input("LIEU DE NAISSANCE", key="lieu_naiss_gar")
            departement_gar = st.text_input("DÉPARTEMENT", key="dep_gar")
            pays_gar = st.text_input("PAYS", key="pays_gar")
            nationalite_gar = st.text_input("NATIONALITÉ", key="nat_gar")
        
        situation_gar = st.selectbox("SITUATION", ["Célibataire", "Marié(e)", "En instance de divorce", "Pacsé(e)", "Divorcé(e)"], key="sit_gar")

    with st.expander("Coordonnées", expanded=True):
        col13, col14 = st.columns(2)
        with col13:
            adresse_gar = st.text_input("ADRESSE ACTUELLE", key="adr_gar")
            code_postal_gar = st.text_input("CODE POSTAL", key="cp_gar")
            ville_gar = st.text_input("VILLE", key="ville_gar")
        with col14:
            telephone_gar = st.text_input("TÉLÉPHONE", key="tel_gar")
            email_gar = st.text_input("EMAIL", key="email_gar")

    with st.expander("Situation professionnelle", expanded=True):
        col15, col16 = st.columns(2)
        with col15:
            profession_gar = st.text_input("PROFESSION", key="prof_gar")
            employeur_gar = st.text_input("EMPLOYEUR", key="emp_gar")
            date_embauche_gar = st.date_input("DATE D'EMBAUCHE", key="date_emb_gar")
        with col16:
            adresse_employeur_gar = st.text_input("ADRESSE DE L'EMPLOYEUR", key="adr_emp_gar")
            cp_employeur_gar = st.text_input("CODE POSTAL DE L'EMPLOYEUR", key="cp_emp_gar")
            ville_employeur_gar = st.text_input("VILLE DE L'EMPLOYEUR", key="ville_emp_gar")
            tel_employeur_gar = st.text_input("TÉLÉPHONE DE L'EMPLOYEUR", key="tel_emp_gar")

    with st.expander("Ressources", expanded=True):
        col17, col18 = st.columns(2)
        with col17:
            revenus_gar = st.number_input("REVENUS MENSUELS (€)", min_value=0.0, step=100.0, key="rev_gar")
            autres_revenus_gar = st.number_input("AUTRES REVENUS JUSTIFIÉS (€)", min_value=0.0, step=100.0, key="autres_rev_gar")
        with col18:
            total_gar = revenus_gar + autres_revenus_gar
            st.metric("TOTAL DES REVENUS", f"{total_gar:,.2f} €")

# Onglet Finalisation
with tabs[2]:
    st.header("Finalisation du dossier")
    
    st.warning("En soumettant ce dossier, je certifie que les renseignements fournis sont sincères et véritables.")
    
    col19, col20 = st.columns(2)
    with col19:
        sign_date = st.date_input("Date du jour", format="DD/MM/YYYY", key="sign_date")
        sign_lieu = st.text_input("Fait à", key="sign_lieu")

    def generer_pdf():
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        def draw_header(title):
            c.setFillColor(colors.HexColor('#E4032E'))
            c.rect(0, height-100, width, 100, fill=1)
            c.setFillColor('white')
            c.setFont("Helvetica-Bold", 24)
            c.drawString(50, height-60, title)
            c.setFont("Helvetica", 14)
            c.drawString(50, height-80, f"Présenté par {conseiller}")

        def draw_section(title, y_position):
            c.setFillColor(colors.HexColor('#E4032E'))
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y_position, title)
            c.line(50, y_position-5, width-50, y_position-5)
            return y_position - 25

        def draw_field(label, value, x, y, label_width=150):
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(colors.HexColor('#2D2D2D'))
            c.drawString(x, y, label)
            c.setFont("Helvetica", 10)
            c.drawString(x + label_width, y, str(value) if value else "")
            return y - 20

        # Page 1 - Locataire
        draw_header("Dossier de candidature location")
        
        y = height - 150
        y = draw_section("INFORMATIONS DU LOCATAIRE", y)
        
        # État civil
        x_left = 50
        x_right = width/2 + 50
        y = draw_field("Nom:", nom_loc, x_left, y)
        y = draw_field("Prénom:", prenom_loc, x_left, y)
        if nom_jeune_fille_loc:
            y = draw_field("Nom de jeune fille:", nom_jeune_fille_loc, x_left, y)
        y = draw_field("Date de naissance:", date_naissance_loc.strftime("%d/%m/%Y"), x_left, y)
        y = draw_field("Lieu de naissance:", f"{lieu_naissance_loc} ({departement_loc})", x_left, y)
        y = draw_field("Nationalité:", nationalite_loc, x_left, y)
        y = draw_field("Situation:", situation_loc, x_left, y)

        # Coordonnées
        y = y - 20
        y = draw_section("COORDONNÉES", y)
        y = draw_field("Adresse:", adresse_loc, x_left, y)
        y = draw_field("Code postal:", code_postal_loc, x_left, y)
        y = draw_field("Ville:", ville_loc, x_left, y)
        y = draw_field("Téléphone:", telephone_loc, x_left, y)
        y = draw_field("Email:", email_loc, x_left, y)
        y = draw_field("Situation actuelle:", situation_logement_loc, x_left, y)
        if nb_enfants_loc > 0:
            y = draw_field("Nombre d'enfants:", str(nb_enfants_loc), x_left, y)
            y = draw_field("Âge des enfants:", ages_enfants_loc, x_left, y)

        # Situation professionnelle
        y = y - 20
        y = draw_section("SITUATION PROFESSIONNELLE", y)
        y = draw_field("Profession:", profession_loc, x_left, y)
        y = draw_field("Employeur:", employeur_loc, x_left, y)
        y = draw_field("Date d'embauche:", date_embauche_loc.strftime("%d/%m/%Y"), x_left, y)
        y = draw_field("Adresse employeur:", adresse_employeur_loc, x_left, y)
        y = draw_field("CP et Ville employeur:", f"{cp_employeur_loc} {ville_employeur_loc}", x_left, y)
        y = draw_field("Téléphone employeur:", tel_employeur_loc, x_left, y)

        # Ressources
        y = y - 20
        y = draw_section("RESSOURCES", y)
        y = draw_field("Revenus mensuels:", f"{revenus_loc:,.2f} €", x_left, y)
        y = draw_field("Autres revenus:", f"{autres_revenus_loc:,.2f} €", x_left, y)
        y = draw_field("Total des revenus:", f"{total_loc:,.2f} €", x_left, y)

        # Page 2 - Garant
        c.showPage()
        draw_header("Dossier de cautionnement")
        
        y = height - 150
        y = draw_section("INFORMATIONS DU GARANT", y)
        
        y = draw_field("Nom:", nom_gar, x_left, y)
        y = draw_field("Prénom:", prenom_gar, x_left, y)
