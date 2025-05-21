import './ActivityShowPage.css';
import React from "react";
import { useNavigate, useParams } from 'react-router-dom';

import DesktopNavigation from 'components/DesktopNavigation';
import DesktopSidebar from 'components/DesktopSidebar';
import ActivityFeed from 'components/ActivityFeed';
import ActivityForm from 'components/ActivityForm';
import ReplyForm from 'components/ReplyForm';

import { checkAuth } from 'lib/CheckAuth';
import { get } from 'lib/Requests';

export default function ActivityShowPage() {
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const params = useParams();
  const navigate = useNavigate();

  React.useEffect(() => {
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    checkAuth(setUser);
  }, []);

  React.useEffect(() => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/${params.activity_uuid}`;
    const options = {
      headers: { 'Accept': 'application/json' },
      auth: true,
      success: function (data) {
        setActivities(data);
      }
    };
    get(url, options);
  }, [params.activity_uuid]);

  return (
    <article>
      <DesktopNavigation user={user} active={'show'} setPopped={setPopped} />
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
        <div className="back" onClick={() => navigate(-1)}>&larr;</div>
        <ActivityFeed
          title="Show"
          setReplyActivity={setReplyActivity}
          setPopped={setPoppedReply}
          activities={activities}
        />
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}