# Week 12 — Modern APIs
## S3 website sync
Added script to update S3 bucket and invalidate CloudFront cache
### Requirements
Required install:
```sh
gem install dotenv
gem install aws_s3_website_sync
```
Updated `bin/frontend/generate-env` to generate sync.env file which is required to run sync command
### How to run
```sh
bin/frontend/generate-env
bin/frontend/static-build
bin/frontend/sync
```
## Github Actions
Added `.github/workflows/sync.yaml`
You must add the following to your GitHub Repository Secrets:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- AWS_COGNITO_USER_POOL_ID
- AWS_COGNITO_USER_POOL_CLIENT_ID
### To Be Potentially Implemented
Potentially implement OIDC provider for GitHub Actions instead of providing credentials directly.
```
aws/cfn/sync/sync.yaml
aws/cfn/sync/config.toml
bin/cfn/sync
```