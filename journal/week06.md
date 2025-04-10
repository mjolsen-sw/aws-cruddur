# Week 6 — Deploying Containers
## Defaults
```sh
export DEFAULT_VPC_ID=$(aws ec2 describe-vpcs \
--filters "Name=isDefault, Values=true" \
--query "Vpcs[0].VpcId" \
--output text);
echo $DEFAULT_VPC_ID
```
```sh
export DEFAULT_SUBNET_IDS=$(aws ec2 describe-subnets  \
 --filters Name=vpc-id,Values=$DEFAULT_VPC_ID \
 --query 'Subnets[*].SubnetId' \
 --output json | jq -r 'join(",")');
echo $DEFAULT_SUBNET_IDS
```
## DB Connection Test
Added connection test script at `./backend-flask/bin/db/test`
## Task Flask Script
We add the following enpoint for our flask app for ELB health checks:
```python
@app.route('/api/health-check')
def health_check():
  return {'success': True}, 200
```
Use the scipt at `bin/flask/health-check` to test the endpoint
## Create CloudWatch Log Group
```sh
aws logs create-log-group --log-group-name cruddur
aws logs put-retention-policy --log-group-name cruddur --retention-in-days 1
```
## Create ECS Cluster
```sh
aws ecs create-cluster --cluster-name cruddur --service-connect-defaults namespace=cruddur
```
```sh
export CRUD_CLUSTER_SG=$(aws ec2 create-security-group \
  --group-name cruddur-ecs-cluster-sg \
  --description "Security group for Cruddur ECS ECS cluster" \
  --vpc-id $DEFAULT_VPC_ID \
  --query "GroupId" --output text)
echo $CRUD_CLUSTER_SG
```
```sh
export CRUD_CLUSTER_SG=$(aws ec2 describe-security-groups \
--group-names cruddur-ecs-cluster-sg \
--query 'SecurityGroups[0].GroupId' \
--output text)
```
## Create ECR repo and push image
### Login to ECR
```sh
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
```
### For Base image python slim-buster
1. Create Repository
```sh
aws ecr create-repository --repository-name cruddur-python --image-tag-mutability MUTABLE
```
2. Set URL
```sh
export ECR_PYTHON_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/cruddur-python"
echo $ECR_PYTHON_URL
```
3. Pull Image
```sh
docker pull python:3.10-slim-buster
```
4. Tag Image
```sh
docker tag python:3.10-slim-buster $ECR_PYTHON_URL:3.10-slim-buster
```
5. Push Image
```sh
docker push $ECR_PYTHON_URL:3.10-slim-buster
```
### For Backend Flask
1. Update Backend Dockerfile to use ECR Base Image URI
2. Create Repo
```sh
aws ecr create-repository --repository-name backend-flask --image-tag-mutability MUTABLE
```
3. Set URL
```sh
export ECR_BACKEND_FLASK_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/backend-flask"
echo $ECR_BACKEND_FLASK_URL
```
4. Build Image
```sh
docker build -t backend-flask .
```
5. Tag Image
```sh
docker tag backend-flask:latest $ECR_BACKEND_FLASK_URL:latest
```
6. Push Image
```sh
docker push $ECR_BACKEND_FLASK_URL:latest
```
### For Base image node
1. Create Repository
```sh
aws ecr create-repository --repository-name cruddur-node --image-tag-mutability MUTABLE
```
2. Set URL
```sh
export ECR_NODE_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/cruddur-node"
echo $ECR_NODE_URL
```
3. Pull Image
```sh
docker pull node:16.18
```
4. Tag Image
```sh
docker tag node:16.18 $ECR_NODE_URL:16.18
```
5. Push Image
```sh
docker push $ECR_NODE_URL:16.18
```
### For Frontend React
1. Create Repo
```sh
aws ecr create-repository --repository-name frontend-react-js --image-tag-mutability MUTABLE
```
2. Set URL
```sh
export ECR_FRONTEND_REACT_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/frontend-react-js"
echo $ECR_FRONTEND_REACT_URL
```
3. Build Image
```sh
docker build \
--build-arg REACT_APP_BACKEND_URL="http://127.0.0.1:4567" \
--build-arg REACT_APP_AWS_PROJECT_REGION="${AWS_REGION}" \
--build-arg REACT_APP_AWS_COGNITO_REGION="${AWS_REGION}" \
--build-arg REACT_APP_AWS_USER_POOLS_ID="${AWS_COGNITO_USER_POOL_ID}" \
--build-arg REACT_APP_CLIENT_ID="${AWS_COGNITO_USER_POOL_CLIENT_ID}" \
-t frontend-react-js \
-f Dockerfile.prod \
.
```
4. Tag Image
```sh
docker tag frontend-react-js:latest $ECR_FRONTEND_REACT_URL:latest
```
5. Push Image
```sh
docker push $ECR_FRONTEND_REACT_URL:latest
```
If you want to run and test is:
```sh
docker run --rm -p 3000:3000 -it frontend-react-js 
```
## Register Task Definitions
### Passing Sensitive Data to Task Definition
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/secrets-envvar-ssm-paramstore.html
```sh
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_ACCESS_KEY_ID" --value $AWS_ACCESS_KEY_ID
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY" --value $AWS_SECRET_ACCESS_KEY
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/CONNECTION_URL" --value $PROD_CONNECTION_URL
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN" --value $ROLLBAR_ACCESS_TOKEN
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS" --value "x-honeycomb-team=$HONEYCOMB_API_KEY"
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_COGNITO_USER_POOL_ID" --value $AWS_COGNITO_USER_POOL_ID
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_COGNITO_USER_POOL_CLIENT_ID" --value $AWS_COGNITO_USER_POOL_CLIENT_ID
```
### Create Task and Execution Roles for Task Definition
#### Create Execution Role
```sh
aws iam create-role \
    --role-name CruddurServiceExecutionRole \
    --assume-role-policy-document file://aws/policies/service-execution-policy.json
```
```sh
aws iam create-role --role-name CruddurServiceExecutionPolicy --assume-role-policy-document file://aws/policies/service-assume-role-execution-policy.json
```
```sh
aws iam put-role-policy --policy-name CruddurServiceExecutionPolicy --role-name CruddurServiceExecutionRole --policy-document file://aws/policies/service-execution-policy.json
```
```sh
aws iam attach-role-policy --policy-arn POLICY_ARN --role-name CruddurServiceExecutionRole
```
#### Create Task Role
```sh
aws iam create-role \
    --role-name CruddurTaskRole \
    --assume-role-policy-document "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[{
    \"Action\":[\"sts:AssumeRole\"],
    \"Effect\":\"Allow\",
    \"Principal\":{
      \"Service\":[\"ecs-tasks.amazonaws.com\"]
    }
  }]
}"
```
```sh
aws iam put-role-policy \
  --policy-name SSMAccessPolicy \
  --role-name CruddurTaskRole \
  --policy-document "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[{
    \"Action\":[
      \"ssmmessages:CreateControlChannel\",
      \"ssmmessages:CreateDataChannel\",
      \"ssmmessages:OpenControlChannel\",
      \"ssmmessages:OpenDataChannel\"
    ],
    \"Effect\":\"Allow\",
    \"Resource\":\"*\"
  }]
}"
```
```sh
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccess --role-name CruddurTaskRole
```
```sh
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess --role-name CruddurTaskRole
```
### Create Json file
Create task definitions `aws/task-definitions/backend-flask.json` and `aws/task-definitions/front-flask.json`
### Register Task Definitions
```sh
aws ecs register-task-definition --cli-input-json file://aws/task-definitions/backend-flask.json
```
```sh
aws ecs register-task-definition --cli-input-json file://aws/task-definitions/frontend-react-js.json
```
### Create Security Group
```sh
export CRUD_SERVICE_SG=$(aws ec2 create-security-group \
  --group-name "crud-srv-sg" \
  --description "Security group for Cruddur services on ECS" \
  --vpc-id $VPC_ID \
  --query "GroupId" --output text)
echo $CRUD_SERVICE_SG
```
```sh
aws ec2 authorize-security-group-ingress \
  --group-id $CRUD_SERVICE_SG \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0
```
> if we need to get the sg group id again
```sh
export CRUD_SERVICE_SG=$(aws ec2 describe-security-groups \
  --filters Name=group-name,Values=crud-srv-sg \
  --query 'SecurityGroups[*].GroupId' \
  --output text)
```
#### Update RDS SG to allow access for the last SG
```sh
aws ec2 authorize-security-group-ingress \
  --group-id $DB_SG_ID \
  --protocol tcp \
  --port 5432 \
  --source-group $CRUD_SERVICE_SG \
  --tag-specifications 'ResourceType=security-group,Tags=[{Key=Name,Value=BACKENDFLASK}]'
```
### Create Services
```sh
aws ecs create-service --cli-input-json file://aws/json/service-backend-flask.json
```
```sh
aws ecs create-service --cli-input-json file://aws/json/service-frontend-react-js.json
```
