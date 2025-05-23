import './NotificationsFeedPage.css';
import React from "react";

import DesktopNavigation from 'components/DesktopNavigation';
import DesktopSidebar from 'components/DesktopSidebar';
import ActivityFeed from 'components/ActivityFeed';
import ActivityForm from 'components/ActivityForm';
import ReplyForm from 'components/ReplyForm';

import { checkAuth } from 'lib/CheckAuth';
import { get } from 'lib/Requests';

export default function NotificationsFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const loadData = async () => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/notifications`;
    const options = {
      headers: { 'Accept': 'application/json' },
      auth: true,
      success: function (data) {
        setActivities(data);
      }
    };
    get(url, options);
  };

  React.useEffect(() => {
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth(setUser);
  }, [])

  return (
    <article>
      <DesktopNavigation user={user} active={'notifications'} setPopped={setPopped} />
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
        <div className='activity_feed'>
          <div className='activity_feed_heading'>
            <div className='title'>Notifications</div>
            <ActivityFeed
              setReplyActivity={setReplyActivity}
              setPopped={setPoppedReply}
              activities={activities}
            />
          </div>
        </div>
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}