# Airbyte

## Setup local Airbyte

1. Install abctl
    - for mac/linux: `curl -LsfS https://get.airbyte.com | bash -`

2. Install airbyte:

```
abctl local install
```

3. Get credentials:

```
abctl local credentials --email test@test.com
```

4. Access UI: http://localhost:8000/

## Add the custom ExchangeRate-API

1. Builder -> New custom connector -> Import a YAML manifest -> select the `airbyte/source-exchange-rate-api/manifest.yaml`
