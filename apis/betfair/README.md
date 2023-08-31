
Market structure example:

```
{
    "marketId": "1.217410092",
    "key": "MARKET:1.217410092",
    "eventTypeId": 2,
    "eventId": 32576349,
    "upperLevelEventId": 32575867,
    "topLevelEventId": 32575867,
    "numberOfUpperLevels": 1,
    "competitionId": 12609621,
    "marketName": "Match Odds",
    "marketTime": "2023-08-23T14:43:00.000Z",
    "marketSuspendTime": "2023-08-23T14:43:00.000Z",
    "canTurnInPlay": true,
    "marketType": "MATCH_ODDS",
    "bspMarket": false,
    "inplay": true,
    "totalMatched": 24071.583359999997,
    "totalAvailable": 17810.7424,
    "runners": [
        {
            "selectionId": 9454905,
            "handicap": 0.0,
            "runnerName": "Ivan Gakhov",
            "sortPriority": 1,
            "runnerStatus": "ACTIVE"
        },
        {
            "selectionId": 20832494,
            "handicap": 0.0,
            "runnerName": "Zachary Svajda",
            "sortPriority": 2,
            "runnerStatus": "ACTIVE"
        }
    ],
    "betDelay": 3,
    "numberOfWinners": 1,
    "numberOfRunners": 2,
    "numberOfActiveRunners": 2,
    "associatedMarkets": [
        {
            "eventId": 32576349,
            "sportsbookMarketId": "924.373420566",
            "eventTypeId": 2
        }
    ],
    "marketLevels": [
        "AVB_EVENT"
    ],
    "bettingType": "ODDS",
    "marketStatus": "OPEN",
    "productType": "EXCHANGE"
}
```

Market data structure:
```
{
    "marketId": "1.217410092",
    "isMarketDataDelayed": false,
    "highWaterMark": "3042349892",
    "state": {
        "betDelay": 3,
        "bspReconciled": false,
        "complete": true,
        "inplay": true,
        "numberOfWinners": 1,
        "numberOfRunners": 2,
        "numberOfActiveRunners": 2,
        "lastMatchTime": "2023-08-23T16:02:02.700Z",
        "totalMatched": 35670.25123602673,
        "totalAvailable": 50851.182300099645,
        "crossMatching": true,
        "runnersVoidable": false,
        "version": 5405052485,
        "status": "OPEN"
    },
    "runners": [
        {
            "selectionId": 9454905,
            "handicap": 0.0,
            "state": {
                "sortPriority": 1,
                "lastPriceTraded": 11.0,
                "totalMatched": 4139.185556769924,
                "status": "ACTIVE"
            },
            "exchange": {
                "availableToBack": [
                    {
                        "price": 10.0,
                        "size": 366.29
                    },
                    {
                        "price": 9.8,
                        "size": 155.05
                    },
                    {
                        "price": 9.6,
                        "size": 7.49
                    }
                ],
                "availableToLay": [
                    {
                        "price": 11.0,
                        "size": 60.24
                    },
                    {
                        "price": 12.5,
                        "size": 76.17
                    },
                    {
                        "price": 13.0,
                        "size": 18.1
                    }
                ]
            }
        },
        {
            "selectionId": 20832494,
            "handicap": 0.0,
            "state": {
                "sortPriority": 2,
                "lastPriceTraded": 1.1,
                "totalMatched": 31531.0656792568,
                "status": "ACTIVE"
            },
            "exchange": {
                "availableToBack": [
                    {
                        "price": 1.1,
                        "size": 602.43
                    },
                    {
                        "price": 1.09,
                        "size": 873.5
                    },
                    {
                        "price": 1.08,
                        "size": 5147.3
                    }
                ],
                "availableToLay": [
                    {
                        "price": 1.11,
                        "size": 1304.62
                    },
                    {
                        "price": 1.12,
                        "size": 6144.96
                    },
                    {
                        "price": 1.13,
                        "size": 1013.87
                    }
                ]
            }
        }
    ],
    "isMarketDataVirtual": true
}
```