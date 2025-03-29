import './HomeFeedPage.css';
import React from "react";

import DesktopNavigation from '../components/DesktopNavigation';
import DesktopSidebar from '../components/DesktopSidebar';
import ActivityFeed from '../components/ActivityFeed';
import ActivityForm from '../components/ActivityForm';
import ReplyForm from '../components/ReplyForm';

// Authenication
import { fetchAuthSession } from '@aws-amplify/auth';

export default function HomeFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const [accessToken, setAccessToken] = React.useState(null);
  const authFetchedRef = React.useRef(false);
  const dataFetchedRef = React.useRef(false);

  const loadData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/home`
      let init = { method: "GET" };
      if (accessToken)
        init.headers = { Authorization: `Bearer ${accessToken}` };
      const res = await fetch(backend_url, init);
      let resJson = await res.json();
      if (res.status === 200) {
        setActivities(resJson);
      } else {
        console.log(res);
      }
    } catch (err) {
      console.log(err);
    }
  };

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
    if (accessToken != null) {
      if (dataFetchedRef.current) return;
      dataFetchedRef.current = true;
      loadData();
    }
  }, [accessToken, loadData]);

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm
          popped={popped}
          setPopped={setPopped}
          setActivities={setActivities}
        />
        <ReplyForm
          activity={replyActivity}
          popped={poppedReply}
          setPopped={setPoppedReply}
          setActivities={setActivities}
          activities={activities}
        />
        <ActivityFeed
          title="Home"
          setReplyActivity={setReplyActivity}
          setPopped={setPoppedReply}
          activities={activities}
        />
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}