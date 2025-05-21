import './UserFeedPage.css';
import React from "react";
import { useParams } from 'react-router-dom';

import DesktopNavigation from 'components/DesktopNavigation';
import DesktopSidebar from 'components/DesktopSidebar';
import ActivityFeed from 'components/ActivityFeed';
import ActivityForm from 'components/ActivityForm';
import ProfileHeading from 'components/ProfileHeading';
import ProfileForm from 'components/ProfileForm';
import ReplyForm from 'components/ReplyForm';

import { checkAuth } from 'lib/CheckAuth';
import { get } from 'lib/Requests';

export default function UserFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [profile, setProfile] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const [poppedProfile, setPoppedProfile] = React.useState([]);
  const [poppedReply, setPoppedReply] = React.useState([]);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);
  const userFetchedRef = React.useRef(false);

  const params = useParams();

  const loadData = async () => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/@${params.handle}`;
    const options = {
      headers: { 'Accept': 'application/json' },
      auth: true,
      success: function (data) {
        setActivities(data.activities);
        setProfile(data.profile);
      }
    };
    get(url, options);
  };

  React.useEffect(() => {
    if (!user) return;

    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
  }, [user])

  React.useEffect(() => {
    //prevents double call
    if (userFetchedRef.current) return;
    userFetchedRef.current = true;

    checkAuth(setUser);
  }, [])

  return (
    <article>
      <DesktopNavigation user={user} active={'profile'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm popped={popped} setActivities={setActivities} />
        <ProfileForm
          profile={profile}
          popped={poppedProfile}
          setPopped={setPoppedProfile}
        />
        <ReplyForm
          activity={replyActivity}
          popped={poppedReply}
          setPopped={setPoppedReply}
          setActivities={setActivities}
          activities={activities}
        />
        <div className='activity_feed'>
          <ProfileHeading
            setPopped={setPoppedProfile}
            profile={profile}
            user={user}
          />
          <ActivityFeed
            activities={activities}
            setReplyActivity={setReplyActivity}
            setPopped={setPoppedReply}
          />
        </div>
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}