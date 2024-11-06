package main

import {
	"github.com/jinzhu/gorm"
	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
	"log"
}
var db *gorm.DB
var erreur error
func main() {
	dsn := "host=localhost user=monuser password=kramo dbname=gestioncontact port=5432 sslmode=disable"
	db, err = gorm.Open("postgres", dsn)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()
}

