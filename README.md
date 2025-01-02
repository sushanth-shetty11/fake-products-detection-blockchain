🚀 **Fake Product Detection Using Blockchain**

🔒 A secure and decentralized system to ensure product authenticity.
This project leverages blockchain technology to detect counterfeit products and ensure authenticity through a tamper-proof system. Built using React.js, Material UI, and Ethereum, it provides a seamless user experience for both admins and consumers.

✨ **Features**

🛠 Admin Dashboard: Add and manage product details for authenticity checks.
🔍 Consumer Portal: Verify product authenticity based on blockchain records.
🔐 Secure Authentication: Retailer, supplier, and consumer logins with default credentials.
📜 Decentralized Verification: Ensures data integrity and prevents tampering using Ethereum.

🗂️ **Project Structure**

📁 hello-eth: Contains blockchain-related code and smart contracts.
📁 blockchaincounterfeit: Frontend application built with Html and css for user 
interactions.

⚙️ **Setup and Usage**

🛠 1. Setting Up Blockchain
Navigate to the hello-eth folder:
cd hello-eth

2.Locate the node_modules folder, then open the .bin directory.

3. Run the runblockchain file:
A terminal will pop up displaying Ethereum accounts and keys.
Copy the mnemonics keys shown in the terminal.

4. Open Ganache:
📥 Download and install Ganache from here.
Launch Ganache and select "New Workspace".

5.Server Setup:
Assign a name to your workspace (e.g., FakeProductDetection).
Set the port number to match the one displayed in the terminal running runblockchain.

6.Mnemonic Setup:
Go to the Accounts and Keys section in Ganache and input the mnemonics you copied earlier.
Click Start to initialize the blockchain environment.

7.Return to the terminal and deploy the smart contracts:
truffle migrate
This will deploy the smart contracts on the local blockchain network.
Copy the contract address displayed after deployment.


🖥️ 2. **Configure the Frontend**

i. Navigate to the blockchaincounterfeit folder:

> cd blockchaincounterfeit
> code .

ii.Open the main file where the contract address is defined.

iii.Replace the placeholder with the contract address you copied earlier.
     Ensure both instances of the contract address are updated.

🌐 3. **Run the Application**

i.In the blockchaincounterfeit folder, double-click the run file.

ii.A new terminal will open, displaying a URL.

iii.Copy the URL and paste it into your browser, appending /index to it:
        ? http://<url /index
        
iv. The web application will load.
  
🧑‍💻 4. **Using the Application**
🔑 Login Credentials
Admin Login:
Username: admin
Password: admin
Supplier/Retailer/Consumer Login: User-specific credentials.

🚀 **Features**
Admin: Add new products and manage existing ones.
Consumer: Check whether a product is authentic or fake.

💻 **Technologies Used**
Frontend: React.js, Material UI, CSS
Backend: Ethereum Smart Contracts
Blockchain Tools: Ganache, Truffle
Other Tools: Visual Studio Code

🔗 **Links**
Repository: Fake Product Detection Using Blockchain
Ganache: [Download Ganache](https://github.com/trufflesuite/ganache-ui/releases/download/v2.7.1/Ganache-2.7.1-win-x64.appx)
Truffle: Learn About Truffle

🤝 **Contributing**
We welcome contributions! Feel free to submit pull requests or report issues in the Issues section.

📜 **License**
This project is licensed under the MIT License.
