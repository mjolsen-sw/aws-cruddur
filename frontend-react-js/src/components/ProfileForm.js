import './ProfileForm.css';
import React from "react";
import process from 'process';

import { post, put } from 'lib/Requests';
import FormErrors from 'components/FormErrors';

export default function ProfileForm(props) {
  const [bio, setBio] = React.useState("");
  const [displayName, setDisplayName] = React.useState("");
  const [errors, setErrors] = React.useState([]);

  React.useEffect(() => {
    setBio(props.profile.bio || "");
    setDisplayName(props.profile.display_name || "");
  }, [props, props.profile]);

  const s3uploadkey = async () => {
    const url = `${process.env.REACT_APP_API_GATEWAY_ENDPOINT}/avatars/key_upload`
    const options = {
      headers: {
        'Origin': `${process.env.REACT_APP_FRONTEND_URL}`,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      auth: true,
      success: function (data) {
        return data;
      },
      returnOnError: null
    }
    return post(url, null, options);
  }

  const s3upload = async (event) => {
    const presigned_url = await s3uploadkey();
    const url = presigned_url["upload_url"];
    const payload_data = event.target.files[0];
    const options = {
      headers: {
        'Content-Type': payload_data.type || 'image/jpeg'
      },
      auth: false,
      success: function (data) {
        console.log("uploaded avatar");
      },
      setErrors: setErrors
    }
    put(url, payload_data, options);
  }

  const onsubmit = async (event) => {
    event.preventDefault();
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/profile/update`;
    const payload_data = {
      bio: bio,
      display_name: displayName
    };
    const options = {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      auth: true,
      success: function (data) {
        window.location.reload();
      },
      setErrors: setErrors
    }
    post(url, payload_data, options);
  }

  const bio_onchange = (event) => {
    setBio(event.target.value);
  }

  const display_name_onchange = (event) => {
    setDisplayName(event.target.value);
  }

  const close = (event) => {
    if (event.target.classList.contains("profile_popup")) {
      props.setPopped(false)
    }
  }

  if (props.popped === true) {
    return (
      <div className="popup_form_wrap profile_popup" onClick={close}>
        <form
          className='profile_form popup_form'
          onSubmit={onsubmit}
        >
          <div className="popup_heading">
            <div className="popup_title">Edit Profile</div>
            <div className='submit'>
              <button type='submit'>Save</button>
            </div>
          </div>
          <div className="popup_content">
            <div className="field upload_avatar">
              <label>Upload Avatar</label>
              <input type="file" name="avatarupload" onChange={s3upload} accept="image/jpeg" />
            </div>
            <div className="field display_name">
              <label>Display Name</label>
              <input
                type="text"
                placeholder="Display Name"
                value={displayName}
                onChange={display_name_onchange}
              />
            </div>
            <div className="field bio">
              <label>Bio</label>
              <textarea
                placeholder="Bio"
                value={bio}
                onChange={bio_onchange}
              />
            </div>
          </div>
          <FormErrors errors={errors} />
        </form>
      </div>
    );
  }
}