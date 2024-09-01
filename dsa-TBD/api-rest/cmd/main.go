package main

import (
	"context"
	"fmt"
	"github.com/gin-contrib/cors"
	"github.com/gin-contrib/gzip"
	"github.com/gin-gonic/gin"
	_ "github.com/golang-migrate/migrate/v4/database/postgres"
	"gopkg.in/go-playground/validator.v9"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
	"uty-api/internal/common/constant"
	"uty-api/internal/config"
	pg "uty-api/internal/db"
	"uty-api/pkg/air-conditioner"
)

func main() {
	conf, err := config.GetConfig()
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(conf)

	db, err := pg.NewPostgresConnectionPool(conf.PostgresURL)
	if err != nil {
		log.Fatalf("listen: %s\n", err)
	}
	//db.Ping()
	pgConn := db.Conn
	fmt.Println(pgConn)

	// SQL REPOSITORIES
	acRepo := air_conditioner.NewRepository(pgConn)

	// WEB SERVER
	r := gin.Default()
	r.Use(cors.Default())
	r.Use(gzip.Gzip(gzip.DefaultCompression))

	// HTTP HANDLERS
	validator := validator.New()
	r.GET("/", handleVersion)
	air_conditioner.NewHandler(r, "iot", validator, acRepo)

	// SERVER SETUP
	srv := &http.Server{
		Handler: r,
		Addr:    ":" + string(conf.GinPort),
	}
	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %s\n", err)
		}
	}()
	log.Print(constant.Green, "WEB SERVER PORT: ", conf.GinPort, constant.Reset)

	// GRACEFULL SHUTDOWNS
	//SERVER
	quit := make(chan os.Signal)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit
	log.Println("Shutting down server...")
	ctx, cancel := context.WithTimeout(context.Background(), 120*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server forced to shutdown:", err)
	}
	log.Println("Server exiting")

}

func handleVersion(c *gin.Context) {
	iot := []string{
		"/iot",
		"iot/create?n=500"}
	res := map[string]interface{}{
		"version":   "USP IoT API v1 - 2022-12-20",
		"time":      time.Now().UTC().String(),
		"endpoints": iot,
	}
	c.JSON(http.StatusOK, res)
}