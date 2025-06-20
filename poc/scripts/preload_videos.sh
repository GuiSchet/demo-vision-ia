#!/usr/bin/env bash
mc alias set local http://minio:9000 admin secret123
mc mb --ignore-existing local/cctv
mc cp /videos/*.mp4 local/cctv/
