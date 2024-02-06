package air_conditioner

import (
	"context"
	"fmt"
	"github.com/georgysavva/scany/pgxscan"
	"github.com/jackc/pgx/v4"
	"github.com/jackc/pgx/v4/pgxpool"
	"log"
	"strings"
)

type postgres struct {
	db *pgxpool.Pool
	//ch cache.Cache
}

func NewRepository(db *pgxpool.Pool) *postgres {
	return &postgres{
		db: db,
	}
}

func (p postgres) GetAll(ctx context.Context, limit, offset string) ([]AirConditionerSensorRead, error) {
	var UserCollection []AirConditionerSensorRead
	var q strings.Builder
	q.WriteString(`
		SELECT * FROM ac_sensor
	`)

	// request with pagination - default limit is 500 if no limit is specified
	if limit == "" {
		limit = "500"
	}
	q.WriteString(fmt.Sprintf("LIMIT %s ", limit))
	if offset != "" {
		q.WriteString("OFFSET ")
		q.WriteString(offset)
	}
	err := pgxscan.Select(ctx, p.db, &UserCollection, q.String())
	if err != nil {
		log.Print("\n[ERROR]:", err)
		return nil, err
	}
	return UserCollection, nil
}

func (p postgres) SaveMany(ctx context.Context, acColl []AirConditionerSensorWrite) (id int64, err error) {
	var data [][]interface{}
	for _, ac := range acColl {
		data = append(data, []interface{}{
			ac.TemperatureCurrent,
			ac.TemperatureDesired,
			ac.Humidity,
			ac.Pressure,
			ac.AirQuality,
			ac.Voltage,
			ac.Current,
			ac.Power,
			ac.IsOn,
			ac.Status,
			ac.Location,
		})
	}
	copyCount, err := p.db.CopyFrom(
		context.Background(),
		pgx.Identifier{"ac_sensor"},
		[]string{
			"temperature_current",
			"temperature_desired",
			"humidity",
			"pressure",
			"air_quality",
			"voltage",
			"current",
			"power",
			"is_on",
			"status",
			"location",
		},
		pgx.CopyFromRows(data),
	)
	if err != nil {
		log.Println(err)
	}
	//fmt.Println(copyCount)
	return copyCount, nil
}
