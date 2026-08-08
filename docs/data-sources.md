# Football Stat and Analysis Data Sources

## NFL Stats
We will need data sources for fantasy player points. We could possibly calculate stats ourselves by using normal NFL stats APIs and math on application side if cost is too much.

https://rapidapi.com/tank01/api/tank01-nfl-live-in-game-real-time-statistics-nfl this rapid api allows for 1000 calls permonth for free, we could possibly use this.

We will need actual NFL stats as well, able to use Fantasy Data for all stats and not just fantasy points.

### [ESPN Endpoint List](https://gist.github.com/nntrn/ee26cb2a0716de0947a0a4e9a157bc1c)
This GitHub Gist lists all the "hidden" endpoints for ESPN. We should really try to use this because it is free, as long as we can get what we need. https://github.com/pseudo-r/Public-ESPN-API?tab=readme-ov-file#endpoints

Check this out: https://github.com/nflverse/nflverse-data this may be useful https://github.com/nflverse

https://pypi.org/project/nfl-data-py/

https://github.com/thadhutch/sports-quant

## Analysis Sources
We should get out analysis by gathering a list of football and fantasy football analysts. This list should be very large. We should then use statistics from previous years to see wwhich analysts are the most accurate. We should keep a running ranking list of the most accurate NFL analysts and value the most accurate ones opinions more. We can use that to make decisions about fantasy football. The criteria they are judged on we will have to develop but this could be a strong way to help the LLM determine things. We could also use Vegas odds.