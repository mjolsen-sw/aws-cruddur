# Week 8 — Serverless Image Processing
Our cdk pipline is in `/thumbing-servless-cdk`
## Install CDK globally
```sh
npm install aws-cdk -g
```
## Initialize a new project
```sh
cdk init app --language typescript
```
## Add an S3 Bucket
Add the following code to `thumbing-serverless-cdk-stack.ts`
```sh
import * as s3 from 'aws-cdk-lib/aws-s3';

const bucketName: string = process.env.THUMBING_BUCKET_NAME as string;

const bucket = new s3.Bucket(this, 'ThumbingBucket', {
  bucketName: bucketName,
  removalPolicy: cdk.RemovalPolicy.DESTROY,
});
```
## Bootstrap with the AWS CDK Toolkit
Bootstrap the CDK to the region(s) you are using
```sh
cdk bootstrap "aws://${AWS_ACCOUNT}/${AWS_REGION}"
cdk bootstrap "${AWS_ACCOUNT}/us-east-1" "${AWS_ACCOUNT}/us-west-1"
```
## Build
We can use build to catch errors prematurely. This just builds typescript
```sh
npm run build
```
## Synth
The synth command is used to synthesize AWS Cloudformation stack(s) that represent your IaC
```sh
cdk synth
```
## Deploy
```sh
cdk deploy
```
## List Stacks
```sh
cdk ls
```

# S3 Presigned URL generation and upload
## Upload Bucket (i.e. 'assets.cruddur.molsen.dev') - Bucket Policy
We need a Bucket Policy such as `aws/s3/upload-bucket-bucket-policy.json`.
The principal needs to be the CruddurAvatarUploadUrl execution role.
## Upload Bucket (i.e. 'assets.cruddur.molsen.dev') - CORS Policy
We also need to add a CORS Policy such as `aws/s3/upload-bucket-cors-policy.json`.
It should at least allow the origin of the frontend application.
## SSM Endpoint
Our lambda generating the S3 upload url will be deployed in our VPC to access the db.
We need to create an SSM endpoint in the VPC so our lambda can grab from Parameter Store.
Add the lambda's security group to its security group's inbound rules.
## API Gateway
Create the API Gateway and make a route for `avatars/key_upload` POST.
This will be set to trigger the S3 presigned url lambda using the lambda-authorizer.
### CORS
Set the following under the CORS tab
#### Access-Control-Allow-Origin
The frontend application url (or http://127.0.0.1:3000 for testing)
#### Access-Control-Allow-Headers
- content-type
- authorization
#### Access-Control-Allow-Methods
- OPTIONS
- POST
#### Access-Control-Expose-Headers
expose_headers='authorization',
#### Access-Control-Allow-Credentials
YES
### Authorization
#### Lambda
Add `aws/lambdas/lambda-authorizer` as lambda function.
It needs access to SSM to retrieve the Cognito user pool id and client id.
#### Create the authorizer
- In the `Authorization` section, click the `Manage authorizers` tab.
- Click `Create`
- Enter a name and select the lambda function from above.
- Set `Response mode` to `IAM Policy`
- Set `Identity Sources` to $request.header.Authorization
- Automatically grant API Gateway permission to invoke your Lambda function
- Click `Create`
### Lambda - S3 Upload URL Generator
Add `aws/lambda/upload-avatar` as a function.
It will need to be deployed in the VPC to be able to connect to the database.
#### Lambda Layer
Use the psycopg2 lambda layer that was generated before.
#### Permissions
- SSM /cruddur/backend-flask/CONNECTION_URL to be able to retrieve handles from db.
The following EC2 permissions are required to run the lambda in the VPC:
- Allow: ec2:CreateNetworkInterface
- Allow: ec2:DescribeNetworkInterfaces
- Allow: ec2:DeleteNetworkInterface
#### Security Group
Make sure to add the following to outbound rules:
- DB security group on the correct port (5432 be default)
- SSM Endpoint security group on HTTPS (port 443)
#### Routes
- In the API Gateway, select `Routes` on the left.
- Select `POST` and `/avatars/keyupload` respectively
- Attach the Authorizer by clicking `Attach authorizer`
- Attach the URL generating lambda by clicking `Attach integration`
-- `Integration type` is 'Lambda Function'
-- Select the create lambda function (created from `upload-avatar`)
-- Grant API Gateway permission to invoke your Lambda function