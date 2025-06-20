### data.py
- data of stocks put into the format you get when you use IKBR API
- data is split into daily and minute dfs so that we can use different time ranges accurately
- considering where to calculate the extra features in data.py or in the models (rate of trading volume, price changes by time)

### trends.py
- calculating the trends of different times ranges
- for price
- for volume
[ ] price changes by time
[ ] volume changes by time

### models
[ ] mean reversion models
[ ] moving average models
[ ] BS models

### dicord.py
- scrap discord for list of penny stocks
- seeing if it is possible to automate

---

- different files for different models
- to get stock data, take input of stock and time
    - doesn't really need to take time as input just date because the data for the time is in the df
- models
    - trends
        - can maybe also include moving average models but I don't think this is the same
        - have the trends for the 1 year, 60 days, 1 month, 1 week, 1 day, 1 hour, 1 min
        - can only do up to 60 days with yfinance
        - for prices
        - for volume (plot this see if it looks cool)
    - BS model
        - if the options of the stock are underpriced or not and if these factors contribute 
    - ML model that incoporates all the other models then sees which factors contribute the most to the stock increasing or not
    - pairs trading that finds connections between pennies (seems pointless tho)
- data
    - volume 
    - voume increase/decrease rate
    - price
- scrapping discord
    - first just all the unique names of the stocks (use random time 1pm GMT)
    - distinguish first time post of the stocks
    - just get all the stocks that are posted at 1 uk time
### Maybe end point of this program is to get weights of variables that have the biggest affect, then use these weights for a different model that says buy or not?

- implied volatility, realised volatility and use them to make returns on earnings
- get name of stocks that have appeared more than twice (not in the same week posting)
- want to plot volume against price, then rate of volume increase against price (maybe in analysis file)

[ ] just look a specific stock first at the time is posting and see what information can extract
