import './MessageGroupsPage.css';
import React from "react";

import DesktopNavigation from 'components/DesktopNavigation';
import MessageGroupFeed from 'components/MessageGroupFeed';

import { checkAuth } from 'lib/CheckAuth';
import { get } from 'lib/Requests';

export default function MessageGroupsPage() {
  const [messageGroups, setMessageGroups] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const loadData = async () => {
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

    checkAuth(setUser);
    loadData();
  }, [])

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <section className='message_groups'>
        <MessageGroupFeed message_groups={messageGroups} />
      </section>
      <div className='content'>
      </div>
    </article>
  );
}