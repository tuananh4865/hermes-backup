#!/bin/bash
# miy-on-query - Dùng Hermes CLI thay vì cron
# Được trigger bởi webhook miy-question → Hermes session tự chạy agent reply

# Đợi 2s cho backend kịp log
sleep 2

# Reply placeholder cho tất cả pending queries qua API
.venv/bin/python auto_reply.py 2>&1 | head -20