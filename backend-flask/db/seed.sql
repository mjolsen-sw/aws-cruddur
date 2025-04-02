-- this file was manually created
INSERT INTO public.users (display_name, handle, email, cognito_user_id)
VALUES
  ('matt', 'cord', 'cord@exampro.co', 'mock_cognito1'),
  ('matt', 'calm', 'calm@exampro.co', 'mock_cognito2');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'cord' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )