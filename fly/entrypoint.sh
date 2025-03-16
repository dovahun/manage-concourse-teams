#!/usr/bin/env bash
fly targets || true
exec "$@"