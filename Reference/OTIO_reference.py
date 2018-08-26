import opentimelineio as otio

path = r'/Users/ws/Python/photools/Footages/simple_Project.xml'
filepath = r'/Users/ws/Python/photools/Footages/test.otio'
timeline0 = otio.adapters.read_from_file(path)
for clip in timeline0.each_clip():
    print (clip.name, clip.duration())


print(timeline0)
# otio.adapters.write_to_file(timeline0, filepath)
print("\n")


# timeline = otio.schema.Timeline()
# timeline.name = "Example Timeline"
# track = otio.schema.Sequence()
# track.name = "V1"
# timeline.tracks.append(track)
# clip = otio.schema.Clip()
# clip.name = "Wedding Video"
# track.append(clip)


# def test_iterators(self):
#     self.maxDiff = None
#     track = otio.schema.Track(name="test_track")
#     tl = otio.schema.Timeline("test_timeline", tracks=[track])
#     rt = otio.opentime.RationalTime(5, 24)
#     mr = otio.schema.ExternalReference(
#         available_range=otio.opentime.range_from_start_end_time(
#             otio.opentime.RationalTime(5, 24),
#             otio.opentime.RationalTime(15, 24)
#         ),
#         target_url="/var/tmp/test.mov"
#     )
#
#     cl = otio.schema.Clip(
#         name="test clip1",
#         media_reference=mr,
#         source_range=otio.opentime.TimeRange(
#             mr.available_range.start_time,
#             rt
#         ),
#     )
#     cl2 = otio.schema.Clip(
#         name="test clip2",
#         media_reference=mr,
#         source_range=otio.opentime.TimeRange(
#             mr.available_range.start_time,
#             rt
#         ),
#     )
#     cl3 = otio.schema.Clip(
#         name="test clip3",
#         media_reference=mr,
#         source_range=otio.opentime.TimeRange(
#             mr.available_range.start_time,
#             rt
#         ),
#     )
#     tl.tracks[0].append(cl)
#     tl.tracks[0].extend([cl2, cl3])
#     self.assertEqual([cl, cl2, cl3], list(tl.each_clip()))
#
#     rt_start = otio.opentime.RationalTime(0, 24)
#     rt_end = otio.opentime.RationalTime(1, 24)
#     search_range = otio.opentime.TimeRange(rt_start, rt_end)
#     self.assertEqual([cl], list(tl.each_clip(search_range)))

timeline = otio.schema.Timeline()
timeline.name = "Example Timeline"
track = otio.schema.Track(name="test_track")
tl = otio.schema.Timeline("test_timeline", tracks=[track])
rt = otio.opentime.RationalTime(5, 24)
mr = otio.schema.ExternalReference(
    available_range=otio.opentime.range_from_start_end_time(
            otio.opentime.RationalTime(5, 24),
            otio.opentime.RationalTime(15, 24)
        ), target_url="/var/tmp/test.mov"    )

cl = otio.schema.Clip(
        name="test clip1",
        media_reference=mr,
        source_range=otio.opentime.TimeRange(
            mr.available_range.start_time,
            rt
        ),
    )
cl2 = otio.schema.Clip(
        name="test clip2",
        media_reference=mr,
        source_range=otio.opentime.TimeRange(
            mr.available_range.start_time,
            rt
        ),
    )
cl3 = otio.schema.Clip(
        name="test clip3",
        media_reference=mr,
        source_range=otio.opentime.TimeRange(
            mr.available_range.start_time,
            rt
        ),
    )
tl.tracks[0].append(cl)
tl.tracks[0].extend([cl2, cl3])

timeline.tracks.append(track)

otio.adapters.write_to_file(timeline, r'/Users/ws/Python/photools/Footages/test2.otio')

print(timeline)