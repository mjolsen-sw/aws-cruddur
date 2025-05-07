# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy
## Backend
Added `backend-flask/buildspec.yml` to bake image for CI/CD pipeline.
### CodePipeline Service Role Permissions
CodePipeline will need the additional permissions from `aws/codepipeline/service-role-codebuild-permissions.json` in order to run the Bake Image project in the pipeline.
### Bake Image
In CodeBuild, we need to build a project to make the flask docker container.
#### Build Project
- Name something like 'cruddur-backend-flask-bake-image'
- `Project Type` of 'Default project'
- Use GitHub as the `Source provider`
- Select the reposity and use `prod` for the 'Source version'
- Check `Rebuild every time a code change is pushed to this repository`
- In `Webhook event filter groups`, for `Event type` use 'PULL_REQUEST_MERGED'
- Use the following under `Environment`:
-- `Environment image`: Managed image
-- `Running mode`: Container
-- `Operating system`: Amazon Linux
-- `Runtime`: Standard
-- `Image`: the lastest (i.e. aws/codebuild/amazonlinux-x86_64-standard:5.0)
-- `Image version`: 'Always use the latest image for this runtime version'
- Under `Additional configuration`, check the `Privileged` box.
- Select the lowest `Compute`: 2 vCPUs, 4 GiB memory
- Under `Buildspec`:
-- Use a buildspec file
-- backend-flask/buildspec.yml
#### Execution Role ECR Permissions
Add an inline policy to the bake-image-service-role using `aws/codebuild/execution-role-ecr-permissions.json`