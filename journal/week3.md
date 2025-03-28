# Week 3 — Decentralized Authentication
## Amplify
### Installation
```sh
npm i aws-amplify --save
```

### Configuration
Hook up cognito pool to our code in `App.js`:
```javascript
import { Amplify } from 'aws-amplify';

Amplify.configure({
  "aws_project_region": process.env.REACT_AWS_PROJECT_REGION,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID
});
```
Add to frontend-react-js environment variables in `docker-compose.yml`:
```sh
      REACT_APP_AWS_PROJECT_REGION: "${AWS_REGION}"
      REACT_APP_AWS_COGNITO_REGION: "${AWS_REGION}"
      REACT_APP_AWS_USER_POOLS_ID: "us-west-1_B66HPLQ2x"
      REACT_APP_CLIENT_ID: "4t2c29mn8j9394g1ce0amjdb42"
```

### Usage
For pages that are querying the backend for data, you'll generally need the following:
```javascript
import { fetchAuthSession } from '@aws-amplify/auth';

  const [accessToken, setAccessToken] = React.useState(null);
  const authFetchedRef = React.useRef(false);

    const checkAuth = async () => {
    fetchAuthSession()
      .then(session => {
        if (session.tokens) {
          setUser({
            display_name: session.tokens.idToken.payload.name,
            handle: session.tokens.idToken.payload.preferred_username
          });
          setAccessToken(session.tokens?.accessToken?.toString());
        }
        else {
          setAccessToken("");
        }
      })
      .catch(err => console.log(err));
  };

  React.useEffect(() => {
    if (authFetchedRef.current) return;
    authFetchedRef.current = true;

    checkAuth();
  }, []);

  React.useEffect(() => {
    if (accessToken) {
      if (dataFetchedRef.current) return;
      dataFetchedRef.current = true;
      // call whatever function(s) load data from backend using accessToken
      loadData();
    }
  }, [accessToken]);
```
For `ConfirmationPage.js`:
```javascript
import { confirmSignUp, resendSignUpCode } from '@aws-amplify/auth';

  const [cognitoErrors, setCognitoErrors] = React.useState('');

  const resend_code = async (event) => {
    setCognitoErrors('')
    try {
      await resendSignUpCode({ username: email });
      console.log('code resent successfully');
      setCodeSent(true)
    } catch (err) {
      // does not return a code
      // does cognito always return english
      // for this to be an okay match?
      console.log(err)
      if (err.message == 'username is required to signUp') {
        setCognitoErrors("You need to provide an email in order to send Resend Activiation Code")
      } else if (err.message == "Username/client id combination not found.") {
        setCognitoErrors("Email is invalid or cannot be found.")
      }
    }
  }

  const onsubmit = async (event) => {
    event.preventDefault();
    setCognitoErrors('')
    try {
      await confirmSignUp({
        username: email,
        confirmationCode: code
      });
      window.location.href = "/signin"
    } catch (error) {
      setCognitoErrors(error.message)
    }
    return false
  }
```
For `RecoverPage.js`:
```javascript
import { resetPassword, confirmResetPassword } from '@aws-amplify/auth';

  const onsubmit_send_code = async (event) => {
    event.preventDefault();
    setCognitoErrors('')
    resetPassword({ username })
      .then((data) => setFormState('confirm_code'))
      .catch((err) => setCognitoErrors(err.message));
    return false
  }

  const onsubmit_confirm_code = async (event) => {
    event.preventDefault();
    setCognitoErrors('')
    if (password == passwordAgain) {
      confirmResetPassword({
        username,
        confirmationCode: code,
        newPassword: password
      })
        .then((data) => setFormState('success'))
        .catch((err) => setCognitoErrors(err.message));
    } else {
      setCognitoErrors('Passwords do not match')
    }
    return false
  }
```
For `SigninPage.js`:
```javascript
import { signIn } from '@aws-amplify/auth';

  const onsubmit = async (event) => {
    setCognitoErrors('')
    event.preventDefault();
    try {
      const { nextStep } = await signIn({
        username: email,
        password: password
      })

      if (nextStep.signInStep === "DONE") {
        window.location.href = "/"
      }
      else if (nextStep.signInStep === "CONFIRM_SIGN_UP") {
        window.location.href = "/confirm"
      }
    } catch (error) {
      setCognitoErrors(error.message)
    }
    return false
  }
```
For `SignupPage.js`:
```javascript
import { signUp } from '@aws-amplify/auth';

  const onsubmit = async (event) => {
    event.preventDefault();
    setCognitoErrors('')
    try {
      const { user } = await signUp({
        username: email,
        password,
        options: {
          userAttributes: {
            preferred_username: username,
            name,
            email,
          },
        },
        autoSignIn: { // optional - enables auto sign in after user is confirmed
          enabled: true,
        }
      });
      console.log(user);
      window.location.href = `/confirm?email=${email}`
    } catch (error) {
      console.log(error);
      setCognitoErrors(error.message)
    }
    return false
  }
```