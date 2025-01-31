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
    ["Killian COURET", "Samuel KITA"]
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
        date_naissance = st.date_input(
            "DATE DE NAISSANCE",
            min_value=datetime(1940, 1, 1),
            max_value=datetime.now(),
            format="DD/MM/YYYY"
        )
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
        width, height = A4  # Pour faciliter le positionnement
        
        # Couleurs ORPI
        rouge_orpi = (228/255, 3/255, 46/255)  # #E4032E
        gris_fonce = (45/255, 45/255, 45/255)  # #2D2D2D
        gris_clair = (128/255, 128/255, 128/255)
        
        # En-tête
        c.setFillColor(rouge_orpi)
        c.rect(0, height-100, width, 100, fill=1)
        c.setFillColor('white')
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, height-60, "Dossier de candidature location")
        c.setFont("Helvetica", 14)
        c.drawString(50, height-80, f"Présenté par {conseiller}")
        
        # Fonction helper pour les sections
        def draw_section(title, y_position):
            c.setFillColor(rouge_orpi)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, y_position, title)
            c.setFillColor(gris_clair)
            c.line(50, y_position-5, width-50, y_position-5)
            c.setFillColor(gris_fonce)
            return y_position - 30

        # Fonction helper pour les champs
        def draw_field(label, value, x, y, label_width=120):
            c.setFont("Helvetica-Bold", 10)
            c.drawString(x, y, label)
            c.setFont("Helvetica", 10)
            c.drawString(x + label_width, y, str(value))
            return y - 20

        # Informations personnelles
        y = height - 150
        y = draw_section("Informations personnelles", y)
        
        # Colonne gauche
        x_left = 50
        y_temp = y
        y_temp = draw_field("Nom:", nom.upper(), x_left, y_temp)
        y_temp = draw_field("Prénom:", prenom.title(), x_left, y_temp)
        if nom_jeune_fille:
            y_temp = draw_field("Nom de j. fille:", nom_jeune_fille.upper(), x_left, y_temp)
        y_temp = draw_field("Date de naissance:", date_naissance.strftime("%d/%m/%Y"), x_left, y_temp)
        y_temp = draw_field("Lieu de naissance:", lieu_naissance, x_left, y_temp)
        
        # Colonne droite
        x_right = width/2 + 50
        y_temp = y
        y_temp = draw_field("Nationalité:", nationalite, x_right, y_temp)
        y_temp = draw_field("Situation:", situation, x_right, y_temp)
        y_temp = draw_field("Téléphone:", telephone, x_right, y_temp)
        y_temp = draw_field("Email:", email, x_right, y_temp)
        
        y = min(y_temp, y) - 30

        # Adresse actuelle
        y = draw_section("Adresse actuelle", y)
        y = draw_field("Adresse:", adresse, 50, y)
        y = draw_field("Code postal:", code_postal, 50, y)
        y = draw_field("Ville:", ville, 50, y)
        y = draw_field("Statut:", situation_logement, 50, y)
        
        # Situation familiale
        y = draw_section("Situation familiale", y-20)
        y = draw_field("Nombre d'enfants:", str(nb_enfants), 50, y)
        if nb_enfants > 0 and ages_enfants:
            y = draw_field("Âge des enfants:", ages_enfants, 50, y)
            
        # Situation professionnelle
        y = draw_section("Situation professionnelle", y-20)
        
        # Colonne gauche
        x_left = 50
        y_temp = y
        y_temp = draw_field("Profession:", profession, x_left, y_temp)
        y_temp = draw_field("Employeur:", employeur, x_left, y_temp)
        y_temp = draw_field("Date d'embauche:", date_embauche.strftime("%d/%m/%Y"), x_left, y_temp)
        
        # Colonne droite
        x_right = width/2 + 50
        y_temp = y
        y_temp = draw_field("Tél. employeur:", tel_employeur, x_right, y_temp)
        
        y = min(y_temp, y) - 20
        
        # Adresse employeur
        y = draw_field("Adresse:", adresse_employeur, 50, y)
        y = draw_field("Code postal:", cp_employeur, 50, y)
        y = draw_field("Ville:", ville_employeur, 50, y)
        
        # Ressources financières
        y = draw_section("Ressources financières", y-20)
        y = draw_field("Revenus mensuels:", f"{revenus:,.2f} €", 50, y)
        y = draw_field("Autres revenus:", f"{autres_revenus:,.2f} €", 50, y)
        
        c.setFillColor(rouge_orpi)
        c.setFont("Helvetica-Bold", 12)
        y = draw_field("TOTAL:", f"{total:,.2f} €", 50, y)
        
        # Pied de page
        c.setFillColor(gris_clair)
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(50, 30, "Document généré le " + datetime.now().strftime("%d/%m/%Y à %H:%M"))
        c.drawString(50, 20, "Les informations contenues dans ce document sont strictement confidentielles")
        
        c.save()
        buffer.seek(0)
        return buffer

    # Fonction pour envoyer le PDF par email
    def envoyer_pdf(pdf_buffer):
        expediteur = "skita@orpi.com"
        destinataire = "kcouret@orpi.com" if conseiller == "Killian COURET" else "skita@orpi.com"
        
        msg = MIMEMultipart()
        msg['From'] = expediteur
        msg['To'] = destinataire
        msg['Subject'] = f"Nouveau dossier de candidature - {nom} {prenom}"
        
        corps_message = f"Bonjour,\n\nVeuillez trouver ci-joint le dossier de candidature de {nom} {prenom}.\n\nCordialement"
        msg.attach(MIMEText(corps_message))
        
        pdf_attachment = MIMEApplication(pdf_buffer.getvalue(), _subtype="pdf")
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename=f"dossier_candidature_{nom}_{prenom}.pdf")
        msg.attach(pdf_attachment)
        
        # Configuration du serveur SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(st.secrets["EMAIL_ADDRESS"], st.secrets["GMAIL_APP_PASSWORD"])
        server.send_message(msg)
        server.quit()

    # Bouton de soumission uniquement dans l'onglet Ressources
    if st.button("Soumettre le dossier"):
        # Vérification que les champs obligatoires sont remplis
        if not nom or not prenom or not profession or not revenus:
            st.error("Veuillez remplir tous les champs obligatoires dans tous les onglets.")
        else:
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
