from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

# Replace YOUR_URL with your mongodb url
cluster = MongoClient("mongodb+srv://gdp:gdp@cluster0.6ccl5.mongodb.net/?retryWrites=true&w=majority")
db = cluster["gdp"]
users = db["users"]
orders = db["orders"]

app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")[:-2]
    res = MessagingResponse()
    user = users.find_one({"number": number})
    if "4142" in text:
        msg = res.message("🤝Congratulations Receive free forex signals on Telegram now: t.me/forexgdpfree"
                         "\n\nReceive *Daily Chart Analysis*, News Updates here: t.me/forexgdp"
                         "\n\n*For receiving signals in WhatsApp, Save this WhatsApp number on your phone contacts*"
                         "\n\n*Contact Name* : Forex GDP"
                         "\n*Contact Number* : +919363168187 (add “+(plus)” sign in front of the number while saving)"
                         "\n\nCheck *Forex GDP* name displayed like here : forexgdp.com/freewa"
                         "\n\nPin this chat to see the signals immediately."
                         "\n\nBe patience & wait for next signal")
        msg.media("https://www.forexgdp.com/wp-content/uploads/2021/10/GDP-phone-number-save-correct-p3.png")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res.message("You can choose from one of the options below: "
                        "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *Signal* plans \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To Know *Where are we from*")
            return str(res)

        if option == 1:
            res.message(
                "You can contact us through phone or e-mail.\n\n*Phone*: 9876543210 \n*E-mail* : contact@gdpcre")
        elif option == 2:
            res.message("You have entered *ordering mode*.")
            users.update_one(
                {"number": number}, {"$set": {"status": "ordering"}})
            res.message(
                "You can select the signal plan: \n\n1️⃣ Premium 1 Month  \n2️⃣ Premium 3 Months \n3️⃣ Premium 6 Months"
                "\n4️⃣ Premium 12 Months \n5️⃣ Supreme 1 Month \n6️⃣ Supreme 3 Months \n7️⃣ Supreme 6 Months \n8️⃣ Supreme 12 Months \n9️⃣ VIP  \n0️⃣ Go Back")
        elif option == 3:
            res.message("We work *24x7*.")

        elif option == 4:
            res.message(
                "We are the group of traders located in different countries such as Singapore, Malaysia, Thailand, India, US, UK. Our motive is to help the retail traders all around the world by sharing our best trading knowledge. We recommend our users, “Do not trade forex market all the time, Trade forex only at confirmed trade setup.” We provide all the signals with the chart analysis and the explanation for buying/selling the trade which helps you to trade with confidence on your account.")
        else:
            res.message("Please enter a valid response")
    elif user["status"] == "ordering":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            res.message("You can choose from one of the options below: "
                        "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *Signal* plans \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To Know *Where are we from*")
        elif 1 <= option <= 9:
            plans = ["Premium 1 Month", "Premium 3 Months", "Premium 6 Months",
                     "Premium 12 Months", "Supreme 1 Month", "Supreme 3 Months", "Supreme 6 Months", "Supreme 12 Months", "VIP"]
            selected = cakes[option - 1]
            users.update_one(
                {"number": number}, {"$set": {"status": "address"}})
            users.update_one(
                {"number": number}, {"$set": {"item": selected}})
            res.message("Great choice 😉")
            res.message("You can join through here")
        else:
            res.message("Please enter a valid response")
    elif user["status"] == "address":
        selected = user["item"]
        res.message("Thanks for shopping with us 😊")
        res.message(f"Your order for *{selected}* has been received and will be Processed within an hour")
        orders.insert_one({"number": number, "item": selected, "address": text, "order_time": datetime.now()})
        users.update_one(
            {"number": number}, {"$set": {"status": "ordered"}})
    elif user["status"] == "ordered":
        res.message("Hi, thanks for contacting *GDP*.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *Signal* plans \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To Know *Where are we from*")
        users.update_one(
            {"number": number}, {"$set": {"status": "main"}})
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run()
