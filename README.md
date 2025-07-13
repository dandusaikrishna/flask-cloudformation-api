# Flask CloudFormation API

A lightweight Flask-based RESTful API service to interact with AWS CloudFormation.

## Features

- Retrieve CloudFormation templates from existing stacks
- Modify subnet properties (e.g., convert public to private)
- Create and monitor CloudFormation ChangeSets

## Technologies Used

- Python
- Flask (REST API)
- Boto3 (AWS SDK)
- AWS CloudFormation

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-username/flask-cloudformation-api.git
cd flask-cloudformation-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set AWS credentials via environment variables.

5. Run the Flask app:
```bash
flask run
```

## API Endpoints

| Endpoint                 | Method | Description                                                                                  |
|--------------------------|--------|----------------------------------------------------------------------------------------------|
| `/template`              | GET    | Retrieve the CloudFormation template (YAML converted to JSON) of a given stack              |
| `/subnet/convert`        | PUT    | Convert public subnets to private in the given template and create a CloudFormation ChangeSet |
| `/changeset/create`      | POST   | Create and monitor a ChangeSet for the given stack using the provided template              |



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


## Permissions Required
- cloudformation:GetTemplate
- cloudformation:CreateChangeSet
- cloudformation:DescribeChangeSet
- cloudformation:UpdateStack
- ec2:DescribeSubnets

MIT License
