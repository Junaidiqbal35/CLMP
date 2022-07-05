# module_videos = ['1', '2', '3', '9', '10']
# visited_video = '2'
#
#
# def do_work(self, list_of_work, progress_observer):
#     total_work_to_do = len(list_of_work)
#     for i, work_item in enumerate(list_of_work):
#         do_work_item(work_item)
#         # tell the progress observer how many out of the total items we have processed
#         progress_observer.set_progress(i, total_work_to_do)
#     return 'work is complete'
#
#
# def track_video_visited(video_id):
#     is_visited = False
#     if video_id in module_videos:
#         is_visited = True
#     return is_visited
#
#
# print(track_video_visited('1'))


# video = {'1': 3, '5': 8, '7': 12}
# visited = {'1': 3, '5': 8}
# n = len(video)
#
# for visited in video:
#     print(len(visited))
#     progress_value = 100 * len(visited) // 100
#     print(progress_value)
from math import floor

d = (4 / 7) * 100
print(floor(d))

# progress = CourseProgress.objects.filter(course=course, user=user).aggregate(total_view=Count('visited'))
# progress['total_view'] / content['total_video'] * 100