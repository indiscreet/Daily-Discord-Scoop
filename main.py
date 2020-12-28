from core import daily as d
from discord_webhook import DiscordWebhook, DiscordEmbed, webhook
###########
###Setup###
###########
#Config
place = "Dallas, TX"
type_of_place = "state" #Must either be country, state or county.
stock = ['BTC', 'GOOG', 'MSFT']

#Single Webhook
single_wh = ""

#Multiple Webhooks
multi_webhook = False
forecast_wh = ""
covid_wh = ""
stocks_wh = ""


if multi_webhook == True:
    forecast = DiscordWebhook(url=forecast_wh, content=f"```{d.forecast(place)}```")
    forecast.execute()
    covid = DiscordWebhook(url=covid_wh, content=f"```{d.covid(place, type_of_place)}```")
    covid.execute
    for s in stock:
        stocks = DiscordWebhook(url=stocks_wh, content=f"Stock: {s}\nPrice: {d.stocks(s)}")
        stocks.execute()
else:
    forecast = DiscordWebhook(url=single_wh, content=f"```{d.forecast(place)}```")
    forecast.execute()
    covid = DiscordWebhook(url=single_wh, content=f"```{d.covid(place, type_of_place)}```")
    covid.execute()
    for s in stock:
        stocks = DiscordWebhook(url=single_wh, content=f"Stock: {s}\nPrice: {d.stocks(s)}")
        stocks.execute()