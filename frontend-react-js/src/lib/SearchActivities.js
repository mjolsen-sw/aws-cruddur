export function searchActivities(activities, search) {
  if (!search) {
    return activities;
  }

  const lowerSearch = search.toLowerCase();
  return activities.filter(activity => {
    return (activity.message && activity.message.toLowerCase().includes(lowerSearch)) ||
      (activity.display_name && activity.display_name.toLowerCase().includes(lowerSearch)) ||
      (activity.handle && activity.handle.toLowerCase().includes(lowerSearch));
  });
}

export function searchReplies(activities, search) {
  if (!search) {
    return activities;
  }

  const lowerSearch = search.toLowerCase();
  return activities.map(activity => {
    const filteredReplies = (activity.replies || []).filter(reply =>
      (reply.message && reply.message.toLowerCase().includes(lowerSearch)) ||
      (reply.display_name && reply.display_name.toLowerCase().includes(lowerSearch)) ||
      (reply.handle && reply.handle.toLowerCase().includes(lowerSearch))
    );
    return {
      ...activity,
      replies: filteredReplies
    };
  });
}