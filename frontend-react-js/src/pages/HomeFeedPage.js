import './HomeFeedPage.css';
import React from "react";

import DesktopNavigation from 'components/DesktopNavigation';
import DesktopSidebar from 'components/DesktopSidebar';
import ActivityFeed from 'components/ActivityFeed';
import ActivityForm from 'components/ActivityForm';
import ReplyForm from 'components/ReplyForm';

import { checkAuth } from 'lib/CheckAuth';
import { get } from 'lib/Requests';
import { searchActivities } from 'lib/SearchActivities';

export default function HomeFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [search, setSearch] = React.useState('');
  const [searchedActivities, setSearchedActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const loadData = async () => {
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/home`;
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
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth(setUser);
  }, []);

  React.useEffect(() => {
    if (search) {
      const results = searchActivities(activities, search);
      setSearchedActivities(results);
    } else {
      setSearchedActivities(activities);
    }
  }, [search, activities]);

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
          activities={searchedActivities}
        />
        <ActivityFeed
          title="Home"
          setReplyActivity={setReplyActivity}
          setPopped={setPoppedReply}
          activities={searchedActivities}
        />
      </div>
      <DesktopSidebar user={user} search={search} setSearch={setSearch} />
    </article>
  );
}