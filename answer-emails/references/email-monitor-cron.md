# Cron-based Email Monitoring

Pattern for automatic email monitoring with cron + answer-emails:

## Setup
```bash
cronjob action=create name="Email Monitor" schedule="every 10m" \
  skills='["answer-emails"]' \
  prompt="Check bar.ai.bot@cudos.ch for unread emails FROM reto.baettig@cudos.ch OR reto@baettig.org..."

# IMPORTANT: set deliver to origin so results reach the user
cronjob action=update job_id=<id> deliver=origin
```

## Silent-when-empty pattern
The prompt MUST include: "If there are NO unread emails, respond with ABSOLUTELY NOTHING — an empty response with zero characters."
This ensures the user isn't spammed every 10 minutes when there's no mail.

## Trade-offs
- 10 min: responsive but 144 agent calls/day
- 5 min: faster but 288 calls/day
- Choose based on how critical email latency is
