import { getAccessToken } from 'lib/CheckAuth';

async function request(method, url, payload_data, options, with_return = false) {
  try {
    const attrs = {
      method: method,
      headers: options.headers
    };

    if (options.hasOwnProperty('auth') && options.auth === true) {
      const accessToken = await getAccessToken();
      attrs.headers['Authorization'] = `Bearer ${accessToken}`;
    }

    if (payload_data) {
      if (attrs.headers['Content-Type'] === 'application/json') {
        attrs.body = JSON.stringify(payload_data);
      } else {
        attrs.body = payload_data;
      }
    }

    const res = await fetch(url, attrs)
    let data;
    if (attrs.headers['Accept'] === 'application/json') {
      try {
        data = await res.json();
      } catch (err) {
        console.error('Failed to parse JSON:', err);
        data = null;
      }
    } else {
      data = await res.text();
    }

    if (res.ok) {
      if (options.hasOwnProperty('setErrors')) {
        options.setErrors([]);
      }
      if (with_return) {
        return options.success(data);
      } else {
        options.success(data);
      }
    } else {
      if (options.hasOwnProperty('setErrors')) {
        options.setErrors(data);
      }
      if (with_return) {
        return options.returnOnError;
      }
    }
  } catch (err) {
    if (options.hasOwnProperty('setErrors')) {
      options.setErrors([err.message]);
    }
    if (with_return) {
      return options.returnOnError;
    }
  }
}

export function post(url, payload_data, options) {
  if (options.hasOwnProperty('returnOnError')) {
    return request('POST', url, payload_data, options, true);
  } else {
    request('POST', url, payload_data, options);
  }
}

export function put(url, payload_data, options) {
  if (options.hasOwnProperty('returnOnError')) {
    return request('PUT', url, payload_data, options, true);
  } else {
    request('PUT', url, payload_data, options);
  }
}

export function get(url, options) {
  if (options.hasOwnProperty('returnOnError')) {
    return request('GET', url, null, options, true);
  } else {
    request('GET', url, null, options);
  }
}

export function destroy(url, payload_data, options) {
  request('DELETE', url, payload_data, options);
}