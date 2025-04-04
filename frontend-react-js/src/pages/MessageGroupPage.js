import './MessageGroupPage.css';
import React from "react";
import { useParams } from 'react-router-dom';

import DesktopNavigation from '../components/DesktopNavigation';
import MessageGroupFeed from '../components/MessageGroupFeed';
import MessagesFeed from '../components/MessageFeed';
import MessagesForm from '../components/MessageForm';

// Authenication
import { fetchAuthSession } from '@aws-amplify/auth';

export default function MessageGroupPage() {
  const [messageGroups, setMessageGroups] = React.useState([]);
  const [messages, setMessages] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const [user, setUser] = React.useState(null);
  const [accessToken, setAccessToken] = React.useState(null);
  const authFetchedRef = React.useRef(false);
  const dataFetchedRef = React.useRef(false);
  const params = useParams();

  const loadMessageGroupsData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/message_groups`
      const res = await fetch(backend_url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setMessageGroups(resJson)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  };

  const loadMessageGroupData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/messages/${params.message_group_uuid}`
      const res = await fetch(backend_url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setMessages(resJson)
      } else {
        console.log(res)
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
    //prevents double call
    if (authFetchedRef.current) return;
    authFetchedRef.current = true;

    checkAuth();
  }, [])

  React.useEffect(() => {
    if (accessToken) {
      if (dataFetchedRef.current) return;
      dataFetchedRef.current = true;
      loadMessageGroupsData();
      loadMessageGroupData();
    }
  }, [accessToken]);

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <section className='message_groups'>
        <MessageGroupFeed message_groups={messageGroups} />
      </section>
      <div className='content messages'>
        <MessagesFeed messages={messages} />
        <MessagesForm setMessages={setMessages} accessToken={accessToken} />
      </div>
    </article>
  );
}