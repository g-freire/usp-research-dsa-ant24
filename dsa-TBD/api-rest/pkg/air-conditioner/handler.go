package air_conditioner

import (
	"context"
	"fmt"
	"github.com/gin-gonic/gin"
	"gopkg.in/go-playground/validator.v9"
	"net/http"
	"strconv"
	"time"
	"uty-api/internal/common/constant"
	errors "uty-api/internal/common/error"
)

type Handler struct {
	Validate     *validator.Validate
	ACRepository ACRepository
}

func NewHandler(r *gin.Engine, route string, val *validator.Validate, acRepo ACRepository) {
	handler := &Handler{
		Validate:     val,
		ACRepository: acRepo,
	}
	v1 := r.Group(route)
	{
		v1.GET("/", handler.GetAll)
		//v1.POST("/", handler.SaveMany)
		v1.GET("/create", handler.SaveMany) // eg. localhost:8080/iot/create?n=500
	}
}

func (h *Handler) GetAll(c *gin.Context) {
	// ctx, cancel := context.WithTimeout(c.Request.Context(), constant.CTX_DEFAULT*time.Second)
	// defer cancel()
	ctx:= context.Background()

	limit := c.Query("limit")
	offset := c.Query("offset")

	result, err := h.ACRepository.GetAll(ctx, limit, offset)
	if err != nil {
		c.JSON(http.StatusNotFound, errors.Response{
			Status:  http.StatusNotFound,
			Type:    constant.ErrUnknownResource,
			Message: []string{err.Error()}})
	} else {
		c.JSON(http.StatusOK, result)
	}
}

func (h *Handler) SaveMany(c *gin.Context) {
	ctx, cancel := context.WithTimeout(c.Request.Context(), constant.CTX_DEFAULT*time.Second)
	defer cancel()

	// random generator
	amount := c.Query("n")
	if amount == "" {
		amount = "100"
	}
	amountInt, _ := strconv.Atoi(amount)
	acColl := createRandomACSensorCollection(amountInt)

	// uncomment for the rest api post
	//var acColl []AirConditionerSensorWrite
	//if err := c.BindJSON(&acColl); err != nil {
	//	c.JSON(http.StatusBadRequest, errors.Response{
	//		Status:  http.StatusBadRequest,
	//		Type:    constant.ErrRequestDecoding,
	//		Message: []string{err.Error()}})
	//	return
	//}
	//// validation of all structs before hitting the db
	//for i, ac := range acColl {
	//	if err := h.Validate.Struct(ac); err != nil {
	//		c.JSON(http.StatusBadRequest, errors.Response{
	//			Status:  http.StatusBadRequest,
	//			Type:    constant.ErrRequestBody,
	//			Message: []string{err.Error(), fmt.Sprintf("Check Air Conditioner at index %d", i+1)}})
	//		return
	//	}
	//}

	count, err := h.ACRepository.SaveMany(ctx, acColl)
	if err != nil {
		c.JSON(http.StatusBadRequest, errors.Response{
			Status:  http.StatusBadRequest,
			Type:    constant.ErrDatabaseOperation,
			Message: []string{err.Error()}})
	}
	msg := fmt.Sprintf("Created %v Air Conditioner successfully", count)
	c.JSON(http.StatusCreated, gin.H{
		"Status":  http.StatusCreated,
		"Message": msg,
	})
}
