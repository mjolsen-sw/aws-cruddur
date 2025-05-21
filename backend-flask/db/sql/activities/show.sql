SELECT
  a.uuid,
  u.display_name,
  u.handle,
  a.message,
  a.replies_count,
  a.reposts_count,
  a.likes_count,
  a.expires_at,
  a.created_at,
  (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json)
  FROM (
    SELECT
      r.uuid,
      ru.display_name,
      ru.handle,
      r.message,
      r.replies_count,
      r.reposts_count,
      r.likes_count,
      r.reply_to_activity_uuid,
      r.created_at
    FROM public.activities r
    LEFT JOIN public.users ru ON ru.uuid = r.user_uuid
    WHERE
      r.reply_to_activity_uuid = a.uuid
    ORDER BY r.created_at ASC
    ) AS array_row
  ) as replies
FROM public.activities a
LEFT JOIN public.users u ON u.uuid = a.user_uuid
WHERE a.uuid = %(uuid)s
ORDER BY a.created_at DESC