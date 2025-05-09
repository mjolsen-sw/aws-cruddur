import './ProfileForm.css';
import React from "react";
import process from 'process';
import { getAccessToken } from 'lib/CheckAuth';

export default function ProfileForm(props) {
  const [bio, setBio] = React.useState("");
  const [displayName, setDisplayName] = React.useState("");

  React.useEffect(() => {
    setBio(props.profile.bio || "");
    setDisplayName(props.profile.display_name || "");
  }, [props, props.profile]);

  const s3uploadkey = async () => {
    try {
      const accessToken = await getAccessToken();
      const gateway_url = `${process.env.REACT_APP_API_GATEWAY_ENDPOINT}/avatars/key_upload`
      const res = await fetch(gateway_url, {
        method: "POST",
        headers: {
          'Origin': `${process.env.REACT_APP_FRONTEND_URL}`,
          'Authorization': `Bearer ${accessToken}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });
      let data = await res.json();
      if (res.status === 200) {
        return data;
      } else {
        console.log(res);
        return null;
      }
    } catch (err) {
      console.log(err);
    }
  }

  const s3upload = async (event) => {
    const file = event.target.files[0];
    //const preview_image_url = URL.createObjectURL(file);
    try {
      const presigned_url = await s3uploadkey();
      const backend_url = presigned_url["upload_url"];
      const res = await fetch(backend_url, {
        method: "PUT",
        headers: {
          'Content-Type': file.type || 'image/jpeg'
        },
        body: file
      });

      if (res.ok) {
        console.log("uploaded avatar");
      } else {
        console.log(res);
      }
    } catch (err) {
      console.log(err);
    }
  }

  const onsubmit = async (event) => {
    event.preventDefault();
    try {
      const accessToken = await getAccessToken();
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/profile/update`
      const res = await fetch(backend_url, {
        method: "POST",
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          bio: bio,
          display_name: displayName
        }),
      });

      if (res.ok) {
        setBio("");
        setDisplayName("");
        props.setPopped(false);
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
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
            <input type="file" name="avatarupload" onChange={s3upload} accept="image/jpeg" />
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
        </form>
      </div>
    );
  }
}