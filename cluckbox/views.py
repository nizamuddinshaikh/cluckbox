from django.http import HttpResponse
from django.shortcuts import render,redirect
from pymongo import MongoClient
from datetime import datetime
from django.contrib import messages
import json


def login(request):

    client = MongoClient("mongodb://localhost:27017/")
    db = client['Project']
    coll= db['Signup']

    if request.method == "POST":

        # email = request.POST.get('email')
        # password = request.POST.get('password')

        email = request.POST['email']
        password = request.POST['password']

    
        for i in coll.find({'Email':email},{'Email':1,'Password':1 ,'_id':0}):
            Email = i['Email']
            Password = i['Password']
        

        if email==Email and password==Password:
            request.session['email'] = email
            return render(request,"home.html")
        else:
            return HttpResponse("Email or Password Incorrect")
        
    return render(request,"login.html")  


def signup(request):

    client = MongoClient("mongodb://localhost:27017/")
    db = client['Project']
    coll= db['Signup']

    if request.method == "POST": 

        name = request.POST.get('name').title()
        phone = int(request.POST.get('phone'))
        email = request.POST.get('email')
        address = request.POST.get('address').title()
        area = request.POST.get('area').title()
        pincode = int(request.POST.get('pincode'))
        password = request.POST.get('password')
    
        #query = {"_id" : phone,"Name" : name,"Phone_no" : phone,"Email" : email,"Address" : address,"Area" : area,'Pincode' : pincode,"Password" : password}
        x = datetime.now()
        query = {"Name" : name,"Phone_no" : phone,"Email" : email,"Address" : address,"Area" : area,'Pincode' : pincode,"JointDate" : x.strftime("%x"),
        "JointTime" : x.strftime("%X %p"),"Password" : password}

        coll.insert_one(query)
        return render(request,"login.html")

    return render(request,"signup.html")

def home(request):
    return render(request,"home.html")


'''
def dashboard(request):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['Project']
    cart = db['Cart']
    signupData = db['Signup']

    email = request.session.get('email')
    if not email:
        return HttpResponse("You are not logged in. Please log in first.")

    user = signupData.find_one({'Email': email}, {'_id': 0})

    if not user:
        return HttpResponse("User not found.")

    Name = user.get('Name')
    Phone_no = user.get('Phone_no')
    Email = user.get('Email')
    Address = user.get('Address')
    Area = user.get('Area')
    Pincode = user.get('Pincode')

    # Product definitions
    prices = {
        'Bonless_Chicken': 400,
        'Breast_Ribs': 450,
        'Chicken_legs': 350,
        'Leg_Quarter': 250,
        'Whole_Legs': 550,
        'Eggs': 160,
        'Drumstick': 360,
        'Keema': 160,
        'Lolipop': 210,
        'Wings': 160
    }
    
    if request.method == "POST":
        # Create a list to store all items added in this request
        new_items = []
        
        # Check each possible product
        for product_name in prices.keys():
            quantity = int(request.POST.get(product_name, 0))
            if quantity > 0:
                price = prices[product_name]
                total = quantity * price
                x = datetime.now()
                
                new_items.append({
                    "Type": product_name,
                    "Quantity": quantity,
                    "Price": price,
                    "Total": total
                })
        
        if new_items:
            # Get current cart or create new one
            current_cart = cart.find_one({"Email": email})
            
            if current_cart:
                # Add new items to existing cart
                updated_items = current_cart.get('items', []) + new_items
                cart.update_one(
                    {"Email": email},
                    {
                        "$set": {
                            "items": updated_items,
                            "last_updated": datetime.now()
                        }
                    }
                    
                )
            else:
                # Create new cart with items
                 cart.insert_one({

                    "Customer_Name" : Name,
                    "Phone_no" : Phone_no,
                    "Email": Email,
                    "Address" : Address,
                    "Area" : Area,
                    "Pincode" : Pincode,
                    "items": new_items,
                    "OrderDate": x.strftime("%x"),
                    "OrderTime": x.strftime("%X %p"),
                    # "created_at": datetime.now(),
                    # "last_updated": datetime.now()
                })
            
            messages.success(request, "Items added to cart successfully!")
        
    # Get current cart items for display
    current_cart = cart.find_one({"Email": email})
    cart_items = current_cart.get('items', []) if current_cart else []
    
    # Calculate cart total
    cart_total = sum(item['Total'] for item in cart_items)
    
    context = {
        "data": cart_items,  # Changed to match your template's expectation
        "cart_total": cart_total
    }
    
    if not cart_items:
        context["message"] = "Your cart is empty."

    
    return render(request, "dashboard.html", context)

'''    


def remove_from_cart(request):
    if request.method == "POST":
        client = MongoClient("mongodb://localhost:27017/")
        db = client['Project']
        cart = db['Cart']
        
        # Get user email from session
        email = request.session.get('email')
        if not email:
            return HttpResponse("You are not logged in. Please log in first.")
        
        # Get the index of item to remove
        item_index = int(request.POST.get('item_index', 0))
        
        # Find user's cart
        user_cart = cart.find_one({"Email": email})
        if user_cart and 'items' in user_cart:
            # Get current items
            items = user_cart['items']
            
            # Remove the item at specified index if it exists
            if 0 <= item_index < len(items):
                items.pop(item_index)
                
                # Update cart with remaining items
                cart.update_one(
                    {"Email": email},
                    {
                        "$set": {
                            "items": items,
                            "last_updated": datetime.now()
                        }
                    }
                )
                messages.success(request, "Item removed from cart successfully!")
            else:
                messages.error(request, "Item not found in cart.")
        else:
            messages.error(request, "Cart is empty.")
            
    return redirect('dashboard')


# def clear_cart(request):
#     if request.method == "POST":
#         client = MongoClient("mongodb://localhost:27017/")
#         db = client['Project']
#         cart = db['Cart']

#         email = request.session.get('email')
#         if not email:
#             return HttpResponse("You are not logged in. Please log in first.")

#         # Find user's cart
#         user_cart = cart.find_one({"Email": email})

#         if user_cart:
#             # Keep cart structure but reset items
#             cart.update_one({"Email": email}, {"$set": {"items": []}})
#             messages.success(request, "Your cart has been cleared after placing the order!")

        
#         return redirect('dashboard')  # Redirect back to the dashboard


def order(request):

    client = MongoClient("mongodb://localhost:27017/")
    db = client['Project']
    cart = db['Cart']
    order = db['Order']

    email = request.session.get('email')

    data = cart.find({'Email' : email})
    userData = []
    #user = cart.find_one({'Email' : email},{'_id':0})

    # for i in data:
    #     date = i['OrderDate']
    #     time = i['OrderTime']
    #     type = i['Order'][0]['Type']
    #     quantity = i['Order'][0]['Quantity']
    #     price = i['Order'][0]['Price']
    #     total = i['Order'][0]['Total']
        
    #     userData.append({"Date" : date,"Time":time,"Type":type,"Quantity":quantity,"Price" : price,"Total":total})

    for i in data:
        date = i.get('OrderDate')
        time = i.get('OrderTime')
        id = str(i.get('_id'))

        orders = i.get('Order', [])  # Ensure 'Order' exists and is a list
        
        if orders and isinstance(orders, list):  # Check if list is not empty

            
            order_item = orders[0]  # Access the first item safely
            
            type = order_item.get('Type', 'Unknown')
            quantity = order_item.get('Quantity', 0)
            price = order_item.get('Price', 0.0)
            total = order_item.get('Total', 0.0)
            userData.append({"Id":id,"Date" : date,"Time":time,"Type":type,"Quantity":quantity,"Price" : price,"Total":total})    

    # user = cart.find_one({'Email' : email},{'_id':0})
    # Name = user['Customer_Name']
    # Phone_no = user['Phone_no']
    # Email = user['Email']
    # Address = user['Address']
    # Area = user['Area']
    # Pincode = user['Pincode']
    
    user = cart.find_one({'Email' : email},{'_id':0})
    Name = user.get('Customer_Name','Unknown')
    Phone_no = user.get('Phone_no',0.0)
    Email = user.get('Email','Unkonwn')
    Address = user.get('Address',0.0)
    Area = user.get('Area',0.0)
    Pincode = user.get('Pincode',0.0)

    new_items = []

    if request.method=="POST":

        type = request.POST.get('type','Unknown')
        quantity = int(request.POST.get('quantity',0))
        price = float(request.POST.get('price',0))
        total = float(request.POST.get('total',0))
        payment = request.POST.get('payment','Unknown')
        new_items.append({"Type":type,"Quantity":quantity,"Price" : price,"Total":total})

        x = datetime.now()

        query = {
            "Customer_Name" : Name,
            "Phone_no" : Phone_no,
            "Email" : Email,
            "Address" : Address,
            "Area" : Area,
            "Pincode" : Pincode,
            "Order" : new_items,
            "Payment_Mode" : payment,
            "OrderDate" : x.strftime("%x"),
            "OrderTime" : x.strftime("%X %p")   
        }

        order.insert_one(query)
  
    return render (request,"order.html",{"data" : userData})

# def delete(request):
    
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client['Project']
#     cart = db['Cart']
#     email = request.session.get('email')
#     if request.method == "POST":

#         order_id = request.POST.get('id')

#         cart.find_one({'_id':order_id,'Email' : email})

#     return render(request,"order.html")

from bson import ObjectId
from django.shortcuts import redirect

def delete(request):
    """ Deletes an order based on the provided ID from MongoDB """

    client = MongoClient("mongodb://localhost:27017/")
    db = client['Project']
    cart = db['Cart']
    email = request.session.get('email')

    if request.method == "POST":
        order_id = request.POST.get('id')

        if order_id:
            try:
                result = cart.delete_one({'_id': ObjectId(order_id), 'Email': email})

                if result.deleted_count == 0:
                    print("No matching order found.")
            except Exception as e:
                print(f"Error deleting order: {e}")

    return redirect('order')  # Redirect instead of rendering template



def about(request):
    return render(request,"about.html")


def contact(request):

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['textarea']

        client = MongoClient("mongodb://localhost:27017/")
        db = client['Project']
        contact = db['Contact']
        query = {"FirstName" : fname,"LastName" : lname,"Email" : email,"Phone" : phone, "Message" : message}
        contact.insert_one(query)

    return render(request,"contact.html")

# #try
# def dashboard(request):
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client['Project']
#     order = db['Order']
#     signupData = db['Signup']


#     if request.method == "POST":
       
#     #     prices = {
#     #     'Bonless_Chicken': 400,
#     #     'Breast_Ribs': 450,
#     #     'Chicken_legs': 350,
#     #     'Leg_Quarter': 250,
#     #     'Whole_Legs': 550,
#     #     'Eggs': 160,
#     #     'Drumstick': 360,
#     #     'Keema': 160,
#     #     'Lolipop': 210,
#     #     'Wings': 160
#     #    }

#         email = request.session.get('email')

#         if not email:
#             return HttpResponse("You are not logged in. Please log in first.")

#         user = signupData.find_one({'Email': email}, {'_id': 0})

#         if not user:
#             return HttpResponse("User not found.")

#         Name = user.get('Name')
#         Phone_no = user.get('Phone_no')
#         Email = user.get('Email')
#         Address = user.get('Address')
#         Area = user.get('Area')
#         Pincode = user.get('Pincode')

#         new_items = []
        
#         # for product_name in prices.keys():
#         #     quantity = int(request.POST.get(product_name, 0))
#         #     if quantity > 0:
#         #         price = prices[product_name]
#         #         total = quantity * price
                
#         #         new_items.append({
#         #             "Type": product_name,
#         #             "Quantity": quantity,
#         #             "Price": price,
#         #             "Total": total
#         #         })    

#         product = request.POST.get(product,0)
#         quantity = request.POST.get(quantity,0)
#         price = request.POST.get(price,0)
#         total = request.POST.get(total,0)

#         new_items.append({
#            "Type": product,
#             "Quantity": quantity,
#             "Price": price,
#             "Total": total
#             })    
        
#         x = datetime.now()
#         query = {
#             "Customer_Name" : Name,
#             "Phone_no" : Phone_no,
#             "Email" : Email,
#             "Address" : Address,
#             "Area" : Area,
#             "Pincode" : Pincode,
#             "Order" : new_items,
#             "OrderDate" : x.strftime("%x"),
#             "OrderTime" : x.strftime("%X %p")   
#         }

#         if query:
#             # Insert the entire order as a single document in the database
#             order.insert_one(query)
#             # Pass the full order data to the template for rendering
#             #return render(request, "dashboard.html", {"data": new_items})
#             return render(request, "dashboard1.html",{"data":new_items})
         
#         else:
#             # Handle the case where no items are selected
#             return render(request, "dashboard1.html", {"message": "No items were selected."})

#     return render(request, "dashboard1.html")
    
#main

def dashboard(request):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['Project']
    cart = db['Cart']
    signupData = db['Signup']


    if request.method == "POST":
       
        prices = {
        'Bonless_Chicken': 400,
        'Breast_Ribs': 450,
        'Chicken_legs': 350,
        'Leg_Quarter': 250,
        'Whole_Legs': 550,
        'Eggs': 160,
        'Drumstick': 360,
        'Keema': 160,
        'Lolipop': 210,
        'Wings': 160
       }

        email = request.session.get('email')

        if not email:
            return HttpResponse("You are not logged in. Please log in first.")

        user = signupData.find_one({'Email': email}, {'_id': 0})

        if not user:
            return HttpResponse("User not found.")

        Name = user.get('Name')
        Phone_no = user.get('Phone_no')
        Email = user.get('Email')
        Address = user.get('Address')
        Area = user.get('Area')
        Pincode = user.get('Pincode')

        new_items = []
        
        for product_name in prices.keys():
            quantity = int(request.POST.get(product_name, 0))
            if quantity > 0:
                price = prices[product_name]
                total = quantity * price
                
                new_items.append({
                    "Type": product_name,
                    "Quantity": quantity,
                    "Price": price,
                    "Total": total
                })    

        x = datetime.now()
        query = {
            "Customer_Name" : Name,
            "Phone_no" : Phone_no,
            "Email" : Email,
            "Address" : Address,
            "Area" : Area,
            "Pincode" : Pincode,
            "Order" : new_items,
            "OrderDate" : x.strftime("%x"),
            "OrderTime" : x.strftime("%X %p")   
        }

        if query:
            # Insert the entire order as a single document in the database
            cart.insert_one(query)
            # Pass the full order data to the template for rendering
            #return render(request, "dashboard.html", {"data": new_items})
            return render(request, "dashboard.html")
         
        else:
            # Handle the case where no items are selected
            return render(request, "dashboard.html", {"message": "No items were selected."})

    return render(request,"dashboard.html")

'''
def dashboard(request):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['chicken_delivery']
    order = db["Order"]  # MongoDB collection

    if request.method == "POST":
        # Get data from POST request safely
        Bonless_Chicken = int(request.POST.get('Bonless_Chicken', 0))
        Breast_Ribs = int(request.POST.get('Breast_Ribs', 0))
        Chicken_legs = int(request.POST.get('Chicken_legs', 0))
        Leg_Quarter = int(request.POST.get('Leg_Quarter', 0))
        Whole_Legs = int(request.POST.get('Whole_Legs', 0))
        Eggs = int(request.POST.get('Eggs', 0))
        Drumstick = int(request.POST.get('Drumstick', 0))
        Wing = int(request.POST.get('Wing', 0))
        Lolipop = int(request.POST.get('Lolipop', 0))
        Wings = int(request.POST.get('Wings', 0))

        # Define product types and prices
        types = [
            "Bonless_Chicken", "Breast_Ribs", "Chicken_legs", "Leg_Quarter",
            "Whole_Legs", "Eggs", "Drumstick", "Wing", "Lolipop", "Wings"
        ]
        quantities = [
            Bonless_Chicken, Breast_Ribs, Chicken_legs, Leg_Quarter,
            Whole_Legs, Eggs, Drumstick, Wing, Lolipop, Wings
        ]

        prices = [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]

        # Combine all data into a single list
        userOrder = []

        for i in range(len(quantities)):
            if quantities[i] > 0:
                total = quantities[i] * prices[i]
                data = {
                    "Type": types[i],
                    "Quantity": quantities[i],
                    "Price": prices[i],
                    "Total": total
                }
                userOrder.append(data)

        # Insert data as a single document in the database with auto-generated _id
        if userOrder:
            document = {
                "Customer Name" : "Fardin",
                "Date" : '20/01/2025',
                "Orders": userOrder  # MongoDB will generate a unique _id for this document
            }
            order.insert_one(document)
            print(f"Inserted data successfully")
        else:
            print("No items to insert.")

        # Pass the full order data to the template for rendering
        return render(request, "dashboard.html", {"data": userOrder})

    return render(request, "dashboard.html")
'''
'''
def dashboard(request):

    order = db['Order']

    if request.method == "POST":
        # Get data from POST request safely
        Bonless_Chicken = int(request.POST.get('Bonless_Chicken', 0))
        Breast_Ribs = int(request.POST.get('Breast_Ribs', 0))
        Chicken_legs = int(request.POST.get('Chicken_legs', 0))
        Leg_Quarter = int(request.POST.get('Leg_Quarter', 0))
        Whole_Legs = int(request.POST.get('Whole_Legs', 0))
        Whole_Leg = int(request.POST.get('Whole_Leg', 0))
        Drumstick = int(request.POST.get('Drumstick', 0))
        Wing = int(request.POST.get('Wing', 0))
        Lolipop = int(request.POST.get('Lolipop', 0))
        Wings = int(request.POST.get('Wings', 0))

        # Define product types and prices
        types = [
            "Bonless_Chicken", "Breast_Ribs", "Chicken_legs", "Leg_Quarter",
            "Whole_Legs", "Whole_Leg", "Drumstick", "Wing", "Lolipop", "Wings"
        ]
        quantities = [
            Bonless_Chicken, Breast_Ribs, Chicken_legs, Leg_Quarter,
            Whole_Legs, Whole_Leg, Drumstick, Wing, Lolipop, Wings
        ]
        prices = [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]

        # Combine all data into a single list
        userOrder = []

        for i in range(len(quantities)):

            if quantities[i] > 0:

                total = quantities[i] * prices[i]
                
                userOrder.append({"Type" : types[i] ,"Quantity": quantities[i],"Price" : prices[i],"Total":total })
                                 
            
        
       # order.insert_one({"Order" : userOrder})

        if userOrder:
            # Insert the order as a single document in the database
            order.insert_one({"order_details": userOrder})
            return render(request, "dashboard.html", {"data": userOrder})

    return render(request, "dashboard.html")
'''
'''
def dashboard(request):
    
    order = db['Order']

    if request.method == "POST":
      
      Bonless_Chicken = request.POST['Bonless_Chicken']
      Breast_Ribs = request.POST['Breast_Ribs']
      Chicken_legs = request.POST['Chicken_legs']
      Leg_Quarter = request.POST['Leg_Quarter']
      Whole_Legs = request.POST['Whole_Legs']
      Whole_Leg = request.POST['Whole_Leg']
      Drumstick = request.POST['Drumstick']
      Wing = request.POST['Wing']
      Lolipop = request.POST['Lolipop']
      Wings = request.POST['Wings']
      
      types = ["Bonless_Chicken","Breast_Ribs","Chicken_legs","Leg_Quarter","Whole_Legs","Whole_Leg","Drumstick","Wing","Lolipop","Wings"]
      quantites = [Bonless_Chicken,Breast_Ribs,Chicken_legs,Leg_Quarter,Whole_Legs,Whole_Leg,Drumstick,Wing,Lolipop,Wings]
      prices = [200,300,400,500,600,700,800,900,1000]
      userOrder = []

      for i in range(len(quantites)):
          
        if int(quantites[i]) > 0:
              
            type = types[i]
            quantity = int(quantites[i])
            price = prices[i]
            total = quantity * price 
     
            data = {"Type" : type,"Quantity" : quantity,"Price" : price,"Total" : total}
            userOrder.append(data)
            return render(request,"dashboard.html",data)
    
      order.insert_one(userOrder)
      return render(request,"dashboard.html")  
      
      #query = {"Bonless_Chicken":Bonless_Chicken, "Breast_Ribs":Breast_Ribs,"Chicken_legs":Chicken_legs,"Leg_Quarter": Leg_Quarter,"Whole_Legs":Whole_Legs,"Whole_Leg":Whole_Leg,"Drumstick":Drumstick,"Wing": Wing,"Lolipop":Lolipop,"Wings": Wings}
      #order.insert_one(query)

      
      #return render(request,"dashboard.html")

    return render(request,"dashboard.html")
'''

'''
def dashboard(request):

    order = db['Order']

    if request.method == "POST":
      
      Bonless_Chicken = int(request.POST.get('Bonless_Chicken',0))
      Breast_Ribs = int(request.POST.get('Breast_Ribs',0))
      Chicken_legs = int(request.POST.get('Chicken_legs',0))
      Leg_Quarter = int(request.POST('Leg_Quarter',0))
      Whole_Legs = int(request.POST.get('Whole_Legs',0))
      Eggs = int(request.POST.get('Eggs',0))
      Drumstick = int(request.POST.get('Drumstick',0))
      Wing = int(request.POST.get('Wing',0))
      Lolipop = int(request.POST.get('Lolipop',0))
      Wings = int(request.POST.get('Wings',0))

      query = [Bonless_Chicken, Breast_Ribs, Chicken_legs, Leg_Quarter, Whole_Legs, Eggs,Drumstick, Wing, Lolipop, Wings]


      Order = []

      for item in query:
          
          if item > 0:
            Order.append(item)
      
      order.insert_one({"Name" : "Shaikh","Order" : Order})

      return render(request,"dashboard.html",{"data":Order})


    return render(request,"dashboard.html")

'''

    
'''
def akdashboard(request):

    if request.method=="POST":

        Lolipop =  request.POST['Lolipop']
        Leg_Piece =  request.POST['Leg_Piece']
        Boneless =  request.POST['Boneless']
        Eggs =  request.POST['Eggs']
        Wings =  request.POST['wings']
        Withskin =  request.POST['withskin']
        Withoutskin =  request.POST['withoutskin']
        Keema =  request.POST['keema']
        Legboneless =  request.POST['legboneless']
        
        # coll= db['Signup']
        # email = request.POST['email']

        # for i in coll.find({'Email':email},{'Email':1,'Phone_no' : 1 ,'Name' : 1,'_id':0}):
        #     email = i['Email']
        #     phone = i['Phone_no']
        #     name = i['Name']
            
        l = [Lolipop,Leg_Piece,Boneless,Eggs,Wings,Withskin,Withoutskin,Keema,Legboneless]

        for i in range(len(l)):

            if l[i] == "":
                l[i] = 0
            else:
                l[i] = int(l[i])    

        order = db['Order']

        query = { 
                  #"Id" : name,
                  #"Phone_no" : phone,
                  #"Email" : email,
                  "Lolipop": [ {"Quantity": l['Lolipop'] } , {"TotalPrice": l['Lolipop'] * 200} ],
                  "Leg_Piece":[{"Quantity":l['Leg_Piece']},{"TotalPrice": l['Leg_Piece'] * 300} ],
                  "Boneless":[{"Quantity":l['Boneless']},{"TotalPrice": l['Boneless'] * 250} ],
                  "Eggs":[{"Quantity":l['Eggs']},{"TotalPrice": l['Eggs'] * 100} ],
                  "Wings":[{"Quantity":l['Wings']},{"TotalPrice": l['Wings'] * 200} ],
                  "Withskin":[{"Quantity":l['Withskin']},{"TotalPrice": l['Withskin'] * 250} ],
                  "Withoutskin" : [ {"Quantity" : l['Withoutskin'] } , {"TotalPrice" : l['Withoutskin'] * 180} ],
                  "Keema":[ { "Quantity" : l['Keema'] } , {"TotalPrice" : l['Keema'] * 190 } ],
                  "Legboneless" : [ {"Quantity" : l['Legboneless'] } , {"TotalPrice": l['Legboneless'] * 300} ],
                }
        
        order.insert_one(query)

    return render(request,"akdashboard.html")
'''

'''
def akdashboard(request):
    
    if request.method == "POST":
        # Extract form data and handle empty strings
        fields = [
            "Lolipop", "Leg_Piece", "Boneless", "Eggs", 
            "Wings", "withskin", "withoutskin", "keema", "legboneless"
        ]
        data = {field: int(request.POST.get(field, 0) or 0) for field in fields}

        # Define prices
        prices = {
            "Lolipop": 200,
            "Leg_Piece": 300,
            "Boneless": 250,
            "Eggs": 100,
            "Wings": 200,
            "withskin": 250,
            "withoutskin": 180,
            "keema": 190,
            "legboneless": 300,
        }

        # Construct order document
        order = db['Order']
        query = {
            field: {
                "Quantity": data[field],
                "TotalPrice": data[field] * prices[field]
            }
            for field in fields
        }

        # Insert into MongoDB
        order.insert_one(query)

    return render(request, "akdashboard.html")
'''

'''
from django.shortcuts import render, redirect
from django.contrib import messages
from pymongo import MongoClient
from datetime import datetime
from django.http import HttpResponse

def dashboard(request):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['Project']
    cart = db['Cart']
    signupData = db['Signup']
    
    # Get current user's email from session
    email = request.session.get('email')
    if not email:
        return HttpResponse("You are not logged in. Please log in first.")
    
    # Get user details
    user_data = signupData.find_one(
        {'Email': email},
        {'Name': 1, 'Phone_no': 1, 'Email': 1, 'Area': 1, 'Pincode': 1, '_id': 0}
    )
    
    if request.method == "POST":
        # Get the item details from the form
        item_type = request.POST.get('item_type')
        quantity = int(request.POST.get(item_type, 0))
        
        if quantity > 0:
            # Get price based on item type
            prices = {
                'Bonless_Chicken': 400,
                'Breast_Ribs': 450,
                'Chicken_legs': 350,
                'Leg_Quarter': 250,
                'Whole_Legs': 550,
                'Eggs': 160,
                'Drumstick': 360,
                'Wing': 160,
                'Lolipop': 210,
                'Wings': 160
            }
            
            price = prices.get(item_type, 0)
            total = quantity * price
            
            # Create new cart item
            cart_item = {
                "OrderDate": datetime.now().strftime("%x"),
                "OrderTime": datetime.now().strftime("%X %p"),
                "Type": item_type,
                "Quantity": quantity,
                "Price": price,
                "Total": total
            }
            
            # Update or create cart for user
            cart.update_one(
                {"Email": email},
                {
                    "$push": {"items": cart_item},
                    "$setOnInsert": {
                        "Customer_Name": user_data['Name'],
                        "Phone_no": user_data['Phone_no'],
                        "Area": user_data['Area'],
                        "Pincode": user_data['Pincode'],
                        "created_at": datetime.now()
                    },
                    "$set": {"last_updated": datetime.now()}
                },
                upsert=True
            )
            
            messages.success(request, f"{item_type} added to cart successfully!")
        
    # Get current cart items
    user_cart = cart.find_one({"Email": email})
    cart_items = user_cart.get('items', []) if user_cart else []
    
    # Calculate cart totals
    cart_total = sum(item['Total'] for item in cart_items)
    item_count = len(cart_items)
    
    context = {
        "cart_items": cart_items,
        "cart_total": cart_total,
        "item_count": item_count,
        "user_data": user_data
    }
    
    return render(request, "dashboard.html", context)
'''
