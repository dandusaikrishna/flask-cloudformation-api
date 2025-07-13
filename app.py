import json
import time
import yaml
from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

app = Flask(__name__)

# credentials from .env
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")

# Create CloudFormation client
cloudformation = boto3.client(
    'cloudformation',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

@app.route('/template', methods=['GET'])
def get_template():
    stack_name = request.args.get('stack_name')
    if not stack_name:
        return jsonify({'error': 'Missing stack_name parameter'}), 400
    try:
        response = cloudformation.get_template(StackName=stack_name)
        template_body = response.get('TemplateBody')
        if isinstance(template_body, str):
            # Parse YAML template string to JSON
            template_json = yaml.safe_load(template_body)
        else:
            template_json = template_body
        return jsonify(template_json), 200
    except ClientError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/subnet/convert', methods=['PUT'])
def convert_subnet():
    data = request.get_json()
    if not data or 'template' not in data or 'stack_name' not in data:
        return jsonify({'error': 'Missing template or stack_name in request body'}), 400
    template = data['template']
    stack_name = data['stack_name']

    # Convert public subnets to private subnets in the template
    try:
        resources = template.get('Resources', {})
        for res_name, res in resources.items():
            if res.get('Type') == 'AWS::EC2::Subnet':
                properties = res.get('Properties', {})
                # Check if MapPublicIpOnLaunch is True, convert to False
                if properties.get('MapPublicIpOnLaunch') is True:
                    properties['MapPublicIpOnLaunch'] = False

            
        # Create ChangeSet with the updated template
        change_set_name = f"changeset-{int(time.time())}"
        response = cloudformation.create_change_set(
            StackName=stack_name,
            TemplateBody=json.dumps(template),
            ChangeSetName=change_set_name,
            ChangeSetType='UPDATE'
        )
        change_set_id = response['Id']

        # Poll for ChangeSet creation completion
        while True:
            desc = cloudformation.describe_change_set(ChangeSetName=change_set_id)
            status = desc['Status']
            if status in ['CREATE_COMPLETE', 'FAILED']:
                break
            time.sleep(3)

        if status == 'FAILED':
            reason = desc.get('StatusReason', 'Unknown reason')
            return jsonify({'error': f'ChangeSet creation failed: {reason}'}), 400

        return jsonify({
            'message': 'ChangeSet created successfully',
            'ChangeSetId': change_set_id,
            'Status': status
        }), 200

    except ClientError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error processing template: {str(e)}'}), 500

@app.route('/changeset/create', methods=['POST'])
def create_changeset():
    data = request.get_json()
    if not data or 'stack_name' not in data or 'template' not in data:
        return jsonify({'error': 'Missing stack_name or template in request body'}), 400

    stack_name = data['stack_name']
    template = data['template']

    try:
        # Create ChangeSet
        change_set_name = f"changeset-{int(time.time())}"
        response = cloudformation.create_change_set(
            StackName=stack_name,
            TemplateBody=json.dumps(template),
            ChangeSetName=change_set_name,
            ChangeSetType='UPDATE'
        )
        change_set_id = response['Id']

        # Poll for ChangeSet creation completion
        while True:
            desc = cloudformation.describe_change_set(ChangeSetName=change_set_id)
            status = desc['Status']
            if status in ['CREATE_COMPLETE', 'FAILED']:
                break
            time.sleep(3)

        if status == 'FAILED':
            reason = desc.get('StatusReason', 'Unknown reason')
            return jsonify({'error': f'ChangeSet creation failed: {reason}'}), 400

        return jsonify({
            'message': 'ChangeSet created successfully',
            'ChangeSetId': change_set_id,
            'Status': status
        }), 200

    except ClientError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
