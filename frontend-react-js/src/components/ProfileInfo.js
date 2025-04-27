import './ProfileInfo.css';
import { ReactComponent as ElipsesIcon } from './svg/elipses.svg';
import React from "react";

import ProfileAvatar from 'components/ProfileAvatar'

import { signOut } from '@aws-amplify/auth';

export default function ProfileInfo(props) {
  const [popped, setPopped] = React.useState(false);

  const click_pop = (event) => {
    setPopped(!popped)
  }

  const sign_out = async () => {
    try {
      await signOut({ global: true });
      window.location.href = "/"
    } catch (error) {
      console.log('error signing out: ', error);
    }
  }

  const classes = () => {
    let classes = ["profile-info-wrapper"];
    if (popped === true) {
      classes.push('popped');
    }
    return classes.join(' ');
  }

  return (
    <div className={classes()}>
      <div className="profile-dialog">
        <button onClick={sign_out}>Sign Out</button>
      </div>
      <div className="profile-info" onClick={click_pop}>
        <ProfileAvatar user={props.user} />
        <div className="profile-desc">
          <div className="profile-display-name">{props.user.display_name || "My Name"}</div>
          <div className="profile-username">@{props.user.handle || "handle"}</div>
        </div>
        <ElipsesIcon className='icon' />
      </div>
    </div>
  )
}