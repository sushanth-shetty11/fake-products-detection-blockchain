from flask import Flask, render_template, request, redirect, url_for, session
import json
from web3 import Web3, HTTPProvider
import hashlib
from hashlib import sha256
import os
import datetime
import sqlite3

import qrcodegen as qrg
import qrreader as qrr

app = Flask(__name__)

app.secret_key = 'welcome'
global uname, details

def readDetails(contract_type):
    global details
    details = ""
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'CounterFeit.json' #counter feit contract code
    deployed_contract_address = '0xdA0b9DdE7F0a0E4255aA112a453B129E83975BB5' #hash address to access counter feit contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'adduser':
        details = contract.functions.getUserDetails().call()
    if contract_type == 'productdata':
        details = contract.functions.getProductDetails().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]    
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'CounterFeit.json' #Counter feit contract file
    deployed_contract_address = '0xdA0b9DdE7F0a0E4255aA112a453B129E83975BB5' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'adduser':
        details+=currentData
        msg = contract.functions.setUserDetails(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'productdata':
        details+=currentData
        msg = contract.functions.setProductDetails(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', msg='')

@app.route('/Login', methods=['GET', 'POST'])
def Login():
   return render_template('Login.html', msg='')
@app.route('/SLogin', methods=['GET', 'POST'])
def SLogin():
   return render_template('SLogin.html', msg='')
@app.route('/RLogin', methods=['GET', 'POST'])
def RLogin():
   return render_template('RLogin.html', msg='')

@app.route('/AdminLogin', methods=['GET', 'POST'])
def AdminLogin():
   return render_template('AdminLogin.html', msg='')

@app.route('/AdminLoginAction', methods=['GET', 'POST'])
def AdminLoginAction():
    global uname
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        if user == "admin" and password == "admin":
            return render_template('AdminScreen.html', msg="Welcome "+user)
        else:
            return render_template('Login.html', msg="Invalid login details")

@app.route('/Signup', methods=['GET', 'POST'])
def Signup():
    return render_template('Signup.html', msg='')

@app.route('/AccessData', methods=['GET', 'POST'])
def AccessData():
    return render_template('AccessData.html', msg='')

@app.route('/LoginAction', methods=['GET', 'POST'])
def LoginAction():
    global uname
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == user and array[1] == password and array[5]=="Consumer":
                uname = user
                status = "success"
                break
        if status == "success":
            return render_template('UserScreen.html', msg="Welcome "+uname)
        else:
            return render_template('Login.html', msg="Invalid login details")
@app.route('/SLoginAction', methods=['GET', 'POST'])
def SLoginAction():
    global uname
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == user and array[1] == password and array[5]=="Supplier":
                uname = user
                status = "success"
                break
        if status == "success":
            return render_template('SUserScreen.html', msg="Welcome "+uname)
        else:
            return render_template('Login.html', msg="Invalid login details")
@app.route('/RLoginAction', methods=['GET', 'POST'])
def RLoginAction():
    global uname
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == user and array[1] == password and array[5]=="Retailer":
                uname = user
                status = "success"
                break
        if status == "success":
            return render_template('RUserScreen.html', msg="Welcome "+uname)
        else:
            return render_template('Login.html', msg="Invalid login details")

@app.route('/ViewProduct', methods=['GET', 'POST'])
def ViewProduct():
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Product Id', 'Product Name', 'Product Price', 'Manufacturing Details', 'Company Details']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('productdata')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            output += "<tr><td>"+font+array[0]+"</td>"
            output += "<td>"+font+array[1]+"</td>"
            output += "<td>"+font+array[2]+"</td>"
            output += "<td>"+font+array[3]+"</td>"
            output += "<td>"+font+array[4]+"</td>"            
        output+="<br/><br/><br/><br/><br/><br/>"
        
        return render_template('ViewProduct.html', msg=output)         

@app.route('/ViewUsers', methods=['GET', 'POST'])
def ViewUsers():
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Username', 'Password', 'Phone No', 'Email ID', 'Address','User type']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('adduser')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            output += "<tr><td>"+font+array[0]+"</td>"
            output += "<td>"+font+array[1]+"</td>"
            output += "<td>"+font+array[2]+"</td>"
            output += "<td>"+font+array[3]+"</td>"
            output += "<td>"+font+array[4]+"</td>"
            output += "<td>"+font+array[5]+"</td>"            
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewUser.html', msg=output) 
        
        
@app.route('/SignupAction', methods=['GET', 'POST'])
def SignupAction():
    if request.method == 'POST':
        global details
        uname = request.form['t1']
        password = request.form['t2']
        phone = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        utype=request.form['utype']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == uname:
                status = uname+" Username already exists"
                break
        if status == "none":
            data = uname+"#"+password+"#"+phone+"#"+email+"#"+address+"#"+utype+"\n"
            saveDataBlockChain(data,"adduser")
            context = "User signup task completed"
            return render_template('Signup.html', msg=context)
        else:
            return render_template('Signup.html', msg=status)

@app.route('/Logout')
def Logout():
    return render_template('index.html', msg='')

@app.route('/AddProduct', methods=['GET', 'POST'])
def AddProduct():
   return render_template('AddProduct.html', msg='')
@app.route('/qrgen', methods=['GET','POST'])
def qrgen():
    pid = request.form['t1']
    pname = request.form['t2']
    qrg.process(pid,pname)
    return render_template('AddProduct1.html', pid=pid,pname=pname,msg="QR code Geerated Successfully")
@app.route('/imgupload',methods=['GET','POST'])
def imgupload():
    if request.method=='POST':
        pid = request.form['t1']
        pname = request.form['t2']
        img = request.files['my_image']
        img_path = "static/products/" + img.filename
        img.save(img_path)
        conn= sqlite3.connect("Database.db")
        cmd="SELECT * FROM product WHERE pid='"+pid+"'"
        print(cmd)
        cursor=conn.execute(cmd)
        isRecordExist=0
        for row in cursor:
            isRecordExist=1
        if(isRecordExist==1):
                print("Username Already Exists")
                return render_template("AddProduct.html",msg="Image Id Already exist")
        else:
                print("insert")
                cmd="INSERT INTO product Values('"+str(pid)+"','"+str(img_path)+"','"+str(pname)+"')"
                print(cmd)
                print("Inserted Successfully")
                conn.execute(cmd)
                conn.commit()
                conn.close() 
                return render_template('AddProduct.html', msg="Image Uploaded Successfully")


@app.route('/AddProductAction', methods=['GET', 'POST'])
def AddProductAction():
    if request.method == 'POST':
        pid = request.form['t1']
        pname = request.form['t2']
        price = request.form['t3']
        manufacture = request.form['t4']
        company = request.form['t5']
        barcode = request.files['t6']
        contents = barcode.read()
        current_time = datetime.datetime.now() 
        digital_signature = sha256(contents).hexdigest();
        data = pid+"#"+pname+"#"+price+"#"+manufacture+"#"+company+"#"+str(current_time)+"#"+digital_signature+"\n"
        saveDataBlockChain(data,"productdata")
        context = "Product details added with id : "+pid+"<br/>Generated Digital Signatures : "+digital_signature
        return render_template('AddProduct2.html',pid=pid,pname=pname, msg=context)
@app.route('/SRetrieveData',methods=['GET','POST'])
def SRetrieveData():
    return render_template('SretrieveData.html',msg='')
        
@app.route('/RetrieveData', methods=['GET', 'POST'])
def RetrieveData():
   return render_template('RetrieveData.html', msg='')
@app.route('/SRetrieveDataAction',methods=['GET','POST'])
def SRetrieveDataAction():
    if request.method == 'POST':
        pid = request.form['t1']
        output =[]
        conn= sqlite3.connect("Database.db")
        cmd="SELECT * FROM product WHERE pid='"+pid+"'"
        cursor=conn.execute(cmd)
        imagepath=""
        for row in cursor:
            print("row=",row)
            imagepath=row[1]
        print("imagepath==es==",imagepath)                
        arr = ['Product ID', 'Product Name', 'Product Price', 'Manufacturing Details', 'Company Details', 'Date & Time', 'Barcode Digital Signatures']
        
                  
        readDetails('productdata')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == pid:
                output.append(array[0])
                output.append(array[1])
                output.append(array[2])
                output.append(array[3])
                output.append(array[4])
                output.append(array[5])
                output.append(array[6])
        #print("Output=="+output)
        return render_template('SViewDetails.html', msg=output,image_path=imagepath)  
@app.route('/RRetrieveData', methods=['GET', 'POST'])
def RRetrieveData():
   return render_template('RRetrieveData.html', msg='')
@app.route('/RRetrieveDataAction',methods=['GET','POST'])
def RRetrieveDataAction():
    if request.method == 'POST':
        pid = request.form['t1']
        output =[]
        conn= sqlite3.connect("Database.db")
        cmd="SELECT * FROM product WHERE pid='"+pid+"'"
        cursor=conn.execute(cmd)
        imagepath=""
        for row in cursor:
            print("row=",row)
            imagepath=row[1]
        print("imagepath==es==",imagepath)                
        arr = ['Product ID', 'Product Name', 'Product Price', 'Manufacturing Details', 'Company Details', 'Date & Time', 'Barcode Digital Signatures']
        
                  
        readDetails('productdata')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == pid:
                output.append(array[0])
                output.append(array[1])
                output.append(array[2])
                output.append(array[3])
                output.append(array[4])
                output.append(array[5])
                output.append(array[6])
        #print("Output=="+output)
        return render_template('RViewDetails.html', msg=output,image_path=imagepath)  


@app.route('/RetrieveDataAction', methods=['GET', 'POST'])
def RetrieveDataAction():
    if request.method == 'POST':
        pid = request.form['t1']
        output =[]
        conn= sqlite3.connect("Database.db")
        cmd="SELECT * FROM product WHERE pid='"+pid+"'"
        cursor=conn.execute(cmd)
        imagepath=""
        for row in cursor:
            print("row=",row)
            imagepath=row[1]
        print("imagepath==es==",imagepath)                
        arr = ['Product ID', 'Product Name', 'Product Price', 'Manufacturing Details', 'Company Details', 'Date & Time', 'Barcode Digital Signatures']
        
                  
        readDetails('productdata')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == pid:
                output.append(array[0])
                output.append(array[1])
                output.append(array[2])
                output.append(array[3])
                output.append(array[4])
                output.append(array[5])
                output.append(array[6])
        #print("Output=="+output)
        return render_template('ViewDetails.html', msg=output,image_path=imagepath)  

@app.route('/AuthenticateScan', methods=['GET', 'POST'])
def AuthenticateScan():
   return render_template('AuthenticateScan.html', msg='')


@app.route('/AuthenticateScanAction', methods=['GET', 'POST'])
def AuthenticateScanAction():
    if request.method == 'POST':
        barcode = request.files['t1']
        contents = barcode.read()
        digital_signature = sha256(contents).hexdigest();
        output = []
        font = '<font size="" color="black">'
        arr = ['Product ID', 'Product Name', 'Product Price', 'Manufacturing Details', 'Company Details', 'Date & Time', 'Barcode Digital Signatures']
        imagepath=""
        
        readDetails('productdata')
        arr = details.split("\n")
        flag = 0
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            print("digital_signature==",str(digital_signature))
            print("array[6]==",str(array[6]))
            if array[6] == digital_signature:
                flag = 1
                output.append(array[0])
                output.append(array[1])
                output.append(array[2])
                output.append(array[3])
                output.append(array[4])
                output.append(array[5])
                output.append(array[6])
                #break
        if flag == 0:
            output.append("Bar code Authenetication failed It is a Fake Product")
        else:
            pid=array[0]
            conn= sqlite3.connect("Database.db")
            cmd="SELECT * FROM product WHERE pid='"+pid+"'"
            cursor=conn.execute(cmd)
            for row in cursor:
                print("row=",row)
                imagepath=row[1]
        
        print("imagepath==es==",imagepath)
        return render_template('ViewDetails.html', msg=output,image_path=imagepath)


if __name__ == '__main__':
    app.run()










