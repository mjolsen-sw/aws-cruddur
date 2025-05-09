import './MessageGroupItem.css';
import { Link } from "react-router-dom";

import ProfileAvatar from 'components/ProfileAvatar';

export default function MessageGroupNewItem(props) {
  return (

    <Link className='message_group_item active' to={`/messages/new/` + props.user.handle}>
      <ProfileAvatar user={props.user} />
      <div className='message_content'>
        <div className='message_group_meta'>
          <div className='message_group_identity'>
            <div className='display_name'>{props.user.display_name}</div>
            <div className="handle">@{props.user.handle}</div>
          </div>{/* activity_identity */}
        </div>{/* message_meta */}
      </div>{/* message_content */}
    </Link>
  );
}