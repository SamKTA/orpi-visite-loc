import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import io
from datetime import datetime

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Dossier de candidature ORPI",
    page_icon="🏠",
    layout="centered"
)

# Style CSS personnalisé
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
    .main {
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Titre et introduction
st.title("Dossier de candidature location")

# Sélection du conseiller
conseiller = st.selectbox(
    "Sélectionnez votre conseiller",
    ["Killian COURET"]
)

# Création des onglets pour séparer les informations
tabs = st.tabs(["Informations personnelles", "Situation professionnelle", "Ressources"])

# Onglet Informations personnelles
with tabs[0]:
    st.subheader("Vos informations")
    
    col1, col2 = st.columns(2)
    with col1:
        nom = st.text_input("NOM")
        nom_jeune_fille = st.text_input("NOM DE JEUNE FILLE (si applicable)")
        prenom = st.text_input("PRÉNOM")
        
    with col2:
        date_naissance = st.date_input("DATE DE NAISSANCE")
        lieu_naissance = st.text_input("LIEU DE NAISSANCE")
        departement = st.text_input("DÉPARTEMENT")

    col3, col4 = st.columns(2)
    with col3:
        pays = st.text_input("PAYS")
        nationalite = st.text_input("NATIONALITÉ")
        
    with col4:
        situation = st.selectbox(
            "SITUATION",
            ["Célibataire", "Marié(e)", "En instance de divorce", "Pacsé(e)", "Divorcé(e)"]
        )
        
    st.subheader("Contact")
    col5, col6 = st.columns(2)
    with col5:
        adresse = st.text_input("ADRESSE ACTUELLE")
        code_postal = st.text_input("CODE POSTAL")
        ville = st.text_input("VILLE")
        
    with col6:
        telephone = st.text_input("TÉLÉPHONE")
        email = st.text_input("EMAIL")
        
    st.subheader("Situation actuelle")
    col7, col8 = st.columns(2)
    with col7:
        situation_logement = st.radio(
            "Actuellement, vous êtes :",
            ["Propriétaire", "Locataire", "Hébergé"]
        )
    with col8:
        nb_enfants = st.number_input("NOMBRE D'ENFANTS AU FOYER", min_value=0)
        if nb_enfants > 0:
            ages_enfants = st.text_input("ÂGE DES ENFANTS (séparés par des virgules)")

# Onglet Situation professionnelle
with tabs[1]:
    st.subheader("Votre situation professionnelle")
    
    col9, col10 = st.columns(2)
    with col9:
        profession = st.text_input("PROFESSION")
        employeur = st.text_input("EMPLOYEUR")
        
    with col10:
        date_embauche = st.date_input("DATE D'EMBAUCHE")
        
    adresse_employeur = st.text_input("ADRESSE DE L'EMPLOYEUR")
    cp_employeur = st.text_input("CODE POSTAL DE L'EMPLOYEUR")
    ville_employeur = st.text_input("VILLE DE L'EMPLOYEUR")
    tel_employeur = st.text_input("TÉLÉPHONE DE L'EMPLOYEUR")

# Onglet Ressources
with tabs[2]:
    st.subheader("Vos ressources mensuelles")
    
    col11, col12 = st.columns(2)
    with col11:
        revenus = st.number_input("REVENUS MENSUELS (€)", min_value=0.0, step=100.0)
        autres_revenus = st.number_input("AUTRES REVENUS JUSTIFIÉS (€)", min_value=0.0, step=100.0)
        
    with col12:
        total = revenus + autres_revenus
        st.metric("TOTAL DES REVENUS", f"{total} €")

# Fonction pour générer le PDF
def generer_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Ajout du logo ORPI
    # c.drawImage("logo_orpi.png", 50, 750, width=100, height=50)
    
    # Titre
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Dossier de candidature location ORPI")
    
    # Informations personnelles
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 750, "Informations personnelles")
    c.setFont("Helvetica", 10)
    c.drawString(50, 730, f"Nom: {nom}")
    c.drawString(50, 715, f"Prénom: {prenom}")
    # ... Ajoutez toutes les autres informations ...
    
    c.save()
    buffer.seek(0)
    return buffer

# Fonction pour envoyer le PDF par email
def envoyer_pdf(pdf_buffer):
    expediteur = "skita@orpi.com"
    destinataire = "kcouret@orpi.com" if conseiller == "Killian COURET" else ""
    
    msg = MIMEMultipart()
    msg['From'] = expediteur
    msg['To'] = destinataire
    msg['Subject'] = f"Nouveau dossier de candidature - {nom} {prenom}"
    
    corps_message = f"Bonjour,\n\nVeuillez trouver ci-joint le dossier de candidature de {nom} {prenom}.\n\nCordialement"
    msg.attach(MIMEText(corps_message))
    
    pdf_attachment = MIMEApplication(pdf_buffer.getvalue(), _subtype="pdf")
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=f"dossier_candidature_{nom}_{prenom}.pdf")
    msg.attach(pdf_attachment)
    
    # Configuration du serveur SMTP (à adapter selon votre configuration)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # server.login(expediteur, "votre_mot_de_passe")
    # server.send_message(msg)
    # server.quit()

# Bouton de soumission
if st.button("Soumettre le dossier"):
    with st.spinner("Génération du PDF en cours..."):
        pdf = generer_pdf()
    
    with st.spinner("Envoi par email en cours..."):
        try:
            envoyer_pdf(pdf)
            st.success("Dossier envoyé avec succès!")
        except Exception as e:
            st.error(f"Erreur lors de l'envoi: {str(e)}")
            st.download_button(
                label="Télécharger le PDF",
                data=pdf,
                file_name=f"dossier_candidature_{nom}_{prenom}.pdf",
                mime="application/pdf"
            )
