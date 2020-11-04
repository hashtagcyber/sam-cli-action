FROM hashtagcyber/sam-automation:1.1

ENV SAM_CLI_TELEMETRY 0

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
