import './DesktopSidebar.css';
import Search from 'components/Search';
import TrendingSection from 'components/TrendingsSection'
import SuggestedUsersSection from 'components/SuggestedUsersSection'
import JoinSection from 'components/JoinSection'

export default function DesktopSidebar(props) {
  const trendings = [
    { "hashtag": "100DaysOfCloud", "count": 2053 },
    { "hashtag": "CloudProject", "count": 8253 },
    { "hashtag": "AWS", "count": 9053 },
    { "hashtag": "FreeWillyReboot", "count": 7753 }
  ]

  const users = [
    { "display_name": "Matt", "handle": "calm" }
  ]

  let trending;
  let suggested;
  let join;
  if (props.user) {
    trending = <TrendingSection trendings={trendings} />
    suggested = <SuggestedUsersSection users={users} />
  } else {
    join = <JoinSection />
  }

  return (
    <section>
      <Search search={props.search} setSearch={props.setSearch} />
      {trending}
      {suggested}
      {join}
      <footer>
        <a href="/about">About</a>
        <a href="/terms-of-service">Terms of Service</a>
        <a href="/privacy-policy">Privacy Policy</a>
      </footer>
    </section>
  );
}