import './SigninPage.css';
import React from "react";
import { ReactComponent as Logo } from 'components/svg/logo.svg';
import { Link } from "react-router-dom";

import { signIn } from '@aws-amplify/auth';

import FormErrors from 'components/FormErrors';

export default function SigninPage() {

  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [errors, setErrors] = React.useState('');

  const onsubmit = async (event) => {
    event.preventDefault();
    setErrors([]);
    try {
      const { nextStep } = await signIn({
        username: email,
        password: password
      });

      if (nextStep.signInStep === "DONE") {
        window.location.href = "/";
      }
      else if (nextStep.signInStep === "CONFIRM_SIGN_UP") {
        window.location.href = "/confirm";
      }
    } catch (error) {
      setErrors([error.message]);
    }
    return false;
  }

  const email_onchange = (event) => {
    setEmail(event.target.value);
  }

  const password_onchange = (event) => {
    setPassword(event.target.value);
  }

  return (
    <article className="signin-article">
      <div className='signin-info'>
        <Logo className='logo' />
      </div>
      <div className='signin-wrapper'>
        <form
          className='signin_form'
          onSubmit={onsubmit}
        >
          <h2>Sign into your Cruddur account</h2>
          <div className='fields'>
            <div className='field text_field username'>
              <label>Email</label>
              <input
                type="text"
                value={email}
                onChange={email_onchange}
              />
            </div>
            <div className='field text_field password'>
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={password_onchange}
              />
            </div>
          </div>
          <div className='submit'>
            <Link to="/forgot" className="forgot-link">Forgot Password?</Link>
            <button type='submit'>Sign In</button>
          </div>
          <FormErrors errors={errors} />
        </form>
        <div className="dont-have-an-account">
          <span>
            Don't have an account?
          </span>
          <Link to="/signup">Sign up!</Link>
        </div>
      </div>
    </article>
  );
}