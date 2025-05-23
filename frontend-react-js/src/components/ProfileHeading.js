import './ProfileHeading.css';
import EditProfileButton from 'components/EditProfileButton';
import ProfileAvatar from 'components/ProfileAvatar';

export default function ProfileHeading(props) {
  const backgroundImage = 'url("https://assets.cruddur.molsen.dev/banners/banner.jpg")';
  const styles = {
    backgroundImage: backgroundImage,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
  };

  return (
    <div className='activity_feed_heading profile_heading'>
      <div className="banner" style={styles} >
        <ProfileAvatar user={props.profile} />
      </div>
      <div className="info">
        <div className='id'>
          <div className="display_name">{props.profile.display_name}</div>
          <div className="handle">@{props.profile.handle}</div>
          <div className="cruds_count">{props.profile.cruds_count} Cruds</div>
        </div>
        {(props.user && props.profile && props.user.handle === props.profile.handle) && <EditProfileButton setPopped={props.setPopped} />}
      </div>
      <div className="bio">{props.profile.bio}</div>

    </div>
  );
}