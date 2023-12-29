from uagents import Agent, Context, Model, Bureau
from api import api
from consts import stocks_name


class Choice(Model):
    choice: int


class StockName(Model):
    name: str


choice_agent = Agent(name="Choice", seed="Choice Agent")
main_agent = Agent(name="Main Agent", seed="Main Agent")
stock_info = Agent(name="Stock Name", seed="Stock Name")
predict_stock_price = Agent(
    name="Predict Stock Price", seed="Predict Stock Price")

CHOICE = None


@choice_agent.on_event("startup")
async def show_choices(ctx: Context):
    print("\n1)Show list of stocks\n2)Show a sepcified Stock\n3)Predict a Specified Stock\n4)Show recommended Stocks\n5) Exit\n")
    CHOICE = int(input("Enter the choice: "))
    await ctx.send(main_agent.address, Choice(choice=CHOICE))


@choice_agent.on_message(model=Choice)
async def show_choices(ctx: Context, sender, choice_agent=Choice):
    print("\n1)Show list of stocks\n2)Show a sepcified Stock\n3)Predict a Specified Stock\n4)Show recommended Stocks\n5) Exit\n")
    CHOICE = int(input("Enter the choice: "))
    await ctx.send(main_agent.address, Choice(choice=CHOICE))


@main_agent.on_message(model=Choice)
async def choice(ctx: Context, sender, choice: Choice):
    if (choice.choice == 1):
        for stock in stocks_name.stock_companies:
            print(stock["company"], "- symbol:", stock["symbol"])
        await ctx.send(choice_agent.address, Choice(choice=0))
    if (choice.choice == 2):
        sk_name = input("Enter the Stock Symbol: ")
        await ctx.send(stock_info.address, StockName(name=sk_name))
    if (choice.choice == 3):
        sk_name = input("Enter the Stock Symbol: ")
        await ctx.send(predict_stock_price.address, StockName(name=sk_name))
    if (choice.choice == 4):
        api.top_gainers()
        await ctx.send(choice_agent.address, Choice(choice=0))
    if choice.choice == 5:
        exit(0)


@stock_info.on_message(model=StockName)
async def stockName(ctx: Context, sender, stock_info: StockName):
    api.get_stock_info(name=stock_info.name)
    await ctx.send(choice_agent.address, Choice(choice=0))


@predict_stock_price.on_message(model=StockName)
async def predictStockPrice(ctx: Context, sender, stock_info: StockName):
    api.predict_stock(name=stock_info.name)
    await ctx.send(choice_agent.address, Choice(choice=0))

breau = Bureau()
breau.add(choice_agent)
breau.add(main_agent)
breau.add(stock_info)
breau.add(predict_stock_price)

if __name__ == "__main__":
    breau.run()
