import './App.css';
import './components/Popup.css';

import HomeFeedPage from 'pages/HomeFeedPage';
import NotificationsFeedPage from 'pages/NotificationsFeedPage';
import UserFeedPage from 'pages/UserFeedPage';
import SignupPage from 'pages/SignupPage';
import SigninPage from 'pages/SigninPage';
import RecoverPage from 'pages/RecoverPage';
import MessageGroupsNewPage from 'pages/MessageGroupNewPage';
import MessageGroupsPage from 'pages/MessageGroupsPage';
import MessageGroupPage from 'pages/MessageGroupPage';
import ConfirmationPage from 'pages/ConfirmationPage';
import ActivityShowPage from 'pages/ActivityShowPage';
import React from 'react';
import {
  createBrowserRouter,
  RouterProvider
} from "react-router-dom";
import { Amplify } from 'aws-amplify';

Amplify.configure({
  "aws_project_region": process.env.REACT_APP_AWS_PROJECT_REGION,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID
});

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomeFeedPage />
  },
  {
    path: "/notifications",
    element: <NotificationsFeedPage />
  },
  {
    path: "/@:handle",
    element: <UserFeedPage />
  },
  {
    path: "/@:handle/status/:activity_uuid",
    element: <ActivityShowPage />
  },
  {
    path: "/messages",
    element: <MessageGroupsPage />
  },
  {
    path: "/messages/new/:handle",
    element: <MessageGroupsNewPage />
  },
  {
    path: "/messages/:message_group_uuid",
    element: <MessageGroupPage />
  },
  {
    path: "/signup",
    element: <SignupPage />
  },
  {
    path: "/signin",
    element: <SigninPage />
  },
  {
    path: "/confirm",
    element: <ConfirmationPage />
  },
  {
    path: "/forgot",
    element: <RecoverPage />
  }
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;