import { fetchAuthSession } from '@aws-amplify/auth';

const checkAuth = async (setUser) => {
  try {
    const session = await fetchAuthSession();
    if (session.tokens) {
      setUser({
        display_name: session.tokens.idToken.payload.name,
        handle: session.tokens.idToken.payload.preferred_username
      });
    }
  } catch (err) {
    console.log(err);
  }
};

const getAccessToken = async () => {
  try {
    const session = await fetchAuthSession();
    if (session.tokens) {
      return session.tokens.accessToken.toString();
    }
  } catch (err) {
    console.log(err)
  }

}

export { checkAuth, getAccessToken };