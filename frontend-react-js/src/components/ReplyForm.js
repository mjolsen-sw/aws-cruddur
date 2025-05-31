import './ReplyForm.css';
import React from "react";
import process from 'process';

import { post } from 'lib/Requests';
import ActivityContent from 'components/ActivityContent';
import FormErrors from 'components/FormErrors';

export default function ReplyForm(props) {
  const [count, setCount] = React.useState(0);
  const [message, setMessage] = React.useState('');
  const [errors, setErrors] = React.useState([]);

  const classes = [];
  classes.push('count');
  if (240 - count < 0) {
    classes.push('err');
  }

  const onsubmit = async (event) => {
    event.preventDefault();
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/${props.activity.uuid}/reply`;
    const payload_data = {
      message: message
    };
    const options = {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      auth: true,
      success: function (data) {
        // add activity to the feed
        let activities_deep_copy = JSON.parse(JSON.stringify(props.activities));
        let found_activity = activities_deep_copy.find(function (element) {
          return element.uuid === props.activity.uuid;
        });

        // ignore if replying to a reply
        if (found_activity !== undefined) {
          found_activity.reply_count += 1;
          // safeguard against replies not being returned with activity
          if (found_activity.replies !== undefined) {
            found_activity.replies.push(data);
          }
        }

        props.setActivities(activities_deep_copy);
        // reset and close the form
        setCount(0);
        setMessage('');
        setErrors([]);
        props.setPopped(false);
      },
      setErrors: setErrors
    }
    post(url, payload_data, options);
  }

  const textarea_onchange = (event) => {
    setCount(event.target.value.length);
    setMessage(event.target.value);
  }

  const close = (event) => {
    if (event.target.classList.contains("reply_popup")) {
      props.setPopped(false)
      setErrors([]);
    }
  }

  let content;
  if (props.activity) {
    content = <ActivityContent activity={props.activity} />;
  }

  if (props.popped === true) {
    return (
      <div className="popup_form_wrap reply_popup" onClick={close}>
        <div className="popup_form">
          <div className="popup_heading">
            <div className="popup_title">
              Reply to...
            </div>
          </div>
          <div className="popup_content">
            <div className="activity_wrap">
              {content}
            </div>
            <form
              className='replies_form'
              onSubmit={onsubmit}
            >
              <textarea
                type="text"
                placeholder="what is your reply?"
                value={message}
                onChange={textarea_onchange}
              />
              <div className='submit'>
                <div className={classes.join(' ')}>{240 - count}</div>
                <button type='submit'>Reply</button>
              </div>
              <FormErrors errors={errors} />
            </form>
          </div>
        </div>
      </div>
    );
  }
}