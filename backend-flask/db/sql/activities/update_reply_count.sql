UPDATE public.activities
SET replies_count = replies_count + 1
WHERE uuid = %(activity_uuid)s
RETURNING replies_count;