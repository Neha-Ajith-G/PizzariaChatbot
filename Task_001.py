
from dotenv import load_dotenv
load_dotenv()

#load from env 
#model is called

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()

from langchain_core.messages import HumanMessage,AIMessage

sys_template='''
    As a chat bot for a fictional pizzeria, you take orders from customers based on your menu {menu}. 
    When customers ask for the menu, you will provide a decent-looking menu template each time. 
    You will act as a real owner, suggest items to customers, and interact respectfully. 
    After each item is ordered, you will calculate the total cost and display it. 
    If a customer's ordered item is not available, you will inform them and ask them to pick from your available options. 
    You won't handle any payment methods; you'll only show the final amount.
    Chat History is provided.{chats}

'''
menu = '''
    Pepperoni Pizza: $12.95 (large), $10.00 (medium), $7.00 (small)
    Cheese Pizza: $10.95 (large), $9.25 (medium), $6.50 (small)
    Eggplant Pizza: $11.95 (large), $9.75 (medium), $6.75 (small)
    Fries: $4.50 (large), $3.50 (small)
    Greek Salad: $7.25
    Toppings:
        Extra Cheese: $2.00
        Mushrooms: $1.50
        Sausage: $3.00
        Canadian Bacon: $3.50
        AI Sauce: $1.50
        Peppers: $1.00
    Drinks:
        Coke: $3.00 (large), $2.00 (medium), $1.00 (small)
        Sprite: $3.00 (large), $2.00 (medium), $1.00 (small)
        Bottled Water: $5.00

'''
#prompts
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system",sys_template),
    ("user","{input}"),
])

chat_history = []

def get_response( user_input):
    chain = prompt | llm | output_parser
    result = chain.invoke({"input": user_input,"chats": chat_history,"menu":menu})
    return result

while True:

    user_ask=input("#USER>>")
    if user_ask=="quit":
        break
    chat_history.append(HumanMessage(content=user_ask))
    response = get_response(user_ask)
    print("PIZZERIA >>>",response)
    chat_history.append(AIMessage(content=response))
