import './ConfirmationPage.css';
import React from "react";
import { useSearchParams } from 'react-router-dom';
import { ReactComponent as Logo } from 'components/svg/logo.svg';

import { confirmSignUp, resendSignUpCode } from '@aws-amplify/auth';

export default function ConfirmationPage() {
  const [email, setEmail] = React.useState('');
  const [code, setCode] = React.useState('');
  const [cognitoErrors, setCognitoErrors] = React.useState('');
  const [codeSent, setCodeSent] = React.useState(false);
  const [searchParams] = useSearchParams();

  const code_onchange = (event) => {
    setCode(event.target.value);
  }
  const email_onchange = (event) => {
    setEmail(event.target.value);
  }

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
      if (err.message === 'username is required to signUp') {
        setCognitoErrors("You need to provide an email in order to send Resend Activiation Code")
      } else if (err.message === "Username/client id combination not found.") {
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

  let errors;
  if (cognitoErrors) {
    errors = <div className='errors'>{cognitoErrors}</div>;
  }


  let code_button;
  if (codeSent) {
    code_button = <div className="sent-message">A new activation code has been sent to your email</div>
  } else {
    code_button = <button className="resend" onClick={resend_code}>Resend Activation Code</button>;
  }

  React.useEffect(() => {
    const email = searchParams.get("email")
    if (email) {
      setEmail(email)
    }
  }, [searchParams])

  return (
    <article className="confirm-article">
      <div className='recover-info'>
        <Logo className='logo' />
      </div>
      <div className='recover-wrapper'>
        <form
          className='confirm_form'
          onSubmit={onsubmit}
        >
          <h2>Confirm your Email</h2>
          <div className='fields'>
            <div className='field text_field email'>
              <label>Email</label>
              <input
                type="text"
                value={email}
                onChange={email_onchange}
              />
            </div>
            <div className='field text_field code'>
              <label>Confirmation Code</label>
              <input
                type="text"
                value={code}
                onChange={code_onchange}
              />
            </div>
          </div>
          {errors}
          <div className='submit'>
            <button type='submit'>Confirm Email</button>
          </div>
        </form>
      </div>
      {code_button}
    </article>
  );
}