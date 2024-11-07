from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Connexion à PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="gestioncontact",
        user="monuser",
        password="kramo"
    )
    return conn

# Modèles Pydantic pour les tables
class Departement(BaseModel):
    nom: str
    localisation: str = None
    description: str = None
    contact: str
    est_interne: bool

class Service(BaseModel):
    nom: str
    description: str = None
    localisation: str = None
    contact: str
    departement_id: int

class Personne(BaseModel):
    nom: str
    prenom: str
    date_naissance: str
    fonction: str = None
    photo: str

class Contact(BaseModel):
    valeur: str
    est_public: bool
    personne_id: int
    type_contact_id: int
    service_id: int

class TypeContact(BaseModel):
    libelle: str
    description: str

# Routes CRUD pour chaque table
# ----------------------------- Departement ----------------------------- #
#CODE POUR AJOUTER UN ELEMENT QUELQCONQUE A LA TABLE DEPARTEMENT
@app.post("/gestioncontact/departement")
def ajouter_departement(departement: Departement):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO departement (nom, localisation, description, contact, est_interne) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (departement.nom, departement.localisation, departement.description, departement.contact, departement.est_interne)
        )
        departement_id = cursor.fetchone()[0]
        conn.commit()
        return {"id": departement_id, "message": "Département ajouté avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
#CODE POUR METTRE A JOUR MA TABLE DEPARTEMENT DE TELLE SORTE QUE LES VALEURS VIDES SOIENT OCCUPEES
@app.put("/gestioncontact/departement/{id}")
def update_departement(id: int, departement: Departement):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE departement SET nom = %s, localisation = %s, description = %s, contact = %s, est_interne = %s WHERE id = %s;",
            (departement.nom, departement.localisation, departement.description, departement.contact, departement.est_interne, id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Département introuvable")
        return {"message": "Département mis à jour avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
#CODE POUR SUPPRIMER UN ELEMENT SPECIFIQUE DE LA TABLE DEPARTEMENT A PARTIR DE L'ID
@app.delete("/gestioncontact/departement/{id}")
def delete_departement(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM departement WHERE id = %s;", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Département introuvable")
        return {"message": "Département supprimé avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

#CODE POUR AJOUTER UN ELEMENT QUELQCONQUE A Service
@app.post("/gestioncontact/service")
def ajouter_service(service: Service):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO service (nom, description, localisation, contact, departement_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (service.nom, service.description, service.localisation, service.contact, service.departement_id)
        )
        service_id = cursor.fetchone()[0]
        conn.commit()
        return {"id": service_id, "message": "Service ajouté avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la creation du service: {e}")
    finally:
        cursor.close()
        conn.close()


#CODE POUR METTRE A JOUR LA TABLE SERVICE DE TELLE SORTE QUE LES VALEURS VIDES A PARTIR DE L'ID
@app.put("/gestioncontact/service/{id}")
def update_service(id: int, service: Service):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE service SET nom = %s, description = %s, localisation = %s, contact = %s, departement_id = %s WHERE id = %s;",
            (service.nom, service.description, service.localisation, service.contact, service.departement_id, id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Service introuvable")
        return {"message": "Service mis à jour avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la mise à jour: {e}")
    finally:
        cursor.close()
        conn.close()
#CODE POUR SUPPRIMER UN ELEMENT SPECIFIQUE DE LA TABLE SERVICE A PARTIR DE L'ID
@app.delete("/gestioncontact/service/{id}")
def delete_service(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM service WHERE id = %s;", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Service introuvable")
        return {"message": "Service supprimé avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la suppression: {e}")
    finally:
        cursor.close()
        conn.close()

# ----------------------------- Personne ----------------------------- #
# (Ajouter ici les routes CRUD pour `Personne`)
#CODE POUR AJOUTER UN ELEMENT QUELQCONQUE A PERSONNE
@app.post("/gestioncontact/personne")
def create_personne(personne: Personne):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO personne (nom, prenom, date_naissance, fonction, photo) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (personne.nom, personne.prenom, personne.date_naissance, personne.fonction, personne.photo)
        )
        personne_id = cursor.fetchone()[0]
        conn.commit()
        return {"id": personne_id, "message": "Personne ajoutée avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'ajout: {e}")
    finally:
        cursor.close()
        conn.close()

#CODE POUR METTRE A JOUR LA TABLE PERSONNE DE TELLE SORTE QUE LES VALEURS VIDES DE PERSONNES SOIENT AJOUTEES
@app.put("/gestioncontact/personne/{id}")
def update_personne(id: int, personne: Personne):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE personne SET nom = %s, prenom = %s, date_naissance = %s, fonction = %s, photo = %s WHERE id = %s;",
            (personne.nom, personne.prenom, personne.date_naissance, personne.fonction, personne.photo, id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Personne introuvable")
        return {"message": "Personne mise à jour avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la mise à jour: {e}")
    finally:
        cursor.close()
        conn.close()
#CODE POUR SUPPRIMER UN ELEMENT SPECIFIQUE DE LA TABLE PERSONNE A PARTIR DE L'ID
@app.delete("/gestioncontact/personne/{id}")
def delete_personne(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM personne WHERE id = %s;", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Personne introuvable")
        return {"message": "Personne supprimée avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la suppression: {e}")
    finally:
        cursor.close()
        conn.close()

# ----------------------------- Contact ----------------------------- #
#les routes CRUD pour Contact
# Route pour créer un contact
@app.post("/gestioncontact/contact")
def create_contact(contact: Contact):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO contact (valeur, est_public, personne_id, type_contact_id, service_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (contact.valeur, contact.est_public, contact.personne_id, contact.type_contact_id, contact.service_id)
        )
        contact_id = cursor.fetchone()[0]
        conn.commit()
        return {"id": contact_id, "message": "Contact ajouté avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'ajout: {e}")
    finally:
        cursor.close()
        conn.close()

# Route pour récupérer un contact avec toutes ses informations associées
@app.get("/gestioncontact/contact/{id}")
def get_contact(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Jointure entre la table contact, personne, type_contact et service
        cursor.execute("""
            SELECT  
                contact.id, contact.valeur, contact.est_public, 
                personne.nom, personne.prenom, personne.date_naissance, personne.fonction, personne.photo, 
                typecontact.type_nom, typecontact.description, 
                service.nom, service.description, service.localisation,
                departement.id as departement_id, departement.nom as departement_nom, 
                departement.localisation as departement_localisation, 
                departement.description as departement_description, departement.contact as departement_contact, 
                departement.est_interne as departement_est_interne
            FROM contact
            JOIN personne ON contact.personne_id = personne.id
            JOIN typecontact ON contact.type_contact_id = typecontact.id
            JOIN service ON contact.service_id = service.id
            JOIN departement ON service.departement_id = departement.id
            WHERE contact.id = %s;
           
        
        """, (id,))
        
        contact = cursor.fetchone()
        if not contact:
            raise HTTPException(status_code=404, detail="Contact introuvable")
        
        # Organiser les données sous forme de dictionnaire
        contact_data = {
            "id": contact[0],
            "valeur": contact[1],
            "est_public": contact[2],
            "personne": {
                "nom": contact[3],
                "prenom": contact[4],
                "date_naissance": contact[5],
                "fonction": contact[6],
                "photo": contact[7]
            },
            "type_contact": {
                "type_nom": contact[8],
                "description": contact[9]
            },
            "service": {
                "nom": contact[10],
                "description": contact[11],
                "localisation": contact[12]
            }
        }
        return contact_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur: {e}")
    finally:
        cursor.close()
        conn.close()

# Route pour mettre à jour un contact a partir de l'id
@app.put("/gestioncontact/contact/{id}")
def update_contact(id: int, contact: Contact):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE contact SET valeur = %s, est_public = %s, personne_id = %s, type_contact_id = %s, service_id = %s WHERE id = %s;",
            (contact.valeur, contact.est_public, contact.personne_id, contact.type_contact_id, contact.service_id, id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Contact introuvable")
        return {"message": "Contact mis à jour avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la mise a jour: {e}")
    finally:
        cursor.close()
        conn.close()

# Route pour supprimer un contact a partir de l'id
@app.delete("/gestioncontact/contact/{id}")
def delete_contact(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM contact WHERE id = %s;", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Contact introuvable")
        return {"message": "Contact supprimé avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la suppression: {e}")
    finally:
        cursor.close()
        conn.close()
# ----------------------------- TypeContact ----------------------------- #
# les routes CRUD pour TypeContact
# Route pour ajouter un type de contact
@app.post("/gestioncontact/typecontact")
def create_type_contact(type_contact: TypeContact):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO type_contact (type_nom, description) VALUES (%s, %s) RETURNING id;",
            (type_contact.type_nom, type_contact.description)
        )
        type_contact_id = cursor.fetchone()[0]
        conn.commit()
        return {"id": type_contact_id, "message": "Type de contact ajouté avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la creation: {e}")
    finally:
        cursor.close()
        conn.close()

# Route pour mettre à jour un type de contact
@app.put("/gestioncontact/typecontact/{id}")
def update_type_contact(id: int, type_contact: TypeContact):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE type_contact SET type_nom = %s, description = %s WHERE id = %s;",
            (type_contact.type_nom, type_contact.description, id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Type de contact introuvable")
        return {"message": "Type de contact mis à jour avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la mise a jour: {e}")

    finally:
        cursor.close()
        conn.close()

# Route pour supprimer un type de contact
@app.delete("/gestioncontact/typecontact/{id}")
def delete_type_contact(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM type_contact WHERE id = %s;", (id,))
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Type de contact introuvable")
        return {"message": "Type de contact supprimé avec succès"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la suppression: {e}")
    finally:
        cursor.close()
        conn.close()
# ...
