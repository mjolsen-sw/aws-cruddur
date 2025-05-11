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