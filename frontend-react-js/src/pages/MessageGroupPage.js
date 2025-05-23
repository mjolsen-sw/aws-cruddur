import './MessageGroupPage.css';
import React from "react";
import { useParams } from 'react-router-dom';

import DesktopNavigation from 'components/DesktopNavigation';
import MessageGroupFeed from 'components/MessageGroupFeed';
import MessagesFeed from 'components/MessageFeed';
import MessagesForm from 'components/MessageForm';

import { checkAuth } from 'lib/CheckAuth';
import { get } from 'lib/Requests';

export default function MessageGroupPage() {
  const [messageGroups, setMessageGroups] = React.useState([]);
  const [messages, setMessages] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);
  const params = useParams();

  const loadMessageGroupsData = async () => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/messages/groups`;
    const options = {
      headers: { 'Accept': 'application/json' },
      auth: true,
      success: function (data) {
        setMessageGroups(data);
      }
    };
    get(url, options);
  };

  React.useEffect(() => {
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadMessageGroupsData();
    checkAuth(setUser);
  }, []);

  React.useEffect(() => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/messages/${params.message_group_uuid}`;
    const options = {
      headers: { 'Accept': 'application/json' },
      auth: true,
      success: function (data) {
        setMessages(data);
      }
    };
    get(url, options);
  }, [params.message_group_uuid]);

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <section className='message_groups'>
        <MessageGroupFeed message_groups={messageGroups} />
      </section>
      <div className='content messages'>
        <MessagesFeed messages={messages} />
        <MessagesForm setMessages={setMessages} />
      </div>
    </article>
  );
}