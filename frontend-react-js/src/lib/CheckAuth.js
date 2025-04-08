import { fetchAuthSession } from '@aws-amplify/auth';

const checkAuth = async (setUser, setAccessToken) => {
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

export default checkAuth;