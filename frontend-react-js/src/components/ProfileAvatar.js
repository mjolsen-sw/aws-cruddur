import React, { useEffect, useState } from 'react';

import './ProfileAvatar.css';

export default function ProfileAvatar(props) {
  const handle = props.user.handle;
  const [avatarUrl, setAvatarUrl] = useState(`https://assets.cruddur.molsen.dev/avatars/${handle}.jpg`);

  const handleError = () => {
    setAvatarUrl("https://assets.cruddur.molsen.dev/avatars/default-avatar-icon.jpg")
  }

  useEffect(() => {
    if (handle) {
      setAvatarUrl(`https://assets.cruddur.molsen.dev/avatars/${handle}.jpg`);
    }
  }, [handle])

  return (
    <img
      className="profile-avatar"
      src={avatarUrl}
      alt="User Avatar"
      onError={handleError}
    />
  );
}