# Flask CloudFormation API

A lightweight Flask-based RESTful API service to interact with AWS CloudFormation.

## Features

- Retrieve CloudFormation templates from existing stacks
- Modify subnet properties (e.g., convert public to private)
- Create and monitor CloudFormation ChangeSets

## Technologies Used

- Python 3.x  
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

4. Set AWS credentials via AWS CLI or environment variables.

5. Run the Flask app:
```bash
flask run
```

## API Endpoints

### 1. GET /template
Query: `stack_name`
```bash
curl "http://127.0.0.1:5000/template?stack_name=MySubnetStack"
```

### 2. PUT /subnet/convert
Convert public subnets to private.
```bash
curl -X PUT http://127.0.0.1:5000/subnet/convert -H "Content-Type: application/json" -d @template.json
```

### 3. POST /changeset/create
Create and track a ChangeSet.
```bash
curl -X POST http://127.0.0.1:5000/changeset/create -H "Content-Type: application/json" -d @template.json
```

## Permissions Required
- cloudformation:GetTemplate
- cloudformation:CreateChangeSet
- cloudformation:DescribeChangeSet
- cloudformation:UpdateStack
- ec2:DescribeSubnets

MIT License
