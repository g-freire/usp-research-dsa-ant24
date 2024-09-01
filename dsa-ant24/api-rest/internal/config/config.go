package config

import (
	"fmt"
	_ "github.com/joho/godotenv"
	_ "github.com/joho/godotenv/autoload"
	"log"
	"os"
	"uty-api/internal/common/constant"
	"uty-api/internal/common/path"
)

// Config is the central setting.
// get config from env
type Config struct {
	Environment   string `json:"environment,omitempty"`
	GinPort       string `json:"gin_port,omitempty"`
	PostgresURL   string `json:"postgres_url"`
	PostgresDNS   string `json:"postgres_dns,omitempty"`
	RedisAddress  string `json:"redis_address"`
	RedisPassword string `json:"redis_password"`
}

// GetConfig returns default config.
func GetConfig() (*Config, error) {
	err := path.LoadEnv()

	if err != nil {
		return nil, err
	}

	env := os.Getenv("ENVIRONMENT")
	if env == "" {
		env = "QA"
		os.Setenv("ENVIRONMENT", env)
	}
	log.Printf("%sENVIRONMENT: %s  %s", constant.Green, env, constant.Reset)

	// POSTGRES
	var postgresDNS, postgresURL string

	if os.Getenv("POSTGRES_USER") == "" ||
		os.Getenv("POSTGRES_PASSWORD") == "" ||
		os.Getenv("POSTGRES_HOST") == "" ||
		os.Getenv("POSTGRES_DATABASE") == "" {
		postgresURL = defaultPostgresURL
	} else {
		postgresDNS = fmt.Sprintf(
			"host=%v user=%v password=%v dbname=%v port=%v sslmode=disable",
			os.Getenv("POSTGRES_HOST"),
			os.Getenv("POSTGRES_USER"),
			os.Getenv("POSTGRES_PASSWORD"),
			os.Getenv("POSTGRES_DATABASE"),
			os.Getenv("POSTGRES_PORT"),
		)
		postgresURL = fmt.Sprintf(
			"postgres://%v:%v@%v:%v/%v?sslmode=disable",
			os.Getenv("POSTGRES_USER"),
			os.Getenv("POSTGRES_PASSWORD"),
			os.Getenv("POSTGRES_HOST"),
			os.Getenv("POSTGRES_PORT"),
			os.Getenv("POSTGRES_DATABASE"))
	}

	return &Config{
		Environment:   env,
		GinPort:       GetEnvString("GIN_PORT", "8080"),
		PostgresURL:   postgresURL,
		PostgresDNS:   postgresDNS,
		RedisAddress:  GetEnvString("REDIS_ADDRESS", "localhost:6379"),
		RedisPassword: GetEnvString("REDIS_PASSWORD", ""),
	}, nil
}
