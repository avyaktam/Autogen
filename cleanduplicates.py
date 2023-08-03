from storyobjects import story_objects
from collections import OrderedDict

# remove duplicates while preserving order
story_objects = list(OrderedDict.fromkeys(story_objects))

# write back the unique list to the file
with open('storyobjects.py', 'w') as file:
    file.write('story_objects = [\n')
    for item in story_objects:
        file.write('    "{}",\n'.format(item))
    file.write(']\n')
