import { ReactComponent as ShareIcon } from './svg/share.svg';

export default function ActivityActionRepost(props) {
  const onclick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('trigger share');
    return false;
  }

  return (
    <div onClick={onclick} className="action activity_action_share">
      <ShareIcon className='icon' />
    </div>
  )
}