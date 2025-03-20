# Week 3 — Decentralized Authentication
## Amplify
### Installation
```sh
npm i aws-amplify --save
```

### Configuration
Hook up cognito pool to our code in **App.js**:
```javascript
import { Amplify } from 'aws-amplify';

Amplify.configure({
  "aws_project_region": process.env.REACT_AWS_PROJECT_REGION,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID
});
```
Add to frontend-react-js environment variables in docker-compose.yml:
```sh
      REACT_APP_AWS_PROJECT_REGION: "${AWS_REGION}"
      REACT_APP_AWS_COGNITO_REGION: "${AWS_REGION}"
      REACT_APP_AWS_USER_POOLS_ID: "us-west-1_B66HPLQ2x"
      REACT_APP_CLIENT_ID: "4t2c29mn8j9394g1ce0amjdb42"
```

