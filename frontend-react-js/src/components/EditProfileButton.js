import './EditProfileButton.css';

export default function EditProfileButton(props) {
  const pop_profile_form = (event) => {
    event.preventDefault();
    console.log('pop profile form');
    props.setPopped(true);
    return false;
  }

  return (
    <button onClick={pop_profile_form} className='profile_edit_button'>Edit Profile</button>
  );
}