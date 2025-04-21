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
