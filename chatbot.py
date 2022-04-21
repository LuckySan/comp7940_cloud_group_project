from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import os
import pandas as pd
from connection.GetDataFromCSV import readRecipeData 
from connection.SQLConnection import SQLConnection
from dotenv import load_dotenv
load_dotenv()

def main():
    # Load your token and create an Updater for your Bot
    print(os.environ['ACCESS_TOKEN'])
    updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello))
    dispatcher.add_handler(CommandHandler("amountRecipes", get_amount_of_recipes))
    dispatcher.add_handler(CommandHandler("searchKeyWord", get_dishes_of_keyWord))
    dispatcher.add_handler(CommandHandler("addFavorite", add_user_favorite))
    dispatcher.add_handler(CommandHandler("getMyFavorite", get_user_favorite))
    mode = os.environ["MODE"]
    print(f'Environment variable is now {mode}')
    # To start the bot:
    if mode == 'webhook':
        # enable webhook
        updater.start_webhook(listen="127.0.0.1",
                            port=8443,
                            url_path=os.environ['ACCESS_TOKEN'],
                            key ='private.key', 
                            cert = 'cert.pem',
                            webhook_url = f'https://{os.environ["DOMAIN"]}.westeurope.azurecontainer.io:8443/{os.environ["ACCESS_TOKEN"]}')

        try: 
            # updater.bot.setWebhook(f'https://{os.environ["DOMAIN"]}.westeurope.azurecontainer.io:8443/{os.environ["ACCESS_TOKEN"]}')
            print("The webhook has not been set this time")
        except:
            print("Webhook error") 

    else:
        # enable polling
        updater.start_polling()
        updater.idle()

def getData(sql):
    with SQLConnection() as conn:
        data = pd.read_sql(sql, conn.connector)
        return data

def echo(update, context):
    msg = update.message.text
    # if the msg is a number, we know our user want to search dish by id
    if(msg.isdigit()):
        sql = f"select * from Dishes where id = {msg}"
        data = getData(sql)
        title = data["title"].values[0]
        ingredients = data["ingredients"].values[0]
        directions = data["directions"].values[0]
        link = data["link"].values[0]
        ret = getStringDishByVar(title, ingredients, directions, link)
        context.bot.send_message(chat_id=update.effective_chat.id, text=ret, parse_mode=ParseMode.HTML)
    # if the msg is a string, we know our user want to search dish by title
    else:
        sql = f"select id,title from Dishes where title like '%{msg}%' limit 0, 50"
        data = getData(sql)
        res = getStringDishByIdAndTitle(data)
        res = "Do you mean these Dishes? \n" + res
        context.bot.send_message(chat_id=update.effective_chat.id, text = res)


# Get All variable of dish
def getStringDishByVar(title,ingredients,directions,link):
    ret = f"""
<b>Dish Title: {title}</b>\n<b>Ingredients:</b>{ingredients}\n<b>Directions:</b>{directions}\n<a href="{link}">{link}</a>
"""
    return ret

# Get id, title of dish
def getStringDishByIdAndTitle(data):
    retTitle = data["title"].values
    retId = data["id"].values
    res = ""
    for (i, j) in zip(retId, retTitle):
        res += (str(i) + ". " + j + "\n")
    return res

# This method is used to retrive the chat id 
def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        # text message
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        # callback message
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        # answer in Poll
        chat_id = context.bot_data[update.poll.id]

    return chat_id

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def get_dishes_of_keyWord(update: Update, context: CallbackContext)->None:
    keyword = context.args[0]
    with SQLConnection() as conn:
        sql = f"select Dishes.id,title from KeyWordDish,Dishes where keyword='{keyword}' and Dishes.id = KeyWordDish.dishId limit 0, 50"
        data = pd.read_sql(sql,conn.connector)
        res = getStringDishByIdAndTitle(data)
        update.message.reply_text(res)


def add_user_favorite(update: Update, context: CallbackContext)->None:
    keyword = context.args[0]
    with SQLConnection() as conn:
        sql = f"insert into Favorite(clientId,dishId) values('{get_chat_id(update,context)}',{keyword})"
        conn.cursor.execute(sql)
        conn.connector.commit()
        update.message.reply_text("add successfully")

def get_user_favorite(update: Update, context: CallbackContext)->None:
    clientId = get_chat_id(update, context)
    with SQLConnection() as conn:
        sql = f"select d.id, d.title from Favorite f, Dishes d where f.clientId = '{clientId}' and d.id = f.dishId"
        data = pd.read_sql(sql, conn.connector)
        res = getStringDishByIdAndTitle(data)
        update.message.reply_text(res)


def get_amount_of_recipes(update: Update, context: CallbackContext)->None: 
    """
    Input: Chatbot /amountRecipes
    Output: Amount of recipes
    """
    with SQLConnection() as conn: 
        sql = "Select count(*) as numberRecipes from Dishes"
        data = pd.read_sql(sql, conn.connector)
        ret = data["numberRecipes"].values[0]
        countRecipes = int(ret)
        update.message.reply_text(f'Number of recipes in the database: {countRecipes}')


    #3 Return result as int 
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("""
    
    /searchKeyWord -> Search the dishes by the ingredient's keyword
/amountRecipes -> Get the amount of dishes in our database
    
    """)


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try: 
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')


def hello(update: Update, context: CallbackContext) -> None:
    try: 
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        update.message.reply_text(f'Good Day {msg}!')
    except (IndexError): 
        update.message.reply_text("Default Text3: Good Day Kevin3!")


if __name__ == '__main__':
    main()