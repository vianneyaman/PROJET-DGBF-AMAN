package main // ca veut dire que models.go est le package principal de l'app, est le package principal ,un package est un assemblage de fichiers sources go compiles en mm temps

import (
	"github.com/jinzhu/gorm"
	_ "github.com/lib/pq"
)

var db *gorm.DB

// ici je vais creer des models, chaque type correspond a une table dans la base de donnees

type departement struct {
	id           uint   `gorm:"primary_key"`                // ca veur dire que id est une cle primaire et est de type entier non signe
	nom          string `gorm:"type:varchar(100);not null"` // veut dire que nom est une chaine de carac , doit avoir au plus 100 carac et ne doit pas etre null
	localisation string `gorm:"type:varchar(100)"`
	description  string `gorm:"type:varchar(200)"`
	contact      string `gorm:"type:varchar(100);not null"`
	est_interne  bool
	Services []Service `gorm:"foreignKey:DepartementID"`
 }

type service struct {
	id             uint   `gorm:"primary_key"`
	nom            string `gorm:"type:varchar(100);not null"` // veut dire que nom est une chaine de carac , doit avoir au plus 100 carac et ne doit pas etre null
	description    string `gorm:"type:varchar(200)"`
	localisation   string `gorm:"type:varchar(100)"`
	contact        string `gorm:"type:varchar(100);not null"`
	departement_id uint   `gorm:"not null"`
}

type Contact struct { 
	id uint `gorm:"primary_key"`
    valeur string `gorm:"type:varchar(200);not null"` 
	est_Public bool
	personne_id uint `gorm:"not null"` // Clé étrangère vers Personne
	typeContact_id uint `gorm:"not null"` // Clé étrangère vers TypeContact 
	Service_id uint `gorm:"not null"` // Clé étrangère vers Service 
	personne personne
	TypeContact TypeContact 
	}

type personne struct {
	id            uint   `gorm:"primary_key"`
	nom           string `gorm:"type:varchar(100);not null"`
	prenom        string `gorm:"type:varchar(250);not null"`
	datenaissance string `gorm:"type:varchar(100);not null"`
	fonction      string `gorm:"type:varchar(100)"`
	photo         string `gorm:"type:varchar(255);not null"`
	Contact []Contact 
}
type TypeContact struct {
	id uint `gorm:"primary_key"`
	Libelle string `gorm:"type:varchar(200);not null"`
	description string `gorm:"type:varchar(200);not null"` 
	Contacts []Contact // Relation avec Contact
}
