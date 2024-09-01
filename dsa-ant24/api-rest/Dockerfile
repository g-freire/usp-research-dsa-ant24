###############################################################
# LIB STAGE
###############################################################
FROM golang:1.18-alpine3.16 as build_base
COPY go.mod go.sum ${APP_HOME}/
RUN go mod download

###############################################################
# BUILD STAGE
###############################################################
FROM build_base as builder
ENV APP_HOME /uty-api
COPY .env ${APP_HOME}/.env
WORKDIR ${APP_HOME}
COPY . ${APP_HOME}/
RUN go build -o uty-api ./cmd/main.go

# ###############################################################
# # DISTRIBUTION STAGE
# ###############################################################
FROM alpine
ENV APP_HOME /uty-api
COPY --from=builder ${APP_HOME}/ ./
CMD ["./uty-api"]


# MountVolume.SetUp failed for volume "kube-api-access-vt6sv" : failed to sync configmap cache: timed out waiting for the condition