## Architecture Guid

Before you run any templates, be sure to create an S3 bucket to contain
all of our artifacts for CloudFormation.

```
aws s3 mk s3://cfn-artifacts-cruddur-molsen
export CFN_BUCKET="cfn-artifacts-cruddur-molsen"
```

> remember bucket names are unique so you may need to adjust the provided code example

