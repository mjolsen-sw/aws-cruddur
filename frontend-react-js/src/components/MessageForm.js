import './MessageForm.css';
import React from "react";
import process from 'process';
import { useParams } from 'react-router-dom';

import { post } from 'lib/Requests';
import FormErrors from 'components/FormErrors';

export default function ActivityForm(props) {
  const [count, setCount] = React.useState(0);
  const [message, setMessage] = React.useState('');
  const [errors, setErrors] = React.useState([]);
  const params = useParams();

  const classes = [];
  classes.push('count');
  if (1024 - count < 0) {
    classes.push('err');
  }

  const onsubmit = async (event) => {
    event.preventDefault();
    const url = `${process.env.REACT_APP_BACKEND_URL}/api/messages`;
    const payload_data = { message: message };
    if (params.handle) {
      payload_data.handle = params.handle;
    } else {
      payload_data.message_group_uuid = params.message_group_uuid;
    }
    const options = {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      auth: true,
      success: function (data) {
        setErrors([]);
        if (data.message_group_uuid) {
          window.location.href = `/messages/${data.message_group_uuid}`;
        } else {
          props.setMessages(current => [...current, data]);
        }
      },
      setErrors: setErrors
    }
    post(url, payload_data, options);
  }

  const textarea_onchange = (event) => {
    setCount(event.target.value.length);
    setMessage(event.target.value);
  }

  return (
    <form
      className='message_form'
      onSubmit={onsubmit}
    >
      <textarea
        type="text"
        placeholder="send a direct message..."
        value={message}
        onChange={textarea_onchange}
      />
      <div className='submit'>
        <div className={classes.join(' ')}>{1024 - count}</div>
        <button type='submit'>Message</button>
      </div>
      <FormErrors errors={errors} />
    </form>
  );
}