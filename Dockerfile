FROM hashtagcyber/sam-automation:latest

ENV SAM_CLI_TELEMETRY 0

COPY entrypoint.sh /entrypoint.sh
COPY find-package.py /find-package.py

ENTRYPOINT ["/entrypoint.sh"]
