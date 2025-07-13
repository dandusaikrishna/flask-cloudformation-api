# AWS CloudFormation Subnet API with Flask

## 👋 Introduction

A lightweight Flask-based RESTful API service to interact with AWS CloudFormation.


The objective of this project is to create a backend Flask API that interacts with **AWS CloudFormation** to:
- ✅ Retrieve CloudFormation stack templates
- ✅ Convert **public subnets to private**
- ✅ Create and monitor **ChangeSets**

---

#Demo 🛠

https://drive.google.com/file/d/1OZNzTxUk-Z1NlNhfXCLmaCxlz5uuHSKV/view?usp=sharing


## 🧰 Technologies Used

- Python + Flask
- Boto3 (AWS SDK for Python)
- CloudFormation
- Postman (for testing)
- `.env` for AWS credentials

---

## 🌐 Subnet & VPC Overview

### 🔍 What is a Subnet?
A **subnet** is a sub-division of a VPC (Virtual Private Cloud) in AWS, used to group and isolate resources.

There are two types of subnets:
- **Public Subnet** → Allows internet access (MapPublicIpOnLaunch: `true`)
- **Private Subnet** → No direct internet access (MapPublicIpOnLaunch: `false`)

This project involves converting public subnets to private in a CloudFormation template.

---

## 🛠️ Subnet Setup (via AWS Console)

1. Create a VPC — CIDR block: `10.0.0.0/16`
2. Create a Subnet — CIDR: `10.0.1.0/24`, enable public IPv4 assignment
3. Import subnet into CloudFormation stack (name it like `MyImportedSubnet`)
4. Use the stack name in the Flask APIs

---

## 🔄 VPC/Subnet Flow

```
VPC (10.0.0.0/16)
│
├── Subnet (10.0.1.0/24) ← Public (MapPublicIpOnLaunch: true)
│
├── Imported into CloudFormation Stack
│
├── Fetched & Modified by Flask API
│
└── ChangeSet Submitted to Update it to Private
```

---

## 🚀 Run the Project

```bash
# Create a virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
flask run
```

---

## 🔐 .env File

Set your credentials in a `.env` file (not pushed to GitHub):

```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
```

---

## 📡 API Endpoints

| Endpoint              | Method | Description                                                                 |
|-----------------------|--------|-----------------------------------------------------------------------------|
| `/template`           | GET    | Retrieve the CloudFormation template (YAML converted to JSON)              |
| `/subnet/convert`     | PUT    | Convert public subnets to private and create a CloudFormation ChangeSet    |
| `/changeset/create`   | POST   | Create and monitor a ChangeSet for a given stack and template               |

---

### 1. GET /template
Query: `stack_name`
```bash
curl "http://127.0.0.1:5000/template?stack_name=MySubnetStack"
```


## ✅ Example 
<img width="1366" height="768" alt="Screenshot 2025-07-13 112328" src="https://github.com/user-attachments/assets/8452ed45-93cd-435f-9a0a-8ca58dd6457b" />


### 2. PUT /subnet/convert
Convert public subnets to private.
```bash
PUT "http://127.0.0.1:5000/subnet/convert"
```


- **Request Body Example:**

```json
{
  "stack_name": "MySubnetStack",
  "template": {
    "Resources": {
      "MyImportedSubnet": {
        "Type": "AWS::EC2::Subnet",
        "Properties": {
          "VpcId": "vpc-0c4274a584fb3fabd",
          "CidrBlock": "10.0.1.0/24",
          "MapPublicIpOnLaunch": true
        }
      }
    }
  }
}

```

## ✅ Example 

<img width="1366" height="768" alt="Screenshot 2025-07-13 113706" src="https://github.com/user-attachments/assets/8c8dca7f-1856-48a0-aa1b-0c3094f08175" />

### 3. POST /changeset/create
Create and track a ChangeSet.
```bash
 POST "http://127.0.0.1:5000/changeset/create"
```

- **Request Body Example:**

```json
{
  "stack_name": "MySubnetStack",
  "template": {
    "Resources": {
      "MyImportedSubnet": {
        "Type": "AWS::EC2::Subnet",
        "Properties": {
          "VpcId": "vpc-0c4274a584fb3fabd",
          "CidrBlock": "10.0.1.0/24",
          "MapPublicIpOnLaunch": false
        }
      }
    }
  }
}

```
## ✅ Example 

<img width="1366" height="768" alt="Screenshot 2025-07-13 113827" src="https://github.com/user-attachments/assets/d0e5ba4e-0fe5-42ee-88db-044018db6c25" />

## 📁 Screenshots

📸 Screenshots are included in this repo to demonstrate successful:
- Subnet setup in AWS Console
- CloudFormation stack import
- ChangeSet creation via API

---


## ✅ Conclusion

Thanks for reviewing this assignment! Feel free to reach out if you have any questions or feedback.

**Author:** Sai Krishna Dandu  
**Email:** saikrishnadandu9@gmail.com  
**Phone:** 9381752077
